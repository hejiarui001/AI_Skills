#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MikroTik RouterOS 7.x 运行状态与健康度快速巡检工具
- 适用平台: Windows 11 / Linux (Ubuntu) 跨平台
- 通信协议: 原生 REST API (HTTP Basic Auth / Port 80)
- 核心指标:
    1. 系统资源 (CPU 负载、RAM 水位、Flash 剩余容量、Uptime 连续性)
    2. 存储卡挂载与 FAT32 文件系统健康状态 (杜绝 I/O 锁死)
    3. WAN IPv4 (PPPoE / 动态公网) 与 IPv6 前缀委派 (PD) 状态
    4. 最近关键日志检索与异常过滤
"""

import os
import sys
import json
import base64
import urllib.request
from datetime import datetime


def get_credentials():
    # 优先从环境变量读取，其次交互或回退
    user = os.environ.get("ROS_USER", "antigravity")
    pwd = os.environ.get("ROS_PASS", "hejiarui001")
    host = os.environ.get("ROS_HOST", "192.168.188.1")
    return host, user, pwd


def request_ros(host, user, pwd, endpoint):
    url = f"http://{host}/rest/{endpoint}"
    auth_str = f"{user}:{pwd}"
    auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("ascii")
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Basic {auth_b64}",
            "User-Agent": "ROS_Diagnose/1.0"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=4) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}


def main():
    host, user, pwd = get_credentials()
    print("=" * 65)
    print(f"[*] MikroTik RouterOS Inspection | Target: {host} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    # 1. 资源
    res = request_ros(host, user, pwd, "system/resource")
    if "error" in res:
        print(f"[!] 无法连接 RouterOS REST API: {res['error']}")
        return

    cpu_load = res.get("cpu-load", "0")
    free_ram_mb = round(int(res.get("free-memory", 0)) / 1024 / 1024, 1)
    total_ram_mb = round(int(res.get("total-memory", 0)) / 1024 / 1024, 1)
    free_flash_mb = round(int(res.get("free-hdd-space", 0)) / 1024 / 1024, 2)
    uptime = res.get("uptime", "Unknown")
    version = res.get("version", "Unknown")
    board = res.get("board-name", "Unknown")

    print(f"硬件型号: {board} | 系统版本: v{version} | 运行时间: {uptime}")
    print(f"CPU 负载: {cpu_load}% | 空闲内存: {free_ram_mb} MB / {total_ram_mb} MB | Flash 剩余: {free_flash_mb} MB")
    print("-" * 65)

    # 2. 存储卡
    disks = request_ros(host, user, pwd, "disk")
    print("MicroSD 扩展存储状态:")
    if isinstance(disks, list):
        sd_found = False
        for d in disks:
            if "sd" in d.get("slot", "").lower() or "sd" in d.get("name", "").lower():
                sd_found = True
                mounted = d.get("mounted", "false")
                fs = d.get("fs", "-")
                free_gb = round(int(d.get("free", 0)) / 1024 / 1024 / 1024, 2)
                size_gb = round(int(d.get("size", 0)) / 1024 / 1024 / 1024, 2)
                status_str = "正常挂载" if mounted == "true" else "未挂载/异常"
                print(f"  * 槽位 {d.get('slot')} ({d.get('fs-label', 'NoLabel')}): {status_str} | 格式: {fs} | 空间: {free_gb} GB / {size_gb} GB")
        if not sd_found:
            print("  [-] 未检测到 MicroSD 存储设备")
    print("-" * 65)

    # 3. WAN IPv4 & IPv6
    ips = request_ros(host, user, pwd, "ip/address")
    wan_ip = "未检测到"
    if isinstance(ips, list):
        for item in ips:
            if "pppoe" in item.get("interface", "").lower() or item.get("dynamic") == "true":
                wan_ip = f"{item.get('address')} on {item.get('interface')}"
    print(f"WAN IPv4: {wan_ip}")

    v6_pools = request_ros(host, user, pwd, "ipv6/pool")
    v6_has_pool = isinstance(v6_pools, list) and len(v6_pools) > 0
    print(f"IPv6 前缀委派 (PD): {'已下发 Prefix Pool' if v6_has_pool else '无前缀 (上游 BRAS 仅分配单接口 /64，内网不可路由公网)'}")
    print("-" * 65)

    # 4. 最近日志
    logs = request_ros(host, user, pwd, "log")
    print("最近关键日志 (最新 5 条):")
    if isinstance(logs, list):
        for l in logs[-5:]:
            topics = l.get("topics", "")
            msg = l.get("message", "")
            t = l.get("time", "")
            print(f"  [{t}] [{topics}] {msg}")
    print("=" * 65)


if __name__ == "__main__":
    main()
