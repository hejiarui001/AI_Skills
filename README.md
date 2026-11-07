# AI Skills - Antigravity Agent Professional Skills Repository
# Antigravity 智能体专业技能全量矩阵仓库

> **远端同步仓库**：`https://github.com/hejiarui001/AI_Skills.git`  
> **多端部署路径**：
> - **Windows 11**：`C:\Users\hejia\.gemini\config\skills\`
> - **Linux (Ubuntu)**：`~/.gemini/config/skills/`

---

## 一、 经典三段式版本号演进规范 (Semantic Versioning Specification)

本仓库所有技能均统一遵循经典三段式语义化版本号（`MAJOR.MINOR.PATCH`，例如 `1.8.0`），**严格按改动产生的影响程度进行递增**：

| 版本段位 | 影响程度 | 触发场景与演进准则 | 典型案例 |
| :---: | :---: | :--- | :--- |
| **`MAJOR`**<br>(主版本号) | **重大影响 / 破坏性变更** | • 发生破坏性变更（Breaking Changes），不向前兼容既有调用范式；<br>• 架构重构、顶层抽象模型重组、总线契约更新；<br>• 核心状态机或数据帧拓扑推倒重构。 | • `embedded-engineering-master`: `2.0.0` (多层总线统揽)<br>• `dbt-bigquery`: `2.0.0` (建模引擎全面升级) |
| **`MINOR`**<br>(次版本号) | **中度影响 / 功能性新增** | • 新增功能特性（Features），且保持向前兼容；<br>• 扩展支持新单片机系列（如新增 ESP32 / RISC-V）、新芯片外设；<br>• 新增通信协议帧（如 CANopen / Modbus）、新上位机工具链对接；<br>• 引入新的运维排查工具或报销算法。 | • `embedded-stm32-rules`: `1.8.0` (引入 PIA 四层与 VOFA+)<br>• `invoice-audit-master`: `1.9.0` (引入高校 11 列报销总账引擎)<br>• `pc-maintenance-master`: `1.3.0` (引入 Sysinternals 全套工具) |
| **`PATCH`**<br>(修订号) | **轻微影响 / 补丁修复** | • 细节缺陷修复（Bug Fixes），不改变既有功能行为与接口；<br>• 勘误手册补丁（Errata Workaround）、时钟/波特率小参数调优；<br>• 规约文字润色、Prompt 提示词微调、示例代码与注释修正。 | • `easyeda-api`: `1.1.64` (立创 EDA API 映射及元器件库字段补丁)<br>• 各基础技能补丁修补 (`1.0.0` $\to$ `1.0.1`) |

---

## 二、 五大领域技能矩阵与版本全表

### 1. 嵌入式与硬件全栈工程 (Embedded & Hardware Suite)
| 技能标识 | 当前版本 | 核心能力与架构定位 | 入口文档 |
| :--- | :---: | :--- | :--- |
| **`embedded-engineering-master`** | `2.0.0` | 端到端软硬件一体化开发、分层总线与全链路闭环协调总控 | [SKILL.md](./embedded-engineering-master/SKILL.md) |
| **`embedded-stm32-rules`** | `1.8.0` | STM32 工业编码军规、PIA 四层架构与 VOFA+ 联调规范 | [SKILL.md](./embedded-stm32-rules/SKILL.md) |
| **`easyeda-api`** | `1.1.64` | 嘉立创 EDA Pro (EasyEDA) 原理图/PCB/封装自动化与 WebSocket Bridge | [SKILL.md](./easyeda-api/SKILL.md) |
| **`cortex-m-pyocd`** | `1.0.0` | ARM Cortex-M 探针调试、pyOCD 固件烧录、整片擦除与内存读取 | [SKILL.md](./cortex-m-pyocd/SKILL.md) |
| **`industrial-serial-agent`** | `1.0.0` | 工业级串口通信、帧协议解析与 VOFA+ 遥测监控通道 | [SKILL.md](./industrial-serial-agent/SKILL.md) |

### 2. 系统管理与学术办公 (System, Academic & Utility Suite)
| 技能标识 | 当前版本 | 核心能力与架构定位 | 入口文档 |
| :--- | :---: | :--- | :--- |
| **`invoice-audit-master`** | `1.9.0` | 高校/竞赛发票全生命周期智能审计、对账凑单与 11 列报销总账生成 | [SKILL.md](./invoice-audit-master/SKILL.md) |
| **`pc-maintenance-master`** | `2.0.0` | 全量工具箱架构治理、Sysinternals 内存优化、启动项体检与磁盘深度清理 | [SKILL.md](./pc-maintenance-master/SKILL.md) |
| **`skills-navigator`** | `1.3.0` | 技能总控台、快捷命令索引、版本健康度多维扫描与主动升级监测 | [SKILL.md](./skills-navigator/SKILL.md) |
| **`everything-search`** | `1.0.0` | voidtools Everything 本地全盘毫秒级极速检索与文件调阅 | [SKILL.md](./everything-search/SKILL.md) |
| **`zotero-assistant`** | `1.0.0` | Zotero 本地文献库只读检索、芯片 Datasheet 与学术元数据调阅 | [SKILL.md](./zotero-assistant/SKILL.md) |
| **`git-worklog-reporter`** | `1.0.0` | 本地 Git 提交提取与高管级研发日报/周报结构化撰写 | [SKILL.md](./git-worklog-reporter/SKILL.md) |

### 3. 云端协同与容灾网关 (Cloud Sync & Safety Gateway)
| 技能标识 | 当前版本 | 核心能力与架构定位 | 入口文档 |
| :--- | :---: | :--- | :--- |
| **`google-sync-guard`** | `1.0.0` | 实时网络探针、断网熔断、离线写前日志（WAL）与唤醒重放网关 | [SKILL.md](./google-sync-guard/SKILL.md) |

### 4. 云原生与大数据管道 (GCP & BigData Cloud Suite)
| 技能标识 | 当前版本 | 核心能力与架构定位 | 入口文档 |
| :--- | :---: | :--- | :--- |
| **`dbt-bigquery`** | `2.0.0` | dbt 数据转换管道编排、高级建模与 BigQuery SQL 优化 | [SKILL.md](./dbt-bigquery/SKILL.md) |
| **`bigquery-ai-ml`** | `1.0.0` | BigQuery 内置机器学习模型训练与生成式 AI 分析 | [SKILL.md](./bigquery-ai-ml/SKILL.md) |
| **`bigquery-bigframes`** | `1.0.0` | BigQuery DataFrames (BigFrames) Python 数据科学接口 | [SKILL.md](./bigquery-bigframes/SKILL.md) |
| **`bigquery-data-transfer-service`**| `1.0.0` | BigQuery 数据传输服务 (DTS) 管道发现与元数据巡检 | [SKILL.md](./bigquery-data-transfer-service/SKILL.md) |
| **`bigquery-graph`** | `1.0.0` | BigQuery 属性图与语义图 GQL 查询与建模定义 | [SKILL.md](./bigquery-graph/SKILL.md) |
| **`bigquery-sql`** | `1.0.0` | BigQuery 高性能 SQL 查询调优、成本缩减与执行最佳实践 | [SKILL.md](./bigquery-sql/SKILL.md) |
| **`bigtable-basics`** | `1.0.0` | Cloud Bigtable 行键设计、列族配置与低延迟存储治理 | [SKILL.md](./bigtable-basics/SKILL.md) |
| **`building-data-apps`** | `1.0.0` | 基于 React + Vite / Streamlit 构建 GCP 现代数据可视化交互应用 | [SKILL.md](./building-data-apps/SKILL.md) |
| **`data-autocleaning`** | `1.0.0` | Dataform / dbt / BigQuery 自动化数据清洗与质量断言管道 | [SKILL.md](./data-autocleaning/SKILL.md) |
| **`dataform-bigquery`** | `1.0.0` | Dataform SQLX 数据管道代码生成与依赖拓扑管理 | [SKILL.md](./dataform-bigquery/SKILL.md) |
| **`discovering-gcp-data-assets`** | `1.0.0` | Google Cloud 数据资产自动发现与元数据深度剖析 | [SKILL.md](./discovering-gcp-data-assets/SKILL.md) |
| **`enforcing-resource-attribution`**| `1.0.0` | CLI 运维命令资源归属与配额标签强制合规注入 | [SKILL.md](./enforcing-resource-attribution/SKILL.md) |
| **`federate-lakehouse-catalog`** | `1.0.0` | GCP 湖仓一体联合编目 (Unity / AWS Glue Iceberg) 架构连接 | [SKILL.md](./federate-lakehouse-catalog/SKILL.md) |
| **`gcp-composer-troubleshooting`**| `1.0.0` | Cloud Composer (Airflow) 故障根因分析 (RCA) 与排障修复 | [SKILL.md](./gcp-composer-troubleshooting/SKILL.md) |
| **`gcp-data-pipelines`** | `1.0.0` | GCP 全栈数据管道编排决策与技术栈路由中枢 | [SKILL.md](./gcp-data-pipelines/SKILL.md) |
| **`gcp-dataflow`** | `1.0.0` | Apache Beam 流批一体任务开发与 Dataflow Flex 模板构建 | [SKILL.md](./gcp-dataflow/SKILL.md) |
| **`gcp-managed-airflow-dag-authoring`** | `1.0.0` | Airflow 2/3 现代化 DAG 代码编写、依赖组织与本地校验 | [SKILL.md](./gcp-managed-airflow-dag-authoring/SKILL.md) |
| **`gcp-managed-airflow-migrations`** | `1.0.0` | Cloud Composer Airflow 跨版本平滑迁移与语法升级 | [SKILL.md](./gcp-managed-airflow-migrations/SKILL.md) |
| **`gcp-managed-airflow-recommendations`** | `1.0.0` | Composer 环境性能调优、资源弹性伸缩与健康基线推荐 | [SKILL.md](./gcp-managed-airflow-recommendations/SKILL.md) |
| **`gcp-pipeline-orchestration`** | `1.0.0` | 异构数据管道 (Spark, dbt, Notebook) 统合调度与部署 | [SKILL.md](./gcp-pipeline-orchestration/SKILL.md) |
| **`gcp-pipeline-resource-provisioning`** | `1.0.0` | 声明式数据管道基础设施编排 (deployment.yaml 驱动) | [SKILL.md](./gcp-pipeline-resource-provisioning/SKILL.md) |
| **`gcp-spark`** | `1.0.0` | Dataproc Serverless PySpark 批处理任务研发与异常诊断 | [SKILL.md](./gcp-spark/SKILL.md) |
| **`gcs-security-assessment`** | `1.0.0` | Google Cloud Storage 存储桶安全水位评估与合规审计 | [SKILL.md](./gcs-security-assessment/SKILL.md) |
| **`google-cloud-auth-verification`** | `1.0.0` | GCP ADC 认证链 0 号前置步骤合规探针 | [SKILL.md](./google-cloud-auth-verification/SKILL.md) |
| **`google-cloud-storage-basics`** | `1.0.0` | GCS 对象全生命周期管理、传输策略与访问控制治理 | [SKILL.md](./google-cloud-storage-basics/SKILL.md) |
| **`google-cloud-storage-bucket-architect`** | `1.0.0` | 安全优先、成本最优的 GCS 存储桶架构专家设计规范 | [SKILL.md](./google-cloud-storage-bucket-architect/SKILL.md) |
| **`google-cloud-storage-fuse`** | `1.0.0` | GCS FUSE POSIX 挂载调优与机器学习 Checkpoint 缓存加速 | [SKILL.md](./google-cloud-storage-fuse/SKILL.md) |
| **`schema-mapping`** | `1.0.0` | 异构数据源 Schema 字段映射规划 (Mapping Manifesto) | [SKILL.md](./schema-mapping/SKILL.md) |

### 5. Agent 运行治理与元能力 (Governance & Meta-Skills Suite)
| 技能标识 | 当前版本 | 核心能力与架构定位 | 入口文档 |
| :--- | :---: | :--- | :--- |
| **`accidental-data-loss-prevention`** | `1.0.0` | 高危破坏性操作防御机制（DROP / RM / DELETE 强制拦截确认） | [SKILL.md](./accidental-data-loss-prevention/SKILL.md) |
| **`managing-python-dependencies`** | `1.0.0` | Python 环境依赖治理与虚拟环境防全局污染守则 | [SKILL.md](./managing-python-dependencies/SKILL.md) |
| **`ml-best-practices`** | `1.0.0` | 机器学习任务流、模型评估与数据科学标准范式 | [SKILL.md](./ml-best-practices/SKILL.md) |
| **`notebook-guidance`** | `1.0.0` | Jupyter Notebook 交互式数据分析与 %%bqsql 规范 | [SKILL.md](./notebook-guidance/SKILL.md) |
| **`skill-repair`** | `1.0.0` | Agent 技能安装依赖异常诊断与 manifest 自动修复引擎 | [SKILL.md](./skill-repair/SKILL.md) |

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

### 1. 更新前强制远端检视 (Pre-Update Remote Inspection)
在任何一次技能修改、新增或提交前，**必须首先探测云端仓库**：
```bash
# 检查云端是否有另一系统提交的新版本
python Tools/sync_skills.py check
```

### 2. 远端增量先拉取后分析 (Pull & Analyze)
若云端存在超前提交（Behind > 0）：
1. **自动拉取**：执行 `git pull origin main`；
2. **结构化梳理**：系统自动输出变更报告（变更涉及哪个具体技能、修改/新增了何种文件、另一端的提交信息）；
3. **经验与规约融合**：将远端已更新的代码逻辑或规约与本地当前需求进行综合分析，避免覆盖回退与逻辑冲突。

### 3. 融合校验后再行提交上传 (Synthesize then Push)
在确保本地与云端逻辑融为一体并根据变动影响更新三段式版本号后，再执行最终推送：
```bash
python Tools/sync_skills.py push -m "feat: [技能名] 升级至 vX.Y.Z 说明"
```
工具会自动在推送前进行二次云端探活拦截，杜绝非快进（non-fast-forward）冲突。
