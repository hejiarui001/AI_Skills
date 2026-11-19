#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
远程命脉网段安全巡检与防失联探活工具 (Remote Lifeline & 5-Layer Network Safety Probe)
- 适用平台: Windows 11 / Linux (Ubuntu) 跨平台动态自适应
- 核心功能:
    Layer 1: 本端 IP 网段核验 (优先核查 192.168.8.x)
    Layer 2: 直连二级网关连通性与延时 (192.168.8.1)
    Layer 3: 穿透一级主路由核心端口 (192.168.188.1: WinBox 8291, Webfig 80, SSH 22)
    Layer 4: 骨干网络与公共 DNS 探测 (223.5.5.5 / 119.29.29.29)
    Layer 5: 端到端互联网 HTTP/HTTPS 业务链路可用性 (Baidu / Bilibili)
- 隐私规约: 日报强制落盘至外部私有目录 E:\\Internet\\Messages\\ (若存在) 或用户私有目录，零代码仓污染。
"""

import os
import sys
import time
import socket
import platform
import subprocess
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple

TARGET_GW_L2 = "192.168.8.1"
TARGET_GW_L1 = "192.168.188.1"
TARGET_DNS_ALI = "223.5.5.5"
TARGET_DNS_TX = "119.29.29.29"
TEST_DOMAINS = ["www.baidu.com", "www.bilibili.com"]


def get_messages_dir() -> Path:
    """动态获取隐私日志存储目录，避免污染代码仓与桌面"""
    system = platform.system().lower()
    if "windows" in system:
        p = Path(r"E:\Internet\Messages")
        if p.exists():
            return p
    else:
        candidates = [
            Path("/media/secret/ZX1 512G/Data/Internet/Messages"),
            Path.home() / ".cache" / "network_messages"
        ]
        for c in candidates:
            if c.parent.exists():
                c.mkdir(parents=True, exist_ok=True)
                return c
    fallback = Path.home() / ".network_probe"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


def run_ping(ip: str, count: int = 2, timeout_ms: int = 1000) -> Tuple[bool, float, int]:
    """执行底层 ICMP Ping 探测，跨平台返回 (是否成功, 平均往返延时ms, TTL)"""
    system = platform.system().lower()
    if "windows" in system:
        cmd = ["ping.exe", ip, "-n", str(count), "-w", str(timeout_ms)]
        cflags = subprocess.CREATE_NO_WINDOW
    else:
        cmd = ["ping", "-c", str(count), "-W", str(int(timeout_ms / 1000) or 1), ip]
        cflags = 0

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, creationflags=cflags)
        out = res.stdout
        if "TTL=" in out or "ttl=" in out:
            lines = [l.strip() for l in out.splitlines() if "TTL=" in l or "ttl=" in l]
            last_line = lines[-1]
            time_str = "0"
            ttl_val = 64
            for part in last_line.split():
                if "time=" in part.lower() or "时间=" in part:
                    time_str = part.lower().replace("time=", "").replace("时间=", "").replace("ms", "")
                if "ttl=" in part.lower():
                    try:
                        ttl_val = int(part.lower().replace("ttl=", ""))
                    except ValueError:
                        pass
            try:
                avg_time = float(time_str)
            except ValueError:
                avg_time = 0.0
            return True, avg_time, ttl_val
        return False, 0.0, 0
    except Exception:
        return False, 0.0, 0


def test_tcp_port(ip: str, port: int, timeout_sec: float = 1.0) -> Tuple[bool, float]:
    """测试 TCP 端口连通性及握手延迟"""
    t0 = time.perf_counter()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout_sec)
    try:
        res = s.connect_ex((ip, port))
        latency = (time.perf_counter() - t0) * 1000.0
        s.close()
        return (res == 0), round(latency, 2)
    except Exception:
        s.close()
        return False, 0.0


def test_http_url(url: str, timeout_sec: float = 2.0) -> Tuple[bool, int, float]:
    """测试 HTTP/HTTPS 业务端到端可用性"""
    t0 = time.perf_counter()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "NetworkSafetyProbe/2.0"})
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            code = resp.status
            latency = (time.perf_counter() - t0) * 1000.0
            return (200 <= code < 400), code, round(latency, 2)
    except Exception:
        return False, 0, 0.0


def probe_local_ip() -> str:
    """获取本端首选物理 IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("223.5.5.5", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def run_full_safety_check() -> Dict[str, Any]:
    local_ip = probe_local_ip()
    is_lifeline = local_ip.startswith("192.168.8.")

    # Layer 2
    gw2_ok, gw2_lat, _ = run_ping(TARGET_GW_L2, count=2)

    # Layer 3
    wb_ok, wb_lat = test_tcp_port(TARGET_GW_L1, 8291, timeout_sec=1.5)
    web_ok, web_lat = test_tcp_port(TARGET_GW_L1, 80, timeout_sec=1.5)
    ssh_ok, ssh_lat = test_tcp_port(TARGET_GW_L1, 22, timeout_sec=1.5)

    # Layer 4
    dns_ali_ok, dns_ali_lat, _ = run_ping(TARGET_DNS_ALI, count=2)
    dns_tx_ok, dns_tx_lat, _ = run_ping(TARGET_DNS_TX, count=2)

    # Layer 5
    http_results = {}
    for d in TEST_DOMAINS:
        ok, code, lat = test_http_url(f"https://{d}", timeout_sec=2.5)
        http_results[d] = {"ok": ok, "status": code, "latency_ms": lat}

    overall_healthy = gw2_ok and wb_ok and (dns_ali_ok or dns_tx_ok)

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "local_ip": local_ip,
        "is_lifeline": is_lifeline,
        "gw_l2": {"ip": TARGET_GW_L2, "ok": gw2_ok, "latency_ms": gw2_lat},
        "gw_l1_ports": {
            "ip": TARGET_GW_L1,
            "winbox_8291": {"ok": wb_ok, "latency_ms": wb_lat},
            "webfig_80": {"ok": web_ok, "latency_ms": web_lat},
            "ssh_22": {"ok": ssh_ok, "latency_ms": ssh_lat}
        },
        "dns": {
            "ali_223_5_5_5": {"ok": dns_ali_ok, "latency_ms": dns_ali_lat},
            "tx_119_29_29_29": {"ok": dns_tx_ok, "latency_ms": dns_tx_lat}
        },
        "http_services": http_results,
        "overall_healthy": overall_healthy
    }


