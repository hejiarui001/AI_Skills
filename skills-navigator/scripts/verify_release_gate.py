#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Skills Release Gate Verifier (确定性机器交付核验门禁)
版本: v1.0.0

职能（根除靠自觉漏步与局部自洽幻觉）：
1. 检查全库 SKILL.md 语义化版本声明与 <80 行 Token 预算门禁；
2. 对全库所有 .py 脚本执行 py_compile 静态编译核验；
3. 扫描并拦截残留脏污文件 (__pycache__, *.sync-conflict-*, *.tmp, index.lock)；
4. 校验 CHANGELOG.md 最新标题版本号与本地 Git Tag 一致性，防止漏打 Tag。
"""

import os
import re
import sys
import json
import subprocess
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[2]
MAX_SKILL_LINES = 80

def check_skill_files():
    issues = []
    warnings = []
    skill_count = 0

    for item in sorted(SKILLS_ROOT.iterdir()):
        if not item.is_dir() or item.name.startswith(".") or item.name in ["docs", "Tools"]:
            continue
        skill_md = item / "SKILL.md"
        if not skill_md.exists():
            continue
        skill_count += 1
        text = skill_md.read_text(encoding="utf-8", errors="ignore")
        lines = len(text.splitlines())

        m = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if not m or not re.search(r"^\s*version:\s*\d+\.\d+\.\d+", m.group(1), re.MULTILINE):
            issues.append(f"[{item.name}] 缺少标准三段式 version 字段")

        if lines > MAX_SKILL_LINES:
            warnings.append(f"[{item.name}] SKILL.md 行数 ({lines}L) 超出 {MAX_SKILL_LINES}L 门禁")

    return skill_count, issues, warnings

def check_python_scripts():
    py_files = list(SKILLS_ROOT.rglob("*.py"))
    failed = []
    for pf in py_files:
        try:
            src = pf.read_text(encoding="utf-8")
            compile(src, str(pf), "exec")
        except Exception as e:
            failed.append(f"{pf.relative_to(SKILLS_ROOT)}: {e}")
    return len(py_files), failed

def check_stray_artifacts():
    dirty = []
    for p in SKILLS_ROOT.rglob("*"):
        if ".git" in p.parts:
            continue
        if p.name == "__pycache__" or ".sync-conflict-" in p.name or p.name.endswith(".tmp") or p.name == "index.lock":
            dirty.append(str(p.relative_to(SKILLS_ROOT)))
    return dirty

def check_changelog_tag_sync():
    changelog = SKILLS_ROOT / "CHANGELOG.md"
    if not changelog.exists():
        return None, False, "CHANGELOG.md 不存在"
    text = changelog.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"^## \[(v\d+\.\d+\.\d+)\]", text, re.MULTILINE)
    if not m:
        return None, False, "未在 CHANGELOG.md 中识别到最新 [vX.Y.Z] 版本"
    latest_ver = m.group(1)

    res = subprocess.run(
        ["git", "-C", str(SKILLS_ROOT), "tag", "-l", latest_ver],
        stdout=subprocess.PIPE, text=True
    )
    has_tag = (latest_ver in res.stdout.splitlines())
    return latest_ver, has_tag, None if has_tag else f"CHANGELOG 最新版 {latest_ver} 尚未创建本地 Git Tag!"

def main():
    skill_count, skill_issues, line_warnings = check_skill_files()
    py_count, py_failed = check_python_scripts()
    dirty_files = check_stray_artifacts()
    latest_ver, has_tag, tag_msg = check_changelog_tag_sync()

    passed = not (skill_issues or py_failed or dirty_files)
    report = {
        "gate_passed": passed and has_tag,
        "skills_audited": skill_count,
        "python_scripts_compiled": py_count,
        "latest_changelog_version": latest_ver,
        "tag_synced": has_tag,
        "issues": skill_issues + py_failed + ([tag_msg] if tag_msg else []),
        "warnings": line_warnings,
        "dirty_artifacts": dirty_files
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if report["gate_passed"] else 1)

if __name__ == "__main__":
    main()
