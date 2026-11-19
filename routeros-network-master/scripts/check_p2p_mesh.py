#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tailscale P2P 网状拓扑与 STUN 端点连通性探测工具
- 适用平台: Windows 11 / Linux (Ubuntu) 跨平台
- 核心功能:
    1. 自动执行 tailscale status --json 并解析本地及对端节点拓扑；
    2. 深度诊断对端是否处于 relay 中继，识别 DERP 区域代码；
    3. 检查 Endpoints 是否丢失 (Endpoints: None / null)，精准诊断 STUN UDP 3478 被劫持/阻断；
    4. 跨平台后台静默运行 (Windows 强制使用 CREATE_NO_WINDOW 避免黑框闪烁)。
"""

import sys
import json
import platform
import subprocess
from datetime import datetime


def get_cflags():
    if platform.system().lower() == "windows":
        return subprocess.CREATE_NO_WINDOW
    return 0


def run_tailscale_cmd(args):
    cflags = get_cflags()
    try:
        proc = subprocess.run(
            ["tailscale"] + args,
            capture_output=True,
            text=True,
            creationflags=cflags,
            timeout=10
        )
        return proc.returncode == 0, proc.stdout.strip(), proc.stderr.strip()
    except Exception as e:
        return False, "", str(e)


def diagnose_mesh():
    ok, out, err = run_tailscale_cmd(["status", "--json"])
    if not ok:
        print(f"[!] 获取 Tailscale 状态失败: {err or '未安装或服务未运行'}")
        return

    try:
        data = json.loads(out)
    except Exception as e:
        print(f"[!] JSON 解析失败: {e}")
        return

    self_info = data.get("Self", {})
    peers = data.get("Peer", {})

    print("=" * 65)
    print(f"[*] Tailscale Mesh Network Diagnosis | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] Local Host  : {self_info.get('HostName')} ({self_info.get('TailscaleIPs')})")
    print(f"[*] Online State: {self_info.get('Online')} | DERP Region: {self_info.get('Relay')}")
    print("-" * 65)

    if not peers:
        print("[-] 未发现对端节点 (No peers found)")
        return

    for peer_id, p in peers.items():
        hostname = p.get("HostName", "Unknown")
        ips = p.get("TailscaleIPs", [])
        online = p.get("Online", False)
        active = p.get("Active", False)
        relay = p.get("Relay", "")
        cur_addr = p.get("CurAddr", "")
        endpoints = p.get("TailscaleEndpoints") or p.get("Endpoints")
        last_hs = p.get("LastHandshake", "")

        is_direct = bool(cur_addr) and (not relay or cur_addr != relay)
        link_type = "DIRECT (直连)" if is_direct else f"RELAY (经由中继 {relay})"

        print(f"Node: {hostname} ({', '.join(ips)})")
        print(f"  * 状态: {'在线' if online else '离线'} | 链路模式: {link_type}")
        print(f"  * 活动端点 (CurAddr): {cur_addr or '无 (通过 DERP 中转)'}")
        print(f"  * 公网/本地端点 (Endpoints): {endpoints if endpoints else 'None (STUN 探测丢失或被代理拦截)'}")
        print(f"  * 最近握手时间: {last_hs}")

        # 智能诊断预警
        if not is_direct and online:
            print("  [!] 诊断建议:")
            if not endpoints:
                print("      - 对端 Endpoints 为空: 说明对端网络 UDP 3478 被拦截，或开启了 TUN 代理且未加白。")
                print("      - 请在移动端代理 App 中通过「应用访问控制 / 绕过模式」排除 Tailscale。")
            if relay in ["sfo", "lax", "nue", "fra"]:
                print(f"      - 中继落在欧美节点 ({relay}): 对端流量疑似被海外代理接管，请将 DERP 与 STUN 设为直连。")
        print("-" * 65)


if __name__ == "__main__":
    diagnose_mesh()
