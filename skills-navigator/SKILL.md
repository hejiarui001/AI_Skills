---
name: skills-navigator
version: 1.4.0
description: >-
  Skills command center, update monitor, and quick navigation guide. Trigger when the
  user says "指令", "命令", "技能", "技能清单", "有哪些技能", "怎么用", "快捷指令", "检查更新",
  "更新技能", "menu", "help", or asks about newly added skills. Displays all active skills
  with clear example prompts, automatically checks for upstream skill updates, and
  proactively guides user workflow.
license: Apache-2.0
metadata:
  version: v1.4.0
  author: Antigravity
---

# Skills Navigator & Update Monitor (技能导航与更新管家)

This skill serves as the centralized dashboard and health/update monitor for the user's local customized workflow.

---

## 1. Operating Procedure (SOP)

When the user triggers this skill:

1. **Check Skill Health & Upstream Updates**:
   Execute the background status check (Cross-Platform):
   * **Linux (Bash)**:
     ```bash
     python ~/.gemini/config/skills/skills-navigator/scripts/check_skills_status.py
     ```
   * **Windows (PowerShell)**:
     ```powershell
     python "$env:USERPROFILE\.gemini\config\skills\skills-navigator\scripts\check_skills_status.py"
     ```
   * If `updates_count > 0`, explicitly display an alert banner:
     > 🔔 **检测到上游官方更新**：`[技能名]` 有 X 个新版本提交待更新！回复“**更新 [技能名]**”即可一键同步。

