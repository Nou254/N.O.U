"""Restart the N.O.U backend (uvicorn :8000) reliably from Python.

Usage:
  restart_backend.py                single-process (default, no Redis needed)
  restart_backend.py --workers 4    multi-process (REQUIRES REDIS_URL in .env
                                    so rate limits + token revocation are shared)
"""
import os
import socket
import subprocess
import sys
import time
import urllib.request

PY = sys.executable
CWD = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(CWD, "uvicorn-ai.log")

WORKERS = 1
if "--workers" in sys.argv:
    try:
        WORKERS = int(sys.argv[sys.argv.index("--workers") + 1])
    except (IndexError, ValueError):
        print("invalid --workers value; using 1")
        WORKERS = 1
    WORKERS = max(1, min(WORKERS, 16))


def redis_configured():
    env_path = os.path.join(CWD, ".env")
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            return "REDIS_URL" in f.read()
    except OSError:
        return False


def health():
    try:
        r = urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=4)
        return f"{r.status} {r.read(120).decode('utf-8', 'replace')}"
    except Exception as e:  # noqa: BLE001
        return f"ERR {type(e).__name__}: {str(e)[:80]}"


def kill_port(port):
    out = subprocess.run(
        ["netstat", "-ano"], capture_output=True, text=True, timeout=10
    ).stdout
    pids = set()
    for line in out.splitlines():
        if f":{port}" in line and "LISTENING" in line:
            parts = line.split()
            if parts:
                pids.add(parts[-1])
    for pid in pids:
        subprocess.run(
            ["taskkill", "/F", "/PID", pid],
            capture_output=True, text=True, timeout=15,
        )
        print(f"killed PID {pid}")


def main():
    workers = WORKERS
    if workers > 1 and not redis_configured():
        print("WARNING: --workers %d requires REDIS_URL in backend/.env "
              "(in-memory rate limits/revocation are per-process). "
              "Falling back to 1 worker." % workers)
        workers = 1
    print(f"workers: {workers}")
    print("health-before:", health())
    kill_port(8000)
    time.sleep(2)
    cmd = [PY, "-m", "uvicorn", "app.main:app",
           "--host", "0.0.0.0", "--port", "8000", "--no-server-header"]
    if workers > 1:
        cmd += ["--workers", str(workers)]
    with open(LOG, "wb") as logf:
        proc = subprocess.Popen(
            cmd,
            cwd=CWD, stdout=logf, stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW,
            close_fds=True,
        )
    print("started pid:", proc.pid)
    for i in range(90):
        time.sleep(1)
        h = health()
        if "ERR" not in h:
            print(f"health-after ({i+1}s): {h}")
            return 0
    print("health-final:", health())
    with open(LOG, "r", encoding="utf-8", errors="replace") as f:
        print("--- log tail ---")
        print("".join(f.readlines()[-20:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
