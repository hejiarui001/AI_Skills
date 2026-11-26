# AI Skills Changelog & Version Archive

> **仓库地址**：`https://github.com/hejiarui001/AI_Skills`  
> **Releases 页面**：`https://github.com/hejiarui001/AI_Skills/releases`  
> **设计原则**：正文 `SKILL.md` 保持最小 Token 负荷；历史原版全文与阶段快照通过 **Git Tags + GitHub Releases + 本台账** 永久封存，按需毫秒级调阅、零日常上下文开销。

---

## [v3.0.0] - 2026-11-26 (底层致错根因重构 · 零 Token 会话内省 + 机器发布门禁 + 跨端冲突扫雷)

**Tag**: `v3.0.0` | **重大重构与升级**: `session-checkpoint-advisor` (`v1.2.0`), `skills-navigator` (`v1.10.0`), `pc-maintenance-master` (`v2.3.0`)

<details open>
<summary>🌟 防错机制架构级重塑 (Systemic Anti-Error Architecture v3.0.0)</summary>

基于对 94 场生产历史会话（1151 步小主机、47 轮代理调试、15,878 冲突文件雪崩）中 AI 致错底层根因的系统剖析，建立**确定性机器校验取代人工记忆自觉**的四大演进体系：

* **`session-checkpoint-advisor` 升级至 v1.2.0**：
  - **本地 0 Token 自我内省引擎**：`analyze_checkpoint.py` 原生直接读取最新 `transcript.jsonl`，精准输出每轮提问 `[HH:MM]` 视觉锚点指纹、负载 Token 估算与“连续空转重复区间”高亮；
  - **二轮不过即熔断守则**：同一故障连续 2 轮未收敛严禁继续猜测性补丁，强制切回拐点或取证穿透；
  - **网络悬空态防锁死门禁**：回退前自动探活本地 `7897` 代理端口，杜绝切代理掉线后带着半截故障网络回退；
  - **零延迟极简接力**：Prompt 携带带状态签名的 **确定性免探核准印章 (Pre-Verified Stamp)**（新会话跳过重复 `git status`）、**单一权威 SSOT 指针**与**脱敏外部私密凭据指针**。
* **`skills-navigator` 升级至 v1.10.0（发布终局机器门禁）**：
  - 新增 [`scripts/verify_release_gate.py`](./skills-navigator/scripts/verify_release_gate.py)：全自动核验所有技能三段式版本、`SKILL.md` <80 行门禁、全量 Python 脚本 `py_compile` 静态编译、脏污文件清零及 `CHANGELOG` 与本地 Git Tag 一致性（根除漏打 Tag）。
* **`pc-maintenance-master` 升级至 v2.3.0（跨端同步冲突防雪崩）**：
  - 新增 [`scripts/sync_conflict_audit.py`](./pc-maintenance-master/scripts/sync_conflict_audit.py)：递归扫雷并一键无损清理跨系统 (NTFS/POSIX) 同步产生的 `.sync-conflict-*` 副本、`.syncthing.*.tmp`、Git `index.lock` 及 `__pycache__`，并固化 Syncthing `ignorePerms="true"` / `<maxConflicts>0</maxConflicts>` 防线。

</details>

---

## [v2.9.0] - 2026-11-24 (RouterOS 运维技能新增二层硬件卸载、Bridge Horizon 端口隔离与规则有效性断言规约)

**Tag**: `v2.9.0` | **功能演进**: `routeros-network-master` (`v1.3.0`)

<details open>
<summary>🌟 二层网桥硬件卸载与端口隔离规约 (Bridge Horizon & Zero Invalid Policy)</summary>

