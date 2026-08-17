import os
import sqlite3
import re
import uuid
import json
import base64
import ipaddress
import secrets
import hmac
import hashlib
from datetime import datetime, timezone
from contextlib import contextmanager
from urllib.parse import quote

import httpx
from fastapi import FastAPI, Request, Form, HTTPException, Header
from fastapi.responses import PlainTextResponse, HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from translations import I18N

DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "data", "dns.db"))
BASE_DOMAIN = os.environ.get("BASE_DOMAIN", "dns.kiokao.com")
BASE_URL = os.environ.get("BASE_URL", f"https://{BASE_DOMAIN}")
CF_ZONE_ID = os.environ.get("CF_ZONE_ID", "")
CF_API_TOKEN = os.environ.get("CF_API_TOKEN", "")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "https://dns.kiokao.com/auth/google/callback")
FREE_MAX_DOMAINS = int(os.environ.get("FREE_MAX_DOMAINS", "10"))
PREMIUM_MAX_DOMAINS = int(os.environ.get("PREMIUM_MAX_DOMAINS", "100"))
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "").strip().lower()

# Lemon Squeezy (Premium) y enlaces opcionales. Vacío = sección desactivada.
LS_API_KEY = os.environ.get("LS_API_KEY", "")
LS_WEBHOOK_SECRET = os.environ.get("LS_WEBHOOK_SECRET", "")
LS_VARIANT_ID = os.environ.get("LS_VARIANT_ID", "")  # legado = anual
LS_VARIANT_ID_YEARLY = os.environ.get("LS_VARIANT_ID_YEARLY", "") or LS_VARIANT_ID
LS_VARIANT_ID_MONTHLY = os.environ.get("LS_VARIANT_ID_MONTHLY", "")
LS_CHECKOUT_URL = os.environ.get("LS_CHECKOUT_URL", "")
DONATE_URL = os.environ.get("DONATE_URL", "") or os.environ.get("KOFI_URL", "")
GITHUB_URL = os.environ.get("GITHUB_URL", "")

if not CF_ZONE_ID or not CF_API_TOKEN:
    raise RuntimeError("Faltan variables de entorno CF_ZONE_ID o CF_API_TOKEN")
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise RuntimeError("Faltan variables de entorno GOOGLE_CLIENT_ID o GOOGLE_CLIENT_SECRET")

CF_BASE = "https://api.cloudflare.com/client/v4"
LS_BASE = "https://api.lemonsqueezy.com/v1"

