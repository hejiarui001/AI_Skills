# Engineering Worklog & Report Templates

Standard templates for transforming raw Git commit logs and diff metrics into professional, polished engineering reports.

---

## 1. 研发日报标准模板 (Daily Standup Template)

```markdown
# 📅 研发日报 - YYYY-MM-DD

### 一、 今日完成核心工作
* **[模块/功能名]**：提炼的改动描述（说明业务目的与实现方案，而非简单抄写 commit message）。
  * 涉及文件：`Drivers/UART/ring_buffer.c`, `Core/Src/main.c`
  * 成果产出：完成环形缓冲区初始化与中断安全设计，单片机在 115200 波特率下高频接收丢包率降至 0。
* **[模块/功能名]**：...

### 二、 遇到的难点与攻关进展
* **问题描述**：...
* **排查与解决**：...

### 三、 明日工作计划
1. [ ] 推进 ...
2. [ ] 联调 ...
```

---

## 2. 研发周报标准模板 (Weekly Engineering Summary)

```markdown
# 📊 研发周报 - YYYY年第W周 (MM.DD ~ MM.DD)

### 📌 本周核心进展与里程碑
1. **[关键里程碑 1]**：达成效果与交付情况。
2. **[关键里程碑 2]**：达成效果与交付情况。

### 🛠️ 详细任务拆解与进展

| 模块 / 任务名称 | 负责人 | 进展状态 | 核心工作说明与代码改动 |
| :--- | :--- | :--- | :--- |
| **通信驱动层** | 开发者 | 已完成 (100%) | 实现了 DMA 串口空闲中断接收与 VOFA+ JustFloat 格式打包 |
| **算法移植** | 开发者 | 进行中 (80%) | 完成了卡尔曼滤波初始参数辨识，待上机验证噪声抑制比 |

### ⚠️ 风险、阻塞点与资源协调
* **阻塞点**：无 / 需要协调示波器硬件资源...

### 🎯 下周重点计划
1. 完成 ...
2. 进行实物板卡联调 ...
```
