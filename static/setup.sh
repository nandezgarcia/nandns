#!/bin/bash
# nandns - Instalador automatico para macOS / Ubuntu / Linux

set -e

echo "========================================"
echo "  Instalador nandns (dns.kiokao.com)"
echo "========================================"
echo ""

# Leer argumentos o preguntar interactivamente
if [ -n "$1" ]; then
    SUBDOMAIN="$1"
else
    read -rp "Nombre de tu subdominio (sin .dns.kiokao.com, ej: prueba): " SUBDOMAIN < /dev/tty
fi

if [ -z "$SUBDOMAIN" ]; then
    echo "Error: Debes introducir un nombre de subdominio."
    echo "Uso: curl -fsSL https://dns.kiokao.com/static/setup.sh | bash -s TU_SUBDOMINIO [TOKEN]"
    exit 1
fi

if [ -n "$2" ]; then
    TOKEN="$2"
else
    read -rp "Tu API Token [pulsa Enter para omitir]: " TOKEN < /dev/tty
fi

SCRIPT_DIR="$HOME/.local/bin"
SCRIPT_PATH="$SCRIPT_DIR/nandns-update"
mkdir -p "$SCRIPT_DIR"

# Crear script de actualizacion
cat > "$SCRIPT_PATH" << EOF
#!/bin/bash
TOKEN="$TOKEN"
DOMAIN="$SUBDOMAIN"
IP_FILE="\$HOME/.nandns_lastip"
API="https://dns.kiokao.com/update?domains=\${DOMAIN}&token=\${TOKEN}"

CURRENT_IP=\$(curl -s --max-time 10 https://api.ipify.org)
if [ -z "\$CURRENT_IP" ]; then
    echo "\$(date '+%Y-%m-%d %H:%M:%S') - Error: no se pudo obtener la IP actual"
    exit 1
fi

LAST_IP=""
if [ -f "\$IP_FILE" ]; then
    LAST_IP=\$(cat "\$IP_FILE")
fi

if [ "\$CURRENT_IP" != "\$LAST_IP" ]; then
    RESPONSE=\$(curl -s --max-time 30 "\${API}&ip=\${CURRENT_IP}")
    if [ "\$RESPONSE" = "OK" ]; then
        echo "\$CURRENT_IP" > "\$IP_FILE"
        echo "\$(date '+%Y-%m-%d %H:%M:%S') - IP actualizada: \$CURRENT_IP"
    else
        echo "\$(date '+%Y-%m-%d %H:%M:%S') - Error del servidor: \$RESPONSE"
    fi
else
    echo "\$(date '+%Y-%m-%d %H:%M:%S') - Sin cambios. IP: \$CURRENT_IP"
fi
EOF

chmod +x "$SCRIPT_PATH"

echo "Script creado en: $SCRIPT_PATH"

# Añadir cron job (cada 5 minutos)
CRON_JOB="*/5 * * * * $SCRIPT_PATH >> $HOME/.nandns.log 2>&1"
(crontab -l 2>/dev/null | grep -v "nandns-update" || true) > /tmp/crontab.tmp
echo "$CRON_JOB" >> /tmp/crontab.tmp
crontab /tmp/crontab.tmp
rm -f /tmp/crontab.tmp

echo "Tarea cron creada (cada 5 minutos)."

# Borrar cache anterior para forzar la primera actualizacion
# (util si se reinstala o se cambia de subdominio)
rm -f "$HOME/.nandns_lastip"

# Ejecutar prueba inicial
echo ""
echo "Ejecutando prueba inicial..."
"$SCRIPT_PATH"

echo ""
echo "========================================"
echo "  INSTALACION COMPLETADA"
echo "========================================"
echo "Subdominio: $SUBDOMAIN.dns.kiokao.com"
echo "Token: $TOKEN"
echo ""
echo "Logs: tail -f ~/.nandns.log"
echo ""