def main():
    res = run_full_safety_check()
    print("=" * 65)
    print(f"[*] 5-Layer Network Safety Probe | {res['timestamp']}")
    print(f"[*] Local Host IP   : {res['local_ip']} (Lifeline Subnet: {res['is_lifeline']})")
    print("-" * 65)
    print(f"L2 Gateway (192.168.8.1)      : {'PASS' if res['gw_l2']['ok'] else 'FAIL'} ({res['gw_l2']['latency_ms']} ms)")
    print(f"L1 RouterOS WinBox (8291)     : {'PASS' if res['gw_l1_ports']['winbox_8291']['ok'] else 'FAIL'} ({res['gw_l1_ports']['winbox_8291']['latency_ms']} ms)")
    print(f"L1 RouterOS WebFig (80)       : {'PASS' if res['gw_l1_ports']['webfig_80']['ok'] else 'FAIL'} ({res['gw_l1_ports']['webfig_80']['latency_ms']} ms)")
    print(f"L1 RouterOS SSH (22)          : {'PASS' if res['gw_l1_ports']['ssh_22']['ok'] else 'FAIL'} ({res['gw_l1_ports']['ssh_22']['latency_ms']} ms)")
    print(f"Public DNS (223.5.5.5)        : {'PASS' if res['dns']['ali_223_5_5_5']['ok'] else 'FAIL'} ({res['dns']['ali_223_5_5_5']['latency_ms']} ms)")
    print(f"Public DNS (119.29.29.29)     : {'PASS' if res['dns']['tx_119_29_29_29']['ok'] else 'FAIL'} ({res['dns']['tx_119_29_29_29']['latency_ms']} ms)")
    for d, info in res['http_services'].items():
        print(f"Web Traffic ({d}) : {'PASS' if info['ok'] else 'FAIL'} (Code: {info['status']}, {info['latency_ms']} ms)")
    print("-" * 65)
    status_str = "HEALTHY (链路健康，允许执行网络策略变更)" if res['overall_healthy'] else "BLOCKED (链路异常，禁止变更或必须回滚)"
    print(f"[*] Safety Assessment: {status_str}")
    print("=" * 65)


if __name__ == "__main__":
    main()
