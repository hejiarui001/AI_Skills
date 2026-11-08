---
name: gcp-airflow-composer-suite
version: 3.0.0
description: >-
  Cloud Composer & Apache Airflow Master Suite: DAG authoring (Airflow 2 & 3), environment
  performance tuning & autoscaling recommendations, cross-version migration, Root Cause Analysis (RCA)
  troubleshooting, declarative resource provisioning (deployment.yaml), and multi-pipeline orchestration.
  Trigger on: "Composer", "Airflow", "Cloud Composer", "Airflow DAG", "DAG authoring",
  "Airflow migration", "Composer RCA", "Composer troubleshooting", "orchestration-pipelines".
license: Apache-2.0
metadata:
  version: v3.0.0
  role: Master Suite
---

# Cloud Composer 与 Airflow 调度总成 (Composer & Airflow Suite) v3.0

整合原 `gcp-managed-airflow-*`（编写/迁移/调优）、`gcp-composer-troubleshooting`、`gcp-pipeline-*` 与 `gcp-data-pipelines` 等七大分散技能，构建统一的 Airflow/Composer 企业级编排方案。

---

## 1. 现代化 Airflow 2/3 DAG 编写规范 (DAG Authoring)
* **TaskFlow API 优先**：全面采用 `@dag` 与 `@task` 装饰器，替代过时的传统 Operator 拼装；
* **顶层性能军规**：
  * 严禁在 DAG 顶层代码执行数据库查询、API 请求或动态计算，防止 Airflow Scheduler 解析死锁与 CPU 飚高；
  * 任务传参使用 XCom Arg，避免超大对象在元数据库序列化。

---

## 2. Composer 环境弹性伸缩与健康基线 (Recommendations & Sizing)
* **资源画像**：合理划分 Web Server、Scheduler 与 Worker 节点的 CPU/内存比例；
* **工作负载自动扩缩容**：基于 CeleryExecutor / KubernetesExecutor 配置弹性范围，避免突发流水线任务积压；
* **心跳与连接池治理**：配置合理的 `sql_alchemy_pool_size` 与任务并发限制。

---

## 3. 故障根因分析与排障 (Troubleshooting & RCA)
* **常见死锁排查**：
  * Worker 发生 OOMKill 时排查单任务内存泄漏与分块数据读取；
  * Scheduler 僵死检测：核验 DAG 文件夹大小与第三方库依赖冲突；
* **执行日志聚合检索**：利用 Cloud Logging 联动过滤 `jsonPayload.message` 快速捕获任务失败堆栈。

---

## 4. 声明式管道基础设施编排 (Resource Provisioning)
* 通过标准声明式规范（`deployment.yaml`）统管 BigQuery 数据集、Cloud Storage 存储桶、Service Account 与 Composer 关联触发器的一键分发。
