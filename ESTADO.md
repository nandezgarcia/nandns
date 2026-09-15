# ESTADO — nandns (dns.kiokao.com) — 2026-09-14

## ESTADO AL 14/09/26 (cierre) — BMC 100% LIVE, COBRANDO DE VERDAD
- Página BMC: https://buymeacoffee.com/nandns (logo, descripción, enlaces dns.kiokao.com + GitHub visibles en el perfil público).
- Membresía "Premium" (id 341069): $7/mes + $60/año, PUBLICADA y visible en https://buymeacoffee.com/nandns/membership (200 OK, botón Join).
- Payout: Stripe Connect onboarding COMPLETADO (reusó la cuenta Stripe de Lemon Squeezy: ES, Calle Santa María de Ordás 15, 41008 Sevilla, tel +34 645 25 23 86, DOB 02/12/1976, ciudadanía ES; Stripe Tax rechazado "Not right now"). Estado: "Instant Payout via Stripe — Connected". Payout a ING ••••1488 (SEPA). El modal "Update your social links" y el "Submit for review" quedan como templates ocultos en DOM (opacity:0) — NO son bloqueantes: los enlaces ya se guardaron (update_page 200) y la página visible solo muestra la tarjeta Stripe Connected.
- Webhook BMC "nandns" (activo): https://dns.kiokao.com/webhook/buymeacoffee — membership.started/updated/cancelled/paused. Secret en .env del servidor. E2E verificado (test events 200, firma HMAC-SHA256 x-signature-sha256; Cloudflare no bloquea BMC, sí python-urllib UA).
- App desplegada: /api/billing/checkout → BMC_MEMBERSHIP_URL; portal = cuenta supporter BMC; premium por MATCH email supporter↔user. Endpoint webhook live (GET da 405). Tests 49/49. Push a github.com/nandezgarcia/nandns hecho.
- OJO WebBridge: el onboarding de Stripe Connect va en iframe cross-origin (connect-js.stripe.com): hay que usar CDP Page.createIsolatedWorld en el frame ui_layer y los botones "Agree/Continue" son <a> sin <button>; clic sintético .click() SÍ funciona; el modal de BMC necesitó CDP Input.dispatchMouseEvent (trusted). offsetParent!==null NO garantiza visible (modales con opacity:0 en DOM).
- PENDIENTE usuario: fiscalidad — BMC no es Merchant of Record: IRPF/IVA con gestor. Los cobros ya llegan a ING ••••1488 vía Stripe.

## Decisión de pagos ACTUAL: Buy Me a Coffee (BMC)
- 2026-08-17: Lemon Squeezy elegido → tienda NUNCA aprobada (4+ semanas, soporte sin responder a emails del 24/08 y 03/09 enviados desde Gmail del usuario).
- 2026-09-14: se probó Paddle → usuario eligió "Probar Paddle" pero el registro fue penoso (antd). Usuario dijo: "Vamos a parar esto, ¿por qué no usamos buymeacoffee.com?" → **DECISIÓN FINAL: BMC**.
- Verificado: BMC tiene memberships mensual/anual + webhooks firmados (membership.started/updated/cancelled/paused + donation.*). Doc: https://help.buymeacoffee.com/en/articles/15743173
- BMC: 5% fees, NO es Merchant of Record (IVA/IRPF a cargo del usuario).

## Cuentas y credenciales
- **BMC** (buymeacoffee.com): página "nandns" ACEPTADA. Registro por email enviado: nandezgarcia@gmail.com + pass generado en `/tmp/bmc_pw.txt`. El OAuth de Google falló (popup bloqueado), por eso email+password. QUEDA: verificar si pide confirmación y entrar al dashboard.
- **Paddle** (NO USAR, parado por el usuario, gratis): cuenta live verificada (negocio "nandns", Individual, Calle Santa Maria de Ordas 15 3ºC, Sevilla 41008, $0-100K, dns.kiokao.com) + cuenta sandbox creada (último paso: código de verificación 466104 del 14/09, ya caducado). Pass Paddle: `Hr49iU71iz2TPKBV` (también en /tmp/paddle_pw.txt).
- **Lemon Squeezy** (en desuso): store "Nandns" test-mode; producto 1296344 (variantes Anual 2028222 60€/año, Mensual 2028770 7€/mes), donación PWYW 1296701, webhook 127450, API key en .env del servidor.

## Estado app nandns (farnsworth /var/www/dns.nandezgarcia.com)
- Web trilingüe es/en/zh, SEO, Premium (LS test), donación visible arriba del todo.
- .env del servidor tiene claves LS de TEST. Repo: github.com/nandezgarcia/nandns (workspace: workspaces/dns-kiokao-com).
- SSH: andres@10.13.0.1 pass aliva-2007 (sudo OK). Servicio: dns-nandezgarcia.service. Tests: tests/manual_check.py (45 checks).
- Plan de 6 hosts gratis / 100 premium. Admin nandezgarcia@gmail.com (ilimitado, plan premium por compra test LS).

## PLAN BMC (pasos pendientes)
1. Terminar registro BMC (verificar acceso al dashboard).
2. Crear membresía Premium: mensual 7€ + anual 60€ (dos niveles o tier con ambas opciones).
3. Donaciones: vienen de serie en la página BMC.
4. Webhook BMC → https://dns.kiokao.com/webhook/buymeacoffee + signing secret.
5. Backend app.py: nuevo endpoint webhook BMC (verificar firma, eventos membership.*), activar premium por MATCH DE EMAIL del supporter con users.email (los usuarios nandns son emails Gmail). billing_checkout devuelve la URL pública de la membresía BMC. Portal: cuenta del supporter en BMC.
6. Env vars nuevas: BMC_WEBHOOK_SECRET, BMC_MEMBERSHIP_URL, BMC_DONATE_URL (reemplazar LS_* cuando todo funcione).
7. Tests + deploy + E2E (BMC tiene "Send test event" en el dashboard de webhooks).

## Otros pendientes
- awesome-selfhosted-data PR #2920 (en revisión, sin acción).
- Search Console + Bing: hechos (sitemap OK).
- PROMOCION.md: publicar difusión cuando el usuario se loguee en plataformas (HN/Reddit/PH/Menéame/X/dev.to — ninguna con sesión activa).
- Cron diario de comprobación LS: CANCELADO de facto con el cambio a BMC (no recrear).
- WebBridge: sesiones "bmc-setup" (activa), "paddle-setup", "lemonsqueezy-setup". Daemon: ~/.kimi-webbridge/bin/kimi-webbridge start.
