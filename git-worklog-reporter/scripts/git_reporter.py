#!/usr/bin/env python3
"""
Git Worklog & Progress Extractor
Extracts git commits, diff stats, and modified file summaries from local Git repositories
to power AI-driven daily and weekly engineering report generation.
"""

import sys
import os
import json
import subprocess
import argparse
from datetime import datetime, timedelta

def run_git(args, cwd):
    try:
        res = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        if res.returncode != 0:
            return None, res.stderr.strip()
        return res.stdout.strip(), None
    except Exception as e:
        return None, str(e)

def get_repo_info(repo_path):
    branch, _ = run_git(["rev-parse", "--abbrev-ref", "HEAD"], repo_path)
    remote, _ = run_git(["config", "--get", "remote.origin.url"], repo_path)
    user_name, _ = run_git(["config", "--get", "user.name"], repo_path)
    return {
        "branch": branch or "unknown",
        "remote": remote or "local",
        "current_user": user_name or "unknown"
    }

def get_commits(repo_path, days=7, author=None, limit=50):
    since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")

    git_args = [
        "log",
        f"--since={since_date}",
        f"-n{limit}",
        "--pretty=format:COMMIT_START%n%H%n%an%n%ad%n%s%n%b%nCOMMIT_END",
        "--date=iso",
        "--numstat"
    ]

    if author:
        git_args.append(f"--author={author}")

    out, err = run_git(git_args, repo_path)
    if err and not out:
        return {"error": err}

    if not out:
        return {"commits": [], "summary": {"total_commits": 0, "files_changed": 0, "insertions": 0, "deletions": 0}}

    commits = []
    total_insertions = 0
    total_deletions = 0
    all_changed_files = set()

    raw_blocks = out.split("COMMIT_START\n")
    for block in raw_blocks:
        if not block.strip():
            continue

        parts = block.split("COMMIT_END\n")
        header_part = parts[0].strip()
        stat_part = parts[1].strip() if len(parts) > 1 else ""

        header_lines = header_part.split("\n")
        if len(header_lines) < 4:
            continue

        commit_hash = header_lines[0]
        commit_author = header_lines[1]
        commit_date = header_lines[2]
        subject = header_lines[3]
        body = "\n".join(header_lines[4:]).strip() if len(header_lines) > 4 else ""

        # Parse numstat
        changed_files = []
        c_ins = 0
        c_del = 0
        for line in stat_part.split("\n"):
            line = line.strip()
            if not line:
                continue
            cols = line.split("\t")
            if len(cols) == 3:
                ins = int(cols[0]) if cols[0].isdigit() else 0
                dele = int(cols[1]) if cols[1].isdigit() else 0
                fpath = cols[2]
                changed_files.append({"file": fpath, "insertions": ins, "deletions": dele})
                all_changed_files.add(fpath)
                c_ins += ins
                c_del += dele

        total_insertions += c_ins
        total_deletions += c_del

        commits.append({
            "hash": commit_hash[:8],
            "author": commit_author,
            "date": commit_date,
            "subject": subject,
            "body": body,
            "insertions": c_ins,
            "deletions": c_del,
            "files": changed_files
        })

    # Group modified files by extension for quick overview
    ext_counter = {}
    for f in all_changed_files:
        ext = os.path.splitext(f)[1] or "no_ext"
        ext_counter[ext] = ext_counter.get(ext, 0) + 1

    return {
        "repo_info": get_repo_info(repo_path),
        "days_queried": days,
        "summary": {
            "total_commits": len(commits),
            "files_changed_count": len(all_changed_files),
            "total_insertions": total_insertions,
            "total_deletions": total_deletions,
            "file_types": ext_counter
        },
        "commits": commits
    }

def main():
    parser = argparse.ArgumentParser(description="Extract Git worklog for AI reporting")
    parser.add_argument("-p", "--path", default=".", help="Path to git repository (default: current dir)")
    parser.add_argument("-d", "--days", type=int, default=7, help="Number of past days to query (default: 7)")
    parser.add_argument("-a", "--author", default=None, help="Filter by author name/email")
    parser.add_argument("-n", "--limit", type=int, default=50, help="Max commits to fetch")

    args = parser.parse_args()
    repo_path = os.path.abspath(args.path)

    if not os.path.exists(os.path.join(repo_path, ".git")):
        print(json.dumps({"error": f"Not a git repository: {repo_path}"}, ensure_ascii=False))
        sys.exit(1)

    result = get_commits(repo_path, days=args.days, author=args.author, limit=args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