* **`routeros-network-master` 升级至 v1.3.0**：
  - **二层硬件端口隔离铁律**：严禁在网桥从属物理端口之间使用三层 IP Filter 进行隔离（会被交换芯片 Hardware Offload 绕过且触发 ROS v7 invalid 报错）；强制使用二层 `Bridge Port Horizon` (`horizon=10`) 借助交换芯片 ASIC 线速丢弃，实现 0% CPU 损耗的硬件级强隔离；
  - **从属物理口匹配语义修复**：在 IP Firewall 中严禁直接指定物理从属口作为 `in-interface`，强制统一修正为采用主网桥 (`bridge-lan`) 结合源/目的 IP 地址（`src-address`）进行精确放行；
  - **自动化巡检断言门禁**：巡检引擎必须嵌入 `invalid == true` 拦截与关键规则零命中（`packets == 0`）审计门禁，杜绝“配置存在即生效”的假阳性误判；
  - **新增 SOP 与避坑手册**：
    - 在 `references/routeros_ops_sop.md` 中新增 `SOP-08: 网桥从属端口二层 Horizon 隔离与规则失效审计`；
    - 新增核心参考手册：[`references/hardware_offload_vs_firewall_pitfalls.md`](./routeros-network-master/references/hardware_offload_vs_firewall_pitfalls.md)。

</details>

---

## [v2.8.0] - 2026-11-23 (RouterOS 运维技能固化最小权限控制 PoLP 与 agent-operator IAM 策略)

**Tag**: `v2.8.0` | **功能演进**: `routeros-network-master` (`v1.2.0`)

<details open>
<summary>🌟 工业级最小权限控制与 IAM 策略红线 (PoLP & IAM Hardening)</summary>

* **`routeros-network-master` 升级至 v1.2.0**：
  - **严禁过度授权红线**：禁止在运维、排障中向用户索要或提议 `full` 组等全量特权；
  - **固化受限运维组 `agent-operator`**：
    - **白名单 (Whitelist)**：`ssh,read,write,test,sensitive,api,rest-api`（满足状态采集、`/export` 配置脚本导出与基础安全操作）；
    - **黑名单 (Blacklist)**：`!local,!telnet,!ftp,!reboot,!policy,!winbox,!password,!web,!sniff,!romon`（严格封死破坏性接口与特权逃逸）；
  - **备份权限边界规范化**：
    - 针对 `/system/backup/save` 涉及系统全量凭据哈希（需 `password`/`policy`）导致的权限限制，明确禁止通过赋予 `full` 组绕过；
    - 确立 `/export file=...` 纯文本配置导出为自动化灾备的标准途径，二进制 `.backup` 留交系统管理员手动或本地定时任务执行；
  - **新增 SOP 手册**：在 `references/routeros_ops_sop.md` 中新增 `SOP-07: 工业级最小权限控制 (PoLP) 与自动化运维账号 IAM 固化`。

</details>

---

## [v2.7.0] - 2026-11-22 (会话断点顾问注入 52 场真实长会话实战经验)

**Tag**: `v2.7.0` | **功能演进**: `session-checkpoint-advisor` (`v1.1.0`)

<details open>
<summary>🌟 生产经验提炼与深度进化 (Ground-Truth Evolution & Pitfall Defenses)</summary>

* **`session-checkpoint-advisor` 升级至 v1.1.0**：
  - **注入 52 场真实会长会话实战经验**：深度挖掘 1151 步小主机开发、678 步网络装机、329 步边缘 VPS 等跨天长工程中的多次真实回退交互；
  - **破解四大实战暗坑**：
    1. **物理隔离定心丸**：首句声明 IDE 会话回退仅影响上下文记忆，磁盘代码、远端 Docker 容器与单片机固件 100% 稳定常驻；
    2. **IDE 后台子进程强杀预警**：提前审计会话拉起的常驻 background tasks，防止回退导致后台服务意外被杀，提前准备自启/重启指令；
    3. **界面视觉原文指纹定位**：强制输出用户当时提问的“原话特征片段 + 时间戳”，让用户 2 秒内在千行聊天流中找到弯箭头（`↶`）；
    4. **回退前成果 DoD 终极验收**：向用户出具已落盘文件与已监听端口的全绿完成度证明，消除回退心理负担；
  - **脚本与手册联动**：
    - 辅助脚本 `analyze_checkpoint.py` 原生支持 `--anchor` 视觉锚点生成；
    - 新增权威参考手册：[`references/ground_truth_lessons.md`](./session-checkpoint-advisor/references/ground_truth_lessons.md)。

