---
name: pc-maintenance-master
version: 2.2.0
description: >-
  Comprehensive Windows PC maintenance, system diagnostics, memory optimization, startup app auditing,
  hardware monitoring, disk cleanup toolkit, and strict Zero Desktop Intrusion for this computer.
  Integrates Sysinternals (RAMMap, Autoruns, Process Explorer, TCPView), WizTree, CrystalDiskInfo, HWiNFO64,
  QuickLook, UniGetUI, FreeFileSync, voidtools Everything, BleachBit, and native PowerShell diagnostics.
  Use when user asks to analyze memory, clean up computer, tune system performance, audit startup apps,
  check disk health, monitor hardware temperature/power, update apps, or manage background services.
license: Apache-2.0
metadata:
  version: v2.2.0
  author: Antigravity
---

# PC Maintenance Master (个人电脑维护与全栈工具箱管家)

本 Skill 是专为当前主机（华为 MateBook / i5-13420H / 16GB / Windows 11 + Linux 双系统）定制的系统级日常维护、深度诊断、优化与全量工具箱（40款顶级运维工具）集成管理技能库。

---

## 1. 核心安全守则与用户生态基准（红线规则）

1. **🔒 核心进程绝对保护**：
   * **华为 RemotePC 保护**：严禁停用、禁用或查杀 `RemotePC_Service` 与 `RemotePC.exe`；
   * **SolidWorks 授权保护**：`SolidWorks Flexnet Server` (`lmgrd.exe`) 严禁关闭，否则导致 SolidWorks 闪退；
2. **🛡️ 备份优先与数据零风险**：
   * 自启项修改前强制备份注册表；清理仅限 `$env:TEMP`、`CrashDumps`、`INetCache` 等无状态临时缓存；回收站清空前人工确认；
3. **🚫 桌面零入侵红线 (Zero Desktop Intrusion Protocol)**：
   * 严禁在未获得用户明确指令的情况下向用户桌面（`Desktop` / `~/桌面`）生成任何快捷方式（`.lnk` / `.desktop`）或临时文件；所有产物收敛在指定目录。

---

## 2. 核心诊断与运维 SOP (Scripts)

| 操作场景 | 调度脚本 (PowerShell) | 关键参数与行为说明 |
| :--- | :--- | :--- |
| **一键性能诊断** | `scripts/system_diagnose.ps1` | CPU/RAM负载、磁盘剩余、热点进程排查 |
| **安全垃圾清理** | `scripts/clean_temp_junk.ps1` | 默认清理TEMP/缓存；`-DeepPreview` 预览安全白名单 |
| **安全态势巡检** | `scripts/security_audit.ps1` | `-Deep` 联动 `autoruns` 与 `tcpview` 输出自启与外联 |
| **全量兵器快速启动** | `scripts/launch_sysinternals.ps1` | `-Tool <工具名>` 模糊直启；`-List` 输出全量纳管清单 |

---

## 3. 深度参考手册

* 📘 **40 款纳管兵器库完整清单与路径映射**：查阅 [`references/tools_inventory.md`](file:///C:/Users/hejia/.gemini/config/skills/pc-maintenance-master/references/tools_inventory.md)（含 Sysinternals、硬件基准、网络串流等 7 大分区完整路径与参数矩阵）。
