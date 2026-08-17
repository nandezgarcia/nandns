#!/usr/bin/env python3
"""Verificación manual de nandns: levanta la app en local con una SQLite
temporal y comprueba i18n, SEO, billing y webhook de Lemon Squeezy.

Uso:  ../.venv/bin/python tests/manual_check.py
(desde la raíz del proyecto; requiere el venv con requirements.txt)
"""
import hashlib
import hmac
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.request

BASE = "http://127.0.0.1:8123"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV = {
    **os.environ,
    "DB_PATH": "",  # se rellena abajo
    "CF_ZONE_ID": "dummy-zone",
    "CF_API_TOKEN": "dummy-token",
    "GOOGLE_CLIENT_ID": "dummy-client",
    "GOOGLE_CLIENT_SECRET": "dummy-secret",
    "ADMIN_EMAIL": "admin@gmail.com",
    "LS_API_KEY": "ls_test_key",
    "LS_WEBHOOK_SECRET": "test-webhook-secret",
    "LS_VARIANT_ID_YEARLY": "12345",
    "LS_VARIANT_ID_MONTHLY": "67890",
    "LS_CHECKOUT_URL": "https://store.lemonsqueezy.test/checkout/buy/abc",
    "DONATE_URL": "https://store.lemonsqueezy.test/checkout/buy/donate",
    "GITHUB_URL": "https://github.com/nandezgarcia/nandns",
}

PASS, FAIL = [], []


def check(name, cond, detail=""):
    if cond:
        PASS.append(name)
        print(f"  OK  {name}")
    else:
        FAIL.append(name)
        print(f"FAIL  {name}  {detail}")


