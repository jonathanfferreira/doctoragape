#!/usr/bin/env python3
"""Start and verify the local development backend; never install host software."""
import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

root = Path(__file__).resolve().parent

def compose(*args):
    subprocess.run(["docker", "compose", *args], cwd=root, check=True)

def wait_http(url="http://localhost:8000/api/method/ping", timeout=180):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        try:
            with urlopen(url, timeout=5) as response:
                if response.status == 200:
                    return
        except (URLError, TimeoutError, OSError):
            time.sleep(3)
    raise RuntimeError(f"Service at {url} did not become ready. Inspect docker compose logs.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-build", action="store_true")
    parser.add_argument("--restart-check", action="store_true")
    args = parser.parse_args()
    if not shutil.which("docker"):
        raise SystemExit("Docker not found. On Windows install/start Docker Desktop with WSL2 first.")
    subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL, check=True)
    subprocess.run(["docker", "compose", "version"], check=True)
    existing = [(root / file).exists() for file in (".env", ".chatwoot.env")]
    if any(existing) and not all(existing):
        raise SystemExit("Partial local configuration found. Resolve it without replacing existing passwords.")
    if not any(existing):
        subprocess.run([sys.executable, str(root / "configure.py")], check=True)
    compose("config", "--quiet")
    if not args.skip_build:
        compose("build")
    compose("up", "-d")
    wait_http()
    wait_http("http://localhost:3000/")
    compose("cp", str(root / "backend_smoke.py"),
            "frappe-web:/home/frappe/frappe-bench/apps/healthcare/healthcare/agape_smoke.py")
    compose("exec", "-T", "frappe-web", "bench", "--site", "agape.localhost",
            "execute", "healthcare.agape_smoke.run")
    if args.restart_check:
        compose("restart", "mariadb", "frappe-web")
        wait_http()
        compose("exec", "-T", "frappe-web", "bench", "--site", "agape.localhost",
                "execute", "healthcare.agape_smoke.run", "--kwargs", '{"verify_only":true}')
    print("Local fictional backend probe passed. No payment or message was sent.")
    print("Frappe: http://agape.localhost:8000 | Chatwoot: http://localhost:3000")
    print("Frontend is not connected yet; local credentials are in .env.")

if __name__ == "__main__":
    main()
