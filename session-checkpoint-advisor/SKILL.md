---
name: session-checkpoint-advisor
version: 1.0.0
description: "会话回退与断点续接顾问 (Session Checkpoint & Rewind Advisor). 当会话过长、上下文被污染或陷入重试死锁时，根据任务进度、物理工作区代码状态与电脑运行环境，自动研判最佳回退位点、执行资产安全防崩检查，并一键生成即插即用的破局重生 Prompt. Trigger on: '回退', '回退记录', '会话太长', '回到之前', '重新开始', '上下文太长', '断点回退', '回退分析', 'rewind', 'checkpoint', '重开会话', '精简上下文'."
license: Apache-2.0
metadata:
  version: v1.0.0
  author: Antigravity
---

# Session Checkpoint & Rewind Advisor (会话回退与断点续接顾问)

专为复杂长会话、反复调试死锁与多任务分叉设计的上下文态势研判与安全回退总控中枢。解决“**不知退到哪、担心丢代码、回退后不知怎么开口**”的三大核心痛点。

---

## 1. 运行规约与操作流程 (Standard Operating Procedure)

当用户提出回退诉求或会话明显过长陷入死锁时，强制执行以下 4 步标准化闭环：

### 步骤 1：物理工作区与运行态势扫描 (Physical & Runtime State Scan)
调用跨平台分析工具获取工作区真实改动、分支与正在运行的开发进程：
* **Linux (Bash)**: `python ~/.gemini/config/skills/session-checkpoint-advisor/scripts/analyze_checkpoint.py`
* **Windows (PowerShell)**: `python "$env:USERPROFILE\.gemini\config\skills\session-checkpoint-advisor\scripts\analyze_checkpoint.py"`

### 步骤 2：三梯队回退位点研判 (Multi-Tier Checkpoint Analysis)
结合会话脉络与工作区状态，向用户输出结构化决策对照：

| 方案梯队 | 推荐位点特征 | 适用场景 | 预期收益 | 潜在代价 |
| :--- | :--- | :--- | :--- | :--- |
| **方案 A: 拐点微回退** | 首次报错或思路分歧提问前 | 总体架构正确，仅最近 1~2 轮的函数/参数陷入局部报错死循环 | 保留绝大部分前期有效上下文，最小代价重试 | 若底层架构已有暗坑，可能再次陷入同类错误 |
| **方案 B: 契约重构回退** *(推荐)* | 架构设计、头文件与数据模型锁死时 | 经过多次补丁后代码产生严重腐化、上下位机协议漂移、上下文充满报错日志 | 洗掉全部试错噪声与无效尝试，从干净起点直奔实现 | 需在交接词中指明磁盘上保留的文件 |
| **方案 C: 空白会话断点续接** | 直接开启全新窗口 (无上下文) | 会话总长极大 (>15万Token)、响应明显延迟、模型注意力严重稀释 | 彻底恢复首字响应与吞吐，规避模型记忆混乱 | 依赖高密度交接 Prompt 将既有成果整体平移 |

### 步骤 3：回退前“零损失”防崩门禁 (Pre-Rewind Safety Gate)
在指导用户回退前，**必须显式提醒执行资产保全**：
1. **代码暂存保全**：指导用户执行 `git stash save "checkpoint-pre-rewind"` 或创建分支 `git checkout -b wip/checkpoint`，防止物理磁盘改动被意外冲刷；
2. **独占进程释放**：若检测到 `pyocd`, `vofa+`, 串口调试器等占用资源，提示用户先行释放。

### 步骤 4：交付即插即用型“破局重生 Prompt (Resumption Prompt)”
根据工作区现状，向用户提供一段**可直接一键复制、在回退后直接发送给 AI** 的高密度提示词，必须包含四要素：
1. **物理磁盘最新现实 (Physical Reality)**：明确列出当前磁盘有效文件，告知模型切勿从零盲目重写；
2. **已确立事实与有效约束 (Hard Facts)**：已验证的硬件参数、波特率、协议头与环境依赖；
3. **已排除的死路清单 (Lessons Learned / Blacklist)**：严禁尝试的错误方案与已踩过的坑；
4. **本轮唯一步骤聚焦 (Single Focus Action)**：锁定单一核心目标，杜绝分散精力。

---

## 2. 自动化交接 Prompt 一键生成指令

快速生成标准化续接 Prompt 骨架：
```bash
# 传入核心目标与避坑清单一键生成
python <path_to_scripts>/analyze_checkpoint.py --prompt --target "重构串口接收环形缓冲区DMA驱动" --dead-ends "不要在中断中调用耗时printf"
```

---

## 3. 权威参考实战库 (Authoritative Playbook)

* 📘 **决策树与复杂场景位点对照表**：查阅 [`references/checkpoint_decision_tree.md`](file:///C:/Users/hejia/.gemini/config/skills/session-checkpoint-advisor/references/checkpoint_decision_tree.md)。
* 📘 **工业级破局重生 Prompt 模板库**：查阅 [`references/prompt_templates.md`](file:///C:/Users/hejia/.gemini/config/skills/session-checkpoint-advisor/references/prompt_templates.md)。
