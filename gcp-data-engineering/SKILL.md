---
name: gcp-data-engineering
version: 3.0.0
description: >-
  GCP Data Engineering Pipeline Suite: Declarative data transformations with dbt & Dataform SQLX,
  stream/batch pipeline processing with Apache Beam (Dataflow), Dataproc Serverless PySpark,
  automated data cleaning (Dataplex), Cloud Bigtable row key schema design, and Lakehouse federated catalogs (Databricks/AWS Glue).
  Trigger on: "dbt", "Dataform", "SQLX", "Dataflow", "Apache Beam", "Dataproc", "Spark",
  "PySpark", "data cleaning", "Bigtable", "Lakehouse", "Iceberg catalog", "data pipeline".
license: Apache-2.0
metadata:
  version: v3.0.0
  role: Master Suite
---

# GCP 全栈数据管道工程总成 (GCP Data Engineering Suite) v3.0

整合 `dbt-bigquery`、`dataform-bigquery`、`gcp-dataflow`、`gcp-spark`、`data-autocleaning`、`federate-lakehouse-catalog` 与 `bigtable-basics` 七大技能，形成统一的现代云原生数据流批处理工程套件。

---

## 1. 声明式数据建模与转换 (dbt & Dataform SQLX)
* **dbt on BigQuery**：精通 staging -> intermediate -> marts 多层分层建模，利用增量表（`incremental`）策略与表分区合并；
* **Dataform (GCP 原生)**：编写标准化 SQLX 断言（`assertions`）与依赖声明（`ref()`, `resolve()`），与 Cloud Build 无缝集成。

---

## 2. 流批一体计算引擎 (Apache Beam on Dataflow)
* **流水线模式**：基于 Python/Java 构建高吞吐流式与批处理管道，处理晚到数据（Watermarks, Allowed Lateness）；
* **Flex 模板与云构建**：标准化打包 Flex Template，通过 Cloud Build 自动化镜像构建与部署；
* **自动扩缩容调优**：排查数据热点（Hotspotting）与 Shuffle 瓶颈。

---

## 3. Serverless 大规模分布式计算 (Dataproc Serverless Spark)
* **PySpark 批处理**：免运维集群直接提交批处理任务，集成 BigQuery Connector 与 Iceberg Catalog；
* **诊断与调优**：通过 Spark UI 监控 Stage 耗时、GC 暂停与倾斜分区。

---

## 4. 湖仓一体联合编目 (Lakehouse Federated Catalog)
* 连接远程 Apache Iceberg REST Catalog（Databricks Unity Catalog / AWS Glue）；
* 在 BigQuery 中无缝跨云联合检索外部数据，无需物理数据搬迁。

---

## 5. 高吞吐实时 NoSQL (Cloud Bigtable)
* **Row Key 黄金法则**：严禁单调递增前缀（防热点写入）；推荐字段散列（Hash/Salting）、倒排时间戳（`MAX_INT - timestamp`）；
* **列族治理**：按更新频率和生存期（GC Policy）严密划分列族。
