# -*- coding: utf-8 -*-
"""Traducciones de nandns (es / en / zh).

Las claves deben ser idénticas en los tres idiomas. El template usa el dict
como `t` y el frontend JS recibe el dict completo como window.I18N.
Los valores {var} se sustituyen con .format() (Jinja) o con t(key, vars) (JS).
"""

ES = {
    # --- meta / chrome ---
    "meta_title": "nandns — DNS dinámico gratuito | tu subdominio .dns.kiokao.com",
    "meta_description": "Servicio gratuito de DNS dinámico (DDNS): crea hasta 6 subdominios .dns.kiokao.com que apuntan siempre a tu IP. API compatible con DuckDNS, actualización automática y plan Premium de 100 hosts por 60 €/año o 7 €/mes.",
    "header_tagline": "DNS dinámico gratuito: tu subdominio .dns.kiokao.com siempre apuntando a tu IP",
    # --- login ---
    "login_title": "Iniciar sesión",
    "login_subtitle": "Solo cuentas Gmail",
    "terms_label": "Acepto usar este servicio de forma responsable y conforme a la legislación vigente. Me comprometo a no utilizar nandns para actividades ilegales, spam, phishing ni ninguna actividad que pueda dañar a terceros o al funcionamiento del servicio.",
    "google_btn": "Continuar con Google",
    # --- dashboard ---
    "your_token": "Tu API Token",
    "token_help": "Usa este token para actualizar tus dominios:",
    "logout": "Cerrar sesión",
    "admin_btn": "Admin",
    "plan_badge_free": "Gratis",
    "plan_badge_premium": "Premium",
    "plan_renews": "Se renueva el {date}",
    "plan_until_cancelled": "Activo hasta el {date} (cancelada, no se renovará)",
    "upgrade_btn": "Hazte Premium — 60 €/año",
    "manage_btn": "Gestionar suscripción",
    # --- añadir dominio ---
    "add_title": "Añadir subdominio",
    "badge_max": "Máx. {max}",
    "add_count": "Llevas {count}/{max} subdominios.",
    "name_ph": "nombre",
    "ip_ph": "IP (ej: 1.2.3.4) - deja en blanco para usar tu IP actual",
    "create_btn": "Crear subdominio",
    "premium_cta": "¿Necesitas más? Con Premium llegas hasta {max} subdominios por 60 €/año (o 7 €/mes).",
    # --- lista ---
    "your_domains": "Tus subdominios",
    "no_domains": "No tienes subdominios aún.",
    "update_ip_btn": "Actualizar IP",
    "delete_btn": "Eliminar",
    # --- API ---
    "api_title": "🔗 API",
    "api_help": "Actualiza tu IP desde cualquier cliente:",
    "copy_btn": "Copiar",
    "copied": "Copiado!",
    "api_note": "Si omites <code>ip</code>, se usará la IP de origen de la petición.",
    # --- setup ---
    "setup_title": "⚙️ Configurar actualización automática",
    "win_help": "Abre <b>PowerShell como Administrador</b> y ejecuta:",
    "mac_help": "Abre la <b>Terminal</b> y ejecuta (sustituye <code>prueba</code>):",
    "linux_help": "Abre la <b>Terminal</b> y ejecuta (sustituye <code>prueba</code>):",
    "token_note": "Si quieres incluir el token: <code>bash -s prueba TU_TOKEN</code>",
    # --- admin ---
    "admin_title": "Panel de Administración",
    "back_btn": "← Volver",
    "stat_users": "Usuarios",
    "stat_domains": "Subdominios",
    "stat_premium": "Premium",
    "all_domains": "Todos los subdominios",
    "col_subdomain": "Subdominio",
    "col_ip": "IP",
    "col_user": "Usuario",
    "col_updated": "Actualizado",
    "none_domains": "No hay subdominios.",
    # --- JS ---
    "js_error_prefix": "Error: ",
    "js_confirm_delete": "¿Eliminar subdominio?",
    "js_new_ip_prompt": "Nueva IP (deja en blanco para detectar automáticamente):",
    "js_domain_created": "Subdominio creado",
    "js_generic_error": "Error",
    # --- landing: qué es ---
    "what_title": "¿Qué es el DNS dinámico (DDNS)?",
    "what_p1": "La mayoría de las conexiones domésticas tienen una IP que cambia cada cierto tiempo. Un servicio de DNS dinámico (DDNS) mantiene un nombre de dominio apuntando siempre a tu IP actual, aunque cambie.",
    "what_p2": "Con nandns creas subdominios como <code>micasa.dns.kiokao.com</code> y un pequeño script (o tu propio router) actualiza la IP automáticamente cada pocos minutos. Tu nombre de dominio nunca deja de funcionar.",
    "uses_title": "¿Para qué puedes usarlo?",
    "uses_items": [
        "Acceder a tu PC o NAS de casa desde cualquier lugar",
        "Self-hosting: Nextcloud, Home Assistant, Jellyfin, tu propia web…",
        "Cámaras IP y domótica",
        "Servidores de juegos (Minecraft, Valheim…)",
        "Tu propia VPN con WireGuard u OpenVPN",
    ],
    # --- landing: comparativa ---
    "compare_title": "nandns frente a DuckDNS y No-IP",
    "compare_p": "Existen otros servicios de DNS dinámico. Así se compara nandns con los más conocidos:",
    "compare_col_feature": "Característica",
    "compare_rows": [
        ["Subdominios gratis", "6", "5", "1"],
        ["El plan gratis caduca", "Nunca", "Nunca", "Cada 30 días hay que confirmarlo"],
        ["API compatible con DuckDNS", "Sí", "Sí", "No"],
        ["Plan Premium", "100 hosts — 60 €/año", "—", "Desde ~2 $/mes"],
        ["Código abierto", "Sí", "No", "No"],
    ],
    # --- landing: precios ---
    "pricing_title": "Precios",
    "pricing_sub": "Gratis para siempre. Premium si necesitas más.",
    "free_name": "Gratis",
    "free_price": "0 €",
    "free_per": "",
    "free_features": [
        "Hasta 6 subdominios",
        "Sin caducidad",
        "API compatible con DuckDNS",
        "Actualización automática cada 5 minutos",
    ],
    "free_cta": "Crear cuenta gratis",
    "premium_name": "Premium",
    "premium_price": "60 €",
    "premium_per": "/año",
    "premium_save": "Equivale a 5 €/mes — ahorras 24 € al año",
    "premium_features": [
        "Hasta 100 subdominios",
        "Todo lo del plan Gratis",
        "Soporte prioritario por email",
        "Ayudas a mantener el servicio",
    ],
    "premium_cta": "Pagar 60 €/año",
    "premium_cta_monthly": "O 7 €/mes",
    "pricing_note": "Pagos gestionados por Lemon Squeezy (IVA incluido). Puedes cancelar cuando quieras.",
    # --- landing: FAQ ---
    "faq_title": "Preguntas frecuentes",
    "faq_items": [
        ["¿Es realmente gratis?",
         "Sí. El plan gratuito incluye hasta 6 subdominios para siempre, sin caducidad ni confirmaciones periódicas. Si necesitas más, el plan Premium permite hasta 100 por 60 €/año (o 7 €/mes si prefieres pagar mes a mes)."],
        ["¿Qué es exactamente un subdominio .dns.kiokao.com?",
         "Es un registro DNS tipo A (por ejemplo micasa.dns.kiokao.com) que apunta a la IP que tú indiques. Cuando tu IP cambia, el subdominio se actualiza automáticamente con el script o la API."],
        ["¿Cómo actualizo mi IP automáticamente?",
         "Desde el panel puedes instalar el script para Windows, macOS o Linux: se ejecuta cada 5 minutos y actualiza tu subdominio. La API es compatible con DuckDNS, así que también funciona en routers y herramientas que soporten DDNS personalizado."],
        ["¿Por qué solo se puede entrar con Gmail?",
         "Para simplificar el servicio y reducir el abuso: no guardamos contraseñas y Google se encarga de la autenticación. Solo recibimos tu dirección de correo."],
        ["¿Puedo usar mi propio dominio?",
         "No. nandns solo ofrece subdominios de dns.kiokao.com. Si necesitas un dominio propio, servicios como Cloudflare te permiten gestionar el DNS de tu dominio directamente."],
        ["¿Qué pasa si cancelo Premium?",
         "Conservas el plan Premium hasta el final del periodo ya pagado. Después vuelves al límite gratuito de 6 subdominios: los que ya tengas creados no se borran, pero no podrás crear nuevos por encima del límite."],
    ],
    # --- landing: donaciones ---
    "donate_title": "☕ Apoya nandns",
    "donate_body": "nandns es gratis y lo seguirá siendo. Si te resulta útil, puedes invitarme a un café: ayuda a pagar el servidor y el dominio.",
    "donate_btn": "Invítame a un café ☕",
    # --- footer / legal ---
    "footer_made": "Hecho con FastAPI y Cloudflare",
    "footer_legal": "Aviso legal",
    "footer_privacy": "Privacidad",
    "footer_terms": "Condiciones",
    "footer_github": "Código fuente",
    "back_home": "← Volver a nandns",
    # --- páginas legales ---
    "legal_legal_title": "Aviso legal",
    "legal_legal_body": """
<h2>Titular del servicio</h2>
<p>nandns (dns.kiokao.com) es un servicio operado a título personal por su titular, contactable en <a href="mailto:nandezgarcia@gmail.com">nandezgarcia@gmail.com</a>. Sitio web: https://dns.kiokao.com.</p>
<h2>Objeto</h2>
<p>Este aviso legal regula el acceso y uso del sitio web y del servicio de DNS dinámico ofrecido en dns.kiokao.com, conforme a la Ley 34/2002, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE).</p>
<h2>Condiciones de uso</h2>
<p>El uso del servicio implica la aceptación de las <a href="/condiciones">Condiciones del servicio</a> y de la <a href="/privacidad">Política de privacidad</a>.</p>
<h2>Responsabilidad</h2>
<p>El titular no se responsabiliza del uso indebido del servicio por parte de los usuarios ni de los contenidos alojados en los equipos a los que apunten los subdominios creados.</p>
""",
    "legal_privacidad_title": "Política de privacidad",
    "legal_privacidad_body": """
<h2>Responsable del tratamiento</h2>
<p>El titular de nandns (contacto: <a href="mailto:nandezgarcia@gmail.com">nandezgarcia@gmail.com</a>).</p>
<h2>Datos que tratamos</h2>
<ul>
<li><b>Dirección de correo electrónico</b> (obtenida mediante Google OAuth; solo cuentas @gmail.com).</li>
<li><b>Subdominios e IPs</b> que registras en el servicio.</li>
<li><b>Token de API</b> generado para tu cuenta.</li>
</ul>
<p>No usamos cookies de seguimiento. Solo una cookie técnica temporal durante el inicio de sesión y almacenamiento local del navegador (localStorage) para tu token.</p>
<h2>Finalidad y base jurídica</h2>
<p>Prestar el servicio de DNS dinámico solicitado (ejecución del contrato, art. 6.1.b RGPD) y, en su caso, gestionar la suscripción Premium.</p>
<h2>Terceros</h2>
<ul>
<li><b>Google</b> (autenticación OAuth).</li>
<li><b>Cloudflare</b> (registros DNS; los subdominios e IPs se sincronizan con su API).</li>
<li><b>Lemon Squeezy</b> (pagos de la suscripción Premium; actúa como vendedor y gestiona la facturación e IVA).</li>
</ul>
<h2>Conservación</h2>
<p>Los datos se conservan mientras mantengas tu cuenta activa. Puedes eliminar tus subdominios desde el panel; para eliminar tu cuenta por completo, escríbenos.</p>
<h2>Tus derechos</h2>
<p>Puedes ejercer los derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a <a href="mailto:nandezgarcia@gmail.com">nandezgarcia@gmail.com</a>. También puedes reclamar ante la Agencia Española de Protección de Datos (aepd.es).</p>
""",
    "legal_condiciones_title": "Condiciones del servicio",
    "legal_condiciones_body": """
<h2>El servicio</h2>
<p>nandns ofrece subdominios de dns.kiokao.com con DNS dinámico: registros A que apuntan a tu IP y se actualizan mediante una API o script.</p>
<h2>Cuentas</h2>
<p>El acceso requiere una cuenta de Google (@gmail.com). Eres responsable de la custodia de tu token de API.</p>
<h2>Planes y límites</h2>
<ul>
<li><b>Gratis:</b> hasta 6 subdominios, sin caducidad.</li>
<li><b>Premium:</b> hasta 100 subdominios, por 60 €/año o 7 €/mes. La suscripción se gestiona a través de Lemon Squeezy, que actúa como vendedor y emite la factura. Puedes cancelarla en cualquier momento desde tu portal de cliente; conservas el plan hasta el final del periodo pagado y no hay reembolsos prorrateados salvo que la ley disponga lo contrario.</li>
</ul>
<h2>Uso aceptable</h2>
<p>Queda prohibido usar el servicio para actividades ilegales, phishing, spam, malware o cualquier uso que dañe a terceros o al propio servicio. El incumplimiento puede suponer la suspensión inmediata de la cuenta y la eliminación de los subdominios.</p>
<h2>Disponibilidad</h2>
<p>El servicio se ofrece "tal cual", con el mejor esfuerzo, pero sin garantía de disponibilidad continua (sin SLA). El titular puede modificar o interrumpir el servicio, procurando avisar con antelación razonable.</p>
<h2>Cambios en las condiciones</h2>
<p>Podemos actualizar estas condiciones; la versión vigente estará siempre publicada en esta página.</p>
<h2>Ley aplicable</h2>
<p>Estas condiciones se rigen por la legislación española.</p>
""",
}

