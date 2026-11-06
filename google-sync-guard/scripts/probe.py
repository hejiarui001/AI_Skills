#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Sync Guard - Network & Proxy Connectivity Probe
Detects local Clash/proxy listening ports and tests live Google API connectivity.
Exit code: 0 = OK (Cloud Sync Ready), 1 = Offline / Proxy Down (Fallback to Cache).
"""

import sys
import os
import json
import time
import socket
import urllib.request
import urllib.error

DEFAULT_PROXY_PORTS = [7897, 7890, 10808, 10809]
TARGET_URL = "http://connectivitycheck.gstatic.com/generate_204"
GOOGLE_API_HOST = "www.googleapis.com"

def check_local_port(host, port, timeout_sec=0.3):
    try:
        with socket.create_connection((host, port), timeout=timeout_sec):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

def find_active_proxy():
    for p in DEFAULT_PROXY_PORTS:
        if check_local_port("127.0.0.1", p):
            return f"127.0.0.1:{p}"
    return None

def probe_google(proxy_str=None, timeout_sec=1.5):
    start = time.perf_counter()
    handlers = []
    if proxy_str:
        handlers.append(urllib.request.ProxyHandler({
            'http': f"http://{proxy_str}",
            'https': f"http://{proxy_str}"
        }))
    opener = urllib.request.build_opener(*handlers)
    req = urllib.request.Request(
        TARGET_URL,
        headers={"User-Agent": "AntigravitySyncGuard/1.0"}
    )
    try:
        with opener.open(req, timeout=timeout_sec) as resp:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            if resp.status in (200, 204):
                return True, elapsed_ms, f"HTTP {resp.status}"
            return False, elapsed_ms, f"HTTP {resp.status}"
    except Exception as e:
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return False, elapsed_ms, str(e)

def main():
    proxy = find_active_proxy()
    online, latency_ms, detail = probe_google(proxy)
    
    result = {
        "status": "online" if online else "offline",
        "proxy_detected": proxy,
        "latency_ms": latency_ms if online else None,
        "detail": detail,
        "action_required": "proceed_cloud" if online else "fallback_local_cache",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if online else 1)

if __name__ == "__main__":
    main()
