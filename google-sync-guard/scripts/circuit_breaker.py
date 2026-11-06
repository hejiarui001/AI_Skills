#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Sync Guard - Circuit Breaker & Safety Lockdown Module
Location: C:\\Users\\hejia\\.gemini\\sync_buffer\\CircuitBreaker.lock
Controls the fail-stop lockdown state and clean shutdown of network sync components.
"""

import sys
import os
import json
import time
from pathlib import Path

BASE_BUFFER_DIR = Path(r"C:\Users\hejia\.gemini\sync_buffer")
LOCK_FILE = BASE_BUFFER_DIR / "CircuitBreaker.lock"
LOG_FILE = BASE_BUFFER_DIR / "Logs" / "circuit_breaker.log"

def is_tripped():
    """Returns (True, info_dict) if circuit breaker is locked/tripped, else (False, None)."""
    if LOCK_FILE.exists():
        try:
            with open(LOCK_FILE, "r", encoding="utf-8") as f:
                info = json.load(f)
            return True, info
        except Exception:
            return True, {"state": "TRIPPED", "raw": "Corrupted lock file"}
    return False, None

def trip(reason: str, failed_task_id: str = None, details: dict = None):
    """
    Trip the circuit breaker, write snapshot lock, and trigger clean shutdown.
    No lingering background polling threads will be maintained.
    """
    BASE_BUFFER_DIR.mkdir(parents=True, exist_ok=True)
    (BASE_BUFFER_DIR / "Logs").mkdir(parents=True, exist_ok=True)
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    lock_info = {
        "state": "TRIPPED_SHUTDOWN",
        "tripped_at": timestamp,
        "reason": reason,
        "failed_task_id": failed_task_id,
        "details": details or {}
    }
    
    # 写入熔断锁
    with open(LOCK_FILE, "w", encoding="utf-8") as f:
        json.dump(lock_info, f, ensure_ascii=False, indent=2)
        
    # 追加写日志
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [TRIP] Reason: {reason} | FailedTask: {failed_task_id}\n")
        
    return lock_info

def reset():
    """Reset and unlock the circuit breaker after all pending tasks are reconciled."""
    if LOCK_FILE.exists():
        try:
            LOCK_FILE.unlink()
        except Exception as e:
            return False, f"Failed to remove lock: {e}"
            
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [RESET] Circuit breaker reset. Normal pipeline restored.\n")
    return True, "Unlocked"
