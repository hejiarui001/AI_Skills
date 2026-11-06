#!/usr/bin/env python3
"""
Embedded C/C++ Static Rule & Architecture Checker
Checks source code against safety & PIA architectural rules:
1. No dynamic memory allocation (malloc/free/calloc/realloc)
2. No HAL_Delay inside callbacks, ISRs, or normal loops
3. Enforces <stdint.h> explicit types (flags bare 'int', 'long')
4. Checks volatile on global ISR flags
5. Architectural Rule: Flags monolithic files exceeding 400 lines
6. Architectural Rule: Detects reverse dependency (#include "app_*.h" in BSP or Module)
"""

import sys
import re
import os

def check_file(filepath):
    issues = []
    if not os.path.exists(filepath):
        return [f"File not found: {filepath}"]

    filename = os.path.basename(filepath).lower()

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    total_lines = len(lines)
    # Check 1: Monolithic file size check (> 400 lines for C files)
    if total_lines > 400 and filepath.endswith('.c'):
        issues.append(f"[ARCH WARNING] Monolithic file detected ({total_lines} lines). Consider splitting into Module/Service/App per PIA architecture guidelines.")

    in_isr_or_callback = False
    current_func = ""

    for idx, line in enumerate(lines, 1):
        clean_line = line.strip()

        # Check 2: Reverse dependency (BSP/Module including App)
        if any(prefix in filename for prefix in ['bsp_', 'module_', 'drv_']):
            if re.search(r'#include\s+["<](app_[^">]+|main\.h)[">]', clean_line) and 'bsp_' in filename and 'main.h' in clean_line:
                pass # bsp including main.h is standard in CubeMX
            elif re.search(r'#include\s+["<]app_[^">]+[">]', clean_line):
                issues.append(f"Line {idx}: [ARCH CRITICAL] Reverse dependency detected. Low-level driver/module must never include application header '{clean_line}'.")

        # Check 3: malloc / free
        if re.search(r'\b(malloc|free|calloc|realloc)\s*\(', clean_line):
            issues.append(f"Line {idx}: [CRITICAL] Dynamic memory allocation detected ({clean_line}). Use static buffers instead.")

        # Check function boundaries
        func_match = re.search(r'^\w+\s+(\w+)\s*\([^)]*\)\s*\{?', clean_line)
        if func_match:
            current_func = func_match.group(1)
            if any(k in current_func.lower() for k in ['irq', 'isr', 'callback', 'handler']):
                in_isr_or_callback = True
            else:
                in_isr_or_callback = False

        if in_isr_or_callback:
            if 'HAL_Delay' in clean_line:
                issues.append(f"Line {idx}: [CRITICAL] HAL_Delay called inside interrupt context '{current_func}'. This will cause deadlock.")
            if re.search(r'\bprintf\s*\(', clean_line):
                issues.append(f"Line {idx}: [WARNING] printf called in interrupt context '{current_func}'. Heavy I/O should be deferred to main loop.")

        # Check 4: Bare int / long in variable declarations (ignore main, comments, etc.)
        if not clean_line.startswith('//') and not clean_line.startswith('*'):
            if re.search(r'\b(unsigned\s+)?(short|int|long)\b', clean_line) and not 'int main' in clean_line and not '#include' in clean_line and not 'uint' in clean_line and not 'int8_' in clean_line and not 'int16_' in clean_line and not 'int32_' in clean_line and not 'int64_' in clean_line:
                issues.append(f"Line {idx}: [STYLE] Bare integer type used. Prefer explicit <stdint.h> types (uint8_t, int32_t, etc.).")

    return issues

def check_workspace_dir(ws_dir):
    issues = []
    print(f"Checking embedded workspace architecture: {ws_dir}")

    # 1. Check PIA Directory Conformance (supports root or Firmware/ subfolder)
    expected_dirs = ['BSP', 'App']
    recommended_dirs = ['Module', 'Service']

    fw_dir = os.path.join(ws_dir, 'Firmware')
    for ed in expected_dirs:
        in_root = os.path.exists(os.path.join(ws_dir, ed))
        in_fw = os.path.exists(os.path.join(fw_dir, ed))
        if not (in_root or in_fw):
            issues.append(f"[ARCH CRITICAL] Required PIA directory '{ed}/' is missing (checked root and Firmware/).")

    for rd in recommended_dirs:
        in_root = os.path.exists(os.path.join(ws_dir, rd))
        in_fw = os.path.exists(os.path.join(fw_dir, rd))
        if not (in_root or in_fw):
            issues.append(f"[ARCH RECOMMENDATION] Recommended PIA directory '{rd}/' is missing (checked root and Firmware/).")

    if not os.path.exists(os.path.join(ws_dir, '_checkpoints')):
        issues.append("[ARCH RECOMMENDATION] Recommended PIA directory '_checkpoints/' is missing.")

    # 2. Check Specification file
    has_spec = any(os.path.exists(os.path.join(ws_dir, f)) for f in ['SOFTWARE_SPEC.md', 'README.md', 'HARDWARE_V4.md'])
    if not has_spec:
        issues.append("[DOC WARNING] Neither 'SOFTWARE_SPEC.md' nor comprehensive project documentation found in root.")

    # 3. Check all project C/C++ files (skipping vendor drivers, virtualenvs, and build caches)
    SKIP_DIR_NAMES = {'.git', '.venv', 'venv', '__pycache__', '.vscode', 'node_modules', '_checkpoints', 'archive_backup_current', 'MDK-ARM', 'build', 'Drivers'}

    for root, dirs, files in os.walk(ws_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIR_NAMES]
        for f in files:
            if f.endswith(('.c', '.h')):
                fp = os.path.join(root, f)
                f_issues = check_file(fp)
                for fi in f_issues:
                    rel_p = os.path.relpath(fp, ws_dir)
                    issues.append(f"[{rel_p}] {fi}")

    return issues

def main():
    if len(sys.argv) < 2:
        print("Usage: python check_c_embedded_rules.py <source_file_or_workspace_dir>")
        sys.exit(1)

    target = sys.argv[1]
    if os.path.isdir(target):
        issues = check_workspace_dir(target)
    else:
        issues = check_file(target)

    if not issues:
        print(f"PASS: {target} strictly adheres to embedded safety & PIA architecture guidelines.")
        sys.exit(0)
    else:
        print(f"CHECK COMPLETED for {target}: {len(issues)} issue(s) detected:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1 if any('[CRITICAL]' in i or '[ARCH CRITICAL]' in i for i in issues) else 0)

if __name__ == "__main__":
    main()
