@echo off
title AustralDrone HQ — Bridge Cazador 360
color 0A

echo.
echo  ╔══════════════════════════════════════════════════════════╗
echo  ║      AustralDrone.CL — Iniciando Bridge Cazador 360     ║
echo  ║         Conectando al HQ: australhq.onrender.com        ║
echo  ╚══════════════════════════════════════════════════════════╝
echo.

:: Ir al directorio del proyecto
cd /d "c:\Users\LyCoNs\Desktop\AGENTES IA"

:: Abrir el HQ en el navegador predeterminado
start "" "https://australhq.onrender.com"

:: Pequeña pausa para que el navegador cargue
timeout /t 2 /nobreak >nul

:: Iniciar el bridge Node.js
echo  ⚡ Iniciando Bridge Worker...
echo.
node local_bridge_worker.js

:: Si el proceso se cierra, mostrar mensaje
echo.
echo  ⚠️  Bridge detenido. Presiona cualquier tecla para cerrar...
pause >nul
