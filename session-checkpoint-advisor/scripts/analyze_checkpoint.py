#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session Checkpoint & Workspace State Analyzer (跨平台会话断点与工作区状态分析器)

职能：
1. 自动定位当前代码仓/工作区根目录，提取 Git 改动资产（修改、新增、暂存）；
2. 探测当前系统环境（Windows / Linux）与活跃开发调试进程；
3. 输出高密度结构化态势看板与三梯队回退位点建议；
4. 自动合成即插即用型“破局重生 Prompt (Resumption Prompt)”。
"""

import os
import sys
import json
import platform
import argparse
import subprocess
from pathlib import Path

# 支持检测的嵌入式与常用研发调试进程清单
DEV_PROCESSES = {
    "pyocd", "openocd", "stlink", "jlink", "vofa+", "lceda-pro",
    "keil", "uvision", "ninja", "cmake", "gcc", "arm-none-eabi-gcc",
    "sunshine", "easytier", "tailscale", "clash"
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
            "modified": [],
            "untracked": [],
            "staged": [],
            "recent_commits": []
        }

    # 获取短状态
    _, status_out, _ = run_cmd(["git", "status", "--porcelain"], git_root)
    modified = []
    untracked = []
    staged = []

    for line in status_out.splitlines():
        if not line or len(line) < 3:
            continue
        x = line[0]
        y = line[1]
        file_path = line[3:].strip()
        if x in ['M', 'A', 'D', 'R', 'C']:
            staged.append(file_path)
        if y == 'M':
            modified.append(file_path)
        elif x == '?' and y == '?':
            untracked.append(file_path)

    # 获取最近 3 条提交
    _, log_out, _ = run_cmd(["git", "log", "-n", "3", "--oneline"], git_root)
    commits = [c.strip() for c in log_out.splitlines() if c.strip()]

    return {
        "is_git": True,
        "root": str(git_root),
        "branch": branch,
        "modified": modified,
        "untracked": untracked,
        "staged": staged,
        "recent_commits": commits
    }

def detect_dev_processes():
    active_dev_procs = []
    sys_name = platform.system().lower()
    try:
        if sys_name == "windows":
            ok, out, _ = run_cmd(["powershell", "-NoProfile", "-Command", "Get-Process | Select-Object -ExpandProperty ProcessName"], None)
            if ok:
                procs = set(line.strip().lower() for line in out.splitlines() if line.strip())
                for dp in DEV_PROCESSES:
                    if dp in procs or any(dp in p for p in procs):
                        active_dev_procs.append(dp)
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

def generate_resumption_prompt(git_info, target_goal=None, dead_ends=None):
    prompt_lines = [
        "【会话回退续接指令 · 状态基线与破局聚焦】",
        "",
        "1. 物理工作区最新状态 (Physical Code Grounding)：",
        f"   - 当前代码仓根目录：`{git_info['root']}` (分支: `{git_info['branch']}`)",
    ]

    all_changes = []
    if git_info["staged"]:
        all_changes.append(f"暂存资产: {', '.join(git_info['staged'][:5])}")
    if git_info["modified"]:
        all_changes.append(f"已改动文件: {', '.join(git_info['modified'][:8])}")
    if git_info["untracked"]:
        all_changes.append(f"新增产物: {', '.join(git_info['untracked'][:5])}")

    if all_changes:
        prompt_lines.append("   - 磁盘文件已变更（请以此为代码现实基准，严禁无故推翻重写）：")
        for c in all_changes:
            prompt_lines.append(f"     * {c}")
    else:
        prompt_lines.append("   - 当前工作区状态纯净 (Clean Working Tree)。")

    prompt_lines.extend([
        "",
        "2. 已确立事实与有效约束 (Hard Facts & Ground Truth)：",
        "   - 硬件与平台环境：宿主系统已对齐，硬件探针与依赖库保持最新。",
        "   - 架构契约：严格遵循既定接口规范与数据模型，禁止引入未定义的外部变量。",
        "",
        "3. 已验证的失败死路与负面清单 (Negative Constraints / Blacklist)："
    ])

    if dead_ends:
        prompt_lines.append(f"   - 严禁尝试：{dead_ends}")
    else:
        prompt_lines.append("   - 严禁尝试：已确认不可行的试错方案（请避免重复产生相同错误或循环修补）。")

    prompt_lines.extend([
        "",
        "4. 本轮唯一行动目标 (Single Focus Action)："
    ])

    if target_goal:
        prompt_lines.append(f"   - 🎯 核心目标：{target_goal}")
    else:
        prompt_lines.append("   - 🎯 核心目标：基于当前物理文件状态，直接推进下一步核心实现，杜绝冗余重构。")

    return "\n".join(prompt_lines)

def main():
    parser = argparse.ArgumentParser(description="Session Checkpoint & Workspace State Analyzer")
    parser.add_argument("--cwd", default=os.getcwd(), help="Target workspace path")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--prompt", action="store_true", help="Generate ready-to-use resumption prompt")
    parser.add_argument("--target", default=None, help="Target goal for resumption prompt")
    parser.add_argument("--dead-ends", default=None, help="Documented dead ends or errors to avoid")

    args = parser.parse_args()

    git_root = find_git_root(args.cwd)
    git_info = inspect_git_state(git_root)
    dev_procs = detect_dev_processes()
    current_os = get_current_os()

    data = {
        "os": current_os,
        "git": git_info,
        "active_dev_processes": dev_procs,
        "summary": {
            "is_dirty": bool(git_info["modified"] or git_info["untracked"] or git_info["staged"]),
            "modified_count": len(git_info["modified"]),
            "untracked_count": len(git_info["untracked"]),
            "staged_count": len(git_info["staged"]),
        }
    }

    if args.prompt:
        prompt_text = generate_resumption_prompt(git_info, args.target, args.dead_ends)
        print(prompt_text)
        return

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    # 默认输出 Markdown 态势看板
    print("# 🛰️ 会话断点与工作区态势诊断看板 (Checkpoint & Workspace Snapshot)")
    print()
    print(f"> **宿主系统**：{current_os} | **工作区根**：`{git_info['root']}` | **当前分支**：`{git_info['branch']}`")
    print()
    print("## 1. 物理工作区资产状态 (Physical Code Reality)")
    if data["summary"]["is_dirty"]:
        print(f"⚠️ **工作区存在未提交改动** (修改: {data['summary']['modified_count']}, 新增: {data['summary']['untracked_count']}, 暂存: {data['summary']['staged_count']}):")
        if git_info["modified"]:
            print("  - **已修改文件**:")
            for f in git_info["modified"][:10]:
                print(f"    * `{f}`")
            if len(git_info["modified"]) > 10:
                print(f"    * ... 及其余 {len(git_info['modified']) - 10} 个文件")
        if git_info["untracked"]:
            print("  - **新增未跟踪文件**:")
            for f in git_info["untracked"][:5]:
                print(f"    * `{f}`")
        print("\n> [!CAUTION] **回退前安全门禁**：回退会话不会改变磁盘代码，但为防止回退后模型意外覆盖，强烈建议先在终端执行 `git stash save \"pre-rewind\"` 或 `git commit -am \"wip: pre-rewind\"`！")
    else:
        print("✅ **工作区纯净**：无未提交改动，磁盘代码与 Git 仓库完全同步。")

    print("\n## 2. 活跃研发与硬件进程 (Active Dev Processes)")
    if dev_procs:
        print(f"⚠️ **正在运行的关键进程**：`{', '.join(dev_procs)}` (注意：若涉及串口或烧录探针，回退后请确保端口未被独占)")
    else:
        print("✅ **无独占研发进程**：无冲突的烧录/串口工具在运行。")

    print("\n## 3. 回退推荐位点建议 (Recommended Checkpoint Targets)")
    print("| 梯队方案 | 推荐位点特征 | 适用场景 | 预期收益 |")
    print("| :--- | :--- | :--- | :--- |")
    print("| **方案 A: 拐点微回退** | 首次报错或思路分叉提问前 | 方向基本正确，仅最近 1~2 个函数陷入报错循环 | 保留绝大部分对话成果，最小代价重试 |")
    print("| **方案 B: 契约重构回退** *(推荐)* | 架构设计/头文件/数据结构刚确定时 | 代码多次打补丁产生腐化、上下文充满报错日志 | 洗掉全部试错噪声，在干净上下文中直奔实现 |")
    print("| **方案 C: 空白会话续接** | 直接开启全新窗口 (无上下文) | 会话总长极大 (>15万Token)、模型注意力严重稀释 | 彻底恢复首字响应速度，杜绝注意力漂移 |")

    print("\n## 4. 破局重生 Prompt 预览 (Resumption Prompt Blueprint)")
    print("```markdown")
    print(generate_resumption_prompt(git_info, args.target, args.dead_ends))
    print("```")

if __name__ == "__main__":
    main()
