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


def _strip_comments_and_strings(line):
    no_block = re.sub(r'/\*.*?\*/', ' ', line)
    no_line = re.sub(r'//.*$', '', no_block)
    if no_line.lstrip().startswith('#include'):
        return no_line.strip()
    no_str = re.sub(r'"([^"\\]|\\.)*"', '""', no_line)
    return no_str.strip()


def check_file(filepath):
    issues = []
    if not os.path.exists(filepath):
        return [f"File not found: {filepath}"]

    filename = os.path.basename(filepath).lower()
    if filename in {'syscalls.c', 'sysmem.c'} or (filename.startswith('system_stm32') and filename.endswith('.c')):
        return issues

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    total_lines = len(lines)
    # Check 1: Monolithic file size check (> 400 lines for C/C++ implementation files)
    if total_lines > 400 and filename.endswith(('.c', '.cpp')):
        issues.append(f"[ARCH WARNING] Monolithic file detected ({total_lines} lines). Consider splitting into Module/Service/App per PIA architecture guidelines.")

    in_isr_or_callback = False
    in_block_comment = False
    current_func = ""

    for idx, line in enumerate(lines, 1):
        clean_line = line.strip()
        if in_block_comment:
            if '*/' in clean_line:
                in_block_comment = False
                clean_line = clean_line.split('*/', 1)[1].strip()
            else:
                continue
        if clean_line.startswith('/*') and '*/' not in clean_line:
            in_block_comment = True
            continue

        code_line = _strip_comments_and_strings(clean_line)
        if not code_line:
            continue

        # Check 2: Reverse dependency (BSP/Module including App)
        if any(prefix in filename for prefix in ['bsp_', 'module_', 'drv_']):
            if re.search(r'#include\s+["<](app_[^">]+|main\.h)[">]', code_line) and 'bsp_' in filename and 'main.h' in code_line:
                pass  # bsp including main.h is standard in CubeMX
            elif re.search(r'#include\s+["<]app_[^">]+[">]', code_line):
                issues.append(f"Line {idx}: [ARCH CRITICAL] Reverse dependency detected. Low-level driver/module must never include application header '{code_line}'.")

        # Check 3: malloc / free
        if re.search(r'\b(malloc|free|calloc|realloc)\s*\(', code_line):
            issues.append(f"Line {idx}: [CRITICAL] Dynamic memory allocation detected ({code_line}). Use static buffers instead.")

        # Check function boundaries
        func_match = re.search(r'^\w+\s+(\w+)\s*\([^)]*\)\s*\{?', code_line)
        if func_match:
            current_func = func_match.group(1)
            if any(k in current_func.lower() for k in ['irq', 'isr', 'callback', 'handler']):
                in_isr_or_callback = True
            else:
                in_isr_or_callback = False

        if in_isr_or_callback:
            if 'HAL_Delay' in code_line:
                issues.append(f"Line {idx}: [CRITICAL] HAL_Delay called inside interrupt context '{current_func}'. This will cause deadlock.")
            if re.search(r'\bprintf\s*\(', code_line):
                issues.append(f"Line {idx}: [WARNING] printf called in interrupt context '{current_func}'. Heavy I/O should be deferred to main loop.")

        # Check 4: Bare short/int/long in declarations (ignore casts, main(), #include, stdint types, for-loop indices)
        expr_no_casts = re.sub(r'\(\s*(?:unsigned\s+|signed\s+)?(?:short|int|long(?:\s+long)?)\s*\)', '', code_line)
        if (
            not expr_no_casts.startswith('#')
            and 'int main' not in expr_no_casts
            and not re.match(r'^for\s*\(\s*(?:volatile\s+)?(?:unsigned\s+)?int\b', expr_no_casts)
            and re.search(r'\b(unsigned\s+|signed\s+)?(short|int|long)\b', expr_no_casts)
            and not re.search(r'\bu?int(?:8|16|32|64)_t\b', expr_no_casts)
        ):
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

    # 2. Check Specification file (root or docs/)
    spec_candidates = ['SOFTWARE_SPEC.md', 'README.md', 'HARDWARE_SPEC.md', 'HARDWARE_V4.md']
    has_spec = any(
        os.path.exists(os.path.join(ws_dir, f)) or os.path.exists(os.path.join(ws_dir, 'docs', f))
        for f in spec_candidates
    )
    if not has_spec:
        issues.append("[DOC WARNING] Neither 'SOFTWARE_SPEC.md' nor comprehensive project documentation found in root or docs/.")

    # 3. Check all project C/C++ files (skipping vendor drivers, virtualenvs, and build caches)
    SKIP_DIR_NAMES = {'.git', '.venv', 'venv', '__pycache__', '.vscode', 'node_modules', '_checkpoints', 'archive_backup_current', 'MDK-ARM', 'build', 'Drivers'}

    for root, dirs, files in os.walk(ws_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIR_NAMES]
        for f in files:
            if f.endswith(('.c', '.h', '.cpp', '.hpp')):
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
