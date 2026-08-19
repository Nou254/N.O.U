# ============================================================================
#  N.O.U - Keep Alive Watchdog
#  Keeps the backend (:8000) and frontend (:3000) servers running at all
#  times. Launched at logon from the Startup folder (NOUKeepAlive.vbs), so
#  after a reboot or power-off the servers come back up automatically.
# ============================================================================
$ErrorActionPreference = 'SilentlyContinue'

$BaseDir   = 'C:\Users\Erick Juma\Projects\N.O.U'
$LogFile   = "$BaseDir\keep_alive.log"
$PidFile   = "$BaseDir\keep_alive.pid"

function Log([string]$msg) {
    "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $msg" | Out-File -FilePath $LogFile -Append -Encoding utf8
}

# Single-instance guard: if another watchdog is already running, exit. This
# allows both the boot-time task and the logon Startup entry to point at this
# script without ever starting duplicate servers.
if (Test-Path $PidFile) {
    $oldPid = (Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1)
    if ($oldPid -and (Get-Process -Id $oldPid -ErrorAction SilentlyContinue)) {
        "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') Another watchdog already running (PID $oldPid) - exiting." | Out-File -FilePath $LogFile -Append -Encoding utf8
        exit
    }
}
try { $PID | Out-File -FilePath $PidFile -Encoding ascii } catch {}

$lastBackendStart  = Get-Date
$lastFrontendStart = Get-Date

function Test-Port([int]$port) {
    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $iar = $client.BeginConnect('127.0.0.1', $port, $null, $null)
        $ok = $iar.AsyncWaitHandle.WaitOne(3000, $false)
        if ($ok) { $client.EndConnect($iar) }
        return $ok
    } catch {
        return $false
    } finally {
        $client.Close()
    }
}

function Start-Backend {
    Log 'Backend down - starting...'
    Start-Process -FilePath 'cmd.exe' `
        -ArgumentList '/c', "`"$BaseDir\backend\launch_backend.bat`"" `
        -WorkingDirectory "$BaseDir\backend" `
        -WindowStyle Hidden
}

function Start-Frontend {
    Log 'Frontend down - starting...'
    Start-Process -FilePath 'cmd.exe' `
        -ArgumentList '/c', "`"$BaseDir\frontend\launch_frontend.bat`"" `
        -WorkingDirectory "$BaseDir\frontend" `
        -WindowStyle Hidden
}

Log '=== N.O.U keep-alive watchdog started ==='
Start-Backend
Start-Frontend

while ($true) {
    # Give a freshly-started server up to 90s to open its port before we
    # consider starting another one (prevents duplicate processes).
    if (-not (Test-Port 8000) -and ((Get-Date) - $lastBackendStart).TotalSeconds -gt 90) {
        Start-Backend
        $lastBackendStart = Get-Date
    }
    if (-not (Test-Port 3000) -and ((Get-Date) - $lastFrontendStart).TotalSeconds -gt 90) {
        Start-Frontend
        $lastFrontendStart = Get-Date
    }
    Start-Sleep -Seconds 20
}
