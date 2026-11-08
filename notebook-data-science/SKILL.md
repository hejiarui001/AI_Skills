---
name: notebook-data-science
version: 2.0.0
description: >-
  Data Science & Interactive Notebook Suite: Enforces machine learning best practices
  (clustering, classification, regression, time-series forecasting, statistical tests, model comparison)
  and Jupyter Notebook structuring, execution hygiene, %%bqsql magics, and publication-ready visualization.
  Trigger on: "machine learning", "ML", "data analysis", "clustering", "classification",
  "regression", "time series", "Jupyter", "notebook", "ipynb", "%%bqsql", "data science".
license: Apache-2.0
metadata:
  version: v2.0.0
  role: Master Suite
---

# 数据科学与交互式笔记本规范 (Notebook & Data Science Suite) v2.0

整合原 `ml-best-practices` 与 `notebook-guidance`，提供从算法选型、数据科学探索到 Jupyter 单元格严谨执行的端到端范式。

---

## 1. 机器学习核心工程原则 (ML Best Practices)
* **数据泄漏防范**：必须在执行任何拟合（fit）或预处理前严格划分训练集、验证集与测试集；
* **特征工程闭环**：空值填充与标准化参数（mean/std）只从训练集计算并应用至验证集；
* **多模型基准对照**：严禁单模型盲目下结论，必须建立 Baseline（如简单规则或线性模型）对照组并输出标准混淆矩阵 / ROC-AUC / RMSE 指标。

---

## 2. Jupyter Notebook 交互式执行规约 (Execution Hygiene)
* **单元格单一职责**：一个 Cell 只做一件事（数据加载 / 预处理 / 绘图展示 / 模型训练）；
* **无状态幂等性**：严禁依赖乱序执行结果；确保从第一单元格到最后一单元格能够无缝一次性执行通过（Restart & Run All）；
* **BigQuery 原生魔术指令**：在交互式笔记本中优先采用 `%%bqsql` 语法直接调用云端计算，绘图前将精简聚合结果转为本地 Pandas。
