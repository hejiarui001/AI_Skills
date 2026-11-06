# Antigravity Skills Architecture & Domain Partitioning
# 技能库顶层架构设计与领域分区规范

> **架构设计准则**：
> 1. **物理层解耦（Physical Stability）**：底层技能维持单层目录物理结构（`skills/<name>/SKILL.md`），保证 Antigravity 官方 Language Server 发现机制与渐进式披露（Progressive Disclosure）100% 稳定可靠；
> 2. **逻辑层矩阵（Domain Partitioning）**：顶层通过五大专业领域分区矩阵（位于 `~/.gemini/config/domains/`）实施归类治理，彻底告别扁平无序；
> 3. **无损演进（Zero-Breaking Evolution）**：升级、更新与增量扩展遵循开放封闭原则。

---

## 一、 五大专业领域分区矩阵 (Domain Partition Matrix)

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

### 分区 04：云原生、大数据与数据管道 (GCP & BigData Cloud Suite)
* **定位**：Google Cloud 官方数据工程生态（分析、数仓、流批一体与存储架构）。
* **涵盖技能**：
  * BigQuery 系列：`bigquery-ai-ml`, `bigquery-bigframes`, `bigquery-data-transfer-service`, `bigquery-graph`, `bigquery-sql`
  * 管道与调度：`dbt-bigquery`, `dataform-bigquery`, `gcp-data-pipelines`, `gcp-dataflow`, `gcp-spark`, `gcp-pipeline-orchestration`, `gcp-managed-airflow-*`
  * 存储与安全：`google-cloud-storage-basics`, `google-cloud-storage-bucket-architect`, `google-cloud-storage-fuse`, `gcs-security-assessment`

---

### 分区 05：Agent 运行治理与元能力 (Governance & Meta-Skills Suite)
* **定位**：Agent 自主运行保护屏障、Python 依赖防污染、数据安全与技能导航。
* **涵盖技能**：
  * [`skills-navigator`](./skills-navigator/SKILL.md)：技能中枢控制台、更新检测与智能路线指引；
  * [`accidental-data-loss-prevention`](./accidental-data-loss-prevention/SKILL.md)：高危销毁指令拦截（DROP/RM/DELETE）；
  * [`managing-python-dependencies`](./managing-python-dependencies/SKILL.md)：全局环境防污染与虚拟环境守则；
  * [`ml-best-practices`](./ml-best-practices/SKILL.md) & [`notebook-guidance`](./notebook-guidance/SKILL.md)：数据科学与交互式笔记本规范；
  * [`skill-repair`](./skill-repair/SKILL.md)：技能安装异常诊断与修复。
