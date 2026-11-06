#!/usr/bin/env python3
"""
Skills Health, Domain Architecture & Upstream Update Monitor
Scans the user's global skills directory to detect skills across 5 architecture domains,
inspect git repositories for upstream updates, and report synchronization status.
"""

import os
import sys
import json
import re
import subprocess

SKILLS_DIR = os.path.expanduser(r"~/.gemini/config/skills")

DOMAINS = {
    "01_Embedded_Hardware": [
        "embedded-engineering-master", "embedded-stm32-rules",
        "cortex-m-pyocd", "industrial-serial-agent", "easyeda-api"
    ],
    "02_System_Academic": [
        "everything-search", "pc-maintenance-master",
        "zotero-assistant", "invoice-audit-master", "git-worklog-reporter"
    ],
    "03_Cloud_Sync_Gateway": [
        "google-sync-guard"
    ],
    "04_GCP_Data_Cloud": [
        "bigquery-ai-ml", "bigquery-bigframes", "bigquery-data-transfer-service",
        "bigquery-graph", "bigquery-sql", "bigtable-basics", "building-data-apps",
        "data-autocleaning", "dataform-bigquery", "dbt-bigquery", "discovering-gcp-data-assets",
        "federate-lakehouse-catalog", "gcp-composer-troubleshooting", "gcp-data-pipelines",
        "gcp-dataflow", "gcp-managed-airflow-dag-authoring", "gcp-managed-airflow-migrations",
        "gcp-managed-airflow-recommendations", "gcp-pipeline-orchestration",
        "gcp-pipeline-resource-provisioning", "gcp-spark", "gcs-security-assessment",
        "google-cloud-auth-verification", "google-cloud-storage-basics",
        "google-cloud-storage-bucket-architect", "google-cloud-storage-fuse"
    ],
    "05_Governance_Meta": [
        "skills-navigator", "accidental-data-loss-prevention", "managing-python-dependencies",
        "ml-best-practices", "notebook-guidance", "schema-mapping", "skill-repair"
    ]
}

def get_skill_domain(skill_name):
    for domain, skill_list in DOMAINS.items():
        if skill_name in skill_list:
            return domain
    return "05_Governance_Meta"

def run_git(args, cwd):
    try:
        res = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10
        )
        return res.returncode == 0, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def parse_frontmatter(skill_md_path):
    if not os.path.exists(skill_md_path):
        return None
    try:
        with open(skill_md_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return None
        fm_text = match.group(1)
        name_match = re.search(r'^\s*name:\s*(.+)$', fm_text, re.MULTILINE)
        ver_match = re.search(r'^\s*version:\s*(.+)$', fm_text, re.MULTILINE)
        desc_match = re.search(r'^\s*description:\s*(?:>-\s*|\|\s*)?\n?(.+?)(?=\n\w|\Z)', fm_text, re.DOTALL | re.MULTILINE)
        name = name_match.group(1).strip() if name_match else os.path.basename(os.path.dirname(skill_md_path))
        version = ver_match.group(1).strip() if ver_match else "1.0.0"
        desc = desc_match.group(1).strip() if desc_match else ""
        return {"name": name, "version": version, "description": desc.replace('\n', ' ')}
    except Exception:
        return None

def check_all_skills():
    if not os.path.exists(SKILLS_DIR):
        return {"error": f"Skills directory not found: {SKILLS_DIR}"}

    skills_status = []
    updates_available = []
    domain_counts = {d: 0 for d in DOMAINS.keys()}

    for entry in os.listdir(SKILLS_DIR):
        entry_path = os.path.join(SKILLS_DIR, entry)
        if not os.path.isdir(entry_path) or entry.startswith('.'):
            continue

        skill_md = os.path.join(entry_path, "SKILL.md")
        meta = parse_frontmatter(skill_md)
        if not meta:
            continue

        domain = get_skill_domain(entry)
        if domain in domain_counts:
            domain_counts[domain] += 1

        skill_info = {
            "dir_name": entry,
            "name": meta["name"],
            "version": meta.get("version", "1.0.0"),
            "domain": domain,
            "description": meta["description"][:120] + "..." if len(meta["description"]) > 120 else meta["description"],
            "is_git": os.path.exists(os.path.join(entry_path, ".git")),
            "update_available": False,
            "commits_behind": 0
        }

        # Check git upstream if applicable
        if skill_info["is_git"]:
            ok, _, _ = run_git(["fetch", "origin"], entry_path)
            if ok:
                ok, status_out, _ = run_git(["status", "-uno"], entry_path)
                if "Your branch is behind" in status_out:
                    behind_match = re.search(r'behind \S+ by (\d+) commit', status_out)
                    commits_behind = int(behind_match.group(1)) if behind_match else 1
                    skill_info["update_available"] = True
                    skill_info["commits_behind"] = commits_behind
                    updates_available.append({
                        "name": skill_info["name"],
                        "domain": domain,
                        "dir": entry_path,
                        "commits_behind": commits_behind
                    })

        skills_status.append(skill_info)

    return {
        "total_skills": len(skills_status),
        "domain_distribution": domain_counts,
        "updates_count": len(updates_available),
        "updates_available": updates_available,
        "skills": skills_status
    }

def update_skill(dir_name):
    target_path = os.path.join(SKILLS_DIR, dir_name)
    if not os.path.exists(os.path.join(target_path, ".git")):
        return {"success": False, "error": f"{dir_name} is not a git repository."}

    ok, out, err = run_git(["pull", "origin", "main"], target_path)
    if not ok:
        ok, out, err = run_git(["pull", "origin", "master"], target_path)

    return {"success": ok, "output": out if ok else err}

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "update" and len(sys.argv) > 2:
        res = update_skill(sys.argv[2])
    else:
        res = check_all_skills()
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
