# 本地全量工具箱架构与纳管速查索引 (D:\Tools Master Inventory)

> **执行环境**：Windows 11 x86_64 | 基线工作区：`D:\Tools`  
> **更新时间**：2026-11-07 | 纳管工具总数：39 款（7 大核心分类 + 1 待收纳区）

---

## 1. 架构设计与分类全景

本机所有日常开发、系统运维、硬件监测与多媒体工具均集中部署在 `D:\Tools`。通过**“业务聚类 + 形态解耦”**架构，分为以下 8 个标准目录：

```text
D:\Tools/
├── 📁 00_Installer_Inbox/        --> 临时安装包过渡收纳箱
├── 📁 01_Sysinternals/           --> 微软官方底层诊断排查工具
├── 📁 02_Hardware_Benchmark/     --> 硬件传感器与磁盘性能测试
├── 📁 03_System_Utilities/       --> 系统增强、装机运维与便携实用工具
├── 📁 04_Network_Transfer/       --> 网络代理、穿透、测速与多线程传输
├── 📁 05_Productivity_Office/    --> 文献知识库、笔记协同与词典翻译
├── 📁 06_Peripherals_Drivers/    --> 外设驱动、键盘控制与跨端协同中枢
└── 📁 07_Media_Tools/            --> 音视频录制、格式转码与多媒体处理
```

---

## 2. 全量工具清单与执行路径映射表

### 01_Sysinternals（微软系统排查套件）
| 工具名称 | 对应目录与核心程序 | 功能与使用场景 | 运行形态 |
| :--- | :--- | :--- | :--- |
| **Autoruns** | `01_Sysinternals\Autoruns\Autoruns64.exe` | 审查注册表、服务、驱动、任务等全维度自启项 | 绿色便携 |
| **Process Explorer** | `01_Sysinternals\ProcessExplorer\procexp64.exe` | 增强版任务管理器，检索被占用文件句柄与 DLL | 绿色便携 |
| **RAMMap** | `01_Sysinternals\RAMMap\RAMMap64.exe` | 物理内存深度透视，一键清空 Standby 备用内存 | 绿色便携 |
| **TCPView** | `01_Sysinternals\TCPView\tcpview64.exe` | 实时网络出站连接与端口占用监控 | 绿色便携 |

### 02_Hardware_Benchmark（硬件与磁盘基准）
| 工具名称 | 对应目录与核心程序 | 功能与使用场景 | 运行形态 |
| :--- | :--- | :--- | :--- |
| **HWiNFO64** | `02_Hardware_Benchmark\HWiNFO\HWiNFO64.exe` | CPU/GPU 温度、各核心功耗(W)、风扇转速监测 | 绿色便携 |
| **CrystalDiskInfo** | `02_Hardware_Benchmark\CrystalDiskInfo\DiskInfo64.exe` | SSD S.M.A.R.T. 健康度、总写入量 TBW 监测 | 绿色便携 |
| **CrystalDiskMark** | `02_Hardware_Benchmark\CrystalDiskMark\DiskMark64.exe` | 固态硬盘顺序与 4K 随机小文件读写测速 | 绿色便携 |
| **WizTree** | `02_Hardware_Benchmark\WizTree\WizTree64.exe` | 读取 MFT 毫秒级生成全盘大文件热力图 | 绿色便携 |

### 03_System_Utilities（系统增强与装机运维）
| 工具名称 | 对应目录与核心程序 | 功能与使用场景 | 运行形态 / 服务 |
| :--- | :--- | :--- | :--- |
| **QuickLook** | `03_System_Utilities\QuickLook\QuickLook.exe` | 空格键秒级文件预览（代码/PDF/Office/图片） | 绿色便携 |
| **Everything** | `03_System_Utilities\Everything\Everything.exe` | 毫秒级全盘文件名搜索 | 常驻服务 (`Everything`) |
| **UniGetUI** | `03_System_Utilities\UniGetUI\UniGetUI.exe` | WinGet/Scoop/Chocolatey 统一包管理器前端 | 开机守护 (`--daemon`) |
| **HiBit Uninstaller**| `03_System_Utilities\HiBit Uninstaller\HiBitUninstaller.exe`| 深度强力卸载器，粉碎注册表与磁盘残留 | 绿色/单文件 |
| **TrafficMonitor** | `03_System_Utilities\TrafficMonitor\TrafficMonitor.exe` | 任务栏实时网速、CPU、内存悬浮窗监控 | 计划任务自启 |
| **Carnac** | `03_System_Utilities\Carnac\Carnac.exe` | 屏幕键盘实时按键悬浮显示（录屏与演示利器） | 绿色便携 |
| **7-Zip** | `03_System_Utilities\7-Zip\7zFM.exe` | 工业级开源高压缩比解压缩 | 注册表集成 |
| **AOMEI Partition** | `03_System_Utilities\AOMEI Partition Assistant\PartAssist.exe` | 磁盘无损扩缩容、系统迁移与 GPT 转换 | 驱动集成 |
| **傲梅恢复之星** | `03_System_Utilities\傲梅恢复之星\4.9.0\MR.exe` | 误删文件与丢失分区数据深度恢复救援 | 注册表集成 |
| **FreeFileSync** | `03_System_Utilities\FreeFileSync\FreeFileSync.exe` | 本地与外部存储双向/镜像增量数据同步备份 | 注册表集成 |
| **BleachBit** | `03_System_Utilities\BleachBit\bleachbit.exe` | 深度清理系统日志与多浏览器无用缓存 | 注册表集成 |
| **Ventoy** | `03_System_Utilities\Ventoy\Ventoy2Disk.exe` | 新一代多系统 U 盘启动制作工具 | 绿色便携 |
| **DesktopOK** | `03_System_Utilities\DesktopOK\DesktopOK_x64.exe` | 桌面图标布局排列一键备份与还原 | 单文件便携 |
| **IHasher** | `03_System_Utilities\IHasherv0.2.exe` | MD5 / SHA1 / CRC32 文件哈希校验小工具 | 单文件便携 |
| **Winstep Nexus** | `03_System_Utilities\Winstep Nexus\Nexus.exe` | 桌面拟态美化 Dock 栏 | 常驻服务 (`WsxService`) |