# idioma -> prefijo de ruta ("" = español, por defecto)
LANG_PREFIX = {"es": "", "en": "/en", "zh": "/zh"}
LEGAL_PAGES = ("legal", "privacidad", "condiciones")


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        token TEXT UNIQUE NOT NULL,
        is_admin INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS domains (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT UNIQUE NOT NULL,
        ip TEXT NOT NULL,
        cf_record_id TEXT,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    for stmt in (
        "ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0",
        "ALTER TABLE users ADD COLUMN plan TEXT DEFAULT 'free'",
        "ALTER TABLE users ADD COLUMN ls_customer_id TEXT",
        "ALTER TABLE users ADD COLUMN ls_subscription_id TEXT",
        "ALTER TABLE users ADD COLUMN plan_status TEXT DEFAULT ''",
        "ALTER TABLE users ADD COLUMN plan_renews_at TEXT",
    ):
        try:
            c.execute(stmt)
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


app = FastAPI()
templates = Jinja2Templates(directory="templates")
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def valid_subdomain(name: str) -> bool:
    return bool(re.fullmatch(r"[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?", name))


def valid_ip(addr: str) -> bool:
    try:
        ipaddress.ip_address(addr)
        return True
    except ValueError:
        return False


def cf_headers():
    return {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json",
    }


def cf_list_records(name: str):
    fqdn = f"{name}.{BASE_DOMAIN}"
    url = f"{CF_BASE}/zones/{CF_ZONE_ID}/dns_records"
    params = {"name": fqdn, "type": "A"}
    r = httpx.get(url, headers=cf_headers(), params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    if not data.get("success"):
        raise RuntimeError(data.get("errors"))
    return data.get("result", [])


def cf_create_record(name: str, ip: str):
    fqdn = f"{name}.{BASE_DOMAIN}"
    url = f"{CF_BASE}/zones/{CF_ZONE_ID}/dns_records"
    payload = {"type": "A", "name": fqdn, "content": ip, "ttl": 120}
    r = httpx.post(url, headers=cf_headers(), json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    if not data.get("success"):
        raise RuntimeError(data.get("errors"))
    return data["result"]["id"]


def cf_update_record(record_id: str, name: str, ip: str):
    fqdn = f"{name}.{BASE_DOMAIN}"
    url = f"{CF_BASE}/zones/{CF_ZONE_ID}/dns_records/{record_id}"
    payload = {"type": "A", "name": fqdn, "content": ip, "ttl": 120}
    r = httpx.put(url, headers=cf_headers(), json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    if not data.get("success"):
        raise RuntimeError(data.get("errors"))
    return data["result"]["id"]


def cf_delete_record(record_id: str):
    url = f"{CF_BASE}/zones/{CF_ZONE_ID}/dns_records/{record_id}"
    r = httpx.delete(url, headers=cf_headers(), timeout=30)
    r.raise_for_status()
    data = r.json()
    if not data.get("success"):
        raise RuntimeError(data.get("errors"))
    return True


def sync_cf_create(name: str, ip: str) -> str:
    existing = cf_list_records(name)
    if existing:
        rec_id = existing[0]["id"]
        cf_update_record(rec_id, name, ip)
        return rec_id
    return cf_create_record(name, ip)


def sync_cf_update(name: str, ip: str, record_id: str | None) -> str:
    if record_id:
        try:
            cf_update_record(record_id, name, ip)
            return record_id
        except Exception:
            pass
    return sync_cf_create(name, ip)


def sync_cf_delete(record_id: str):
    if record_id:
        try:
            cf_delete_record(record_id)
        except Exception:
            pass


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip
    if request.client:
        return request.client.host
    return "127.0.0.1"


def decode_jwt_payload(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT")
    payload = parts[1]
    payload += "=" * (4 - len(payload) % 4)
    return json.loads(base64.urlsafe_b64decode(payload))


@app.on_event("startup")
def startup():
    init_db()


# ============ PLANES (free / premium) ============

def _parse_dt(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except Exception:
        return None


def effective_premium(user) -> bool:
    """Premium efectivo: plan premium con suscripción activa, en periodo de
    gracia (past_due) o cancelada pero aún dentro del periodo pagado."""
    if (user["plan"] or "free") != "premium":
        return False
    status = user["plan_status"] or ""
    if status in ("active", "on_trial", "past_due"):
        return True
    if status == "cancelled":
        ends = _parse_dt(user["plan_renews_at"])
        return bool(ends and datetime.now(timezone.utc) < ends)
    return False


def user_max_domains(user) -> int:
    if user["is_admin"]:
        return 10 ** 9
    return PREMIUM_MAX_DOMAINS if effective_premium(user) else FREE_MAX_DOMAINS


# ============ PÁGINAS (i18n + SEO) ============

def _json_for_script(obj) -> str:
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def build_jsonld(lang: str) -> str:
    t = I18N[lang]
    software = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "nandns",
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "Web",
        "url": BASE_URL + "/",
        "description": t["meta_description"],
        "offers": [
            {"@type": "Offer", "name": t["free_name"], "price": "0", "priceCurrency": "EUR"},
            {"@type": "Offer", "name": t["premium_name"], "price": "5.00", "priceCurrency": "EUR"},
        ],
    }
    if GITHUB_URL:
        software["codeRepository"] = GITHUB_URL
    data = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": "nandns", "url": BASE_URL + "/"},
        software,
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in t["faq_items"]
            ],
        },
    ]
    return _json_for_script(data)


def render_index(request: Request, lang: str):
    t = I18N[lang]
    prefix = LANG_PREFIX[lang]
    return templates.TemplateResponse("index.html", {
        "request": request,
        "t": t,
        "lang": lang,
        "prefix": prefix or "",
        "canonical": f"{BASE_URL}{prefix}/",
        "alternates": [(l, f"{BASE_URL}{LANG_PREFIX[l]}/") for l in ("es", "en", "zh")],
        "base_domain": BASE_DOMAIN,
        "kofi_url": DONATE_URL,
        "github_url": GITHUB_URL,
        "premium_enabled": bool(LS_CHECKOUT_URL),
        "free_max": FREE_MAX_DOMAINS,
        "premium_max": PREMIUM_MAX_DOMAINS,
        "i18n_json": _json_for_script(t),
        "jsonld": build_jsonld(lang),
    })


def render_legal(request: Request, lang: str, page: str):
    t = I18N[lang]
    return templates.TemplateResponse("legal.html", {
        "request": request,
        "t": t,
        "lang": lang,
        "title": t[f"legal_{page}_title"],
        "body": t[f"legal_{page}_body"],
        "home_url": f"{LANG_PREFIX[lang]}/",
        "canonical": f"{BASE_URL}{LANG_PREFIX[lang]}/{page}",
    })


@app.get("/", response_class=HTMLResponse)
def index_es(request: Request):
    return render_index(request, "es")


@app.get("/en/", response_class=HTMLResponse)
def index_en(request: Request):
    return render_index(request, "en")


@app.get("/zh/", response_class=HTMLResponse)
def index_zh(request: Request):
    return render_index(request, "zh")


def _make_legal_handler(page: str, lang: str):
    def handler(request: Request):
        return render_legal(request, lang, page)
    return handler


for _page in LEGAL_PAGES:
    for _lang, _prefix in LANG_PREFIX.items():
        app.add_api_route(
            f"{_prefix}/{_page}",
            _make_legal_handler(_page, _lang),
            methods=["GET"],
            response_class=HTMLResponse,
        )


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /api/\n"
        "Disallow: /auth/\n"
        "Disallow: /update\n"
        "\n"
        f"Sitemap: {BASE_URL}/sitemap.xml\n"
    )


@app.get("/sitemap.xml")
def sitemap():
    alternates = "".join(
        f'        <xhtml:link rel="alternate" hreflang="{l}" href="{BASE_URL}{LANG_PREFIX[l]}/"/>\n'
        for l in ("es", "en", "zh")
    )
    urls = ""
    for lang, prefix in LANG_PREFIX.items():
        urls += (
            "  <url>\n"
            f"    <loc>{BASE_URL}{prefix}/</loc>\n"
            f"{alternates}"
            f'        <xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}/"/>\n'
            "  </url>\n"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        f"{urls}"
        "</urlset>\n"
    )
    return Response(content=xml, media_type="application/xml")


# ============ AUTH (Google OAuth) ============

@app.get("/auth/google")
def auth_google(request: Request):
    state = secrets.token_urlsafe(32)
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&response_type=code"
        "&scope=openid%20email"
        f"&state={state}"
    )
    response = RedirectResponse(url=auth_url)
    response.set_cookie(key="oauth_state", value=state, max_age=600, httponly=True, secure=True, samesite="lax")
    return response


