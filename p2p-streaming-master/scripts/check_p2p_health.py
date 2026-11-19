#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2P Streaming & Mesh Network Health Probe
Cross-Platform (Windows & Linux)
"""

import sys
import subprocess
import platform
import shutil

TARGET_IP = "10.144.144.2"  # Android Tablet EasyTier IP
HOST_IP = "10.144.144.1"    # Host PC EasyTier IP

def check_ping(ip, count=3):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    timeout_param = "-w" if platform.system().lower() == "windows" else "-W"
    cmd = ["ping", param, str(count), timeout_param, "1000", ip]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        return res.returncode == 0, res.stdout
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 60)
    print("🚀 P2P Streaming & EasyTier Mesh Network Health Probe")
    print(f"OS: {platform.system()} ({platform.machine()})")
    print("=" * 60)
    
    # 1. Check Ping to Tablet
    print(f"[*] Probing Tablet Virtual IP: {TARGET_IP} ...")
    ok, out = check_ping(TARGET_IP, count=3)
    if ok:
        print(f"    [+] Tablet Reachable! P2P Mesh Tunnel is ACTIVE.")
    else:
        print(f"    [-] Tablet Unreachable or Offline (Virtual IP: {TARGET_IP}).")
    
    # 2. Check Sunshine Process
    if platform.system().lower() == "windows":
        try:
            p_out = subprocess.check_output('tasklist /FI "IMAGENAME eq sunshine.exe" /NH', shell=True, text=True)
            if "sunshine.exe" in p_out.lower():
                print("    [+] Sunshine Host Service: RUNNING")
            else:
                print("    [-] Sunshine Host Service: NOT RUNNING")
        except Exception:
            pass
            
    print("=" * 60)
    print("[*] For comprehensive 230-burst stress test, run:")
    print("    python E:\\AI_Workspace\\05_Network_Development\\03_EasyTier_Mesh\\p2p_stress_test.py")

if __name__ == "__main__":
    main()
