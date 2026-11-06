#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Sync Guard - Offline Queue & Buffer Pool Manager
Root directory: C:\\Users\\hejia\\.gemini\\sync_buffer\\
Structure:
- Queue\\Sheets\\
- Queue\\Docs\\
- Queue\\Drive\\
- Queue\\Calendar\\
- Archived\\
- Logs\\
"""

import sys
import os
import json
import time
import uuid
import shutil
from pathlib import Path

BASE_BUFFER_DIR = Path(r"C:\Users\hejia\.gemini\sync_buffer")
QUEUE_DIR = BASE_BUFFER_DIR / "Queue"
ARCHIVED_DIR = BASE_BUFFER_DIR / "Archived"
LOGS_DIR = BASE_BUFFER_DIR / "Logs"

SERVICES = {
    "sheets": "Sheets",
    "docs": "Docs",
    "drive": "Drive",
    "calendar": "Calendar"
}

def ensure_dirs():
    BASE_BUFFER_DIR.mkdir(parents=True, exist_ok=True)
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVED_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    for folder_name in SERVICES.values():
        (QUEUE_DIR / folder_name).mkdir(parents=True, exist_ok=True)

def normalize_service(service: str) -> str:
    s = service.strip().lower()
    if s not in SERVICES:
        raise ValueError(f"Unsupported service '{service}'. Must be one of {list(SERVICES.keys())}")
    return SERVICES[s]

def enqueue(service: str, payload: dict, target_name: str = "", note: str = ""):
    ensure_dirs()
    folder_name = normalize_service(service)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    short_id = uuid.uuid4().hex[:6]
    task_id = f"{service.lower()}_{timestamp}_{short_id}"
    
    task_obj = {
        "task_id": task_id,
        "service": service.lower(),
        "status": "pending",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "target_name": target_name,
        "note": note,
        "payload": payload
    }
    
    task_file = QUEUE_DIR / folder_name / f"{task_id}.json"
    with open(task_file, "w", encoding="utf-8") as f:
        json.dump(task_obj, f, ensure_ascii=False, indent=2)
        
    return task_id, str(task_file)

def list_pending(service: str = None):
    ensure_dirs()
    target_folders = [normalize_service(service)] if service else list(SERVICES.values())
    pending_tasks = []
    
    for folder_name in target_folders:
        s_dir = QUEUE_DIR / folder_name
        for json_file in s_dir.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    task = json.load(f)
                    if task.get("status") == "pending":
                        pending_tasks.append(task)
            except Exception:
                pass
                
    # 严格按照时间先后（FIFO）排序
    pending_tasks.sort(key=lambda x: x.get("created_at", ""))
    return pending_tasks

def mark_synced(task_id: str):
    ensure_dirs()
    parts = task_id.split("_")
    if not parts:
        return False, "Invalid task ID format"
    service_key = parts[0].lower()
    if service_key not in SERVICES:
        return False, f"Unknown service prefix in {task_id}"
        
    folder_name = SERVICES[service_key]
    src_file = QUEUE_DIR / folder_name / f"{task_id}.json"
    if not src_file.exists():
        return False, f"Task file {src_file} not found"
        
    dst_file = ARCHIVED_DIR / f"{task_id}.json"
    try:
        with open(src_file, "r", encoding="utf-8") as f:
            task = json.load(f)
        task["status"] = "synced"
        task["synced_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(dst_file, "w", encoding="utf-8") as f:
            json.dump(task, f, ensure_ascii=False, indent=2)
        src_file.unlink()
        return True, str(dst_file)
    except Exception as e:
        return False, str(e)

def get_stats():
    ensure_dirs()
    stats = {}
    total = 0
    for key, folder in SERVICES.items():
        count = len(list((QUEUE_DIR / folder).glob("*.json")))
        stats[key] = count
        total += count
    archived_count = len(list(ARCHIVED_DIR.glob("*.json")))
    return {"total_pending": total, "services": stats, "archived_total": archived_count}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Buffer Queue Manager")
    parser.add_argument("--stats", action="store_true", help="Show queue statistics")
    parser.add_argument("--list", action="store_true", help="List all pending tasks")
    args = parser.parse_args()
    
    if args.stats:
        print(json.dumps(get_stats(), ensure_ascii=False, indent=2))
    elif args.list:
        tasks = list_pending()
        print(json.dumps(tasks, ensure_ascii=False, indent=2))
    else:
        parser.print_help()