@app.get("/auth/google/callback")
def auth_google_callback(request: Request, code: str = "", state: str = "", error: str = ""):
    if error:
        return RedirectResponse(url="/?error=google_auth_denied")

    stored_state = request.cookies.get("oauth_state")
    if not stored_state or stored_state != state:
        return RedirectResponse(url="/?error=invalid_state")

    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    try:
        r = httpx.post(token_url, data=payload, timeout=30)
        r.raise_for_status()
        token_data = r.json()
        id_token = token_data.get("id_token")
        if not id_token:
            return RedirectResponse(url="/?error=no_id_token")
        user_info = decode_jwt_payload(id_token)
    except Exception:
        return RedirectResponse(url="/?error=token_exchange_failed")

    email = user_info.get("email", "").strip().lower()
    if not email or not email.endswith("@gmail.com"):
        return RedirectResponse(url="/?error=only_gmail_allowed")

    with get_db() as db:
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if not user:
            token = uuid.uuid4().hex
            is_admin = 1 if ADMIN_EMAIL and email == ADMIN_EMAIL else 0
            db.execute(
                "INSERT INTO users (email, token, is_admin, created_at) VALUES (?,?,?,?)",
                (email, token, is_admin, datetime.now(timezone.utc).isoformat()),
            )
            db.commit()
            user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

    response = RedirectResponse(url=f"/?token={user['token']}")
    response.delete_cookie("oauth_state")
    return response