</details>

---

## [v2.6.0] - 2026-11-22 (技能结构化合并与治理域精炼脱水)

**Tag**: `v2.6.0` | **合并吸纳**: `skill-repair` ➔ `skills-navigator` (`v1.9.0`) | **总技能数**: 24 项

<details open>
<summary>🌟 结构化合并与渐进式脱水 (Structural Merge & Progressive Slimming)</summary>

* **`skill-repair` 完整吸纳至 `skills-navigator` (v1.9.0)**：
  - **单一权威运维入口**：将分散的技能健康巡检、上游更新监控与损坏修复（`manifest.json` 手术式修复）深度整合为统一的技能生命周期管家；
  - **SOP 资产下沉**：修复指南完整下沉至 [`skills-navigator/references/skill_repair_guide.md`](./skills-navigator/references/skill_repair_guide.md)；
  - **CLI 命令升级**：`check_skills_status.py` 原生支持 `repair <skill_name>` 校验并重置损坏清单；
  - **物理结构提炼**：删除冗余的 `skill-repair/` 目录，全库技能数优雅收敛至 24 项。
* **`managing-python-dependencies` 渐进式脱水至 40 行 (v1.1.0)**：
  - **瘦身幅度**：行数从 `103 行` 锐减至 `40 行`（**-61.2%**），消除全库唯一的超标技能；
  - **多包管理器检测下沉**：将 uv、Poetry、Pipenv、Conda、venv 六大包管理器优先级矩阵与复合探测指令下沉至 [`managing-python-dependencies/references/package_managers.md`](./managing-python-dependencies/references/package_managers.md)；
  - **全库 100% 达标**：当前全库 24 项技能行数全部严格收敛在 32~77 行之间，日常上下文加载 Token 负荷极低。

</details>

---

## [v2.5.0] - 2026-11-22 (会话断点与回退续接顾问技能 + 教程联动)

**Tag**: `v2.5.0` | **新增技能**: `session-checkpoint-advisor` (`v1.0.0`) | **总技能数**: 25 项

<details open>
<summary>🌟 新增技能与架构演进 (New Skill & Architecture Evolution)</summary>

* **上线会话回退与断点续接顾问 (`session-checkpoint-advisor` v1.0.0)**：
  - **核心定位**：专为复杂长会话、反复调试死锁与多任务分叉设计的上下文态势研判与安全回退总控中枢；
  - **破解三大痛点**：
    1. **不知退到哪**：提供“拐点微回退 (Micro-Rewind) / 契约重构回退 (Contract Baseline) / 空白会话续接 (Clean-Slate)”三梯队方案；
    2. **担心丢代码**：设计回退前物理工作区保全门禁（Git Stash / Commit Guard 与开发进程占用探测）；
    3. **回退不知怎么开口**：自动合成即插即用型“破局重生 Prompt (Resumption Prompt)”，涵盖物理磁盘现实、已验证事实、死路黑名单与单一聚焦目标；
  - **跨平台辅助工具**：`scripts/analyze_checkpoint.py` 自动分析 Git 资产与进程，支持一键参数化合成续接提示词；
  - **实战手册下沉**：
    - `references/checkpoint_decision_tree.md`：会话回退决策树与复杂场景位点速查表；
    - `references/prompt_templates.md`：工业级破局重生 Prompt 模板库（驱动破局、全新会话交接、上下位机契约重塑）。
* **技能总控与教程联动演化**：
  - `skills-navigator` 升级至 `v1.8.0`，纳入第 25 个专业技能，更新提示词矩阵与多维状态审计脚本；
  - 联动更新 [05_Agent 运行治理、元能力与安全守则教程](./docs/tutorials/05_agent_governance_and_meta_tutorial.md)。

</details>

---

