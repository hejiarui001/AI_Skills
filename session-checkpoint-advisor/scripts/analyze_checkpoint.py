#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session Checkpoint & Transcript Introspector (跨平台会话断点内省与态势分析器)
版本: v1.2.0

职能：
1. 本地零 Token 剖析 Antigravity transcript.jsonl：提取精确时间轴指纹、预估负载、自动预警连续空转/重复死锁区间；
2. 扫描工作区 Git 状态与单一权威文档 (SSOT)；
3. 网络与代理悬空态门禁：探测 Clash 端口 (7897) 与开发/独占进程；
4. 合成带“确定性免探核准印章 (Pre-Verified Stamp)”与“脱敏私密指针”的极简破局重生 Prompt。
"""

import os
import sys
import json
import socket
import hashlib
import platform
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

DEV_PROCESSES = {
    "pyocd", "openocd", "stlink", "jlink", "vofa+", "lceda-pro",
    "keil", "uvision", "ninja", "cmake", "gcc", "arm-none-eabi-gcc",
    "sunshine", "easytier", "tailscale", "clash", "syncthing"
}

def get_current_os():
    sys_name = platform.system().lower()
    if sys_name == "windows":
        return "Windows 11"
    elif sys_name == "linux":
        try:
            with open("/etc/os-release", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="):
                        return line.split("=", 1)[1].strip().strip('"')
        except Exception:
            return "Linux (Generic)"
    return platform.system()

def find_git_root(start_dir):
    p = Path(start_dir).resolve()
    for parent in [p] + list(p.parents):
        if (parent / ".git").is_dir():
            return parent
    return p

def run_cmd(cmd_list, cwd):
    try:
        res = subprocess.run(
            cmd_list,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=8
        )
        return res.returncode == 0, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def inspect_git_state(git_root):
    is_git, branch, _ = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"], git_root)
    if not is_git:
        return {
            "is_git": False,
            "root": str(git_root),
            "branch": "None",
            "head_sha": "None",
            "modified": [],
            "untracked": [],
            "staged": [],
            "ssot_docs": []
        }

    _, head_sha, _ = run_cmd(["git", "rev-parse", "--short", "HEAD"], git_root)
    _, status_out, _ = run_cmd(["git", "status", "--porcelain"], git_root)
    modified, untracked, staged = [], [], []

    for line in status_out.splitlines():
        if not line or len(line) < 3:
            continue
        x, y = line[0], line[1]
        file_path = line[3:].strip()
        if x in ['M', 'A', 'D', 'R', 'C']:
            staged.append(file_path)
        if y == 'M':
            modified.append(file_path)
        elif x == '?' and y == '?':
            untracked.append(file_path)

    # 发现根 docs/ 下的权威规格文件
    ssot_docs = []
    docs_dir = Path(git_root) / "docs"
    if docs_dir.is_dir():
        ssot_docs = [f"docs/{f.name}" for f in sorted(docs_dir.glob("*.md"))[:6]]

    return {
        "is_git": True,
        "root": str(git_root),
        "branch": branch,
        "head_sha": head_sha or "HEAD",
        "modified": modified,
        "untracked": untracked,
        "staged": staged,
        "ssot_docs": ssot_docs
    }

def check_network_guard():
    """探测常见本地代理端口 (7897 Clash Verge) 避免自断网悬空状态回退"""
    proxy_port = 7897
    proxy_alive = False
    try:
        with socket.create_connection(("127.0.0.1", proxy_port), timeout=0.8):
            proxy_alive = True
    except Exception:
        proxy_alive = False
    return {
        "clash_7897_listening": proxy_alive
    }

def detect_dev_processes():
    active_dev_procs = []
    sys_name = platform.system().lower()
    try:
        if sys_name == "windows":
            ok, out, _ = run_cmd(["powershell", "-NoProfile", "-Command", "Get-Process | Select-Object -ExpandProperty ProcessName"], None)
        else:
            ok, out, _ = run_cmd(["ps", "-A", "-o", "comm="], None)
        if ok:
            procs = set(line.strip().lower() for line in out.splitlines() if line.strip())
            for dp in DEV_PROCESSES:
                if dp in procs or any(dp in p for p in procs):
                    active_dev_procs.append(dp)
    except Exception:
        pass
    return sorted(list(set(active_dev_procs)))

def introspect_transcript(session_id=None):
    """本地零 Token 剖析最近或指定会话的 transcript.jsonl"""
    brain_dir = Path.home() / ".gemini" / "antigravity" / "brain"
    if not brain_dir.is_dir():
        return None

    target_log = None
    if session_id:
        matches = list(brain_dir.glob(f"{session_id}*"))
        if matches:
            cand = matches[0] / ".system_generated" / "logs" / "transcript.jsonl"
            if cand.exists():
                target_log = cand
    else:
        # 自动定位最近活跃且包含 USER_INPUT 的会话日志
        candidates = []
        for item in brain_dir.iterdir():
            if item.is_dir():
                lf = item / ".system_generated" / "logs" / "transcript.jsonl"
                if lf.exists():
                    candidates.append((lf.stat().st_mtime, lf))
        candidates.sort(key=lambda x: x[0], reverse=True)
        if candidates:
            target_log = candidates[0][1]

    if not target_log:
        return None

    turns = []
    total_steps = 0
    total_chars = 0

    try:
        with open(target_log, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                total_steps += 1
                total_chars += len(line)
                try:
                    d = json.loads(line)
                    if d.get("type") == "USER_INPUT":
                        c = d.get("content", "").replace("<USER_REQUEST>", "").replace("</USER_REQUEST>", "").strip()
                        if "<ADDITIONAL_METADATA>" in c:
                            c = c.split("<ADDITIONAL_METADATA>")[0].strip()
                        ts_raw = d.get("created_at", "")
                        hhmm = ts_raw[11:16] if len(ts_raw) >= 16 else "--:--"
                        turns.append({
                            "turn": len(turns) + 1,
                            "time": hhmm,
                            "snippet": c.replace("\n", " ")[:45]
                        })
                except Exception:
                    pass
    except Exception:
        return None

    # 空转死锁 / 连续重复检测
    spinning_loops = []
    streak = 1
    for i in range(1, len(turns)):
        if turns[i]["snippet"] and turns[i]["snippet"] == turns[i-1]["snippet"]:
            streak += 1
        else:
            if streak >= 2:
                spinning_loops.append(f"T{i - streak + 1:02d}~T{i:02d} (连续重复 {streak} 次: '{turns[i-1]['snippet'][:20]}...')")
            streak = 1
    if streak >= 2 and turns:
        spinning_loops.append(f"T{len(turns) - streak + 1:02d}~T{len(turns):02d} (连续重复 {streak} 次: '{turns[-1]['snippet'][:20]}...')")

    est_tokens = int(total_chars / 3.2)
    return {
        "session_id": target_log.parent.parent.parent.name[:8],
        "total_steps": total_steps,
        "total_turns": len(turns),
        "est_tokens": est_tokens,
        "turns": turns,
        "spinning_loops": spinning_loops
    }

def generate_resumption_prompt(git_info, target_goal=None, dead_ends=None, ssot_doc=None, secret_ptr=None):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    is_dirty = bool(git_info["modified"] or git_info["untracked"] or git_info["staged"])
    state_sig = hashlib.md5(f"{git_info['head_sha']}:{len(git_info['modified'])}:{now_str[:13]}".encode()).hexdigest()[:8]

    lines = [
        "【会话断点续接指令 · 零延迟接力与免探核准】",
        "",
        f"1. 确定性免探核准印章 (Pre-Verified Stamp | Sig: `{state_sig}` | {now_str})：",
        f"   - 物理工作区 `{git_info['root']}` (分支 `{git_info['branch']} @ {git_info['head_sha']}`) 已由断点分析器完成静态校验。",
        f"   - 状态声明：{'存在受控未提交改动（见下方列表）' if is_dirty else '工作区纯净 (Clean Working Tree)'}。**新 AI 无需重复运行 git status 盘查，请直接从第 5 项推进执行！**"
    ]

    if is_dirty:
        all_changes = git_info["staged"] + git_info["modified"] + git_info["untracked"]
        lines.append(f"   - 磁盘保留改动资产：{', '.join(all_changes[:8])}")

    lines.extend([
        "",
        "2. 单一权威技术文档指针 (SSOT Anchor)：",
        f"   - 权威规范：`{ssot_doc}`" if ssot_doc else (
            f"   - 权威目录参考：{', '.join(git_info['ssot_docs'][:3])}" if git_info["ssot_docs"] else "   - 严格以根目录 `README.md` / `TASK.md` 为唯一权威基线，忽略过时碎片文档。"
        ),
        "",
        "3. 脱敏外部私密凭据指针 (Zero Credential Leakage)：",
        f"   - 敏感配置/节点/密钥绝对不入对话，请本地按需安全读取：`{secret_ptr}`" if secret_ptr else "   - 若涉及私有密码/节点/密钥，严禁在文本中回显，统一检索本地 `E:\\Internet\\Messages\\` 外部脱敏目录。",
        "",
        "4. 已验证死路与负面清单 (Negative Constraints)：",
        f"   - 严禁尝试：{dead_ends}" if dead_ends else "   - 严禁尝试已验证失败的重试路径（遵循“二轮不过即熔断”原则，先取证再变更）。",
        "",
        "5. 本轮唯一行动目标 (Single Focus Action)：",
        f"   - 🎯 核心目标：{target_goal}" if target_goal else "   - 🎯 核心目标：基于上述已锁定的物理基线与权威文档，直接执行下一阶段核心交付。"
    ])
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Session Checkpoint & Transcript Introspector v1.2.0")
    parser.add_argument("--cwd", default=os.getcwd(), help="Target workspace path")
    parser.add_argument("--session-id", default=None, help="Target session ID prefix to introspect")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--prompt", action="store_true", help="Generate ready-to-use resumption prompt")
    parser.add_argument("--target", default=None, help="Target goal")
    parser.add_argument("--dead-ends", default=None, help="Dead ends to avoid")
    parser.add_argument("--ssot", default=None, help="Single Source of Truth doc path")
    parser.add_argument("--secret-ptr", default=None, help="Private external config path pointer")

    args = parser.parse_args()

    git_root = find_git_root(args.cwd)
    git_info = inspect_git_state(git_root)
    dev_procs = detect_dev_processes()
    net_guard = check_network_guard()
    transcript_info = introspect_transcript(args.session_id)
    current_os = get_current_os()

    data = {
        "version": "1.2.0",
        "os": current_os,
        "git": git_info,
        "network_guard": net_guard,
        "active_dev_processes": dev_procs,
        "transcript": transcript_info
    }

    if args.prompt:
        print(generate_resumption_prompt(git_info, args.target, args.dead_ends, args.ssot, args.secret_ptr))
        return

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    print("# 🛰️ 会话断点内省与工作区态势诊断看板 (v1.2.0)")
    print()
    print("> 🛡️ **物理资产安全定心丸**：IDE 会话回退**仅影响模型上下文记忆与对话树**，本地磁盘代码、远端 Docker 容器及单片机 Flash 固件 **100% 稳定常驻，绝不丢失**！")
    print()
    print(f"> **宿主**：{current_os} | **代码仓**：`{git_info['root']}` (`{git_info['branch']} @ {git_info['head_sha']}`) | **本地代理(7897)**：{'🟢 活跃' if net_guard['clash_7897_listening'] else '🔴 未监听(注意防失联!)'}")
    print()

    if transcript_info:
        print(f"## 1. 本地会话内省剖析 (`{transcript_info['session_id']}` · 0 Token 本地读取)")
        print(f"* **会话负载**：共 `{transcript_info['total_turns']}` 轮有效提问 / `{transcript_info['total_steps']}` 步 | 预估累计上下文：约 **{transcript_info['est_tokens']:,} Tokens**")
        if transcript_info["est_tokens"] > 100000 or transcript_info["total_turns"] >= 35:
            print("* 🔴 **高负载告警**：上下文已进入注意力稀释区，强烈推荐 **方案 C（里程碑结项开新会话）**！")
        if transcript_info["spinning_loops"]:
            print("* ⚠️ **检测到空转死锁区间（建议作为拐点微回退参考坐标）**：")
            for sp in transcript_info["spinning_loops"]:
                print(f"  - `{sp}`")
        
        print("\n### 📍 精确时间轴视觉锚点表 (Anchor Timeline)")
        turns = transcript_info["turns"]
        # 展示关键采样的锚点（头2轮、中段、最后5轮）
        show_idx = sorted(list(set(list(range(min(2, len(turns)))) + list(range(max(0, len(turns)-6), len(turns))))))
        for idx in show_idx:
            t = turns[idx]
            print(f"* **`T{t['turn']:02d}`** [`{t['time']}`] : `{t['snippet']}...`")
        print()

    print("## 2. 物理工作区与防锁死门禁 (Safety Gates)")
    is_dirty = bool(git_info["modified"] or git_info["untracked"] or git_info["staged"])
    if is_dirty:
        print(f"⚠️ **存在未提交改动** (修改:{len(git_info['modified'])}, 新增:{len(git_info['untracked'])}) — 建议先执行 `git stash save \"pre-rewind\"`！")
    else:
        print("✅ **工作区纯净**：无未提交代码改动。")
    if dev_procs:
        print(f"⚠️ **活跃开发/同步进程**：`{', '.join(dev_procs)}`（注意：会话内拉起的后台 task 回退后会被 IDE 强杀）。")

    print("\n## 3. 破局重生 Prompt 预览 (含免探核准印章与脱敏指针)")
    print("```markdown")
    print(generate_resumption_prompt(git_info, args.target, args.dead_ends, args.ssot, args.secret_ptr))
    print("```")

if __name__ == "__main__":
    main()
