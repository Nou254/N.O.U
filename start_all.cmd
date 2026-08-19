@echo off
title N.O.U - Start All Servers
echo.
echo   Starting N.O.U backend (:8000) and frontend (:3000)...
echo.
start "NOU-Backend" /min cmd /c "C:\Users\Erick Juma\Projects\N.O.U\backend\launch_backend.bat"
start "NOU-Frontend" /min cmd /c "C:\Users\Erick Juma\Projects\N.O.U\frontend\launch_frontend.bat"
echo.
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:8000
echo.
echo   Servers are starting (frontend takes ~30s to be ready).
timeout /t 5 >nul
