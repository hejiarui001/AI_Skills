---
name: skills-navigator
version: 1.6.0
description: >-
  Skills command center, update monitor, and quick navigation guide. Trigger when the
  user says "指令", "命令", "技能", "技能清单", "有哪些技能", "怎么用", "快捷指令", "检查更新",
  "更新技能", "menu", "help", or asks about newly added skills. Displays all active skills
  with clear example prompts, automatically checks for upstream skill updates, and
  proactively guides user workflow.
license: Apache-2.0
metadata:
  version: v1.6.0
  author: Antigravity
---

# Skills Navigator & Update Monitor (技能导航与更新管家)

本技能为本地 AI 研发与运维技能库的总控中枢、健康审计与上游更新监控器。

---

## 1. 运行规约 (Operating Procedure)

当用户触发本技能时，执行以下标准化流程：

1. **检查技能健康与上游更新**：
   * **Linux (Bash)**: `python ~/.gemini/config/skills/skills-navigator/scripts/check_skills_status.py`
   * **Windows (PowerShell)**: `python "$env:USERPROFILE\.gemini\config\skills\skills-navigator\scripts\check_skills_status.py"`
   * 若 `updates_count > 0`，显式横幅提示更新：“*检测到上游官方更新：[技能名] 有 X 个新提交待同步。回复‘更新 [技能名]’即可一键同步。*”

2. **精炼领域技能清单 (Curated Cheatsheet)**：

| 领域分类 | 核心技能 | 代表性触发意图 |
| :--- | :--- | :--- |
| **01. 嵌入式与硬件** | `embedded-engineering-master`, `embedded-stm32-rules`, `cortex-m-pyocd`, `industrial-serial-agent`, `easyeda-api` | 编写固件驱动、电路/BOM校验、pyOCD烧录、串口联调 |
| **02. 个人运维与学术** | `pc-maintenance-master`, `invoice-audit-master`, `git-worklog-reporter`, `zotero-assistant`, `everything-search` | 电脑体检清理、竞赛发票对账总账、Git日报周报、文献检索、全盘秒搜 |
| **03. 路由与网络穿透** | `routeros-network-master`, `p2p-streaming-master`, `google-sync-guard` | 主路由运维巡检、EasyTier低延迟串流/P2P压测、192.168.8.x命脉自检、Google离线防断网 |
| **04. GCP 大数据** | `bigquery-master`, `gcs-storage-suite`, `gcp-airflow-composer-suite`, `gcp-data-engineering`, `gcp-governance-assets` | BigQuery优化/BQML、GCS存储设计、Airflow DAG、dbt/Dataform、ADC认证 |
| **05. 治理与元能力** | `notebook-data-science`, `skills-navigator`, `accidental-data-loss-prevention` | 数据科学Notebook规范、技能更新管理、高危破坏拦截 |

3. **一键更新命令**：
   * 更新指定技能：`python .../check_skills_status.py update <skill_name>`

---

## 2. 深度参考手册

* 📘 **全量 21 技能自然语言 Prompt 实战矩阵**：查阅 [`references/prompt_matrix.md`](file:///C:/Users/hejia/.gemini/config/skills/skills-navigator/references/prompt_matrix.md)。
