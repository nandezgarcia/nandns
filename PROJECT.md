# nandns - dns.kiokao.com

Servicio de DNS dinámico autoalojado, alternativa a DuckDNS, usando Cloudflare como backend DNS.

## Arquitectura

- **Backend**: FastAPI (Python) + Uvicorn
- **DNS**: Cloudflare API (no se usa BIND9 en producción actual)
- **Base de datos**: SQLite3 local
- **Proxy inverso**: Nginx
- **SSL**: Let's Encrypt (Certbot)
- **Proceso**: systemd service `dns-nandezgarcia.service`

## Estructura de archivos

```
/var/www/dns.nandezgarcia.com/
├── app.py                  # Aplicación principal FastAPI
├── translations.py         # i18n es/en/zh (92 claves por idioma, simétricas)
├── data/
│   └── dns.db              # Base de datos SQLite
├── templates/
│   ├── index.html          # Panel web + landing (HTML+CSS+JS, trilingüe)
│   └── legal.html          # Páginas legales (aviso/privacidad/condiciones)
├── static/
│   ├── setup.ps1           # Instalador Windows (PowerShell)
│   ├── setup.sh            # Instalador macOS/Ubuntu (Bash)
│   └── og.png              # Imagen Open Graph 1200x630
├── tests/
│   └── manual_check.py     # Verificación local (43 checks: i18n, SEO, billing, webhook)
├── .env                    # Variables de entorno (0600, NO en git)
└── PROJECT.md              # Este archivo
```

## Variables de entorno

Desde el 17/08/26 las variables viven en `/var/www/dns.nandezgarcia.com/.env`
(0600, propietario andres), cargadas con `EnvironmentFile=` desde
`/etc/systemd/system/dns-nandezgarcia.service` (ya NO hay secretos en el unit
file). Claves:

- `CF_ZONE_ID` / `CF_API_TOKEN` — zona y token de Cloudflare
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` — OAuth de Google
- `ADMIN_EMAIL` — email del administrador
- `LS_API_KEY` / `LS_WEBHOOK_SECRET` / `LS_VARIANT_ID` / `LS_CHECKOUT_URL` —
  Lemon Squeezy (Premium; vacías = sección Premium oculta, webhook 503)
- `KOFI_URL` — enlace de donaciones (vacío = sección oculta)
- `GITHUB_URL` — repo del código (vacío = sin enlace en footer/JSON-LD)
- `FREE_MAX_DOMAINS` (10) / `PREMIUM_MAX_DOMAINS` (100) — límites por plan

## Flujo de autenticación

1. El usuario marca el checkbox de responsabilidad
2. Pulsa "Continuar con Google"
3. OAuth2 con Google (solo emails @gmail.com)
4. Si es nuevo y coincide con ADMIN_EMAIL → se crea como admin
5. Se redirige al panel con token JWT en URL (guardado en localStorage)

## Endpoints principales

| Ruta | Descripción |
|------|-------------|
| `GET /` `/en/` `/zh/` | Panel web + landing (es/en/zh, hreflang + JSON-LD) |
| `GET /legal` `/privacidad` `/condiciones` (+ `/en/` `/zh/`) | Páginas legales |
| `GET /robots.txt` `GET /sitemap.xml` | SEO |
| `GET /auth/google` | Inicia OAuth con Google |
| `GET /auth/google/callback` | Callback OAuth |
| `GET /api/me` | Info del usuario (email, plan, max_domains, renews_at) |
| `GET /api/domains` | Listar subdominios del usuario |
| `POST /api/domains` | Crear subdominio (límite según plan: 10 free / 100 premium) |
| `PUT /api/domains/{id}` | Actualizar IP |
| `DELETE /api/domains/{id}` | Eliminar subdominio |
| `GET /update` | API compatible DuckDNS |
| `GET /api/billing/checkout` | URL de checkout Lemon Squeezy (Premium) |
| `GET /api/billing/portal` | URL del portal de cliente Lemon Squeezy |
| `POST /webhook/lemonsqueezy` | Webhook LS (firma HMAC-SHA256 en `X-Signature`) |
| `GET /api/admin/stats` | Stats para admin (usuarios/subdominios/premium) |
| `GET /api/admin/domains` | Todos los subdominios (admin) |

## Configuración del servidor

### Nginx

`/etc/nginx/sites-enabled/dns.kiokao.com`
- Proxy pass a `127.0.0.1:8002`
- SSL gestionado por Certbot

### systemd

`/etc/systemd/system/dns-nandezgarcia.service`
- Usuario: `andres`
- Puerto: `8002`
- Workers: 2

### Base de datos SQLite

Tablas:
- `users` (id, email, token, is_admin, created_at, plan, ls_customer_id,
  ls_subscription_id, plan_status, plan_renews_at)
- `domains` (id, user_id, name, ip, cf_record_id, updated_at)

`plan` es 'free' o 'premium'; el plan efectivo lo decide `effective_premium()`
según `plan_status` (active/on_trial/past_due = premium; cancelled = premium
hasta `plan_renews_at`; expired/unpaid = free). Los subdominios por encima del
límite NO se borran al perder Premium: solo se bloquea crear nuevos.

## Actualización automática en clientes

### Windows 11
- Script: `C:\Scripts\nandns-update.ps1`
- Wrapper silencioso: `C:\Scripts\nandns-update.vbs`
- Tarea: `nandns-update` cada 5 minutos

### macOS / Ubuntu
- Script: `~/.local/bin/nandns-update`
- Cron: `*/5 * * * *`

## Mantenimiento

### Reiniciar servicio
```bash
sudo systemctl restart dns-nandezgarcia.service
```

### Ver logs
```bash
sudo journalctl -u dns-nandezgarcia.service -f
```

### Backup base de datos
```bash
cp /var/www/dns.nandezgarcia.com/data/dns.db /backup/nandns-$(date +%Y%m%d).db
```

### Renew SSL manual
```bash
sudo certbot renew
```

## Notas

- La app usa `httpx` para comunicarse con Cloudflare API y Lemon Squeezy
- Cada dominio creado genera un registro A en Cloudflare para `{name}.dns.kiokao.com`
- El endpoint `/update` es compatible con clientes DuckDNS
- Límite por plan: 10 subdominios gratis, 100 con Premium (5 €/mes, Lemon Squeezy)
- Web trilingüe (es/en/zh) con i18n server-side; al añadir texto a la UI hay que
  añadir la clave en los 3 diccionarios de `translations.py` (verificar simetría)
- Los mensajes de error del servidor siguen en español (decisión consciente:
  el frontend los muestra tal cual y el operador es hispanohablante)
