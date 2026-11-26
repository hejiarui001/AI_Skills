---
name: session-checkpoint-advisor
version: 1.2.0
description: "会话回退与断点续接顾问：本地 0 Token 内省、精确时间轴锚点、二轮熔断、安全门禁与免探接力 Prompt。Trigger on: 回退, 回退记录, 会话太长, 重开会话, 精简上下文, rewind, checkpoint。"
license: Apache-2.0
metadata:
  version: v1.2.0
  author: Antigravity
---

# Session Checkpoint & Rewind Advisor (v1.2.0)

基于 94 场生产会话复盘打造的高阶上下文治理解法。实现 **“0 Token 本地会话内省 + 二轮空转主动熔断 + 物理与网络防锁死门禁 + 免探核准零延迟接力”** 四位一体闭环。

---

## 1. 运行规约与四步闭环 (Standard Operating Procedure)

### 步骤 1：本地零 Token 会话内省与物理态势扫描 (Introspect & Scan)
* **首句定心丸**：“IDE 回退仅清除大模型记忆，本地磁盘代码、远端 Docker 容器与芯片固件 **100% 常驻绝不丢失**！”
* **运行本地内省引擎**（自动剖析最新 `transcript.jsonl`、时间轴锚点、空转死锁区间、Git 与代理端口 `7897`）：
  - **Linux**: `python ~/.gemini/config/skills/session-checkpoint-advisor/scripts/analyze_checkpoint.py`
  - **Windows**: `python "$env:USERPROFILE\.gemini\config\skills\session-checkpoint-advisor\scripts\analyze_checkpoint.py"`

### 步骤 2：精确时间轴锚点与二轮空转熔断研判
* **精确锚点定位**：直接引用脚本抽取出的 `Txx [HH:MM]: "原话前35字..."`，指导用户点击对应消息右上角弯箭头（`↶`）；
* **空转熔断红线**：若检测到连续 $\ge 2$ 轮无效“试试/不行”或重发循环，必须切断试错，推荐退至拐点之前或直接开新窗口（方案 C）。

### 步骤 3：回退前“零损失 + 防自断网”双维门禁 (Safety Gates)
1. **成果 DoD 验收**：确认已完成落盘文件、监听端口与权威规范（`docs/*_SPEC.md`）；
2. **代码保全与后台任务**：提示 `git stash save "pre-rewind"`，并预警会话内拉起的后台 task 会被 IDE 强杀；
3. **网络悬空态预检**：若涉及代理/路由调试，确认本地 `7897` 代理端口活跃且未遗留残缺网络配置。

### 步骤 4：交付带“免探核准印章”的极简接力 Prompt
生成 Prompt 必须包含：
1. **确定性免探核准印章 (Pre-Verified Stamp)**：附带 Git 状态签名与时间戳，授权新 AI 跳过开局重复 `git status`，首轮直入执行；
2. **单一权威 SSOT 文档指针** (`docs/<MODULE>_SPEC.md`)；
3. **脱敏外部凭据指针**（严禁明文密钥入上下文，统一指引用本地 `E:\Internet\Messages\...`）；
4. **死路黑名单 + 本轮唯一目标**。

---

## 2. 深度参考实战库 (Authoritative Playbook)

* 📘 **实战暗坑与 9 大认知铁律**：[`references/ground_truth_lessons.md`](file:///C:/Users/hejia/.gemini/config/skills/session-checkpoint-advisor/references/ground_truth_lessons.md)
* 📘 **决策树与场景对照表**：[`references/checkpoint_decision_tree.md`](file:///C:/Users/hejia/.gemini/config/skills/session-checkpoint-advisor/references/checkpoint_decision_tree.md)
* 📘 **破局重生 Prompt 模板库**：[`references/prompt_templates.md`](file:///C:/Users/hejia/.gemini/config/skills/session-checkpoint-advisor/references/prompt_templates.md)
