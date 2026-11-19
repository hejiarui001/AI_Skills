# 云原生大数据、数据流与治理实战教程 (GCP BigData Master Tutorial)

> **领域定位**：Google Cloud 企业级数据平台构建、BigQuery 高性能数仓、GCS 存储分层、Airflow/Composer 调度总成、dbt/Dataform 转换流水线与 Dataproc Serverless 计算  
> **联动技能群**：`bigquery-master`、`gcs-storage-suite`、`gcp-airflow-composer-suite`、`gcp-data-engineering`、`gcp-governance-assets`  
> **更新机制**：随云数仓建模、复杂 DAG 调试与大数据流水线调优持续演进

---

## 一、 云原生大数据端到端工程流水线

```text
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 1. 认证与凭据   │ ──> │ 2. 存储与摄取   │ ──> │ 3. 数据流转换   │
│governance-assets│     │gcs-storage/DTS  │     │data-engineering │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐                             ┌─────────────────┐
│ 5. 统一数仓&ML  │ <────────────────────────── │ 4. 调度编排总成 │
│ bigquery-master │                             │airflow-composer │
└─────────────────┘                             └─────────────────┘
```

---

## 二、 阶段实战指南与技能联动矩阵

### 1. GCP 环境基线与认证合规 (ADC)
* **核心目标**：保障 gcloud CLI、Python SDK 与 Terraform 在统一安全凭据下运行，注入强制性资源标签。
* **【联动技能】**：[`gcp-governance-assets`](../../gcp-governance-assets/SKILL.md)
  - *触发示例*：“校验当前 GCP ADC 认证与环境凭据合规性”、“为 BigQuery 数据集构建 Streamlit 数据大屏”。

### 2. GCS 企业级存储中枢与高性能挂载
* **核心目标**：设计符合安全基线（SAIF）的存储桶拓扑，调优 POSIX `gcsfuse` 挂载参数。
* **SOP 规范**：启用冷热分层生命周期规则（Standard -> Nearline -> Coldline），开启防误删软删除（Soft Delete）。
* **【联动技能】**：[`gcs-storage-suite`](../../gcs-storage-suite/SKILL.md)
  - *触发示例*：“设计生产合规的 GCS 存储桶分层与生命周期策略”、“配置并调优 gcsfuse 高性能挂载参数”。

### 3. 数据转换流水线：dbt 与 Dataform 双轨工程
* **核心目标**：使用 SQLX / dbt 实现数据仓库维度建模、增量表抽取与自动化数据质量清洗。
* **【联动技能】**：[`gcp-data-engineering`](../../gcp-data-engineering/SKILL.md)
  - *触发示例*：“用 dbt / Dataform 编写数仓建模与转换 SQLX”、“提交一个 Dataproc Serverless PySpark 流批处理作业”。

### 4. Cloud Composer 与 Airflow 调度总成
* **核心目标**：编写兼容 Airflow 2/3 的高可用弹性调度 DAG，执行端到端任务依赖编排与死锁排障。
* **【联动技能】**：[`gcp-airflow-composer-suite`](../../gcp-airflow-composer-suite/SKILL.md)
  - *触发示例*：“编写一个 Airflow 3 兼容的高可用调度 DAG”、“对 Composer 任务死锁和 Worker 重启进行 RCA 根本原因分析”。

### 5. BigQuery 统一数仓、优化与 BQML
* **核心目标**：优化 SQL 扫描字节与计算槽位（Slot）消耗，运用内置 ML 函数与 BigFrames 进行大规模分布式分析。
* **SOP 规范**：优先使用分区（Partitioning）与聚簇（Clustering），严禁全表扫描。
* **【联动技能】**：[`bigquery-master`](../../bigquery-master/SKILL.md)
  - *触发示例*：“优化这条 BigQuery SQL 查询性能并评估槽位消耗”、“使用 BigQuery 内置 ML 函数训练异常检测模型”。

---

## 三、 实战踩坑手记与经验增量池 (Hard-Won Knowledge)

1. **BigQuery 分区字段必须在 WHERE 首位**：未带分区过滤的查询会导致全量扫描，消耗巨额配额；
2. **gcsfuse 写入原子性陷阱**：GCS 是对象存储，多进程同时写入同一挂载文件可能导致覆盖丢失，必须配置临时中间文件；
3. **Composer 2/3 内存 OOM 防御**：PySpark 或大型 Pandas 任务严禁在 Airflow Worker 进程内部就地执行，必须通过 Dataproc Operator 或 Cloud Run 异步下沉。
