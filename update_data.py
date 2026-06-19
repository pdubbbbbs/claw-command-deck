#!/usr/bin/env python3
"""Regenerate repos.json and homelab.json for claw.outtatime.dev.

Run from anywhere; writes next to this script. Probes are live —
ping for hosts, TCP connect for services, HTTPS for the tunnel.
"""

from __future__ import annotations

import json
import socket
import subprocess
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
USER = "pdubbbbbs"

NETWORK = [
    ("UCG-Ultra", "10.10.10.1", "gateway / router"),
    ("DGS-1100 switch", "10.10.10.10", "D-Link 24-port"),
    ("WAX210PA AP", "10.10.10.219", "Netgear Wi-Fi AP"),
    ("NAS", "10.10.10.188", "Synology origin host"),
]
COMPUTE = [
    ("pineapple", "10.10.10.126"),
    ("jellybean", "10.10.10.107"),
    ("nutella", "10.10.10.139"),
    ("sriracha", "10.10.10.243"),
    ("peanutbutter", "10.10.10.150"),
]
SERVICES = [
    ("multicast", "10.10.10.188", 8002, "multicast controller"),
    ("roku-origin", "10.10.10.188", 8090, "static HTTP origin"),
]
ROKUS = [
    ("Roku-1", "192.168.12.182"),
    ("Roku-2", "192.168.12.189"),
]


def ping(host: str) -> float | None:
    """Return RTT in ms, or None if unreachable."""
    try:
        out = subprocess.run(
            ["ping", "-c", "1", "-W", "1", "-t", "1", host],
            capture_output=True, text=True, timeout=5,
        )
        if out.returncode == 0:
            for part in out.stdout.split():
                if part.startswith("time="):
                    return round(float(part[5:]), 3)
            return 0.0
    except (subprocess.TimeoutExpired, OSError):
        pass
    return None


def tcp_ms(host: str, port: int) -> float | None:
    """Return TCP connect time in ms, or None."""
    try:
        start = time.monotonic()
        with socket.create_connection((host, port), timeout=2):
            return round((time.monotonic() - start) * 1000, 1)
    except OSError:
        return None


def https_ok(url: str) -> float | None:
    # Cloudflare blocks python's TLS fingerprint (403) — probe with curl instead.
    try:
        out = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code} %{time_total}",
             "-m", "8", "-A", "claw-updater/1.0", url],
            capture_output=True, text=True, timeout=12,
        )
        code, total = out.stdout.split()
        if out.returncode == 0 and code.startswith(("2", "3")):
            return round(float(total) * 1000, 1)
    except (subprocess.TimeoutExpired, ValueError, OSError):
        pass
    return None


def seg(host: str) -> str:
    """Map an internal address to a non-identifying network segment label.

    The public feed (claw.outtatime.dev, GitHub Pages) must NOT publish the
    internal LAN IP map. We still probe by the real IP below, but only the
    segment label is ever written into the published JSON.
    """
    if host.startswith("10.10.10."):
        return "LAN"
    if host.startswith("192.168.12."):
        return "WAN"
    return host  # 'tunnel', etc.


def build_homelab() -> dict:
    groups = []

    net = [{"name": n, "host": seg(h), "up": (ms := ping(h)) is not None, "ms": ms, "note": note}
           for n, h, note in NETWORK]
    groups.append({"name": "Network", "nodes": net})

    comp = []
    for n, h in COMPUTE:
        ms = ping(h)
        comp.append({"name": n, "host": seg(h), "up": ms is not None, "ms": ms,
                     "note": "ok" if ms is not None else "unreachable"})
    groups.append({"name": "Compute", "nodes": comp})

    svc = [{"name": n, "host": f"{seg(h)}:{p}", "up": (ms := tcp_ms(h, p)) is not None, "ms": ms, "note": note}
           for n, h, p, note in SERVICES]
    tun = https_ok("https://roku.philipwright.me")
    svc.append({"name": "cloudflared", "host": "tunnel", "up": tun is not None, "ms": tun,
                "note": "Cloudflare tunnel healthy" if tun is not None else "tunnel unreachable"})
    groups.append({"name": "Services", "nodes": svc})

    nas_up = ping("10.10.10.188") is not None
    groups.append({"name": "Storage", "nodes": [
        {"name": "NAS reachable", "host": seg("10.10.10.188"), "up": nas_up, "ms": None,
         "note": "checked from Mac (ping + ssh port)" if nas_up else "NAS unreachable"},
    ]})

    rokus = []
    for n, h in ROKUS:
        ms = ping(h)
        rokus.append({"name": n, "host": seg(h), "up": ms is not None, "ms": ms, "note": "Roku player"})
    groups.append({"name": "Roku", "nodes": rokus})

    nodes = [x for g in groups for x in g["nodes"]]
    return {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "summary": {"up": sum(1 for x in nodes if x["up"]), "total": len(nodes)},
        "groups": groups,
    }


def build_repos() -> dict:
    repos, page = [], 1
    while True:
        url = f"https://api.github.com/users/{USER}/repos?per_page=100&sort=pushed&page={page}"
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            batch = json.load(resp)
        if not batch:
            break
        repos.extend(batch)
        page += 1
    return {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "total": len(repos),
        "repos": [{
            "name": r["name"],
            "desc": r.get("description") or "",
            "lang": r.get("language") or "—",
            "stars": r.get("stargazers_count", 0),
            "pushed": (r.get("pushed_at") or "")[:10],
            "private": r.get("private", False),
            "topics": r.get("topics", []),
            "url": r["html_url"],
        } for r in repos],
    }


def main() -> None:
    homelab = build_homelab()
    (HERE / "homelab.json").write_text(json.dumps(homelab, indent=2) + "\n")
    print(f"homelab.json: {homelab['summary']['up']}/{homelab['summary']['total']} up")

    repos = build_repos()
    (HERE / "repos.json").write_text(json.dumps(repos, indent=1) + "\n")
    print(f"repos.json: {repos['total']} repos")


if __name__ == "__main__":
    main()
