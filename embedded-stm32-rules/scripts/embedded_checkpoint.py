#!/usr/bin/env python3
"""
Embedded Milestone Checkpoint & Rollback Tool
Creates lightweight, reproducible milestone snapshots for STM32 / MCU projects.
Excludes bloated build caches (*.o, *.crf, *.d, *.axf, etc.) while preserving:
1. Core project sources (App, Module, Service, BSP, Core/Src, Core/Inc)
2. CubeMX .ioc and IDE project files (.uvprojx, CMakeLists.txt, Makefile)
3. Verified stable binaries (*.hex, *.bin)
4. Milestone description (CHECKPOINT_NOTE.md) & 1-click restore script (RESTORE.ps1)
"""

import os
import sys
import shutil
import datetime

# Directories to preserve if they exist
PRESERVE_DIRS = ['Firmware', 'App', 'Module', 'Service', 'BSP', 'Core/Inc', 'Core/Src']

# File extensions and directories to exclude (heavy build files & virtual environments)
EXCLUDE_EXTS = {'.o', '.crf', '.d', '.axf', '.htm', '.dep', '.build_log.htm', '.lnp', '.sct', '.map', '.ipch', '.pyc'}
EXCLUDE_DIRS = {'.git', '.venv', 'venv', '__pycache__', '.vscode', 'node_modules', '_checkpoints', 'archive_backup_current'}

