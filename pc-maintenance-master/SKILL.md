---
name: pc-maintenance-master
version: 2.1.0
description: >-
  Comprehensive Windows PC maintenance, system diagnostics, memory optimization,
  startup app auditing, hardware monitoring, disk cleanup toolkit, and strict Zero Desktop Intrusion for this computer.
  Integrates Sysinternals (RAMMap, Autoruns, Process Explorer, TCPView), WizTree, CrystalDiskInfo,
  HWiNFO64, QuickLook, UniGetUI, FreeFileSync, voidtools Everything, BleachBit, and native PowerShell diagnostics.
  Use when user asks to analyze memory, clean up computer, tune system performance, audit startup apps,
  check disk health, monitor hardware temperature/power, update apps, or manage background services.
license: Apache-2.0
metadata:
  version: v2.1.0
  author: Antigravity
---

# PC Maintenance Master (个人电脑维护与全栈工具箱管家)

本 Skill 是专为当前主机（华为 MateBook / i5-13420H / 16GB / Windows 11 + Linux 双系统）定制的系统级日常维护、深度诊断、优化与全量工具箱集成管理技能库。它融合了底层 CIM/WMI 探针与当前全盘纳管的 39 款顶级效率与运维工具阵列。

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
   * 回收站清空前必须扫描拦截并交由用户人工确认。
5. **🛡️ 白名单防滥用**：
   * Defender 白名单仅允许添加明确的受信任开发目录（如 `D:\Tools`、工程库），严禁对 `C:\`、`C:\Windows` 或 `System32` 等高危系统目录做全免扫描。
6. **🚫 桌面零入侵红线 (Zero Desktop Intrusion Protocol)**：
   * 严禁在未获得用户明确允许或主动指令的情况下，向用户操作系统桌面（`$env:USERPROFILE\Desktop` 或 `$(xdg-user-dir DESKTOP)`）生成任何快捷方式（`.lnk` / `.desktop`）、临时测试脚本或软件文件。所有诊断工具、配置及输出产物必须严格收敛在指定目录（如 `D:\Tools` 或工作区内），保持用户桌面纯净。

---

## 2. 本机已纳管全量顶尖兵器库架构 (D:\Tools)

所有工具均已规范部署在 `D:\Tools` 的 7 大功能子域中，结构严密且零散乱冲突：

| 分类分类分区 | 覆盖工具清单 | 核心用途与能力 |
| :--- | :--- | :--- |
| **01_Sysinternals** | `Autoruns`, `ProcessExplorer`, `RAMMap`, `TCPView` | 微软官方系统级底层进程、网络连接、内存与自启深度审计排查 |
| **02_Hardware_Benchmark** | `HWiNFO64`, `CrystalDiskInfo`, `CrystalDiskMark`, `WizTree` | 硬件传感器功耗温度监测、SSD寿命S.M.A.R.T.、读写测速与MFT大文件透视 |
| **03_System_Utilities** | `QuickLook`, `Everything`, `UniGetUI`, `HiBit Uninstaller`, `TrafficMonitor`, `Carnac`, `Winstep Nexus`, `7-Zip`, `AOMEI Partition Assistant`, `傲梅恢复之星`, `FreeFileSync`, `BleachBit`, `Ventoy`, `DesktopOK`, `IHasher` | 空格键秒级文件预览、全盘极速搜索、软件批量更新、拟态Dock栏、屏幕按键显示、U盘启动、深度卸载与数据恢复 |
| **04_Network_Transfer** | `Clash Verge`, `ToDesk`, `CloudDrive2`, `Rayburst`, `SpeedManager` | 核心网络代理规则分流、低延迟远程桌面、网盘本地虚拟盘挂载、Aria2 多线程下载与宽带精准测速 |
| **05_Productivity_Office** | `Zotero`, `zotero-pdf2zh`, `Notion`, `TencentDocs`, `YoudaoDict` | 学术文献与数据手册管理、PDF文献双语翻译、结构化个人知识库、多端在线协作与屏幕取词翻译 |
| **06_Peripherals_Drivers** | `ATK HUB`, `AULA F3020`, `VivoSuite`, `MouseClick` | 外设8K/磁轴驱动控制、键盘按键宏、vivo手机多屏互传与鼠标连点器 |
| **07_Media_Tools** | `EVCapture`, `FormatFactory` | 高清无水印桌面屏幕录制、全能音视频转码压缩与媒体处理 |

> 完整工具路径、服务关联与详细参数矩阵详见手册：[tools_inventory.md](./references/tools_inventory.md)

---

## 3. 标准操作规程 (SOP)

### 操作一：一键全盘健康体检与性能诊断
```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\hejia\.gemini\config\skills\pc-maintenance-master\scripts\system_diagnose.ps1"
```

### 操作二：安全磁盘与临时垃圾清理（保护登录态）
```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\hejia\.gemini\config\skills\pc-maintenance-master\scripts\clean_temp_junk.ps1"
```

### 操作三：系统安全态势与基线巡检
```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\hejia\.gemini\config\skills\pc-maintenance-master\scripts\security_audit.ps1"
```

### 操作四：统一快速启动全量纳管工具
```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\hejia\.gemini\config\skills\pc-maintenance-master\scripts\launch_sysinternals.ps1" -Tool <工具名> [-RunAsAdmin]
```
*(支持模糊匹配与自动回退查找，如 `-Tool Carnac`、`-Tool WizTree`、`-Tool Everything`、`-Tool FormatFactory`)*
