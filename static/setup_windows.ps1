# nandns - Instalador silencioso para Windows
# Descarga y ejecuta como Administrador

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Instalador nandns (dns.kiokao.com)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Solicitar datos
$defaultToken = ""
$subdomain = Read-Host "Nombre de tu subdominio (sin .dns.kiokao.com, ej: prueba)"
if ([string]::IsNullOrWhiteSpace($subdomain)) {
    Write-Host "Error: Debes introducir un nombre de subdominio." -ForegroundColor Red
    pause
    exit 1
}

$token = Read-Host "Tu API Token [pulsa Enter para omitir]"
if ([string]::IsNullOrWhiteSpace($token)) {
    $token = $defaultToken
}

$scriptDir = "C:\Scripts"
$scriptPath = "$scriptDir\nandns-update.ps1"
$ipFile = "$env:LOCALAPPDATA\nandns_lastip.txt"
$taskName = "nandns-update"

# Crear directorio
if (!(Test-Path $scriptDir)) {
    New-Item -ItemType Directory -Path $scriptDir -Force | Out-Null
    Write-Host "Creado directorio: $scriptDir" -ForegroundColor Green
}

# Crear script de actualizacion silencioso
$updateScript = @"
`$token = "$token"
`$domains = "$subdomain"
`$updateUrl = "https://dns.kiokao.com/update?domains=`$domains&token=`$token"
`$ipFile = "$ipFile"

try {
    `$currentIp = (Invoke-RestMethod -Uri "https://api.ipify.org?format=json" -TimeoutSec 10).ip
    `$lastIp = ""
    if (Test-Path `$ipFile) {
        `$lastIp = Get-Content `$ipFile -ErrorAction SilentlyContinue
    }
    if (`$currentIp -ne `$lastIp) {
        `$response = Invoke-RestMethod -Uri `$updateUrl -TimeoutSec 30
        if (`$response -eq "OK") {
            Set-Content -Path `$ipFile -Value `$currentIp
        }
    }
} catch { }
"@

Set-Content -Path $scriptPath -Value $updateScript -Encoding UTF8
Write-Host "Creado script: $scriptPath" -ForegroundColor Green

# Crear tarea programada (oculta, sin ventana)
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 9999)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -Hidden
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType S4U -RunLevel Highest

# Eliminar tarea anterior si existe
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force | Out-Null
Write-Host "Tarea programada creada: '$taskName' (cada 5 minutos, sin ventana)" -ForegroundColor Green

# Borrar cache anterior para forzar la primera actualizacion
# (util si se reinstala o se cambia de subdominio)
if (Test-Path $ipFile) {
    Remove-Item -Path $ipFile -Force
}

# Prueba inicial silenciosa
Write-Host ""
Write-Host "Ejecutando prueba inicial..." -ForegroundColor Yellow
& powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "$scriptPath"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  INSTALACION COMPLETADA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Subdominio: $subdomain.dns.kiokao.com" -ForegroundColor White
Write-Host ""
Write-Host "La tarea se ejecuta cada 5 minutos en segundo plano." -ForegroundColor Cyan
Write-Host "Puedes verificarla en el Programador de Tareas." -ForegroundColor Cyan
Write-Host ""
pause
