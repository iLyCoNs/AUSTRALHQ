@echo off
title INSTALADOR Y COMPILADOR CRM AUSTRALDRONE ENTERPRISE
color 0B
cls
echo ====================================================================
echo        🛸 AUSTRALDRONE.CL -- INSTALADOR CRM ENTERPRISE (EXE)
echo ====================================================================
echo.
echo [1/3] Verificando entorno Node.js y dependencias...
call npm install --no-audit --no-fund

echo.
echo ====================================================================
echo  SELECCIONA UNA OPCION DE EJECUCION:
echo ====================================================================
echo [1] Iniciar Programa Nativo de Escritorio (Modo Electron)
echo [2] Compilar Instalador Oficial de Windows (.exe / .msi)
echo [3] Compilar Ejecutable Portable (.exe 1-Clic)
echo ====================================================================
set /p op="Opcion (1, 2 o 3): "

if "%op%"=="1" (
    echo.
    echo Invocando Programa Nativo...
    npx electron .
    goto fin
)

if "%op%"=="2" (
    echo.
    echo Compilando Instalador Oficial de Windows (dist/CRM AustralDrone Setup.exe)...
    npx electron-builder --win nsis
    goto fin
)

if "%op%"=="3" (
    echo.
    echo Compilando Ejecutable Portable (dist/CRM AustralDrone Portable.exe)...
    npx electron-builder --win portable
    goto fin
)

:fin
echo.
echo Operacion finalizada exitosamente.
pause
