---
name: skills-navigator
version: 1.10.0
description: "技能库总控台：全量技能导航、上游更新、损坏修复与发布门禁校验。Trigger on: 指令, 技能, 技能清单, 检查更新, 更新技能, 修复技能, menu, help。"
license: Apache-2.0
metadata:
  version: v1.10.0
  author: Antigravity
---

# Skills Navigator & Update Monitor (技能导航与更新管家)

本技能为本地 AI 研发与运维技能库的总控中枢、健康审计、发布门禁校验、上游更新与损坏修复一体化管家。

---

## 1. 运行规约 (Operating Procedure)

当用户触发本技能时，执行以下标准化流程：

1. **检查技能健康与上游更新**：
   * **Linux (Bash)**: `python ~/.gemini/config/skills/skills-navigator/scripts/check_skills_status.py`
   * **Windows (PowerShell)**: `python "$env:USERPROFILE\.gemini\config\skills\skills-navigator\scripts\check_skills_status.py"`
   * 若 `updates_count > 0`，显式横幅提示更新：“*检测到上游官方更新：[技能名] 有 X 个新提交待同步。回复‘更新 [技能名]’即可一键同步。*”

2. **精炼领域技能清单 (Curated Cheatsheet · 24 项)**：

| 领域分类 | 核心技能 | 代表性触发意图 |
| :--- | :--- | :--- |
| **01. 嵌入式与硬件** | `embedded-engineering-master`, `embedded-stm32-rules`, `cortex-m-pyocd`, `industrial-serial-agent`, `easyeda-api` | 编写固件驱动、电路/BOM校验、pyOCD烧录、串口联调 |
| **02. 个人运维与学术** | `pc-maintenance-master`, `invoice-audit-master`, `git-worklog-reporter`, `zotero-assistant`, `everything-search`, `divergent-search-guide` | 电脑体检与冲突清理、竞赛发票对账总账、Git日报周报、文献检索、全盘秒搜、多维发散搜索 |
| **03. 路由与网络穿透** | `routeros-network-master`, `p2p-streaming-master`, `google-sync-guard` | 主路由运维巡检、EasyTier低延迟串流/P2P压测、192.168.8.x命脉自检、Google离线防断网 |
| **04. GCP 大数据** | `bigquery-master`, `gcs-storage-suite`, `gcp-airflow-composer-suite`, `gcp-data-engineering`, `gcp-governance-assets` | BigQuery优化/BQML、GCS存储设计、Airflow DAG、dbt/Dataform、ADC认证 |
| **05. 治理与元能力** | `session-checkpoint-advisor`, `notebook-data-science`, `skills-navigator`, `accidental-data-loss-prevention`, `managing-python-dependencies` | 会话零Token内省与断点续接、数据科学Notebook规范、技能更新与门禁校验、高危拦截、依赖隔离 |

3. **管理、门禁与修复指令**：
   * **发布终局机器门禁校验**：`python .../scripts/verify_release_gate.py`（强制验证脚本编译、行数<80、脏污清零及 Tag 一致性）
   * **一键更新/修复技能**：`python .../check_skills_status.py update <skill>` / `repair <skill>`

---

## 2. 深度参考手册

* 📘 **全量 24 技能自然语言 Prompt 实战矩阵**：查阅 [`references/prompt_matrix.md`](file:///C:/Users/hejia/.gemini/config/skills/skills-navigator/references/prompt_matrix.md)。
* 📘 **技能异常诊断与 Manifest 修复指南**：查阅 [`references/skill_repair_guide.md`](file:///C:/Users/hejia/.gemini/config/skills/skills-navigator/references/skill_repair_guide.md)。
