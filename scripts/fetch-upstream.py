#!/usr/bin/env python3
"""Fetch exact upstream code without running it or replacing existing checkouts."""
import argparse
import json
from pathlib import Path
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    lock = Path(__file__).resolve().parents[1] / "infrastructure/open-source/sources.lock.json"
    sources = json.loads(lock.read_text())["sources"]
    target = args.destination.resolve()
    target.mkdir(parents=True, exist_ok=True)
    for source in sources:
        path = target / source["name"]
        if path.exists():
            raise SystemExit(f"Refusing to overwrite {path}. Choose a fresh directory.")
        subprocess.run(["git", "init", "--quiet", str(path)], check=True)
        subprocess.run(["git", "-C", str(path), "remote", "add", "origin", source["repository"]], check=True)
        subprocess.run(["git", "-C", str(path), "fetch", "--depth", "1", "origin", source["commit"]], check=True)
        subprocess.run(["git", "-C", str(path), "checkout", "--quiet", "--detach", "FETCH_HEAD"], check=True)
        actual = subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()
        if actual != source["commit"]:
            raise SystemExit(f"Commit mismatch for {source['name']}")
        print(f"{source['name']}: {actual}")
    print("Sources downloaded. No installation, startup or database changes performed.")

if __name__ == "__main__":
    main()