### 04_Network_Transfer（网络传输与远程）
| 工具名称 | 对应目录与核心程序 | 功能与使用场景 | 运行形态 / 服务 |
| :--- | :--- | :--- | :--- |
| **Clash Verge** | `04_Network_Transfer\Clash Verge\clash-verge.exe` | 网络规则分流、代理内核与 TUN 网卡模式 | 内核守护 |
| **ToDesk** | `04_Network_Transfer\ToDesk\ToDesk.exe` | 低延迟跨平台远程桌面控制与文件互传 | 常驻服务 (`ToDesk_Service`) |
| **CloudDrive2** | `04_Network_Transfer\CloudDrive2\clouddrive.exe` | 将百度/阿里/115等网盘直接挂载为本地磁盘 | 驱动集成 |
| **Rayburst** | `04_Network_Transfer\Rayburst\rayburst.exe` | 基于 Aria2 Next 的全能多线程下载工具 | 托盘开机常驻 |
| **SpeedManager** | `04_Network_Transfer\SpeedManager\测速网.exe` | 测速网国内节点宽带上/下行与延迟精准测试 | 桌面客户端 |

### 05_Productivity_Office（办公协同与知识管理）
| 工具名称 | 对应目录与核心程序 | 功能与使用场景 | 运行形态 |
| :--- | :--- | :--- | :--- |
| **Zotero** | `05_Productivity_Office\Zotero\zotero.exe` | 学术文献与芯片 Datasheet 管理（数据存 C 盘） | 桌面客户端 |
| **zotero-pdf2zh** | `05_Productivity_Office\zotero-pdf2zh\start_server.bat` | Zotero PDF 英文文献双语对照翻译本地推理服务 (Port:8890) | 后端脚本/服务 |
| **Notion** | `05_Productivity_Office\Notion\Notion.exe` | 结构化个人知识库、项目看板与协同笔记 | Electron 客户端 |
| **TencentDocs** | `05_Productivity_Office\TencentDocs\TencentDocsLauncher.exe` | 腾讯在线多端协作文档与收集表 | 常驻服务更新项 |
| **YoudaoDict** | `05_Productivity_Office\YoudaoDict\YoudaoDict.exe` | 屏幕取词、OCR 划词翻译与专业词典 | 桌面客户端 |

### 06_Peripherals_Drivers（外设驱动与控制中心）
| 工具名称 | 对应目录与核心程序 | 功能与使用场景 | 运行形态 / 服务 |
| :--- | :--- | :--- | :--- |
| **ATK HUB** | `06_Peripherals_Drivers\ATK HUB\ATK HUB.exe` | ATK/VGN 全系外设驱动、8K回报率与磁轴调节 | 服务已设手动 (`AtkHubAgentService`) |
| **AULA F3020** | `06_Peripherals_Drivers\AULA F3020\Config.exe` | 狼蛛机械键盘按键宏与 RGB 灯效控制 | 硬件驱动 |
| **VivoSuite** | `06_Peripherals_Drivers\VivoSuite\pcsuite\pcsuite.exe` | vivo 手机电脑多屏协同、剪贴板流转互传 | 3 项底层常驻服务 |
| **MouseClick** | `06_Peripherals_Drivers\MouseClick\MouseClick.exe` | 鼠大侠高频毫秒级鼠标连点器 | 桌面客户端 |

### 07_Media_Tools（多媒体与录屏）
| 工具名称 | 对应目录与核心程序 | 功能与使用场景 | 运行形态 |
| :--- | :--- | :--- | :--- |
| **EVCapture** | `07_Media_Tools\EVCapture\EVCapture.exe` | 高清无水印桌面屏幕录制与音频采集 | 桌面客户端 |
| **FormatFactory** | `07_Media_Tools\FormatFactory\FormatFactory.exe` | 全能音视频格式转换、压制压缩与音频提取 | 桌面客户端 |

---

## 3. 全局联动脚本使用指南

通过统一启动脚本可在 Agent 或终端中秒级调起任意工具：

```powershell
# 语法
powershell -ExecutionPolicy Bypass -File "C:\Users\hejia\.gemini\config\skills\pc-maintenance-master\scripts\launch_sysinternals.ps1" -Tool <工具名> [-RunAsAdmin]

# 示例
launch_sysinternals.ps1 -Tool Carnac          # 启动屏幕按键显示
launch_sysinternals.ps1 -Tool HWiNFO          # 启动硬件传感器监测
launch_sysinternals.ps1 -Tool WizTree         # 启动磁盘大文件透视仪
launch_sysinternals.ps1 -Tool Everything      # 启动全盘秒搜
launch_sysinternals.ps1 -Tool FormatFactory   # 启动格式工厂
```