2. **Display Curated Skills Dashboard**:
   Present an organized cheatsheet of installed specialized skills with copy-pasteable **natural language prompt examples**:

   ### 01. 嵌入式与硬件全栈工程 (Embedded & Hardware Suite)
   * 🏆 **嵌入式软硬件全栈工程大师 (`embedded-engineering-master`)**:
     - *“帮我把这个气泵驱动写完并烧进板子里测一下”*
     - *“板子死机了，帮我全链路排查硬件与固件”*
     - *“从原理图引脚核对到串口遥测跑通端到端闭环”*
     - *“合并立创EDA导出的BOM表并按日期归档整理”*
   * ⚡ **STM32 工业编码与 PIA 架构 (`embedded-stm32-rules`)**:
     - *“以 MDK-ARM + CMake 双工作流模式初始化新工程”*
     - *“按照 PIA 架构与标准目录规范重构当前工程”*
     - *“排查 ArmClang 6 与 CMSIS-DSP / MicroLIB 编译链接冲突”*
     - *“用 HAL 库写一个双缓冲 UART DMA 接收驱动并检查合规性”*
   * 🛠️ **固件烧录与硬件调试 (`cortex-m-pyocd`)**:
     - *“检测一下插在电脑上的 ST-Link 和单片机型号”*
     - *“把 build/firmware.bin 烧进单片机 Flash”*
   * 🔌 **工业级串口实机联调 (`industrial-serial-agent`)**:
     - *“扫描当前电脑可用的 COM / ttyUSB 端口”*
     - *“向串口发送一条 AT 指令测试连通性”*
   * 🎨 **嘉立创EDA 官方联动 (`easyeda-api`)**:
     - *“在嘉立创EDA里把选中的网络标号批量改成 VCC_3V3”*

   ### 02. 系统管理与学术办公 (System & Academic Suite)
   * 🔍 **全盘文件秒搜 (`everything-search`)**:
     - *“帮我搜一下电脑里所有的 .ioc 工程”*
     - *“找一下名字包含 motor 的 SOLIDWORKS 零件”*
   * 📚 **Zotero 文献与手册 (`zotero-assistant`)**:
     - *“查一下我 Zotero 里的 STM32F4 芯片手册”*
     - *“总结一下我文献库里最近添加的论文”*
   * 💰 **高校发票报销与合规审计 (`invoice-audit-master`)**:
     - *“审计一下这个批次里的所有发票合规性与税号”*
     - *“自动生成标准 11 列报销总账 Excel 表格”*
     - *“检查物料目录发票查重、序号连续性与红包差额”*
   * 💻 **电脑体检与全量工具箱管家 (`pc-maintenance-master`)**:
     - *“帮我全面体检一下电脑状态和内存占用”*
     - *“安全清理一下系统临时垃圾”*
     - *“运行系统安全态势与端口审计”*
   * 📝 **Git 智能日报与周报 (`git-worklog-reporter`)**:
     - *“根据我今天的 git 提交写一份今日研发日报”*
     - *“整理我过去 7 天的代码修改生成一份结构化周报”*

   ### 03. 云端协同与容灾网关 (Cloud Sync & Gateway)
   * 🛡️ **云协同与防断网熔断网关 (`google-sync-guard`)**:
     - *“探测当前 Google 云端网络连通性”*
     - *“检查离线暂存队列是否有未同步的日志”*

   ### 04. 云原生大数据工程 (GCP Cloud & BigData Master Suite)
   * 📊 **BigQuery 统一中枢 (`bigquery-master`)**:
     - *“优化这条 BigQuery SQL 查询性能并评估槽位消耗”*
     - *“使用 BigQuery 内置 ML 函数训练一个异常检测模型”*
     - *“用 BigFrames Python 编写分布式数据预处理流水线”*
   * 🪣 **GCS 统一存储中枢 (`gcs-storage-suite`)**:
     - *“设计一个符合生产合规的 GCS 存储桶分层与生命周期策略”*
     - *“配置并调优 gcsfuse 高性能挂载参数”*
   * 🔄 **Airflow / Composer 调度总成 (`gcp-airflow-composer-suite`)**:
     - *“编写一个 Airflow 3 兼容的高可用调度 DAG”*
     - *“对 Composer 任务死锁和 Worker 重启进行 RCA 根本原因分析”*
   * ⚙️ **全栈数据管道工程 (`gcp-data-engineering`)**:
     - *“用 dbt / Dataform 编写数仓建模与转换 SQLX”*
     - *“提交一个 Dataproc Serverless PySpark 流批处理作业”*
   * 🏛️ **GCP 资产治理与数据应用 (`gcp-governance-assets`)**:
     - *“校验当前 GCP ADC 认证与环境凭据合规性”*
     - *“为 BigQuery 数据集构建一个 Streamlit / React 数据大屏”*

   ### 05. Agent 运行治理与元能力 (Governance & Meta Suite)
   * 🔬 **数据科学与交互式笔记本规范 (`notebook-data-science`)**:
     - *“按照专业数据科学规范重构并审计这个 Jupyter Notebook”*
   * 🧭 **技能全景总控与更新 (`skills-navigator`)**:
     - *“技能清单” / “检查技能更新”*
   * 🛡️ **误删与数据安全防线 (`accidental-data-loss-prevention`)**:
     - *“拦截 DROP / Broad DELETE / rm -rf 等高危操作”*
   * 🐍 **Python 环境依赖隔离防污染 (`managing-python-dependencies`)**:
     - *“审计当前项目的虚拟环境与依赖健康度”*
   * 🔧 **技能异常修复引擎 (`skill-repair`)**:
     - *“诊断并修复安装失败的技能清单”*

3. **Handle One-Click Updates**:
   When the user asks to update a skill (e.g. "更新嘉立创技能" or "更新技能"):
   * **Linux (Bash)**:
     ```bash
     python ~/.gemini/config/skills/skills-navigator/scripts/check_skills_status.py update <dir_name>
     ```
   * **Windows (PowerShell)**:
     ```powershell
     python "$env:USERPROFILE\.gemini\config\skills\skills-navigator\scripts\check_skills_status.py" update <dir_name>
     ```

4. **Proactive Intent Inquiry**:
   Conclude by warmly asking what specific task the user wants to accomplish right now.
