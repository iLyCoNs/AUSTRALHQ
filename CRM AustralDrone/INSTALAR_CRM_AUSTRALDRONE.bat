@echo off
title CRM AUSTRALDRONE ENTERPRISE -- EJECUTABLE WINDOWS
color 0B
cls
echo ====================================================================
echo        🛸 AUSTRALDRONE.CL -- ENTERPRISE CRM WINDOWS SUITE
echo ====================================================================
echo.

echo ====================================================================
echo  SELECCIONA UNA OPCION:
echo ====================================================================
echo [1] Iniciar Programa Nativo de Escritorio (Modo Electron)
echo [2] Compilar Programa Ejecutable de Windows (dist\CRM_AustralDrone_Enterprise.exe)
echo [3] Abrir Ejecutable Compilado (.exe)
echo ====================================================================
set /p op="Opcion (1, 2 o 3): "

if "%op%"=="1" (
    echo.
    echo Invocando Programa Nativo de Escritorio...
    cmd.exe /c "npx electron ."
    goto fin
)

if "%op%"=="2" (
    echo.
    echo Compilando ejecutable nativo de Windows (dist\CRM_AustralDrone_Enterprise.exe)...
    cmd.exe /c "npx electron-packager . CRM_AustralDrone_Enterprise --platform=win32 --arch=x64 --out=dist --overwrite"
    echo.
    echo ¡COMPILACION EXITOSA!
    echo Tu programa ejecutable esta listo en:
    echo dist\CRM_AustralDrone_Enterprise-win32-x64\CRM_AustralDrone_Enterprise.exe
    goto fin
)

if "%op%"=="3" (
    echo.
    echo Lanzando CRM_AustralDrone_Enterprise.exe...
    start "" "dist\CRM_AustralDrone_Enterprise-win32-x64\CRM_AustralDrone_Enterprise.exe"
    goto fin
)

:fin
echo.
echo Operacion finalizada.
pause