def get_user_by_token(token: str | None) -> sqlite3.Row:
    if not token:
        raise HTTPException(401, "Falta token")
    with get_db() as db:
        user = db.execute("SELECT * FROM users WHERE token = ?", (token,)).fetchone()
    if not user:
        raise HTTPException(401, "Token inválido")
    return user


def require_admin(token: str | None) -> sqlite3.Row:
    user = get_user_by_token(token)
    if not user["is_admin"]:
        raise HTTPException(403, "Acceso denegado")
    return user


def count_user_domains(user_id: int) -> int:
    with get_db() as db:
        row = db.execute("SELECT COUNT(*) as c FROM domains WHERE user_id = ?", (user_id,)).fetchone()
    return row["c"]


@app.get("/api/me")
def me(authorization: str | None = Header(None)):
    token = authorization.replace("Bearer ", "") if authorization else None
    user = get_user_by_token(token)
    premium = effective_premium(user)
    return {
        "email": user["email"],
        "is_admin": bool(user["is_admin"]),
        "plan": "premium" if premium else "free",
        "plan_status": user["plan_status"] or "",
        "plan_renews_at": user["plan_renews_at"] or "",
        "max_domains": user_max_domains(user),
        "premium_enabled": bool(LS_CHECKOUT_URL),
        "has_subscription": bool(user["ls_customer_id"]),
    }


@app.get("/api/domains")
def list_domains(authorization: str | None = Header(None)):
    token = authorization.replace("Bearer ", "") if authorization else None
    user = get_user_by_token(token)
    with get_db() as db:
        rows = db.execute(
            "SELECT id, name, ip, updated_at FROM domains WHERE user_id = ? ORDER BY name",
            (user["id"],),
        ).fetchall()
    return [{"id": r["id"], "name": r["name"], "ip": r["ip"], "updated_at": r["updated_at"]} for r in rows]


@app.post("/api/domains")
def create_domain(
    name: str = Form(...), ip: str = Form(None), authorization: str | None = Header(None)
):
    token = authorization.replace("Bearer ", "") if authorization else None
    user = get_user_by_token(token)
    name = name.strip().lower()
    if not valid_subdomain(name):
        raise HTTPException(400, "Nombre de subdominio inválido")
    if not ip:
        raise HTTPException(400, "IP requerida")
    ip = ip.strip()
    if not valid_ip(ip):
        raise HTTPException(400, "IP inválida")

    limit = user_max_domains(user)
    if count_user_domains(user["id"]) >= limit:
        raise HTTPException(400, f"Límite de {limit} subdominios alcanzado")

    try:
        cf_id = sync_cf_create(name, ip)
    except Exception as e:
        raise HTTPException(502, f"Error al sincronizar con Cloudflare: {e}")

    try:
        with get_db() as db:
            db.execute(
                "INSERT INTO domains (user_id, name, ip, cf_record_id, updated_at) VALUES (?,?,?,?,?)",
                (user["id"], name, ip, cf_id, datetime.now(timezone.utc).isoformat()),
            )
            db.commit()
    except sqlite3.IntegrityError:
        sync_cf_delete(cf_id)
        raise HTTPException(400, "El subdominio ya existe")

    return {"message": "Subdominio creado"}


