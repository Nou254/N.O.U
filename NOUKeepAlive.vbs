' N.O.U Keep Alive launcher - runs the server watchdog fully hidden at logon.
' Placed in the user Startup folder so the site is always on after reboot.
CreateObject("Wscript.Shell").Run "powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File ""C:\Users\Erick Juma\Projects\N.O.U\keep_alive.ps1""", 0, False