## [v2.4.0] - 2026-11-20 (发散搜索与多维信息调研导航技能 + 教程联动)

**Tag**: `v2.4.0` | **新增技能**: `divergent-search-guide` (`v1.0.0`) | **总技能数**: 24 项

<details open>
<summary>🌟 新增技能与架构演进 (New Skill & Architecture Evolution)</summary>

* **上线启发式发散搜索与多维信息调研导航 (`divergent-search-guide` v1.0.0)**：
  - **核心定位**：专治单一检索盲区、信息孤岛、官方营销包装与盲目多轮抓取导致的 Token 额度浪费；
  - **启发式发散导引**：非强制性拦截，作为发散思维模型辅助搜索意图解构；
  - **极低额度负荷**：正文 `SKILL.md` 仅 40 行，严格控制 Token 消耗；
  - **核心 4 步循环**：意图解构（平台/支付/合规/替代） ➔ 社区穿透（`site:v2ex.com` / `site:nodeseek.com` / `site:linux.do` / `site:reddit.com`） ➔ 多分支发散 ➔ 2026 时效核验；
  - **实战手册下沉 (`references/search_playbook.md`)**：
    - 精准搜索语法大表（双引号强匹配、`site:` 限定、减号排除营销号、`filetype:pdf`、intitle）；
    - 海外域名申请全景决策树（Porkbun / Cloudflare / Namecheap / Spaceship 对比、支付摩擦、WHOIS 隐私、DNS 托管防失联）；
    - 海外免实名 VPS 选购决策链与开源技术栈生态调研模板。
* **领域教程双向联动**：
  - 更新 [02_系统运维、科研学术与财务报销教程](./docs/tutorials/02_system_academic_finance_tutorial.md)，新增第 5 阶段“启发式发散搜索与多维信息调研”及实战 Prompt；
  - `skills-navigator` 升级至 `v1.7.0`，全量 Prompt 矩阵收录发散搜索触发用例，健康自检脚本接入该技能。

</details>

---

## [v2.3.0] - 2026-11-20 (全域技能二次无损提炼与 Token 瘦身)

**Tag**: `v2.3.0` | **基线演进**: 全库行数从 `1,616 行` 压缩至 `1,184 行`（**-26.7%**），预估 Token 从 `22,051` 压缩至 `16,550`（**节省 5,501 Tokens / -25.0%**）。

<details open>
<summary>🚀 优化与精简 (Optimization & Token Slimming)</summary>

对系统运维、财务报销、网络路由与技能总控四大高负荷技能执行渐进式披露（Progressive Disclosure）重构，正文 `SKILL.md` 总体积大幅脱水：

| 技能标识 | 版本跃迁 | 精简前指标 | 精简后指标 | 削减比例 | 详尽知识与 SOP 去向 |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`invoice-audit-master`** | `1.9.0` -> `1.10.0` | `297 L / 11,939 B` (3,730 T) | `77 L / 3,041 B` (950 T) | **-74.1%** | 赛季层级、双月提醒、双文件夹打印架构与11列Excel格式下沉至 `references/lifecycle_and_extraction_guide.md` |
| **`routeros-network-master`** | `1.0.0` -> `1.1.0` | `138 L / 5,555 B` (1,735 T) | `49 L / 2,175 B` (679 T) | **-64.5%** | SOP-01~06 终端排障与双轨自动备份脚本代码下沉至 `references/routeros_ops_sop.md` |
| **`skills-navigator`** | `1.5.0` -> `1.6.0` | `133 L / 5,068 B` (1,583 T) | `48 L / 2,114 B` (660 T) | **-63.9%** | 全量 21 技能自然语言 Prompt 实战矩阵穷举下沉至 `references/prompt_matrix.md` |
| **`pc-maintenance-master`** | `2.1.0` -> `2.2.0` | `86 L / 4,416 B` (1,380 T) | `48 L / 2,042 B` (638 T) | **-44.2%** | 40 款纳管兵器库详细分类大表收敛，统一指针链接至已有的 `references/tools_inventory.md` |

