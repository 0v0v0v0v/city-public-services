@echo off
setlocal

set "ROOT_DIR=%~dp0"

echo Starting city-public-services...
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://127.0.0.1:5173
echo.

start "City Backend" powershell.exe -NoExit -ExecutionPolicy Bypass -File "%ROOT_DIR%scripts\start-backend.ps1"
start "City Frontend" powershell.exe -NoExit -ExecutionPolicy Bypass -File "%ROOT_DIR%scripts\start-frontend.ps1"

echo Two windows were opened for backend and frontend.
echo You can close this launcher window now.