def get(path, headers=None):
    req = urllib.request.Request(BASE + path, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def post_raw(path, body, headers=None):
    req = urllib.request.Request(BASE + path, data=body, headers=headers or {}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def main():
    tmp = tempfile.mkdtemp(prefix="nandns-test-")
    ENV["DB_PATH"] = os.path.join(tmp, "test.db")

    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8123"],
        cwd=ROOT, env=ENV,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(50):
            try:
                urllib.request.urlopen(BASE + "/", timeout=2)
                break
            except Exception:
                time.sleep(0.3)
        else:
            print("El servidor no arrancó")
            return 1

        print("== Páginas por idioma ==")
        for path, lang, marker in (
            ("/", "es", "DNS dinámico gratuito"),
            ("/en/", "en", "Free dynamic DNS"),
            ("/zh/", "zh", "免费动态DNS"),
        ):
            st, body = get(path)
            check(f"GET {path} -> 200", st == 200, f"status={st}")
            check(f"{path} contiene marcador {lang}", marker in body)
            check(f"{path} tiene hreflang", 'hreflang="x-default"' in body)
            check(f"{path} tiene JSON-LD FAQ", "FAQPage" in body)
            check(f"{path} tiene canonical", 'rel="canonical"' in body)

        print("== Páginas legales ==")
        for path in ("/legal", "/privacidad", "/condiciones",
                     "/en/legal", "/en/privacidad", "/en/condiciones",
                     "/zh/legal", "/zh/privacidad", "/zh/condiciones"):
            st, body = get(path)
            check(f"GET {path} -> 200", st == 200, f"status={st}")

        print("== robots / sitemap ==")
        st, body = get("/robots.txt")
        check("robots.txt", st == 200 and "sitemap.xml" in body.lower(), f"status={st}")
        st, body = get("/sitemap.xml")
        check("sitemap.xml 200", st == 200, f"status={st}")
        check("sitemap incluye /en/ y /zh/", "/en/" in body and "/zh/" in body)
        check("sitemap xhtml alternates", "xhtml:link" in body)

        print("== Donaciones / GitHub / Premium visibles ==")
        st, body = get("/")
        check("sección donaciones visible", "checkout/buy/donate" in body)
        check("enlace GitHub visible", "github.com/nandezgarcia/nandns" in body)
        check("sección precios visible", "plan-card featured" in body)

        print("== Usuario de prueba + billing ==")
        conn = sqlite3.connect(ENV["DB_PATH"])
        conn.execute(
            "INSERT INTO users (email, token, is_admin, created_at, plan, plan_status)"
            " VALUES ('test@gmail.com', 'tok123', 0, '2026-01-01', 'free', '')"
        )
        conn.commit()
        uid = conn.execute("SELECT id FROM users WHERE token='tok123'").fetchone()[0]

        st, body = get("/api/me", {"Authorization": "Bearer tok123"})
        me = json.loads(body)
        check("/api/me 200", st == 200, f"status={st}")
        check("plan free y max 10", me.get("plan") == "free" and me.get("max_domains") == 10, body)

        st, body = get("/api/billing/checkout", {"Authorization": "Bearer tok123"})
        checkout = json.loads(body)
        check("checkout devuelve url", st == 200 and checkout.get("url", "").startswith("https://store.lemonsqueezy.test"), body)
        check("checkout lleva email y user_id", "checkout%5Bemail%5D=test%40gmail.com" in checkout.get("url", "") or "test%40gmail.com" in checkout.get("url", ""), checkout.get("url", ""))
        check("checkout por defecto es anual", "variant=12345" in checkout.get("url", ""), checkout.get("url", ""))
        st, body = get("/api/billing/checkout?plan=monthly", {"Authorization": "Bearer tok123"})
        checkout_m = json.loads(body)
        check("checkout mensual lleva variante mensual", "variant=67890" in checkout_m.get("url", ""), checkout_m.get("url", ""))

        print("== Webhook Lemon Squeezy ==")
        payload = json.dumps({
            "meta": {"event_name": "subscription_created",
                     "custom_data": {"user_id": str(uid)}},
            "data": {"id": "sub_999", "type": "subscriptions",
                     "attributes": {"customer_id": "cus_999", "status": "active",
                                    "renews_at": "2026-09-17T00:00:00.000000Z"}},
        }).encode()
        st, _ = post_raw("/webhook/lemonsqueezy", payload, {"X-Signature": "firma-mala"})
        check("firma inválida -> 401", st == 401, f"status={st}")

        sig = hmac.new(b"test-webhook-secret", payload, hashlib.sha256).hexdigest()
        st, body = post_raw("/webhook/lemonsqueezy", payload, {"X-Signature": sig})
        check("firma válida -> 200", st == 200, f"status={st} body={body}")

        st, body = get("/api/me", {"Authorization": "Bearer tok123"})
        me = json.loads(body)
        check("plan premium tras webhook", me.get("plan") == "premium", body)
        check("max 100 tras webhook", me.get("max_domains") == 100, body)
        check("renews_at guardado", "2026-09-17" in (me.get("plan_renews_at") or ""), body)

        # expiración -> vuelve a free
        payload2 = json.dumps({
            "meta": {"event_name": "subscription_expired", "custom_data": {"user_id": str(uid)}},
            "data": {"id": "sub_999", "type": "subscriptions",
                     "attributes": {"customer_id": "cus_999", "status": "expired"}},
        }).encode()
        sig2 = hmac.new(b"test-webhook-secret", payload2, hashlib.sha256).hexdigest()
        st, _ = post_raw("/webhook/lemonsqueezy", payload2, {"X-Signature": sig2})
        st, body = get("/api/me", {"Authorization": "Bearer tok123"})
        me = json.loads(body)
        check("expirada -> free y max 10", me.get("plan") == "free" and me.get("max_domains") == 10, body)

        # cancelada con ends_at futuro -> sigue premium
        payload3 = json.dumps({
            "meta": {"event_name": "subscription_cancelled", "custom_data": {"user_id": str(uid)}},
            "data": {"id": "sub_999", "type": "subscriptions",
                     "attributes": {"customer_id": "cus_999", "status": "cancelled",
                                    "ends_at": "2099-01-01T00:00:00.000000Z"}},
        }).encode()
        sig3 = hmac.new(b"test-webhook-secret", payload3, hashlib.sha256).hexdigest()
        st, _ = post_raw("/webhook/lemonsqueezy", payload3, {"X-Signature": sig3})
        st, body = get("/api/me", {"Authorization": "Bearer tok123"})
        me = json.loads(body)
        check("cancelada con periodo pagado -> premium hasta ends_at", me.get("plan") == "premium", body)

        print("== /update sin token ==")
        st, body = get("/update?domains=x")
        check("/update sin token -> KO", body.strip() == "KO", body)

        conn.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()

    print(f"\n{len(PASS)} OK, {len(FAIL)} FAIL")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