</details>

<details open>
<summary>✨ 架构保真与收益核验</summary>

* **无损知识留存**：所有被精简的业务细节（发票双文件夹打印规约、光栅化防伪禁令、RouterOS 脚本源码、Prompt 矩阵）均在对应 `references/` 案例手册中 100% 保真沉淀，调用时按需毫秒级调阅；
* **入口极速唤起**：全库除独立规约外，其余所有技能入口 `SKILL.md` 均压密在 80 行以内（平均 45~65 行），彻底终结“调一个技能即耗空额度”的痛点。

</details>

<details open>
<summary>🌟 核心架构升级 (New Architecture & Domain Tutorials)</summary>

* **上线全域精炼实战教程体系 (`docs/tutorials/`)**：
  - 确立“**原子技能保持极简执行单项武器，领域教程写透实战心法与全景联动**”的双向共生规范；
  - 交付 5 大领域教程总汇：[01_嵌入式全栈](./docs/tutorials/01_embedded_hardware_tutorial.md)、[02_系统科研财务](./docs/tutorials/02_system_academic_finance_tutorial.md)、[03_路由穿透串流](./docs/tutorials/03_network_and_p2p_streaming_tutorial.md)、[04_GCP大数据](./docs/tutorials/04_gcp_bigdata_engineering_tutorial.md)、[05_治理元能力](./docs/tutorials/05_agent_governance_and_meta_tutorial.md)；
  - 建立“项目实战踩坑 -> 教程吸收沉淀 -> 技能升级进化”的持续飞轮演进闭环。
* **新增网络串流旗舰技能 (`p2p-streaming-master` v1.0.0)**：
  - 覆盖 EasyTier 国内 Mesh 专网 (`10.144.144.0/24`)、Moonlight/Sunshine 4K 串流调优、230 发阶梯压测 A+ 门禁与 Tailscale 按需冷备；
  - 正文仅 54 行，核心指南下沉至 `references/p2p_streaming_guide.md`，配套快速探针 `check_p2p_health.py`。

</details>

---

## [v2.2.0] - 2026-11-12 (嵌入式技能无损精炼 + 版本归档基线)

