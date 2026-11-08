---
name: bigquery-master
version: 3.0.0
description: >-
  BigQuery Master Suite: End-to-end BigQuery SQL optimization, Machine Learning (BQML),
  Generative AI functions, BigFrames DataFrames Python API, Property Graph (GQL) querying,
  and Data Transfer Service (DTS) ingestion.
  Trigger on: "BigQuery", "bqsql", "bigquery-sql", "BQML", "BigFrames", "GQL", "DTS",
  "BigQuery ML", "BigQuery transfer", "BigQuery graph", "BigQuery optimization".
license: Apache-2.0
metadata:
  version: v3.0.0
  role: Master Suite
---

# BigQuery 统一技术中枢 (BigQuery Master Suite) v3.0

整合原 `bigquery-sql`、`bigquery-ai-ml`、`bigquery-bigframes`、`bigquery-data-transfer-service` 与 `bigquery-graph` 五大技能，形成 BigQuery 平台级全栈技术中枢。

---

## 1. 高性能 SQL 查询调优与成本治理 (SQL Optimization)
* **避免全表扫描**：严禁无限制 `SELECT *`；对分区表（Partitioned）必须携带分区过滤条件（如 `_PARTITIONDATE >= ...`）；
* **聚簇利用 (Clustering)**：针对高频筛选与高基数关联列合理利用 Cluster 机制加速；
* **JOIN 优化与倾斜防范**：大表 JOIN 小表放右侧或采用 Broadcast；避免在 JOIN 关联键上使用非确定性函数；
* **物化视图与结果缓存**：合理配置 Materialized Views 加速聚合。

---

## 2. 内置机器学习与生成式 AI (BQML & GenAI)
BigQuery 原生集成了 ML 与 Gemini GenAI 扩展函数：
* **时序预测 (Forecasting)**：`CREATE MODEL ... OPTIONS(model_type='ARIMA_PLUS')` 或调用 `ML.FORECAST()`；
* **异常检测 (Anomaly Detection)**：使用 `ML.DETECT_ANOMALIES()`；
* **生成式文本与嵌入**：
  * `ML.GENERATE_TEXT()`：连接 Vertex AI 模型生成结构化回复；
  * `ML.GENERATE_EMBEDDING()`：多维向量生成，结合 `VECTOR_SEARCH()` 实现千万级向量检索；
* **智能分析函数**：`AI_SUMMARIZE()`, `AI_CLASSIFY()`, `AI_SCORE()` 等。

---

## 3. BigFrames (Pandas-style DataFrame over BigQuery)
* 针对 Python 数据科学与 Jupyter Notebook 场景，使用 `bigframes.pandas`：
```python
import bigframes.pandas as bpd
bpd.options.bigquery.project = "your-project-id"

df = bpd.read_gbq("your_project.dataset.table")
filtered = df[df["amount"] > 1000].groupby("category").sum()
```
* 计算全量下推至 BigQuery 执行引擎，免除海量数据拉取至客户端的 OOM 风险。

---

## 4. 属性图与语义图查询 (BigQuery Graph / GQL)
* 基于 SQL:2023 GQL 标准，在 BigQuery 中直接对属性图谱拓扑执行模式匹配：
```sql
SELECT *
FROM GRAPH_TABLE(my_graph
  MATCH (p:Person)-[:WORKS_AT]->(c:Company)
  WHERE c.name = 'Google'
  COLUMNS (p.name, p.role)
)
```

---

## 5. 数据传输服务自动化巡检 (Data Transfer Service - DTS)
* 通过 `scripts/bigquery_dts.py` 巡检与发现定时调度数据导入配置，支持从 GCS、S3、Redshift、YouTube 等权威源全自动抽取元数据。
