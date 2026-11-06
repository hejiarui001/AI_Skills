---
name: pc-maintenance-master
version: 1.3.0
description: >-
  Comprehensive Windows PC maintenance, system diagnostics, memory optimization,
  startup app auditing, and disk cleanup toolkit for this computer. Integrates Sysinternals
  (RAMMap, Autoruns, Process Explorer, TCPView), WizTree, CrystalDiskInfo, voidtools Everything,
  BleachBit, and native PowerShell diagnostics. Use when user asks to analyze memory, clean up computer,
  tune system performance, audit startup apps, check disk health, or manage background services.
license: Apache-2.0
metadata:
  version: v1.3.0
  author: Antigravity
---

# PC Maintenance Master (个人电脑维护与性能医生)

本 Skill 是专为当前主机（华为 MateBook / i5-13420H / 16GB / Windows 11）定制的系统级日常维护、深度诊断、优化与安全基线防护技能库。它融合了底层 CIM/WMI 探针与当前全网最顶级的轻量绿色维护工具阵列。

---

## 1. 核心安全守则与用户生态基准（红线规则）

在执行任何维护操作前，必须严格遵守以下设备特定规则：

1. **🔒 华为 RemotePC 保护**：
   * 用户高度依赖华为远程电脑功能。**严禁**自动停用、禁用或查杀 `RemotePC_Service` 与 `RemotePC.exe`。
2. **🔒 SolidWorks 授权保护**：
   * `SolidWorks Flexnet Server` (`lmgrd.exe`) 是本地核心许可进程，**严禁**关闭，否则会导致 SolidWorks 闪退。
3. **🛡️ 备份优先原则**：
   * 修改注册表自启项时，必须先备份到 `HKCU:\Software\Microsoft\Windows\CurrentVersion\Run_DisabledBackup`。
   * 移除快捷方式时，必须先暂存至本地备份文件夹（如 `AppData\Local\SolidWorks_Startup_Backup`）。
4. **⚠️ 数据零风险原则**：
   * 清理操作仅限于 `$env:TEMP`、`CrashDumps`、`INetCache` 等明确的临时无状态目录。严禁跨越目录触碰用户的代码、工程文档、微信/QQ 数据或系统核心文件。
5. **🛡️ 白名单防滥用**：
   * Defender 白名单仅允许添加明确的受信任开发目录（如 `D:\Tools`、工程库），严禁对 `C:\`、`C:\Windows` 或 `System32` 等高危系统目录做全免扫描。

---

## 2. 本机全量顶尖兵器库 (D:\Tools)

所有工具均已部署在已配置 Defender 白名单的 `D:\Tools` 目录中，秒级启动且零杀毒拦截：

| 工具名称 | 部署路径 | 核心用途与集成状态 |
| :--- | :--- | :--- |
| **WizTree** | `D:\Tools\WizTree\WizTree64.exe` | **全网最快 MFT 磁盘大文件透视仪**（2秒画出全盘空间热力图） |
| **CrystalDiskInfo** | `D:\Tools\CrystalDiskInfo\DiskInfo64.exe` | **固态硬盘 (SSD) 寿命健康/写入量/温度监控** |
| **TCPView** | `D:\Tools\TCPView\tcpview64.exe` | **微软官方网络连接窥视镜**（实时监控程序外网通信与端口） |
| **RAMMap** | `D:\Tools\RAMMap\RAMMap64.exe` | 深度透视物理内存分布，一键清空 Standby List 备用内存缓存 |
| **Autoruns** | `D:\Tools\Autoruns\Autoruns64.exe` | 深度审计所有自启项（驱动、WMI、服务、注册表、计划任务） |
| **Process Explorer** | `D:\Tools\ProcessExplorer\procexp64.exe` | 增强版任务管理器，按句柄/DLL检索被占用的文件并一键解锁 |
| **Everything** | `D:\Tools\Everything\Everything.exe` | 毫秒级全盘文件索引与检索 |
| **BleachBit** | `D:\Tools\BleachBit\bleachbit.exe` | 国际开源清理标杆，支持多浏览器痕迹与深层系统垃圾清除 |
| **HiBit Uninstaller** | `D:\Tools\HiBit Uninstaller\HiBitUninstaller.exe` | 强力卸载顽固软件，深度粉碎注册表与磁盘残留 |
| **PowerToys** | `C:\Users\hejia\AppData\Local\PowerToys\` | 窗口分屏、Alt+Space 快速启动、屏幕 OCR 提取、防休眠 |

---

## 3. 标准操作规程 (SOP)

### 操作一：一键全盘健康体检与性能诊断
```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\hejia\.gemini\config\skills\pc-maintenance-master\scripts\system_diagnose.ps1"
```
* **输出内容**：物理内存（总/已用/可用/占用率）、非分页池/分页池、前 10 大内存进程组、全部分区剩余容量、核心服务状态、用户垃圾缓存大小。

### 操作二：安全磁盘与临时垃圾清理
```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\hejia\.gemini\config\skills\pc-maintenance-master\scripts\clean_temp_junk.ps1"
```
* **安全特性**：清理用户临时缓存（`$env:TEMP`）、崩溃日志（`CrashDumps`）与网络缓存，自动跳过正在读写占用的文件，安全无损。

### 操作三：系统安全态势与基线巡检
```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\hejia\.gemini\config\skills\pc-maintenance-master\scripts\security_audit.ps1"
```
* **巡检项目**：Windows Defender 实时防护与病毒库时效、Defender 排除项安全性审计、网络防火墙三级配置文件、UAC 提权控制等级、高危监听端口暴露面（RDP/3389、SMB/445）、以及隐藏在 Temp/Public 的可疑伪装启动项。

### 操作四：统一快速启动维护工具箱
```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\hejia\.gemini\config\skills\pc-maintenance-master\scripts\launch_sysinternals.ps1" -Tool <WizTree|CrystalDiskInfo|TCPView|RAMMap|Autoruns|ProcessExplorer|Everything|BleachBit|HiBitUninstaller> [-RunAsAdmin]
```
