---
name: gcp-governance-assets
version: 3.0.0
description: "GCP 治理与数据应用套件：ADC 认证校验、资产拓扑发现、资源标签归因、Schema 映射与 Streamlit/React 数据大屏。Trigger on: GCP auth, discover data assets, data dashboard。"
license: Apache-2.0
metadata:
  version: v3.0.0
  role: Master Suite
---

# GCP 治理、资产发现与应用大屏 (Governance, Discovery & Data Apps) v3.0

整合 `discovering-gcp-data-assets`、`google-cloud-auth-verification`、`enforcing-resource-attribution`、`schema-mapping` 与 `building-data-apps` 五大技能。

---

## 1. 认证链前置探针 (ADC Step 0 Pre-flight)
在执行任何 `gcloud`、`bq` 或 GCP SDK 脚本前，必须首先确认凭据链完整性（`gcloud auth print-access-token` 或 `GOOGLE_APPLICATION_CREDENTIALS` 环境变量）。

## 2. 数据资产拓扑发现 (Asset Discovery)
使用 Dataplex 与 BigQuery Information Schema 检索与探测数据集、表、视图、字段类型与敏感数据标签，替代低效的盲猜扫描。

## 3. 命令行资源归属与合规标签 (Resource Attribution)
运行 `bq query` 或基础设施变更时，强制注入项目代码与成本中心标签（Labeling），杜绝无归属高额计费。

## 4. 异构 Schema 映射规划 (Schema Mapping Manifesto)
在复杂迁移项目中，产出高保真映射清单（包含字段类型映射、空值策略、重命名映射、业务约束转换规则）。

## 5. 交互式数据大屏与前端应用 (Modern Data Apps)
基于 React + Vite 或 Python Streamlit 快速拉起连接 GCP 数据源的交互式看板，支持嵌入 Gemini Data Analytics 达成自然语言“与数据对话”。
