# AI Skills Changelog & Version Archive

> **仓库地址**：`https://github.com/hejiarui001/AI_Skills`  
> **Releases 页面**：`https://github.com/hejiarui001/AI_Skills/releases`  
> **设计原则**：正文 `SKILL.md` 保持最小 Token 负荷；历史原版全文与阶段快照通过 **Git Tags + GitHub Releases + 本台账** 永久封存，按需毫秒级调阅、零日常上下文开销。

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
