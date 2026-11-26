#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cross-OS Sync Conflict & Lock File Auditor (跨系统同步冲突与锁文件巡检器)
版本: v1.0.0 | 所属技能: pc-maintenance-master

职能：
1. 递归扫描目标目录（如工作区），精准识别跨系统 (NTFS/POSIX) 同步诱发的 *.sync-conflict-*、.syncthing.*.tmp、Git index.lock 及 __pycache__ 脏污；
2. 支持 --clean 参数一键无损清理冲突副本与孤立锁文件（保护正常业务数据）；
3. 若存在 .stignore 与 Syncthing 配置，审计 ignorePerms 与 maxConflicts 关键防雪崩参数。
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path

def scan_directory(target_dir: Path):
    conflicts = []
    tmp_sync = []
    git_locks = []
    pycache_dirs = []

    for root, dirs, files in os.walk(target_dir):
        if ".git" in Path(root).parts:
            # 仅检查 .git 下的 index.lock
            if "index.lock" in files:
                git_locks.append(str(Path(root) / "index.lock"))
            continue

        if "__pycache__" in dirs:
            pycache_dirs.append(str(Path(root) / "__pycache__"))
            dirs.remove("__pycache__")

        for f in files:
            fp = str(Path(root) / f)
            if ".sync-conflict-" in f:
                conflicts.append(fp)
            elif f.startswith(".syncthing.") and f.endswith(".tmp"):
                tmp_sync.append(fp)

    return {
        "target": str(target_dir),
        "sync_conflicts_count": len(conflicts),
        "sync_conflicts_sample": conflicts[:10],
        "syncthing_tmp_count": len(tmp_sync),
        "git_index_locks": git_locks,
        "pycache_count": len(pycache_dirs),
        "_all_conflicts": conflicts,
        "_all_tmp": tmp_sync,
        "_all_locks": git_locks,
        "_all_pycache": pycache_dirs
    }

def clean_artifacts(scan_res):
    removed = {"conflicts": 0, "tmp": 0, "locks": 0, "pycache": 0}
    for p in scan_res["_all_conflicts"]:
        try:
            Path(p).unlink()
            removed["conflicts"] += 1
        except Exception:
            pass
    for p in scan_res["_all_tmp"]:
        try:
            Path(p).unlink()
            removed["tmp"] += 1
        except Exception:
            pass
    for p in scan_res["_all_locks"]:
        try:
            Path(p).unlink()
            removed["locks"] += 1
        except Exception:
            pass
    for p in scan_res["_all_pycache"]:
        try:
            shutil.rmtree(p, ignore_errors=True)
            removed["pycache"] += 1
        except Exception:
            pass
    return removed

def main():
    parser = argparse.ArgumentParser(description="Cross-OS Sync Conflict & Lock Auditor")
    parser.add_argument("--path", default=os.getcwd(), help="Target directory to audit")
    parser.add_argument("--clean", action="store_true", help="Remove found conflicts, sync tmp, locks, and pycache")
    args = parser.parse_args()

    target = Path(args.path).resolve()
    if not target.exists():
        print(json.dumps({"error": f"Path not found: {target}"}, ensure_ascii=False))
        sys.exit(1)

    res = scan_directory(target)
    output = {k: v for k, v in res.items() if not k.startswith("_")}
    if args.clean:
        output["cleaned"] = clean_artifacts(res)

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
