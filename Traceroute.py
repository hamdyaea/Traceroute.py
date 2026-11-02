#!/usr/bin/env python3
# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-only
"""Portable Linux traceroute frontend without raw socket privileges."""
from __future__ import annotations
import argparse
import ipaddress
import re
import shutil
import subprocess

def validate_host(host: str) -> str:
    if not host or len(host) > 253 or any(ch.isspace() for ch in host) or host.startswith("-"):
        raise ValueError("Invalid destination")
    try:
        ipaddress.ip_address(host)
        return host
    except ValueError:
        pass
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?", host):
        raise ValueError("Invalid DNS hostname")
    return host

def trace(host: str, max_hops: int = 30, timeout: int = 2,
          finder=shutil.which, runner=subprocess.run) -> subprocess.CompletedProcess:
    validate_host(host)
    if not 1 <= max_hops <= 64 or not 1 <= timeout <= 10:
        raise ValueError("Hops must be 1–64 and timeout 1–10 seconds")
    if finder("traceroute"):
        command = ["traceroute", "-m", str(max_hops), "-w", str(timeout), host]
    elif finder("tracepath"):
        command = ["tracepath", "-m", str(max_hops), host]
    else:
        raise RuntimeError("Install traceroute or tracepath")
    return runner(command, capture_output=True, text=True, timeout=min(300, max_hops * (timeout + 1) * 3), check=False)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host", nargs="?", help="IP address or DNS name")
    parser.add_argument("--max-hops", type=int, default=30)
    parser.add_argument("--timeout", type=int, default=2)
    args = parser.parse_args()
    host = args.host or input("Destination: ").strip()
    try:
        result = trace(host, args.max_hops, args.timeout)
    except (ValueError, RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        parser.error(str(exc))
    print(result.stdout or result.stderr, end="")
    raise SystemExit(result.returncode)

if __name__ == "__main__":
    main()
