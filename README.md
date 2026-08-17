# nandns — DNS dinámico gratuito

Servicio de DNS dinámico (DDNS) autoalojado, alternativa a DuckDNS, usando
Cloudflare como backend DNS. En producción en **https://dns.kiokao.com**.

> English: nandns is a self-hosted dynamic DNS (DDNS) service — a free
> DuckDNS alternative built with FastAPI and the Cloudflare API. Users sign
> in with Google, create up to 10 subdomains that always point to their
> current IP, and update them via a DuckDNS-compatible API
> (`GET /update?domains=X&token=Y`). Ships with a trilingual (es/en/zh) web
> UI, auto-update scripts for Windows/macOS/Linux, and an optional Premium
> plan (100 hosts) billed through Lemon Squeezy (Merchant of Record).

## Características

- Subdominios `{nombre}.dns.kiokao.com` con TTL 120 s, sin caducidad
- Login con Google (sin contraseñas que guardar)
- API compatible con DuckDNS: `curl "https://dns.kiokao.com/update?domains=X&token=Y"`
- Scripts de autoactualización cada 5 min (Windows / macOS / Linux)
- Web trilingüe (español, inglés, chino) con SEO (hreflang, JSON-LD, sitemap)
- Plan Premium opcional: 100 subdominios por 5 €/mes con Lemon Squeezy
- Panel de administración con estadísticas

## Requisitos

- Python 3.11+
- Una zona de Cloudflare y un token de API con permisos de edición DNS
- Un proyecto de Google Cloud con OAuth (solo se aceptan cuentas @gmail.com)

## Instalación

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
cp .env.example .env   # rellena las claves
venv/bin/uvicorn app:app --host 127.0.0.1 --port 8002
```

## Configuración

Todas las variables se leen del entorno (ver `.env.example`):

| Variable | Descripción |
|---|---|
| `CF_ZONE_ID` / `CF_API_TOKEN` | Zona y token de Cloudflare (obligatorias) |
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | OAuth de Google (obligatorias) |
| `BASE_DOMAIN` | Dominio base (por defecto `dns.kiokao.com`) |
| `ADMIN_EMAIL` | Email del administrador |
| `FREE_MAX_DOMAINS` / `PREMIUM_MAX_DOMAINS` | Límites por plan (10 / 100) |
| `LS_API_KEY` / `LS_WEBHOOK_SECRET` / `LS_VARIANT_ID` / `LS_CHECKOUT_URL` | Lemon Squeezy (Premium; vacío = desactivado) |
| `KOFI_URL` / `GITHUB_URL` | Enlaces opcionales en la web |

### Premium con Lemon Squeezy

1. Crea un producto de suscripción (5 €/mes) y copia su URL de checkout y variant ID.
2. Configura el webhook: `https://tu-dominio/webhook/lemonsqueezy` con los
   eventos `subscription_*` y guarda el signing secret.
3. Rellena las variables `LS_*` en `.env`.

El webhook verifica la firma HMAC-SHA256 (`X-Signature`) y actualiza el plan
del usuario (`free`/`premium`) según el estado de la suscripción.

## Desarrollo

```bash
venv/bin/python tests/manual_check.py   # 43 checks: i18n, SEO, billing, webhook
```

Al añadir texto a la UI, añade la clave en los **tres** diccionarios de
`translations.py` (es/en/zh) — el test de simetría falla si falta alguna.

## Licencia

MIT — ver [LICENSE](LICENSE).
