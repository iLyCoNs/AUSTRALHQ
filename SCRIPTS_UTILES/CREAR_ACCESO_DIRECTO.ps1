# Script PowerShell — Crea acceso directo con ícono AustralDrone en el Escritorio

$batPath  = "c:\Users\LyCoNs\Desktop\AGENTES IA\INICIAR_BRIDGE_CAZADOR360.bat"
$icoPath  = "c:\Users\LyCoNs\Desktop\AGENTES IA\australdrone.ico"
$linkPath = "$env:USERPROFILE\Desktop\🚁 AustralDrone HQ Bridge.lnk"

$WScriptShell = New-Object -ComObject WScript.Shell
$shortcut = $WScriptShell.CreateShortcut($linkPath)

$shortcut.TargetPath       = $batPath
$shortcut.WorkingDirectory = "c:\Users\LyCoNs\Desktop\AGENTES IA"
$shortcut.IconLocation     = "$icoPath, 0"
$shortcut.Description      = "Inicia el Bridge Cazador 360 y abre AustralDrone HQ"
$shortcut.WindowStyle      = 1

$shortcut.Save()

Write-Host ""
Write-Host "  ✅ Acceso directo creado en el Escritorio:" -ForegroundColor Green
Write-Host "     $linkPath" -ForegroundColor Cyan
Write-Host ""
