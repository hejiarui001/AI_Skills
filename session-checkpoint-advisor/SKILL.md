---
name: session-checkpoint-advisor
version: 1.1.0
description: "会话回退与断点续接顾问 (Session Checkpoint & Rewind Advisor). 当会话过长、上下文被污染或陷入重试死锁时，根据任务进度、物理工作区代码状态与电脑运行环境，自动研判最佳回退位点、执行资产安全防崩检查，并一键生成即插即用的破局重生 Prompt. Trigger on: '回退', '回退记录', '会话太长', '回到之前', '重新开始', '上下文太长', '断点回退', '回退分析', 'rewind', 'checkpoint', '重开会话', '精简上下文'."
license: Apache-2.0
metadata:
  version: v1.1.0
  author: Antigravity
---

# Session Checkpoint & Rewind Advisor (会话回退与断点续接顾问)

专为复杂长会话、反复调试死锁与多任务分叉设计的上下文态势研判与安全回退总控中枢。基于 52 个生产会长会话经验构建，提供“**物理安全定心、视觉锚点指引、DoD终极验收与破局续接**”一体化方案。

---

## 1. 运行规约与操作流程 (Standard Operating Procedure)

当用户提出回退诉求或会话明显过长陷入死锁时，强制执行以下 4 步标准化闭环：

### 步骤 1：物理隔离定心声明与态势扫描 (Physical Decoupling & Scan)
* **首句声明**：“IDE 会话回退仅清除大模型记忆上下文，本地磁盘代码、远端 Docker 容器与芯片 Flash 固件 100% 稳定常驻，绝不丢失！”
* **态势探测**：
  - **Linux**: `python ~/.gemini/config/skills/session-checkpoint-advisor/scripts/analyze_checkpoint.py`
  - **Windows**: `python "$env:USERPROFILE\.gemini\config\skills\session-checkpoint-advisor\scripts\analyze_checkpoint.py"`

### 步骤 2：三梯队位点研判与视觉锚点指引 (Visual Anchor Guidance)
向用户输出三梯队决策矩阵，并**强制附带原话特征指纹**：
* 💡 **回退操作指引**：明确标注“请向上翻找你在 **[HH:MM]** 发送的：`【用户提问特征原话……】`，点击右上角弯箭头（`↶` 编辑/回退）”。

| 方案梯队 | 推荐位点特征 | 适用场景 | 预期收益 |
| :--- | :--- | :--- | :--- |
| **方案 A: 拐点微回退** | 首次报错或思路分歧提问前 | 30 轮内单函数/参数陷入局部报错循环 | 保留绝大部分对话成果，最小代价重试 |
| **方案 B: 契约重构回退** *(推荐)* | 架构设计、头文件与协议锁死时 | 代码多次修补产生腐化、协议漂移 | 洗掉全部试错噪声，在干净上下文中直奔实现 |
| **方案 C: 里程碑结项新开** | 直接开启全新窗口 (无上下文) | 50 轮以上超长任务或大模块阶段完结 | 彻底恢复首字响应速度，杜绝注意力漂移 |

### 步骤 3：回退前“零损失”防崩门禁与 DoD 验收 (Pre-Rewind DoD Gate)
1. **成果 DoD 终极验收**：向用户简报已落盘文件、已监听端口与已完成配置，出具全绿通过证明；
2. **代码暂存保全**：提示在终端执行 `git stash save "checkpoint-pre-rewind"` 固化物理代码；
3. **后台子进程预警**：提示会话内启动的后台 task 会被 IDE 终止，提前提供重新拉起命令。

### 步骤 4：交付即插即用型“破局重生 Prompt (Resumption Prompt)”
向用户交付包含【物理代码现实、已确认硬事实、已验证死路黑名单、本轮唯一步骤聚焦】的高密度 Prompt，用户一键复制发送。

---

## 2. 深度参考实战库 (Authoritative Playbook)

* 📘 **会话回退五大实战暗坑与经验沉淀**：查阅 [`references/ground_truth_lessons.md`](file:///C:/Users/hejia/.gemini/config/skills/session-checkpoint-advisor/references/ground_truth_lessons.md)。
* 📘 **决策树与复杂场景位点速查**：查阅 [`references/checkpoint_decision_tree.md`](file:///C:/Users/hejia/.gemini/config/skills/session-checkpoint-advisor/references/checkpoint_decision_tree.md)。
* 📘 **工业级破局重生 Prompt 模板库**：查阅 [`references/prompt_templates.md`](file:///C:/Users/hejia/.gemini/config/skills/session-checkpoint-advisor/references/prompt_templates.md)。
