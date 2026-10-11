"""Bounded Docker readiness recovery; no WSL resets, installs or data removal."""
import os
import shutil
import subprocess
import time
from pathlib import Path


class DockerNotReady(RuntimeError):
    pass


def _text(value):
    if isinstance(value, str):
        return value
    value = value or b""
    if value.count(b"\x00") > len(value) // 4:
        return value.decode("utf-16-le", errors="replace").lstrip("\ufeff")
    return value.decode("utf-8", errors="replace")


def _run(command, env, timeout=15):
    try:
        return subprocess.run(command, env=env, capture_output=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return subprocess.CompletedProcess(command, 1, b"", str(exc).encode())


def _probe(env, timeout=15):
    result = _run(["docker", "info", "--format", "{{.ServerVersion}}"], env, timeout)
    ready = result.returncode == 0 and bool(_text(result.stdout).strip())
    return ready, _text(result.stderr).strip() or "Docker server did not report a version."


def _desktop_exe(env):
    for key, suffix in (("ProgramFiles", "Docker/Docker/Docker Desktop.exe"),
                        ("LOCALAPPDATA", "Programs/DockerDesktop/Docker Desktop.exe")):
        base = env.get(key)
        if base:
            candidate = Path(base) / suffix
            if candidate.is_file():
                return candidate
    return None


def _diagnostics(folder, env, last_error):
    lines = ["Doctor Agape local Docker diagnostics", last_error]
    for command in (["docker", "context", "show"], ["docker", "version"],
                    ["docker", "desktop", "status"], ["wsl", "--status"],
                    ["wsl", "--list", "--verbose"]):
        result = _run(command, env, timeout=10)
        lines.extend(["\n> " + " ".join(command),
                      _text(result.stdout)[-10000:], _text(result.stderr)[-3000:]])
    path = Path(folder) / "docker-diagnostics.txt"
    try:
        path.write_text("\n".join(lines), encoding="utf-8")
        return str(path)
    except OSError:
        return "Could not write diagnostics; run docker version and wsl --status manually."


def ensure_docker(folder, platform=None, timeout=180):
    """Return child-process environment only once the Docker server responds."""
    env = os.environ.copy()
    if not shutil.which("docker"):
        raise DockerNotReady("Docker not found. Install Docker Desktop with WSL2 on Windows.")
    if env.pop("DOCKER_API_VERSION", None) is not None:
        print("Ignoring DOCKER_API_VERSION for this run so Docker can negotiate its API.")
    deadline = time.monotonic() + timeout
    ready, error = _probe(env, min(15, timeout))
    if ready:
        return env
    if (platform or os.name) != "nt":
        raise DockerNotReady("Docker server is unavailable: " + error[-1200:])

    print("Docker Linux engine is unavailable. Attempting Docker Desktop restart (data preserved)...", flush=True)
    remaining = deadline - time.monotonic()
    if remaining > 0:
        result = _run(["docker", "desktop", "restart"], env, min(60, remaining))
        if result.returncode != 0:
            exe = _desktop_exe(env)
            if exe:
                try:
                    subprocess.Popen([str(exe)], env=env, stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL)
                except OSError as exc:
                    error = str(exc)
    print("Waiting for the Docker server (up to 3 minutes)...", flush=True)
    while time.monotonic() < deadline:
        remaining = deadline - time.monotonic()
        ready, error = _probe(env, max(0.1, min(10, remaining)))
        if ready:
            print("Docker server is ready.")
            return env
        remaining = deadline - time.monotonic()
        if remaining > 0:
            time.sleep(min(5, remaining))
    report = _diagnostics(folder, env, error)
    raise DockerNotReady("Docker Desktop Linux engine remains unavailable.\n" + error[-1200:]
                         + "\nLocal diagnostics: " + report
                         + "\nNo project containers were started. WSL and volumes were not reset.")