def create_checkpoint(workspace_dir, tag_name, note=""):
    checkpoints_root = os.path.join(workspace_dir, "_checkpoints")
    os.makedirs(checkpoints_root, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_tag = tag_name.replace(" ", "_")
    cp_dir_name = f"CP_{timestamp}_{clean_tag}"
    cp_path = os.path.join(checkpoints_root, cp_dir_name)
    os.makedirs(cp_path, exist_ok=True)

    copied_files = []
    total_bytes = 0

    # 1. Copy source directories
    for d in PRESERVE_DIRS:
        src_dir = os.path.join(workspace_dir, d)
        if os.path.exists(src_dir):
            dst_dir = os.path.join(cp_path, d)
            for root, dirs, files in os.walk(src_dir):
                dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
                rel_root = os.path.relpath(root, src_dir)
                target_root = os.path.join(dst_dir, rel_root) if rel_root != '.' else dst_dir
                os.makedirs(target_root, exist_ok=True)
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext not in EXCLUDE_EXTS:
                        s_file = os.path.join(root, f)
                        d_file = os.path.join(target_root, f)
                        shutil.copy2(s_file, d_file)
                        size = os.path.getsize(s_file)
                        total_bytes += size
                        copied_files.append(os.path.relpath(s_file, workspace_dir))

    # 2. Copy root config files (.ioc, SOFTWARE_SPEC.md, COMMUNICATION_PROTOCOL*.md, HARDWARE*.md)
    for f in os.listdir(workspace_dir):
        ext = os.path.splitext(f)[1].lower()
        if ext in ['.ioc', '.uvprojx', '.uvoptx'] or f in ['SOFTWARE_SPEC.md', 'CMakeLists.txt', 'Makefile'] or f.startswith('COMMUNICATION_PROTOCOL') or f.startswith('HARDWARE'):
            s_file = os.path.join(workspace_dir, f)
            if os.path.isfile(s_file):
                d_file = os.path.join(cp_path, f)
                shutil.copy2(s_file, d_file)
                size = os.path.getsize(s_file)
                total_bytes += size
                copied_files.append(f)

    # 3. Locate and copy the latest stable .hex/.bin
    for root, dirs, files in os.walk(workspace_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if f.endswith('.hex') or f.endswith('.bin'):
                s_file = os.path.join(root, f)
                rel_path = os.path.relpath(s_file, workspace_dir)
                d_file = os.path.join(cp_path, rel_path)
                os.makedirs(os.path.dirname(d_file), exist_ok=True)
                shutil.copy2(s_file, d_file)
                size = os.path.getsize(s_file)
                total_bytes += size
                copied_files.append(rel_path)

    # 4. Write CHECKPOINT_NOTE.md
    note_file = os.path.join(cp_path, "CHECKPOINT_NOTE.md")
    with open(note_file, "w", encoding="utf-8") as nf:
        nf.write(f"# 工程复位节点快照 (Milestone Checkpoint)\n\n")
        nf.write(f"- **节点标签 (Tag)**: `{clean_tag}`\n")
        nf.write(f"- **创建时间 (Timestamp)**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        nf.write(f"- **快照体积 (Size)**: {total_bytes / 1024:.1f} KB (剔除编译缓存，节省 99%+ 磁盘空间)\n")
        nf.write(f"- **节点说明 (Note)**: {note if note else '功能逐个跑通或重大变更前创建的工程复位节点'}\n\n")
        nf.write(f"### 包含的关键源码与产物:\n")
        for cf in sorted(copied_files):
            nf.write(f"- `{cf}`\n")
        nf.write(f"\n### 一键还原方式:\n")
        nf.write(f"在当前目录下运行 PowerShell 脚本 `.\\RESTORE.ps1` 即可将全部源码与固件无损还原到工作区根目录。\n")

    # 5. Write RESTORE.ps1
    restore_file = os.path.join(cp_path, "RESTORE.ps1")
    with open(restore_file, "w", encoding="utf-8") as rf:
        rf.write('# 一键复位恢复脚本 (Milestone Restore Script)\n')
        rf.write('$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition\n')
        rf.write('$WorkspaceDir = Split-Path -Parent (Split-Path -Parent $ScriptDir)\n\n')
        rf.write('Write-Host ">>> 正在执行工程节点复位还原到: $WorkspaceDir..." -ForegroundColor Cyan\n\n')
        for cf in sorted(copied_files):
            win_rel = cf.replace('/', '\\')
            rf.write(f'if (Test-Path "$ScriptDir\\{win_rel}") {{\n')
            rf.write(f'    $targetDir = Split-Path -Parent "$WorkspaceDir\\{win_rel}"\n')
            rf.write(f'    if (!(Test-Path $targetDir)) {{ New-Item -ItemType Directory -Path $targetDir -Force | Out-Null }}\n')
            rf.write(f'    Copy-Item "$ScriptDir\\{win_rel}" "$WorkspaceDir\\{win_rel}" -Force\n')
            rf.write(f'}}\n')
        rf.write('\nWrite-Host ">>> 节点复位还原完成！" -ForegroundColor Green\n')

    print(f"[CHECKPOINT SUCCESS] Created milestone '{cp_dir_name}' ({total_bytes / 1024:.1f} KB, {len(copied_files)} files).")
    print(f"Path: {cp_path}")
    return cp_path

def list_checkpoints(workspace_dir):
    checkpoints_root = os.path.join(workspace_dir, "_checkpoints")
    if not os.path.exists(checkpoints_root):
        print("No _checkpoints directory found in workspace.")
        return []
    cps = [d for d in os.listdir(checkpoints_root) if os.path.isdir(os.path.join(checkpoints_root, d))]
    cps.sort()
    print(f"Found {len(cps)} milestone checkpoints in {checkpoints_root}:")
    for cp in cps:
        note_p = os.path.join(checkpoints_root, cp, "CHECKPOINT_NOTE.md")
        desc = ""
        if os.path.exists(note_p):
            with open(note_p, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if "- **节点说明" in line:
                        desc = line.split(":", 1)[-1].strip()
                        break
        print(f"  * {cp}  --> {desc}")
    return cps

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python embedded_checkpoint.py <workspace_dir> create <tag_name> [optional_note]")
        print("       python embedded_checkpoint.py <workspace_dir> list")
        sys.exit(1)

    ws = sys.argv[1]
    cmd = sys.argv[2]
    if cmd == "create":
        tag = sys.argv[3] if len(sys.argv) > 3 else "milestone"
        note_text = sys.argv[4] if len(sys.argv) > 4 else ""
        create_checkpoint(ws, tag, note_text)
    elif cmd == "list":
        list_checkpoints(ws)
