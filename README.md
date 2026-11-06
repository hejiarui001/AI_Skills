# AI Skills - Antigravity Agent Professional Skills Repository
# Antigravity 智能体专业技能全量矩阵仓库

> **远端同步仓库**：`https://github.com/hejiarui001/AI_Skills.git`  
> **多端部署路径**：
> - **Windows 11**：`C:\Users\hejia\.gemini\config\skills\`
> - **Linux (Ubuntu)**：`~/.gemini/config/skills/`

---

## 一、 仓库定位与架构原则

本仓库收录了 Antigravity AI Agent 的全部核心技能体系，采用单层物理目录结构以保障 Antigravity Language Server 的自动发现机制与渐进式披露（Progressive Disclosure），顶层通过五大专业领域分区矩阵进行治理与演进。

### 核心架构准则
1. **物理层解耦（Physical Stability）**：每个技能独立为一目录（`skills/<name>/SKILL.md`），包含规约、依赖与辅助脚本；
2. **逻辑层矩阵（Domain Partitioning）**：涵盖嵌入式硬件全栈、系统管理与学术办公、云协同与容灾、云原生数据工程、以及治理与元能力；
3. **跨平台双轨自适应（Cross-Platform OS Adaptation）**：核心 Python 脚本与 Shell/PowerShell 统一跨端兼容。

---

## 二、 五大领域技能矩阵清单

### 1. 嵌入式与硬件全栈工程 (Embedded & Hardware Suite)
| 技能名称 | 核心能力 | 入口文档 |
| :--- | :--- | :--- |
| **`embedded-engineering-master`** | 软硬件一体化开发、全链路闭环协调总控 | [SKILL.md](./embedded-engineering-master/SKILL.md) |
| **`embedded-stm32-rules`** | STM32 工业编码军规、PIA 四层架构规范 | [SKILL.md](./embedded-stm32-rules/SKILL.md) |
| **`cortex-m-pyocd`** | ARM Cortex-M 探针调试、pyOCD 固件烧录与擦除 | [SKILL.md](./cortex-m-pyocd/SKILL.md) |
| **`industrial-serial-agent`** | 工业级串口通信、帧协议与 VOFA+ 联调监控 | [SKILL.md](./industrial-serial-agent/SKILL.md) |
| **`easyeda-api`** | 嘉立创 EDA Pro (EasyEDA) 原理图/PCB/封装自动化交互 | [SKILL.md](./easyeda-api/SKILL.md) |

### 2. 系统管理与学术办公 (System, Academic & Utility Suite)
| 技能名称 | 核心能力 | 入口文档 |
| :--- | :--- | :--- |
| **`everything-search`** | voidtools Everything 本地全盘毫秒级极速检索 | [SKILL.md](./everything-search/SKILL.md) |
| **`pc-maintenance-master`** | Sysinternals 内存优化、启动项体检与磁盘清理 | [SKILL.md](./pc-maintenance-master/SKILL.md) |
| **`zotero-assistant`** | Zotero 本地文献库只读检索与 Datasheet 调阅 | [SKILL.md](./zotero-assistant/SKILL.md) |
| **`invoice-audit-master`** | 高校/竞赛发票智能审计、对账凑单与总账生成 | [SKILL.md](./invoice-audit-master/SKILL.md) |
| **`git-worklog-reporter`** | 本地 Git 提交提取与研发日报/周报结构化撰写 | [SKILL.md](./git-worklog-reporter/SKILL.md) |

### 3. 云端协同与容灾网关 (Cloud Sync & Safety Gateway)
| 技能名称 | 核心能力 | 入口文档 |
| :--- | :--- | :--- |
| **`google-sync-guard`** | 实时网络探针、断网熔断、离线写前日志（WAL）与唤醒重放 | [SKILL.md](./google-sync-guard/SKILL.md) |

### 4. 云原生与大数据管道 (GCP & BigData Cloud Suite)
| 技能名称 | 核心能力 | 入口文档 |
| :--- | :--- | :--- |
| **`bigquery-*`** | BigQuery SQL 调优、AI/ML、BigFrames、图数据库、DTS 传输 | [bigquery-sql](./bigquery-sql/SKILL.md) 等 |
| **`dataform-bigquery` / `dbt-bigquery`** | Dataform / dbt 数据转换管道编排与优化 | [dataform](./dataform-bigquery/SKILL.md) / [dbt](./dbt-bigquery/SKILL.md) |
| **`gcp-dataflow` / `gcp-spark`** | Apache Beam (Dataflow) 与 Dataproc Spark 流批处理 | [dataflow](./gcp-dataflow/SKILL.md) / [spark](./gcp-spark/SKILL.md) |
| **`gcp-pipeline-*` / `gcp-managed-airflow-*`** | Cloud Composer (Airflow) 编排、迁移与资源编排 | [composer](./gcp-composer-troubleshooting/SKILL.md) 等 |
| **`google-cloud-storage-*`** | GCS 基础运维、存储桶架构设计与 FUSE 挂载 | [gcs-basics](./google-cloud-storage-basics/SKILL.md) 等 |

### 5. Agent 运行治理与元能力 (Governance & Meta-Skills Suite)
| 技能名称 | 核心能力 | 入口文档 |
| :--- | :--- | :--- |
| **`skills-navigator`** | 技能总控台、快捷命令索引与主动升级监测 | [SKILL.md](./skills-navigator/SKILL.md) |
| **`accidental-data-loss-prevention`** | 高危破坏性操作拦截机制（DROP / RM / DELETE） | [SKILL.md](./accidental-data-loss-prevention/SKILL.md) |
| **`managing-python-dependencies`** | Python 环境依赖治理与虚拟环境防污染守则 | [SKILL.md](./managing-python-dependencies/SKILL.md) |
| **`ml-best-practices` / `notebook-guidance`** | 机器学习任务流与 Jupyter Notebook 规范 | [ml](./ml-best-practices/SKILL.md) / [notebook](./notebook-guidance/SKILL.md) |
| **`skill-repair`** | 技能依赖修复与清单修复引擎 | [SKILL.md](./skill-repair/SKILL.md) |

---

## 三、 多操作系统部署与日常同步指南

### 1. Linux (Ubuntu) 端部署与拉取
在 Linux 操作系统上，只需执行：
```bash
# 若尚未安装，直接克隆到配置目录
git clone https://github.com/hejiarui001/AI_Skills.git ~/.gemini/config/skills