EN = {
    "meta_title": "nandns — Free dynamic DNS | your .dns.kiokao.com subdomain",
    "meta_description": "Free dynamic DNS (DDNS) service: create up to 6 .dns.kiokao.com subdomains that always point to your current IP. DuckDNS-compatible API, automatic updates and a 100-host Premium plan for €60/year or €7/month.",
    "header_tagline": "Free dynamic DNS: your .dns.kiokao.com subdomain always pointing to your IP",
    "login_title": "Sign in",
    "login_subtitle": "Gmail accounts only",
    "terms_label": "I agree to use this service responsibly and in compliance with applicable law. I will not use nandns for illegal activities, spam, phishing or any activity that could harm third parties or the service itself.",
    "google_btn": "Continue with Google",
    "your_token": "Your API Token",
    "token_help": "Use this token to update your domains:",
    "logout": "Sign out",
    "admin_btn": "Admin",
    "plan_badge_free": "Free",
    "plan_badge_premium": "Premium",
    "plan_renews": "Renews on {date}",
    "plan_until_cancelled": "Active until {date} (cancelled, will not renew)",
    "upgrade_btn": "Go Premium — €60/year",
    "manage_btn": "Manage subscription",
    "add_title": "Add subdomain",
    "badge_max": "Max {max}",
    "add_count": "You have {count}/{max} subdomains.",
    "name_ph": "name",
    "ip_ph": "IP (e.g. 1.2.3.4) - leave blank to use your current IP",
    "create_btn": "Create subdomain",
    "premium_cta": "Need more? Premium gives you up to {max} subdomains for €60/year (or €7/month).",
    "your_domains": "Your subdomains",
    "no_domains": "You have no subdomains yet.",
    "update_ip_btn": "Update IP",
    "delete_btn": "Delete",
    "api_title": "🔗 API",
    "api_help": "Update your IP from any client:",
    "copy_btn": "Copy",
    "copied": "Copied!",
    "api_note": "If you omit <code>ip</code>, the request's source IP will be used.",
    "setup_title": "⚙️ Set up automatic updates",
    "win_help": "Open <b>PowerShell as Administrator</b> and run:",
    "mac_help": "Open the <b>Terminal</b> and run (replace <code>prueba</code>):",
    "linux_help": "Open the <b>Terminal</b> and run (replace <code>prueba</code>):",
    "token_note": "To include the token: <code>bash -s prueba YOUR_TOKEN</code>",
    "admin_title": "Administration Panel",
    "back_btn": "← Back",
    "stat_users": "Users",
    "stat_domains": "Subdomains",
    "stat_premium": "Premium",
    "all_domains": "All subdomains",
    "col_subdomain": "Subdomain",
    "col_ip": "IP",
    "col_user": "User",
    "col_updated": "Updated",
    "none_domains": "No subdomains.",
    "js_error_prefix": "Error: ",
    "js_confirm_delete": "Delete subdomain?",
    "js_new_ip_prompt": "New IP (leave blank to auto-detect):",
    "js_domain_created": "Subdomain created",
    "js_generic_error": "Error",
    "what_title": "What is dynamic DNS (DDNS)?",
    "what_p1": "Most home internet connections have an IP address that changes from time to time. A dynamic DNS (DDNS) service keeps a domain name always pointing to your current IP, even when it changes.",
    "what_p2": "With nandns you create subdomains like <code>myhome.dns.kiokao.com</code> and a small script (or your own router) updates the IP automatically every few minutes. Your domain name never stops working.",
    "uses_title": "What can you use it for?",
    "uses_items": [
        "Reach your home PC or NAS from anywhere",
        "Self-hosting: Nextcloud, Home Assistant, Jellyfin, your own website…",
        "IP cameras and home automation",
        "Game servers (Minecraft, Valheim…)",
        "Your own VPN with WireGuard or OpenVPN",
    ],
    "compare_title": "nandns vs DuckDNS and No-IP",
    "compare_p": "There are other dynamic DNS services. Here is how nandns compares with the best-known ones:",
    "compare_col_feature": "Feature",
    "compare_rows": [
        ["Free subdomains", "6", "5", "1"],
        ["Free plan expires", "Never", "Never", "Must be confirmed every 30 days"],
        ["DuckDNS-compatible API", "Yes", "Yes", "No"],
        ["Premium plan", "100 hosts — €60/year", "—", "From ~$2/month"],
        ["Open source", "Yes", "No", "No"],
    ],
    "pricing_title": "Pricing",
    "pricing_sub": "Free forever. Premium if you need more.",
    "free_name": "Free",
    "free_price": "€0",
    "free_per": "",
    "free_features": [
        "Up to 6 subdomains",
        "No expiry",
        "DuckDNS-compatible API",
        "Automatic updates every 5 minutes",
    ],
    "free_cta": "Create free account",
    "premium_name": "Premium",
    "premium_price": "€60",
    "premium_per": "/year",
    "premium_save": "Works out at €5/month — save €24 a year",
    "premium_features": [
        "Up to 100 subdomains",
        "Everything in the Free plan",
        "Priority email support",
        "You help keep the service running",
    ],
    "premium_cta": "Pay €60/year",
    "premium_cta_monthly": "Or €7/month",
    "pricing_note": "Payments handled by Lemon Squeezy (VAT included). Cancel anytime.",
    "faq_title": "Frequently asked questions",
    "faq_items": [
        ["Is it really free?",
         "Yes. The free plan includes up to 6 subdomains forever, with no expiry and no periodic confirmations. If you need more, the Premium plan allows up to 100 for €60/year (or €7/month if you prefer to pay monthly)."],
        ["What exactly is a .dns.kiokao.com subdomain?",
         "It is a DNS A record (e.g. myhome.dns.kiokao.com) pointing to the IP you choose. When your IP changes, the subdomain is updated automatically via the script or the API."],
        ["How do I update my IP automatically?",
         "From the dashboard you can install the script for Windows, macOS or Linux: it runs every 5 minutes and updates your subdomain. The API is DuckDNS-compatible, so it also works with routers and tools that support custom DDNS."],
        ["Why can I only sign in with Gmail?",
         "To keep the service simple and reduce abuse: we store no passwords and Google handles authentication. We only receive your email address."],
        ["Can I use my own domain?",
         "No. nandns only offers subdomains of dns.kiokao.com. If you need your own domain, services like Cloudflare let you manage your domain's DNS directly."],
        ["What happens if I cancel Premium?",
         "You keep the Premium plan until the end of the period you already paid for. Then you go back to the free limit of 6 subdomains: the ones you already created are not deleted, but you cannot create new ones above the limit."],
    ],
    "donate_title": "☕ Support nandns",
    "donate_body": "nandns is free and will stay free. If you find it useful, you can buy me a coffee: it helps pay for the server and the domain.",
    "donate_btn": "Buy me a coffee ☕",
    "footer_made": "Built with FastAPI and Cloudflare",
    "footer_legal": "Legal notice",
    "footer_privacy": "Privacy",
    "footer_terms": "Terms",
    "footer_github": "Source code",
    "back_home": "← Back to nandns",
    "legal_legal_title": "Legal notice",
    "legal_legal_body": """
<h2>Service owner</h2>
<p>nandns (dns.kiokao.com) is a service operated personally by its owner, reachable at <a href="mailto:nandezgarcia@gmail.com">nandezgarcia@gmail.com</a>. Website: https://dns.kiokao.com.</p>
<h2>Purpose</h2>
<p>This legal notice governs access to and use of the website and of the dynamic DNS service offered at dns.kiokao.com, in accordance with Spanish Law 34/2002 on Information Society Services and Electronic Commerce (LSSI-CE).</p>
<h2>Terms of use</h2>
<p>Using the service implies acceptance of the <a href="/en/condiciones">Terms of service</a> and the <a href="/en/privacidad">Privacy policy</a>.</p>
<h2>Liability</h2>
<p>The owner is not responsible for misuse of the service by users, nor for content hosted on the machines that user-created subdomains point to.</p>
""",
    "legal_privacidad_title": "Privacy policy",
    "legal_privacidad_body": """
<h2>Data controller</h2>
<p>The owner of nandns (contact: <a href="mailto:nandezgarcia@gmail.com">nandezgarcia@gmail.com</a>).</p>
<h2>Data we process</h2>
<ul>
<li><b>Email address</b> (obtained via Google OAuth; @gmail.com accounts only).</li>
<li><b>Subdomains and IPs</b> you register in the service.</li>
<li><b>API token</b> generated for your account.</li>
</ul>
<p>We do not use tracking cookies. Only a temporary technical cookie during sign-in and browser local storage (localStorage) for your token.</p>
<h2>Purpose and legal basis</h2>
<p>Providing the requested dynamic DNS service (performance of a contract, art. 6.1.b GDPR) and, where applicable, managing the Premium subscription.</p>
<h2>Third parties</h2>
<ul>
<li><b>Google</b> (OAuth authentication).</li>
<li><b>Cloudflare</b> (DNS records; subdomains and IPs are synced with their API).</li>
<li><b>Lemon Squeezy</b> (Premium subscription payments; they act as the seller and handle billing and VAT).</li>
</ul>
<h2>Retention</h2>
<p>Data is kept while your account remains active. You can delete your subdomains from the dashboard; to delete your account entirely, contact us.</p>
<h2>Your rights</h2>
<p>You may exercise your rights of access, rectification, erasure, objection, restriction and portability by writing to <a href="mailto:nandezgarcia@gmail.com">nandezgarcia@gmail.com</a>. You may also lodge a complaint with the Spanish Data Protection Agency (aepd.es).</p>
""",
    "legal_condiciones_title": "Terms of service",
    "legal_condiciones_body": """
<h2>The service</h2>
<p>nandns provides subdomains of dns.kiokao.com with dynamic DNS: A records pointing to your IP, updated via an API or script.</p>
<h2>Accounts</h2>
<p>Access requires a Google account (@gmail.com). You are responsible for keeping your API token safe.</p>
<h2>Plans and limits</h2>
<ul>
<li><b>Free:</b> up to 6 subdomains, no expiry.</li>
<li><b>Premium:</b> up to 100 subdomains, for €60/year or €7/month. The subscription is managed through Lemon Squeezy, which acts as the seller and issues the invoice. You can cancel anytime from your customer portal; you keep the plan until the end of the paid period and there are no pro-rated refunds unless the law says otherwise.</li>
</ul>
<h2>Acceptable use</h2>
<p>Using the service for illegal activities, phishing, spam, malware or any use that harms third parties or the service itself is forbidden. Breaches may lead to immediate account suspension and deletion of subdomains.</p>
<h2>Availability</h2>
<p>The service is provided "as is", on a best-effort basis, with no guarantee of continuous availability (no SLA). The owner may modify or discontinue the service, trying to give reasonable advance notice.</p>
<h2>Changes to these terms</h2>
<p>We may update these terms; the current version will always be published on this page.</p>
<h2>Governing law</h2>
<p>These terms are governed by Spanish law.</p>
""",
}