**Tag**: `v2.2.0` | **Compare**: [`v2.1.0-pre-slim...v2.2.0`](https://github.com/hejiarui001/AI_Skills/compare/v2.1.0-pre-slim...v2.2.0)

<details open>
<summary>🚀 优化与精简 (Optimization & Token Slimming)</summary>

对分部 01 五项嵌入式核心技能执行渐进式披露（Progressive Disclosure）重构，入口 `SKILL.md` 总体积从 **`1,135 行 / 63,561 B`** 压缩至 **`262 行 / 21,111 B`**（行数 **-76.9%**，字节 **-66.8%**）：

| 技能标识 | 版本跃迁 | 精简前 | 精简后 | 内容去向 |
| :--- | :---: | :---: | :---: | :--- |
| `easyeda-api` | `1.1.64` -> `1.2.0` | `747 L / 32,310 B` | `72 L / 5,324 B` | 全文迁移至 `easyeda-api/references/workflow_and_examples.md` |
| `embedded-stm32-rules` | `1.10.0` -> `1.11.0` | `134 L / 14,142 B` | `63 L / 5,335 B` | 压密至 10 份 `references/*.md` + 脚本静态门禁 |
| `embedded-engineering-master` | `2.4.0` -> `2.5.0` | `153 L / 13,947 B` | `47 L / 5,984 B` | 移除冗余流程图与失效外链，收敛为 6 阶段索引表 |
| `cortex-m-pyocd` | `1.1.0` -> `1.2.0` | `56 L / 1,658 B` | `44 L / 2,376 B` | 补全双端可执行路径发现与 `-M under-reset -e chip` |
| `industrial-serial-agent` | `1.1.0` -> `1.2.0` | `45 L / 1,504 B` | `36 L / 2,092 B` | 对齐 `list`/`capture`/`send` 真实参数与 `--exclude-bt` |

</details>

<details>
<summary>✨ 新增特性 (New Features)</summary>

* **`embedded-stm32-rules` (`v1.11.0`)**：
  * 新增 `references/display_and_host_hardening.md`：沉淀 ST7789 `MADCTL` 方向偏移耦合、RGB565 大端字节序、`SPI_FLAG_BSY` 守护、脏矩形差分刷新、ESP32-C6 `32 KB` GPSPI 分块及 PyQt5 `sys.excepthook` / UTF-8 `.bat` 禁用 `::` 等实战经验。
  * 增强 `scripts/embedded_checkpoint.py`：同步备份 `Firmware/`、`Host/`、`Tools/`、`docs/`、`cmake/` 与根目录构建配置，自动生成双端恢复脚本 `RESTORE.ps1` (CRLF) + `RESTORE.sh` (LF, 0755)。
* **`industrial-serial-agent` (`v1.2.0`)**：`scripts/serial_tool.py` 新增蓝牙虚拟串口识别（`is_bluetooth`，匹配 `BTHENUM`/`BLUETOOTH`/`Bluetooth`/`蓝牙`）与 `list --exclude-bt` 过滤子命令。
* **`pc-maintenance-master` (`v2.1.0`)**：纳入 `Sunshine` 串流工具、`-DeepPreview`/`-DeepClean`/`-Deep`/`-Json` 无头模式及 `scripts/clean_admin_c_drive.ps1`（提交 `6bfd574`）。
* **工程化版本管理**：建立根目录 `CHANGELOG.md`、Git 历史里程碑标签及 `.github/workflows/release.yml` 自动 Release 发布流水线。

</details>

<details>
<summary>🐛 修复问题 (Bug Fixes)</summary>

* 修复 `embedded-stm32-rules/scripts/check_c_embedded_rules.py`：
  * 读取文件切换为 `utf-8-sig` 消除 Windows UTF-8 BOM 对首行 `#include` 的干扰；
  * 修复 Check 2 中 `'main.h' in code_line` 错误放行 `#include "app_main.h"` 的逻辑漏洞；
  * 跳过 `syscalls.c` / `sysmem.c` / `system_stm32*.c`，识别 `docs/` 说明书，忽略注释、字符串与 `for (int ...)` 循环计数，消除误报。
* 清除 `easyeda-api` 中仅 Linux 可用的 `lsof` 提示，改为 Windows `Get-NetTCPConnection` 与 Linux `lsof` 双端对照。
* 清除 `armclang_cmsis_dsp_compatibility.md` 与 `dual_workflow_mdk_cmake_guide.md` 中对 `E:\Keil ARM\...`、`E:/Tools/STM32CubeCLT_1.22.0/...` 的单机硬编码，改为环境变量及 `find_program` 动态解析。
* 清除 `embedded-engineering-master/SKILL.md` 中的失效 `file:///E:/ST/...` 本地绝对链接。
* 修正 `industrial-serial-agent/SKILL.md` 与 `cortex-m-pyocd/SKILL.md` 中与工具真实帮助输出不符的 CLI 参数示例。

</details>

<details>
<summary>📦 原版删减保留对照与调回指令 (v2.1.0-pre-slim 对照)</summary>

本版本精简掉的详尽正文与历史示例均已在标签 **`v2.1.0-pre-slim`**（提交 `1938138`）及对应 GitHub Release 离线压缩包中 **100% 原样保留**：

| 技能 | 本次被精简或迁移的原版内容 | 查看原版一键命令 |
| :--- | :--- | :--- |
| `easyeda-api` | 原 `v1.1.64` 完整 747 行手册（Bridge HTTP/WS 协议、多窗口选择、Team+Folder、常见错误 Top 5、完整 API 示例） | 已无损迁入 `easyeda-api/references/workflow_and_examples.md`；或 `git show v2.1.0-pre-slim:easyeda-api/SKILL.md` |
| `embedded-engineering-master` | 原 `v2.4.0` 完整 153 行正文（Mode A/B ASCII 框图、5+1 Mermaid 全景图、`E:/ST/...` 示例及各阶段展开 SOP） | `git show v2.1.0-pre-slim:embedded-engineering-master/SKILL.md` |
| `embedded-stm32-rules` | 原 `v1.10.0` 完整 134 行正文（12 条长展开 SOP、16 项交互前逐条核对清单 Checklist） | `git show v2.1.0-pre-slim:embedded-stm32-rules/SKILL.md` |
| `cortex-m-pyocd` | 原 `v1.1.0` 基础探针烧录格式与旧参数示例 | `git show v2.1.0-pre-slim:cortex-m-pyocd/SKILL.md` |
| `industrial-serial-agent` | 原 `v1.1.0` 旧参数示例（`--list` / `--duration`） | `git show v2.1.0-pre-slim:industrial-serial-agent/SKILL.md` |
| 整库对比 diff | 查看 5 项技能精简前后逐行改动明细 | `git diff v2.1.0-pre-slim..v2.2.0 --stat` |

</details>

---

## [v2.1.0-pre-slim] - 2026-11-09 (精简前完整原版快照)

**Tag**: `v2.1.0-pre-slim` | **Commit**: `1938138` | **Compare**: [`v2.0.0...v2.1.0-pre-slim`](https://github.com/hejiarui001/AI_Skills/compare/v2.0.0...v2.1.0-pre-slim)

<details>
<summary>✨ 里程碑快照说明 (Pre-Slim Baseline)</summary>

* 保留 21 套高内聚技能在**未进行分部 01 Token 精炼拆分前**的最后完整原版文档与历史脚本基线。
* 包含 `embedded-engineering-master v2.4.0` 与 `pc-maintenance-master` 首次引入的 **Zero Desktop Intrusion Protocol（桌面零入侵红线）** 完整原文。
* 离线包 `AI_Skills-v2.1.0-pre-slim.zip` 与 `embedded-skills-v2.1.0-pre-slim.zip` 随 GitHub Release 长期归档。

</details>

---

## [v2.0.0] - 2026-11-09 (45 合 21 高内聚技能套件重构)

**Tag**: `v2.0.0` | **Commit**: `94df693` | **Compare**: [`v1.1.0...v2.0.0`](https://github.com/hejiarui001/AI_Skills/compare/v1.1.0...v2.0.0)

<details>
<summary>🚀 架构重构明细</summary>

* 将 GCP BigQuery / GCS / Composer / Data Engineering / Governance 与数据科学领域共 45 项分散技能整合提纯为 **5 大领域 21 大核心技能套件**。
* 新增 `bigquery-master (3.0.0)`、`gcs-storage-suite (3.0.0)`、`gcp-airflow-composer-suite (3.0.0)`、`gcp-data-engineering (3.0.0)`、`gcp-governance-assets (3.0.0)`、`notebook-data-science (2.0.0)`。
* 如需追溯合并前 45 个原始独立技能目录，可执行：`git show v1.1.0:<skill-name>/SKILL.md`。

</details>

---

## [v1.1.0] - 2026-11-07 (三段式语义化版本体系基线)

**Tag**: `v1.1.0` | **Commit**: `9221a3f` | **Compare**: [`v1.0.0...v1.1.0`](https://github.com/hejiarui001/AI_Skills/compare/v1.0.0...v1.1.0)

<details>
<summary>✨ 版本治理上线</summary>

* 为全库 45 个原始技能统一补充 YAML frontmatter `version: MAJOR.MINOR.PATCH` 三段式语义版本号。
* 固化双端 `Fetch-Analyze-Merge-Push` 同步协议。

</details>

---

## [v1.0.0] - 2026-11-06 (初始全量技能库基线)

**Tag**: `v1.0.0` | **Commit**: `c65016d`

<details>
<summary>✨ 初始基线</summary>

* 完成 45 项原始 Agent 技能首次全量入库与五大领域分区矩阵初始化。

</details>