@app.put("/api/domains/{domain_id}")
def update_domain(domain_id: int, ip: str = Form(...), authorization: str | None = Header(None)):
    token = authorization.replace("Bearer ", "") if authorization else None
    user = get_user_by_token(token)
    ip = ip.strip()
    if not valid_ip(ip):
        raise HTTPException(400, "IP inválida")

    with get_db() as db:
        row = db.execute(
            "SELECT * FROM domains WHERE id = ? AND user_id = ?", (domain_id, user["id"])
        ).fetchone()
        if not row:
            raise HTTPException(404, "Dominio no encontrado")

        try:
            cf_id = sync_cf_update(row["name"], ip, row["cf_record_id"])
        except Exception as e:
            raise HTTPException(502, f"Error al sincronizar con Cloudflare: {e}")

        db.execute(
            "UPDATE domains SET ip = ?, cf_record_id = ?, updated_at = ? WHERE id = ?",
            (ip, cf_id, datetime.now(timezone.utc).isoformat(), domain_id),
        )
        db.commit()

    return {"message": "IP actualizada"}


@app.delete("/api/domains/{domain_id}")
def delete_domain(domain_id: int, authorization: str | None = Header(None)):
    token = authorization.replace("Bearer ", "") if authorization else None
    user = get_user_by_token(token)
    with get_db() as db:
        row = db.execute(
            "SELECT * FROM domains WHERE id = ? AND user_id = ?", (domain_id, user["id"])
        ).fetchone()
        if not row:
            raise HTTPException(404, "Dominio no encontrado")

        sync_cf_delete(row["cf_record_id"])

        db.execute("DELETE FROM domains WHERE id = ?", (domain_id,))
        db.commit()

    return {"message": "Dominio eliminado"}


@app.get("/update", response_class=PlainTextResponse)
def update(request: Request, domains: str = "", token: str = "", ip: str = ""):
    if not domains or not token:
        return "KO"
    user = get_user_by_token(token)
    target_ip = ip.strip() if ip else get_client_ip(request)
    if not valid_ip(target_ip):
        return "KO"

    names = [n.strip().lower() for n in domains.split(",") if n.strip()]
    if not names:
        return "KO"

    updated = False
    with get_db() as db:
        for name in names:
            row = db.execute(
                "SELECT * FROM domains WHERE user_id = ? AND name = ?", (user["id"], name)
            ).fetchone()
            if row:
                try:
                    cf_id = sync_cf_update(name, target_ip, row["cf_record_id"])
                except Exception:
                    return "KO"
                db.execute(
                    "UPDATE domains SET ip = ?, cf_record_id = ?, updated_at = ? WHERE id = ?",
                    (target_ip, cf_id, datetime.now(timezone.utc).isoformat(), row["id"]),
                )
                updated = True
            else:
                if count_user_domains(user["id"]) >= user_max_domains(user):
                    return "KO"
                try:
                    cf_id = sync_cf_create(name, target_ip)
                except Exception:
                    return "KO"
                try:
                    db.execute(
                        "INSERT INTO domains (user_id, name, ip, cf_record_id, updated_at) VALUES (?,?,?,?,?)",
                        (user["id"], name, target_ip, cf_id, datetime.now(timezone.utc).isoformat()),
                    )
                    updated = True
                except sqlite3.IntegrityError:
                    pass
        db.commit()

    return "OK" if updated else "KO"


# ============ BILLING (Lemon Squeezy) ============

@app.get("/api/billing/checkout")
def billing_checkout(plan: str = "yearly", authorization: str | None = Header(None)):
    token = authorization.replace("Bearer ", "") if authorization else None
    user = get_user_by_token(token)
    if not LS_CHECKOUT_URL:
        raise HTTPException(503, "Pagos no configurados")
    variant = LS_VARIANT_ID_MONTHLY if plan == "monthly" else LS_VARIANT_ID_YEARLY
    sep = "&" if "?" in LS_CHECKOUT_URL else "?"
    url = f"{LS_CHECKOUT_URL}{sep}"
    if variant:
        url += f"variant={variant}&"
    url += (
        f"checkout[email]={quote(user['email'])}"
        f"&checkout[custom][user_id]={user['id']}"
    )
    return {"url": url}