ZH = {
    "meta_title": "nandns — 免费动态DNS | 你的 .dns.kiokao.com 子域名",
    "meta_description": "免费动态DNS（DDNS）服务：创建最多6个始终指向你当前IP的 .dns.kiokao.com 子域名。兼容DuckDNS的API、自动更新，另有Premium方案：100个主机，60 €/年或7 €/月。",
    "header_tagline": "免费动态DNS：你的 .dns.kiokao.com 子域名始终指向你的IP",
    "login_title": "登录",
    "login_subtitle": "仅限Gmail账户",
    "terms_label": "我同意遵守适用法律并负责任地使用本服务。我承诺不会将nandns用于非法活动、垃圾邮件、网络钓鱼或任何可能损害第三方或服务本身的行为。",
    "google_btn": "使用Google登录",
    "your_token": "你的API令牌",
    "token_help": "使用此令牌更新你的域名：",
    "logout": "退出登录",
    "admin_btn": "管理",
    "plan_badge_free": "免费版",
    "plan_badge_premium": "Premium",
    "plan_renews": "将于 {date} 续订",
    "plan_until_cancelled": "有效期至 {date}（已取消，不再续订）",
    "upgrade_btn": "升级Premium — 60 €/年",
    "manage_btn": "管理订阅",
    "add_title": "添加子域名",
    "badge_max": "最多 {max} 个",
    "add_count": "你已有 {count}/{max} 个子域名。",
    "name_ph": "名称",
    "ip_ph": "IP（例如 1.2.3.4）— 留空则使用当前IP",
    "create_btn": "创建子域名",
    "premium_cta": "需要更多？Premium每年60 €（或每月7 €），最多 {max} 个子域名。",
    "your_domains": "你的子域名",
    "no_domains": "你还没有子域名。",
    "update_ip_btn": "更新IP",
    "delete_btn": "删除",
    "api_title": "🔗 API",
    "api_help": "从任何客户端更新你的IP：",
    "copy_btn": "复制",
    "copied": "已复制！",
    "api_note": "如果省略 <code>ip</code>，将使用请求的来源IP。",
    "setup_title": "⚙️ 配置自动更新",
    "win_help": "以<b>管理员身份打开PowerShell</b>并运行：",
    "mac_help": "打开<b>终端</b>并运行（替换 <code>prueba</code>）：",
    "linux_help": "打开<b>终端</b>并运行（替换 <code>prueba</code>）：",
    "token_note": "如需包含令牌：<code>bash -s prueba 你的令牌</code>",
    "admin_title": "管理面板",
    "back_btn": "← 返回",
    "stat_users": "用户",
    "stat_domains": "子域名",
    "stat_premium": "Premium",
    "all_domains": "所有子域名",
    "col_subdomain": "子域名",
    "col_ip": "IP",
    "col_user": "用户",
    "col_updated": "更新时间",
    "none_domains": "暂无子域名。",
    "js_error_prefix": "错误：",
    "js_confirm_delete": "删除子域名？",
    "js_new_ip_prompt": "新IP（留空则自动检测）：",
    "js_domain_created": "子域名已创建",
    "js_generic_error": "错误",
    "what_title": "什么是动态DNS（DDNS）？",
    "what_p1": "大多数家庭网络的IP地址会不定期变化。动态DNS（DDNS）服务能让一个域名始终指向你当前的IP，即使它发生变化。",
    "what_p2": "使用nandns，你可以创建类似 <code>myhome.dns.kiokao.com</code> 的子域名，一个小脚本（或你的路由器）每隔几分钟自动更新IP。你的域名永不失效。",
    "uses_title": "可以用来做什么？",
    "uses_items": [
        "随时随地访问家里的电脑或NAS",
        "自托管：Nextcloud、Home Assistant、Jellyfin、个人网站……",
        "网络摄像头与智能家居",
        "游戏服务器（Minecraft、Valheim……）",
        "使用WireGuard或OpenVPN搭建自己的VPN",
    ],
    "compare_title": "nandns 与 DuckDNS、No-IP 对比",
    "compare_p": "市面上还有其他动态DNS服务，以下是nandns与最知名服务的对比：",
    "compare_col_feature": "特性",
    "compare_rows": [
        ["免费子域名数量", "6", "5", "1"],
        ["免费方案是否过期", "永不", "永不", "每30天需确认一次"],
        ["兼容DuckDNS的API", "是", "是", "否"],
        ["Premium方案", "100个主机 — 60 €/年", "—", "约2 $/月起"],
        ["开源", "是", "否", "否"],
    ],
    "pricing_title": "价格",
    "pricing_sub": "永久免费。需要更多可选Premium。",
    "free_name": "免费版",
    "free_price": "0 €",
    "free_per": "",
    "free_features": [
        "最多6个子域名",
        "永不过期",
        "兼容DuckDNS的API",
        "每5分钟自动更新",
    ],
    "free_cta": "免费注册",
    "premium_name": "Premium",
    "premium_price": "60 €",
    "premium_per": "/年",
    "premium_save": "相当于每月5 €——每年节省24 €",
    "premium_features": [
        "最多100个子域名",
        "包含免费版全部功能",
        "优先邮件支持",
        "帮助维持服务运行",
    ],
    "premium_cta": "支付 60 €/年",
    "premium_cta_monthly": "或 7 €/月",
    "pricing_note": "付款由 Lemon Squeezy 处理（含增值税）。随时可以取消。",
    "faq_title": "常见问题",
    "faq_items": [
        ["真的免费吗？",
         "是的。免费方案包含最多6个子域名，永久有效，无需定期确认。如需更多，Premium方案每年60 €（也可选择每月7 €），最多100个。"],
        [".dns.kiokao.com 子域名到底是什么？",
         "它是一条DNS A记录（例如 myhome.dns.kiokao.com），指向你指定的IP。当你的IP变化时，子域名会通过脚本或API自动更新。"],
        ["如何自动更新我的IP？",
         "在面板中可以安装适用于Windows、macOS或Linux的脚本：每5分钟运行一次并更新你的子域名。API兼容DuckDNS，因此也适用于支持自定义DDNS的路由器和工具。"],
        ["为什么只能用Gmail登录？",
         "为了简化服务并减少滥用：我们不保存密码，身份验证由Google完成，我们只会收到你的邮箱地址。"],
        ["可以使用自己的域名吗？",
         "不可以。nandns仅提供 dns.kiokao.com 的子域名。如果你需要自己的域名，可以使用Cloudflare等服务直接管理你域名的DNS。"],
        ["取消Premium会怎样？",
         "你可以保留Premium直到已付费周期结束。之后恢复为6个子域名的免费上限：已创建的子域名不会被删除，但超过上限后无法再创建新的。"],
    ],
    "donate_title": "☕ 支持nandns",
    "donate_body": "nandns免费，并将永远免费。如果它对你有用，可以请我喝杯咖啡：帮助支付服务器和域名费用。",
    "donate_btn": "请我喝杯咖啡 ☕",
    "footer_made": "基于 FastAPI 和 Cloudflare 构建",
    "footer_legal": "法律声明",
    "footer_privacy": "隐私政策",
    "footer_terms": "服务条款",
    "footer_github": "源代码",
    "back_home": "← 返回 nandns",
    "legal_legal_title": "法律声明",
    "legal_legal_body": """
<h2>服务所有者</h2>
<p>nandns（dns.kiokao.com）是由其所有者个人运营的服务，联系方式：<a href="mailto:nandezgarcia@gmail.com">nandezgarcia@gmail.com</a>。网站：https://dns.kiokao.com。</p>
<h2>目的</h2>
<p>本法律声明根据西班牙《信息社会服务与电子商务法》（LSSI-CE，第34/2002号法律）规范对 dns.kiokao.com 网站及动态DNS服务的访问和使用。</p>
<h2>使用条款</h2>
<p>使用本服务即表示接受<a href="/zh/condiciones">服务条款</a>和<a href="/zh/privacidad">隐私政策</a>。</p>
<h2>责任</h2>
<p>所有者不对用户滥用本服务的行为负责，也不对用户创建的子域名所指向设备上托管的内容负责。</p>
""",
    "legal_privacidad_title": "隐私政策",
    "legal_privacidad_body": """
<h2>数据控制者</h2>
<p>nandns的所有者（联系方式：<a href="mailto:nandezgarcia@gmail.com">nandezgarcia@gmail.com</a>）。</p>
<h2>我们处理的数据</h2>
<ul>
<li><b>电子邮箱地址</b>（通过Google OAuth获取；仅限@gmail.com账户）。</li>
<li><b>你在服务中注册的子域名和IP</b>。</li>
<li><b>为你的账户生成的API令牌</b>。</li>
</ul>
<p>我们不使用跟踪Cookie。仅在登录期间使用一个临时技术Cookie，并在浏览器本地存储（localStorage）中保存你的令牌。</p>
<h2>目的与法律依据</h2>
<p>提供你请求的动态DNS服务（履行合同，GDPR第6.1.b条），并在适用时管理Premium订阅。</p>
<h2>第三方</h2>
<ul>
<li><b>Google</b>（OAuth身份验证）。</li>
<li><b>Cloudflare</b>（DNS记录；子域名和IP通过其API同步）。</li>
<li><b>Lemon Squeezy</b>（Premium订阅付款；作为销售方处理账单和增值税）。</li>
</ul>
<h2>保留期限</h2>
<p>在你的账户处于活跃状态期间保留数据。你可以在面板中删除子域名；如需完全删除账户，请联系我们。</p>
<h2>你的权利</h2>
<p>你可以通过发送邮件至 <a href="mailto:nandezgarcia@gmail.com">nandezgarcia@gmail.com</a> 行使访问、更正、删除、反对、限制和可携带权。你也可以向西班牙数据保护局（aepd.es）投诉。</p>
""",
    "legal_condiciones_title": "服务条款",
    "legal_condiciones_body": """
<h2>服务内容</h2>
<p>nandns提供 dns.kiokao.com 的动态DNS子域名：指向你的IP的A记录，可通过API或脚本更新。</p>
<h2>账户</h2>
<p>访问需要Google账户（@gmail.com）。你有责任妥善保管你的API令牌。</p>
<h2>方案与限制</h2>
<ul>
<li><b>免费版：</b>最多6个子域名，永不过期。</li>
<li><b>Premium：</b>最多100个子域名，60 €/年或7 €/月。订阅通过Lemon Squeezy管理，其作为销售方开具发票。你可以随时在客户门户中取消；在已付费周期结束前仍可继续使用，除法律规定外不按比例退款。</li>
</ul>
<h2>可接受使用</h2>
<p>禁止将本服务用于非法活动、网络钓鱼、垃圾邮件、恶意软件或任何损害第三方或服务本身的行为。违规可能导致账户立即被暂停并删除子域名。</p>
<h2>可用性</h2>
<p>本服务按“现状”提供，尽最大努力维护，但不保证持续可用（无SLA）。所有者可能会修改或停止服务，并会尽量提前合理通知。</p>
<h2>条款变更</h2>
<p>我们可能会更新这些条款；当前版本将始终发布在本页面上。</p>
<h2>适用法律</h2>
<p>本条款受西班牙法律管辖。</p>
""",
}

I18N = {"es": ES, "en": EN, "zh": ZH}
LANGS = ("es", "en", "zh")
