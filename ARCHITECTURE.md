# Antigravity Skills Architecture & Domain Partitioning
# 技能库顶层架构设计与领域分区规范

> **架构设计准则**：
> 1. **物理层解耦（Physical Stability）**：底层技能维持单层目录物理结构（`skills/<name>/SKILL.md`），保证 Antigravity 官方 Language Server 发现机制与渐进式披露（Progressive Disclosure）100% 稳定可靠；
> 2. **逻辑层矩阵（Domain Partitioning）**：顶层通过五大专业领域分区矩阵（位于 `~/.gemini/config/domains/`）实施归类治理，彻底告别扁平无序；
> 3. **无损演进（Zero-Breaking Evolution）**：升级、更新与增量扩展遵循开放封闭原则。

---

## 二、 经典三段式版本号演进规范 (Semantic Versioning Specification)

所有技能均严格在 `SKILL.md` 的 YAML frontmatter 中显式声明 `version: MAJOR.MINOR.PATCH`，并根据实际变更的影响程度进行版本递增：

1. **`MAJOR` (主版本号 - 影响程度: 重大 / 破坏性变更)**：
   * **触发场景**：发生破坏性变更（Breaking Changes），既有 Prompt/指令无法向下兼容；核心架构模型重构；物理/逻辑总线契约变更；
   * **示例**：`embedded-engineering-master`: `2.0.0`，`dbt-bigquery`: `2.0.0`。

2. **`MINOR` (次版本号 - 影响程度: 中度 / 功能性新增)**：
   * **触发场景**：新增功能特性且向前兼容；新增单片机系列/驱动协议；新增排查算法/自动化脚本；
   * **示例**：`embedded-stm32-rules`: `1.8.0`，`invoice-audit-master`: `1.9.0`，`pc-maintenance-master`: `1.3.0`，`skills-navigator`: `1.2.0`。

3. **`PATCH` (修订补丁号 - 影响程度: 轻微 / 补丁修复)**：
   * **触发场景**：细节 Bug 修复、勘误手册补丁（Errata Workaround）、参数微调、文档/注释优化；
   * **示例**：`easyeda-api`: `1.1.64`，各基础模块修复 (`1.0.0` -> `1.0.1`)。

### 分区 01：嵌入式与硬件全栈工程 (Embedded & Hardware Suite)
* **定位**：软硬件一体化开发、EDA 原理图校验、底层 C/C++ 规范、编译烧录与遥测联调。
* **涵盖技能**：
  * [`embedded-engineering-master`](./embedded-engineering-master/SKILL.md)：端到端软硬件闭环总指挥官；
  * [`embedded-stm32-rules`](./embedded-stm32-rules/SKILL.md)：STM32 工业编码与 PIA 四层分层架构；
  * [`cortex-m-pyocd`](./cortex-m-pyocd/SKILL.md)：ARM Cortex-M 硬件调试与 pyOCD 固件烧录；
  * [`industrial-serial-agent`](./industrial-serial-agent/SKILL.md)：工业级串口与 VOFA+ 调试协议通道；
  * [`easyeda-api`](./easyeda-api/SKILL.md)：立创 EDA Pro 原理图、PCB 与封装自动化协同。

---

### 分区 02：系统管理与学术办公 (System, Academic & Utility Suite)
* **定位**：Windows 系统性能运维、本地知识库与文献调阅、报销审计与工作汇报。
* **涵盖技能**：
  * [`everything-search`](./everything-search/SKILL.md)：基于 voidtools Everything 的本地全盘秒级检索；
  * [`pc-maintenance-master`](./pc-maintenance-master/SKILL.md)：Sysinternals 内存优化、启动项与磁盘治理；
  * [`zotero-assistant`](./zotero-assistant/SKILL.md)：本地 Zotero 论文文献与芯片 Datasheet 快速索引；
  * [`invoice-audit-master`](./invoice-audit-master/SKILL.md)：高校与竞赛发票智能审计、对账与凑单生成总账；
  * [`git-worklog-reporter`](./git-worklog-reporter/SKILL.md)：本地 Git 提交提取与高管级研发日报/周报提炼。

---

### 分区 03：云端协同与容灾网关 (Cloud Sync & Safety Gateway)
* **定位**：与 Google Workspace 等云服务的安全通道、写前缓冲、断网熔断与恢复补偿。
* **涵盖技能**：
  * [`google-sync-guard`](./google-sync-guard/SKILL.md)：实时代理探活、离线写入暂存（WAL）、异常全关熔断与唤醒重放。

---

### 分区 04：云原生大数据工程 (GCP Cloud & BigData Master Suite - 5 大提纯套件)
* **定位**：Google Cloud 官方数据工程全栈生态（分析、数仓、流批一体、存储架构、声明式调度与元数据治理）。
* **涵盖技能**：
  * [`bigquery-master`](./bigquery-master/SKILL.md)：BigQuery 统一技术中枢（SQL 调优、BigFrames、属性图 GQL、数据传输 DTS、内置 GenAI/ML）；
  * [`gcs-storage-suite`](./gcs-storage-suite/SKILL.md)：GCS 统一存储中枢（架构设计 Bucket Architect、POSIX FUSE 高性能挂载、安全水位审计 Security Assessment）；
  * [`gcp-airflow-composer-suite`](./gcp-airflow-composer-suite/SKILL.md)：Composer / Airflow 调度总成（现代 DAG 编写、弹性伸缩、Airflow 2/3 迁移、端到端 RCA 排障与声明式部署）；
  * [`gcp-data-engineering`](./gcp-data-engineering/SKILL.md)：全栈数据管道工程（dbt / Dataform 双轨 SQLX 建模、Beam Dataflow、Dataproc Spark 流批一体、Data Clean 质检、Lakehouse 与 Bigtable）；
  * [`gcp-governance-assets`](./gcp-governance-assets/SKILL.md)：GCP 治理与数据应用开发（ADC 认证前置校验、资源标签强制注入、资产拓扑发现、Schema 映射与前端数据大屏）。

---

### 分区 05：Agent 运行治理与元能力 (Governance & Meta-Skills Suite - 5 项)
* **定位**：Agent 自主运行保护屏障、Python 依赖防污染、数据安全、科学建模规范与技能导航。
* **涵盖技能**：
  * [`notebook-data-science`](./notebook-data-science/SKILL.md)：数据科学与交互式笔记本规范（机器学习建模评估与 Jupyter Notebook 交互式规约）；
  * [`skills-navigator`](./skills-navigator/SKILL.md)：技能总控台、快捷命令索引、21 大精炼技能健康度多维扫描与主动升级监测；
  * [`accidental-data-loss-prevention`](./accidental-data-loss-prevention/SKILL.md)：高危破坏性操作防御机制（DROP / RM / DELETE 强制拦截确认）；
  * [`managing-python-dependencies`](./managing-python-dependencies/SKILL.md)：Python 环境依赖治理与虚拟环境防全局污染守则；
  * [`skill-repair`](./skill-repair/SKILL.md)：Agent 技能安装依赖异常诊断与 manifest 自动修复引擎。