@app.get("/api/billing/portal")
def billing_portal(authorization: str | None = Header(None)):
    token = authorization.replace("Bearer ", "") if authorization else None
    user = get_user_by_token(token)
    if not LS_API_KEY:
        raise HTTPException(503, "Pagos no configurados")
    customer_id = user["ls_customer_id"]
    if not customer_id:
        raise HTTPException(400, "Sin suscripción")
    try:
        r = httpx.get(
            f"{LS_BASE}/customers/{customer_id}",
            headers={
                "Authorization": f"Bearer {LS_API_KEY}",
                "Accept": "application/vnd.api+json",
            },
            timeout=30,
        )
        r.raise_for_status()
        portal = r.json()["data"]["attributes"]["urls"]["customer_portal"]
    except Exception as e:
        raise HTTPException(502, f"Error contactando con la pasarela de pago: {e}")
    return {"url": portal}


# Eventos de suscripción que actualizan el estado almacenado.
_LS_STATUS_EVENTS = {
    "subscription_created",
    "subscription_updated",
    "subscription_cancelled",
    "subscription_resumed",
    "subscription_expired",
    "subscription_paused",
    "subscription_unpaused",
    "subscription_plan_changed",
}


@app.post("/webhook/lemonsqueezy")
async def lemonsqueezy_webhook(request: Request):
    if not LS_WEBHOOK_SECRET:
        raise HTTPException(503, "Webhooks no configurados")
    raw = await request.body()
    signature = request.headers.get("x-signature", "")
    expected = hmac.new(LS_WEBHOOK_SECRET.encode(), raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        raise HTTPException(401, "Firma inválida")

    try:
        data = json.loads(raw)
    except Exception:
        raise HTTPException(400, "JSON inválido")

    meta = data.get("meta") or {}
    event = meta.get("event_name", "")
    custom = meta.get("custom_data") or {}
    attrs = (data.get("data") or {}).get("attributes") or {}
    sub_id = str((data.get("data") or {}).get("id", ""))
    customer_id = str(attrs.get("customer_id", ""))

    if event == "subscription_payment_failed":
        status = "past_due"
    elif event in _LS_STATUS_EVENTS:
        status = attrs.get("status", "")
    else:
        # evento no relevante (p. ej. subscription_payment_success)
        return {"ok": True}

    renews = attrs.get("renews_at") or attrs.get("ends_at") or ""

    with get_db() as db:
        user = None
        uid = custom.get("user_id")
        if uid:
            user = db.execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()
        if not user and customer_id:
            user = db.execute("SELECT * FROM users WHERE ls_customer_id = ?", (customer_id,)).fetchone()
        if not user:
            return {"ok": True}
        db.execute(
            "UPDATE users SET plan = 'premium', plan_status = ?, ls_customer_id = ?,"
            " ls_subscription_id = ?, plan_renews_at = ? WHERE id = ?",
            (status, customer_id, sub_id, renews, user["id"]),
        )
        db.commit()

    return {"ok": True}


# ============ ADMIN ============

@app.get("/api/admin/stats")
def admin_stats(authorization: str | None = Header(None)):
    require_admin(authorization.replace("Bearer ", "") if authorization else None)
    with get_db() as db:
        users = db.execute("SELECT COUNT(*) as c FROM users").fetchone()["c"]
        domains = db.execute("SELECT COUNT(*) as c FROM domains").fetchone()["c"]
        premium = db.execute("SELECT COUNT(*) as c FROM users WHERE plan = 'premium'").fetchone()["c"]
    return {"users": users, "domains": domains, "premium": premium}


@app.get("/api/admin/domains")
def admin_domains(authorization: str | None = Header(None)):
    require_admin(authorization.replace("Bearer ", "") if authorization else None)
    with get_db() as db:
        rows = db.execute("""
            SELECT d.id, d.name, d.ip, d.updated_at, u.email as user_email
            FROM domains d JOIN users u ON d.user_id = u.id
            ORDER BY d.updated_at DESC
        """).fetchall()
    return [{"id": r["id"], "name": r["name"], "ip": r["ip"], "updated_at": r["updated_at"], "user_email": r["user_email"]} for r in rows]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)
