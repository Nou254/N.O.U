@echo off
title N.O.U - Install Boot Auto-Start
rem ==========================================================================
rem  Optional step: start N.O.U servers at BOOT (before login).
rem  Double-click this file once and approve the UAC prompt.
rem  The regular logon auto-start (Startup folder) already works without this;
rem  this just adds pre-login startup for extra reliability.
rem ==========================================================================
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"%~f0\"' -Verb RunAs"
    exit /b
)

echo.
echo Registering boot-time task "NOUKeepAliveBoot"...
schtasks /Create /TN "NOUKeepAliveBoot" /TR "wscript.exe \"C:\Users\Erick Juma\Projects\N.O.U\NOUKeepAlive.vbs\"" /SC ONSTARTUP /RU SYSTEM /RL HIGHEST /F
echo.
echo Done. The servers will now start at every boot, before you log in.
echo Frontend: http://localhost:3000   Backend: http://localhost:8000
echo.
pause
