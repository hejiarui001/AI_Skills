# AI Skills - Antigravity Agent Professional Skills Repository
# Antigravity 智能体专业技能全量矩阵仓库 (精炼提纯版)

> **远端同步仓库**：`https://github.com/hejiarui001/AI_Skills.git`  
> **多端部署路径**：
> - **Windows 11**：`C:\Users\hejia\.gemini\config\skills\`
> - **Linux (Ubuntu)**：`~/.gemini/config/skills/`
> **架构设计准则**：21 大高内聚全场景旗舰技能，涵盖嵌入式硬件全栈、系统运维、学术办公、云协同、大数据管道与治理元能力。

---

## 一、 经典三段式版本号演进规范 (Semantic Versioning Specification)

所有技能均严格遵循经典三段式语义化版本号（`MAJOR.MINOR.PATCH`），按改动产生的影响程度进行版本跃迁：

| 版本段位 | 影响程度 | 触发场景与演进准则 | 典型案例 |
| :---: | :---: | :--- | :--- |
| **`MAJOR`**<br>(主版本号) | **重大影响 / 破坏性变更** | • 发生破坏性变更（Breaking Changes），调用接口/指令重构；<br>• 底层架构重构、总线契约更新、多技能合并提纯；<br>• 核心状态机或数据拓扑推倒重置。 | • `bigquery-master`: `3.0.0` (五合一大套件)<br>• `gcs-storage-suite`: `3.0.0` (四合一存储中枢)<br>• `embedded-engineering-master`: `2.3.0` (UCA/PIA 双轨总控) |
| **`MINOR`**<br>(次版本号) | **中度影响 / 功能性新增** | • 新增向下兼容的功能特性（Feature Additions）；<br>• 扩展支持新芯片系列（ESP32 / RISC-V）、新协议（CAN / VOFA+）；<br>• 跨平台多操作系统适配升级（如同时兼容 Windows / Linux CLI）。 | • `cortex-m-pyocd`: `1.1.0` (双端可执行程序自适应)<br>• `industrial-serial-agent`: `1.1.0` (自适应 COM 与 ttyUSB)<br>• `invoice-audit-master`: `1.9.0` (11 列报销总账引擎) |
| **`PATCH`**<br>(修订号) | **轻微影响 / 补丁修复** | • 细节缺陷修复（Bug Fixes），不改变既有功能与调用接口；<br>• 勘误手册补丁（Errata Workaround）、时钟/波特率小参数调优；<br>• 规约文字润色、Prompt 提示词微调、注释修正。 | • `easyeda-api`: `1.1.64` (元器件库字段补丁)<br>• 各基础技能补丁修补 (`1.0.0` $\to$ `1.0.1`) |

---

## 二、 五大领域 21 大精炼技能矩阵清单

### 1. 嵌入式与硬件全栈工程 (Embedded & Hardware Suite - 5 项)
| 技能标识 | 当前版本 | 核心能力与架构定位 | 入口文档 |
| :--- | :---: | :--- | :--- |
| **`embedded-engineering-master`** | `2.3.0` | 端到端软硬件一体化开发、UCA/PIA 分层总线与全链路闭环协调总控中枢 | [SKILL.md](./embedded-engineering-master/SKILL.md) |
| **`embedded-stm32-rules`** | `1.10.0` | STM32 工业编码军规、PIA 四层架构、时间片调度器与 VOFA+ 联调规范 | [SKILL.md](./embedded-stm32-rules/SKILL.md) |
| **`easyeda-api`** | `1.1.64` | 嘉立创 EDA Pro (EasyEDA) 原理图/PCB/封装自动化与 WebSocket Bridge | [SKILL.md](./easyeda-api/SKILL.md) |
| **`cortex-m-pyocd`** | `1.1.0` | ARM Cortex-M 探针调试、pyOCD 固件烧录、整片擦除 (自适应 Win/Linux) | [SKILL.md](./cortex-m-pyocd/SKILL.md) |
| **`industrial-serial-agent`** | `1.1.0` | 工业级串口通信、帧协议解析与 VOFA+ 遥测监控通道 (自适应 COM/ttyUSB) | [SKILL.md](./industrial-serial-agent/SKILL.md) |

### 2. 系统管理与学术办公 (System, Academic & Utility Suite - 5 项)
| 技能标识 | 当前版本 | 核心能力与架构定位 | 入口文档 |
| :--- | :---: | :--- | :--- |
| **`invoice-audit-master`** | `1.9.0` | 高校/竞赛发票全生命周期智能审计、对账凑单与 11 列报销总账生成 | [SKILL.md](./invoice-audit-master/SKILL.md) |
| **`pc-maintenance-master`** | `2.0.0` | Sysinternals 内存优化、启动项体检、服务治理、硬件监控与磁盘深度清理 | [SKILL.md](./pc-maintenance-master/SKILL.md) |
| **`everything-search`** | `1.0.0` | voidtools Everything 本地全盘毫秒级极速检索与文件调阅 | [SKILL.md](./everything-search/SKILL.md) |
| **`zotero-assistant`** | `1.0.0` | Zotero 本地文献库只读检索、芯片 Datasheet 与学术元数据调阅 | [SKILL.md](./zotero-assistant/SKILL.md) |
| **`git-worklog-reporter`** | `1.0.0` | 本地 Git 提交提取与高管级研发日报/周报结构化撰写 | [SKILL.md](./git-worklog-reporter/SKILL.md) |

### 3. 云端协同与容灾网关 (Cloud Sync & Safety Gateway - 1 项)
| 技能标识 | 当前版本 | 核心能力与架构定位 | 入口文档 |
| :--- | :---: | :--- | :--- |
| **`google-sync-guard`** | `1.0.0` | 实时网络探针、断网熔断、离线写前日志（WAL）与唤醒重放网关 | [SKILL.md](./google-sync-guard/SKILL.md) |

### 4. 云原生大数据工程 (GCP Cloud & BigData Master Suite - 5 大提纯套件)
| 技能标识 | 当前版本 | 整合吸收的原技能 | 核心能力与架构定位 | 入口文档 |
| :--- | :---: | :--- | :--- | :--- |
| **`bigquery-master`** | `3.0.0` | `bigquery-sql`<br>`bigquery-ai-ml`<br>`bigquery-bigframes`<br>`bigquery-data-transfer-service`<br>`bigquery-graph` | **BigQuery 统一技术中枢**：高性能 SQL 调优、BigFrames Python 接口、属性图 GQL、数据传输 DTS 以及内置 GenAI/ML 模型全场景能力 | [SKILL.md](./bigquery-master/SKILL.md) |
| **`gcs-storage-suite`** | `3.0.0` | `google-cloud-storage-basics`<br>`google-cloud-storage-bucket-architect`<br>`google-cloud-storage-fuse`<br>`gcs-security-assessment` | **GCS 统一存储中枢**：存储桶架构设计 (Bucket Architect)、POSIX FUSE 高性能挂载、安全水位审计 (Security Assessment) 及生命周期治理 | [SKILL.md](./gcs-storage-suite/SKILL.md) |
| **`gcp-airflow-composer-suite`** | `3.0.0` | `gcp-managed-airflow-*`<br>`gcp-composer-troubleshooting`<br>`gcp-pipeline-*`<br>`gcp-data-pipelines` | **Composer / Airflow 调度总成**：现代 DAG 编写、环境弹性伸缩、跨版本迁移 (Airflow 2/3)、端到端排障 (RCA) 与声明式部署 (`deployment.yaml`) | [SKILL.md](./gcp-airflow-composer-suite/SKILL.md) |
| **`gcp-data-engineering`** | `3.0.0` | `dbt-bigquery`<br>`dataform-bigquery`<br>`gcp-dataflow`<br>`gcp-spark`<br>`data-autocleaning`<br>`federate-lakehouse-catalog`<br>`bigtable-basics` | **全栈数据管道工程**：dbt / Dataform 双轨 SQLX 建模、Apache Beam (Dataflow)、Dataproc Spark 流批计算、Data Clean 质检、Lakehouse 编目与 Bigtable | [SKILL.md](./gcp-data-engineering/SKILL.md) |
| **`gcp-governance-assets`** | `3.0.0` | `discovering-gcp-data-assets`<br>`google-cloud-auth-verification`<br>`enforcing-resource-attribution`<br>`schema-mapping`<br>`building-data-apps` | **GCP 治理与数据应用开发**：ADC 认证前置校验、资源标签强制注入、资产拓扑发现、Schema 映射与前端数据大屏 (React/Streamlit) 构建 | [SKILL.md](./gcp-governance-assets/SKILL.md) |

### 5. Agent 运行治理与元能力 (Governance & Meta-Skills Suite - 5 项)
| 技能标识 | 当前版本 | 整合吸收的原技能 | 核心能力与架构定位 | 入口文档 |
| :--- | :---: | :--- | :--- | :--- |
| **`notebook-data-science`** | `2.0.0` | `ml-best-practices`<br>`notebook-guidance` | **数据科学与交互式笔记本规范**：机器学习建模评估范式 (ML Best Practices) 与 Jupyter Notebook 交互式数据分析规约 | [SKILL.md](./notebook-data-science/SKILL.md) |
| **`skills-navigator`** | `1.4.0` | - | 技能总控台、快捷命令索引、21 大精炼技能健康度多维扫描与主动升级监测 | [SKILL.md](./skills-navigator/SKILL.md) |
| **`accidental-data-loss-prevention`**| `1.0.0` | - | 高危破坏性操作防御机制（DROP / RM / DELETE 强制拦截确认） | [SKILL.md](./accidental-data-loss-prevention/SKILL.md) |
| **`managing-python-dependencies`** | `1.0.0` | - | Python 环境依赖治理与虚拟环境防全局污染守则 | [SKILL.md](./managing-python-dependencies/SKILL.md) |
| **`skill-repair`** | `1.0.0` | - | Agent 技能安装依赖异常诊断与 manifest 自动修复引擎 | [SKILL.md](./skill-repair/SKILL.md) |

---

## 三、 多操作系统部署与日常同步指南

### 1. Linux (Ubuntu) 端部署与拉取
在 Linux 操作系统上，只需执行：
```bash
# 若尚未安装，直接克隆到配置目录
git clone https://github.com/hejiarui001/AI_Skills.git ~/.gemini/config/skills

# 若已存在，拉取最新技能更新
cd ~/.gemini/config/skills
git pull origin main
```

### 2. Windows 11 端推送与更新
在 Windows 操作系统上：
```powershell
cd "$env:USERPROFILE\.gemini\config\skills"
git pull origin main
# 技能修改或新增后：
git add .
git commit -m "feat: [技能名] 升级至 vX.Y.Z"
git push origin main
```

---

## 四、 持续演进与双端协同准则 (Skill Evolution & Dual-OS Sync Protocol)

在 Windows 11 与 Linux (Ubuntu) 双系统交叉开发场景下，遵循 **Fetch-Analyze-Merge-Push（云端检视 -> 增量分析 -> 本地融合 -> 提交推送）** 军规：
1. **更新前强制远端检视**：运行 `python Tools/sync_skills.py check`；
2. **远端增量先拉取后分析**：运行 `python Tools/sync_skills.py pull`；
3. **融合校验后再行提交上传**：运行 `python Tools/sync_skills.py push -m "feat: ..."`。
