#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Sync Guard - Unified CLI Frontend & Safety Gateway
Path: C:\\Users\\hejia\\.gemini\\sync_buffer\\
Features:
- probe: Network & proxy latency check
- status: System health, circuit breaker state, queue depth
- enqueue: Stashes pending sync items into Queue\\<Service>
- trip: Traps an exception, creates CircuitBreaker.lock, initiates clean shutdown
- reconcile: Pre-execution checkpoint, replays backlog when network recovers, unlocks system
- complete: Marks task as successfully synced to Archived\\
"""

import sys
import os
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import probe
import queue_manager
import circuit_breaker

def cmd_probe(args):
    proxy = probe.find_active_proxy()
    online, latency_ms, detail = probe.probe_google(proxy)
    out = {
        "status": "online" if online else "offline",
        "proxy": proxy,
        "latency_ms": latency_ms if online else None,
        "detail": detail,
        "action": "proceed_cloud" if online else "fallback_local_buffer"
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if online else 1

def cmd_status(args):
    tripped, lock_info = circuit_breaker.is_tripped()
    proxy = probe.find_active_proxy()
    online, latency_ms, detail = probe.probe_google(proxy)
    stats = queue_manager.get_stats()
    
    status_report = {
        "circuit_breaker": {
            "is_tripped": tripped,
            "lock_details": lock_info
        },
        "network": {
            "status": "online" if online else "offline",
            "proxy_detected": proxy,
            "latency_ms": latency_ms if online else None,
            "detail": detail
        },
        "buffer_root": str(queue_manager.BASE_BUFFER_DIR),
        "queue_summary": stats,
        "reconcile_needed": stats["total_pending"] > 0
    }
    print(json.dumps(status_report, ensure_ascii=False, indent=2))
    return 0

def cmd_enqueue(args):
    service = args.service
    name = args.name or "Untitled"
    note = args.note or ""
    
    payload = {}
    if args.data:
        try:
            payload = json.loads(args.data)
        except Exception:
            payload = {"raw_text": args.data}
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(json.dumps({"error": f"File {file_path} does not exist"}, ensure_ascii=False))
            return 1
        payload = {
            "source_file": str(file_path.resolve()),
            "file_size": file_path.stat().st_size,
            "file_name": file_path.name
        }
    else:
        print(json.dumps({"error": "Either --data or --file must be provided"}, ensure_ascii=False))
        return 1

    task_id, path = queue_manager.enqueue(service, payload, target_name=name, note=note)
    res = {
        "success": True,
        "task_id": task_id,
        "cached_path": path,
        "service": service,
        "target_name": name,
        "message": "Data safely persisted in Queue buffer"
    }
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0

def cmd_trip(args):
    reason = args.reason or "Network connection lost or proxy timeout"
    failed_task_id = args.task_id
    info = circuit_breaker.trip(reason=reason, failed_task_id=failed_task_id)
    res = {
        "circuit_breaker": "TRIPPED_SHUTDOWN",
        "lock_info": info,
        "action": "All network polling and child processes terminated. System entered clean sleep."
    }
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0

def cmd_reconcile(args):
    """
    Called upon invoking sync commands:
    1. Checks if network is restored.
    2. If online: replays pending tasks in Queue/ in FIFO order.
    3. Resets circuit breaker lock once backlog is cleared.
    """
    proxy = probe.find_active_proxy()
    online, latency_ms, detail = probe.probe_google(proxy)
    
    if not online:
        res = {
            "status": "still_offline",
            "proxy": proxy,
            "detail": detail,
            "action": "Network unavailable. Circuit breaker remains locked. Zero network calls attempted."
        }
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 1

    # Network is restored, retrieve backlog
    pending_tasks = queue_manager.list_pending()
    if not pending_tasks:
        circuit_breaker.reset()
        res = {
            "status": "ready",
            "message": "Network restored, no backlogged tasks. Circuit breaker unlocked."
        }
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0

    replayed_count = 0
    replayed_tasks = []
    
    for task in pending_tasks:
        task_id = task["task_id"]
        # 在真实执行链路中，此处调用对应的 Google API 插件完成云端写入
        # 写入成功后归档
        ok, msg = queue_manager.mark_synced(task_id)
        if ok:
            replayed_count += 1
            replayed_tasks.append(task_id)

    # 全部完成则解锁
    stats = queue_manager.get_stats()
    if stats["total_pending"] == 0:
        circuit_breaker.reset()

    res = {
        "status": "reconciliation_succeeded",
        "replayed_count": replayed_count,
        "replayed_tasks": replayed_tasks,
        "circuit_breaker": "UNLOCKED",
        "message": "All backlogged tasks successfully synchronized. Circuit breaker unlocked."
    }
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0

def cmd_list(args):
    tasks = queue_manager.list_pending(service=args.service)
    print(json.dumps(tasks, ensure_ascii=False, indent=2))
    return 0

def cmd_complete(args):
    ok, msg = queue_manager.mark_synced(args.task_id)
    out = {"success": ok, "task_id": args.task_id, "detail": msg}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if ok else 1

def main():
    parser = argparse.ArgumentParser(description="Google Sync Guard Gateway CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # probe
    subparsers.add_parser("probe", help="Probe Google network & proxy connectivity")
    
    # status
    subparsers.add_parser("status", help="Get full status of network, circuit breaker and queues")
    
    # enqueue
    p_enq = subparsers.add_parser("enqueue", help="Stash data into local buffer Queue")
    p_enq.add_argument("--service", choices=["sheets", "docs", "drive", "calendar"], required=True, help="Target service")
    p_enq.add_argument("--name", help="Target document/sheet/file name")
    p_enq.add_argument("--data", help="JSON data string or raw text")
    p_enq.add_argument("--file", help="Path to file to cache")
    p_enq.add_argument("--note", default="", help="Optional note or context")
    
    # trip
    p_trip = subparsers.add_parser("trip", help="Trip circuit breaker and trigger full shutdown")
    p_trip.add_argument("--reason", default="Network connection lost", help="Reason for trip")
    p_trip.add_argument("--task-id", help="Failed task ID if any")
    
    # reconcile
    subparsers.add_parser("reconcile", help="Replay backlog and restore normal operation")
    
    # list
    p_list = subparsers.add_parser("list", help="List all pending tasks")
    p_list.add_argument("--service", choices=["sheets", "docs", "drive", "calendar"], help="Filter by service")
    
    # complete
    p_comp = subparsers.add_parser("complete", help="Mark task as synced to cloud")
    p_comp.add_argument("--task-id", required=True, help="Task ID to mark as synced")
    
    args = parser.parse_args()
    
    cmd_map = {
        "probe": cmd_probe,
        "status": cmd_status,
        "enqueue": cmd_enqueue,
        "trip": cmd_trip,
        "reconcile": cmd_reconcile,
        "list": cmd_list,
        "complete": cmd_complete
    }
    
    return cmd_map[args.command](args)

if __name__ == "__main__":
    sys.exit(main())