# 若已存在，拉取最新技能更新
cd ~/.gemini/config/skills
git pull origin main
```

### 2. Windows 11 端推送与更新
在 Windows 操作系统上：
```powershell
cd "$env:USERPROFILE\.gemini\config\skills"
git pull origin main
# 技能修改或新增后：
git add .
git commit -m "feat: update/add new skills"
git push origin main
```

---

## 四、 持续演进与双端协同准则 (Skill Evolution & Dual-OS Sync Protocol)

在 Windows 11 与 Linux (Ubuntu) 双系统交叉开发场景下，遵循 **Fetch-Analyze-Merge-Push（云端检视 -> 增量分析 -> 本地融合 -> 提交推送）** 军规：

### 1. 更新前强制远端检视 (Pre-Update Remote Inspection)
在任何一次技能修改、新增或提交前，**必须首先探测云端仓库**：
```bash
# 检查云端是否有另一系统提交的新版本
python Tools/sync_skills.py check
```

### 2. 远端增量先拉取后分析 (Pull & Analyze)
若云端存在超前提交（Behind > 0）：
1. **自动拉取**：执行 `git pull origin main`；
2. **结构化梳理**：系统自动输出变更报告（变更涉及哪个具体技能、修改/新增了何种文件、另一端的提交信息）；
3. **经验与规约融合**：将远端已更新的代码逻辑或规约与本地当前需求进行综合分析，避免覆盖回退与逻辑冲突。

### 3. 融合校验后再行提交上传 (Synthesize then Push)
在确保本地与云端逻辑融为一体后，再执行最终推送：
```bash
python Tools/sync_skills.py push -m "feat: [技能名] 优化与多端融合"
```
工具会自动在推送前进行二次云端探活拦截，杜绝非快进（non-fast-forward）冲突。
