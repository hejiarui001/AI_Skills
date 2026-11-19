# 嵌入式软硬件全栈实战教程与技能联动体系 (Embedded & Hardware Master Tutorial)

> **领域定位**：STM32、ARM Cortex-M、ESP32/RISC-V 软硬件全栈研发、电路设计、工业编码、无头烧录与遥测排障  
> **联动技能群**：`easyeda-api`、`embedded-stm32-rules`、`cortex-m-pyocd`、`industrial-serial-agent`、`embedded-engineering-master`  
> **更新机制**：随实盘项目持续增量沉淀，形成“项目踩坑 -> 教程吸收 -> 技能升级”飞轮

---

## 一、 嵌入式全生命周期工程流水线 (Pipeline)

```text
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 1. 原理图与引脚 │ ──> │ 2. PIA 架构驱动 │ ──> │ 3. 无头固件烧录 │
│  easyeda-api    │     │stm32-rules/HAL  │     │ cortex-m-pyocd  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                                               │
         ▼                                               ▼
┌─────────────────┐                             ┌─────────────────┐
│ 5. 全链路闭环编排│ <────────────────────────── │ 4. 串口/VOFA+遥测│
│engineering-master│                             │serial-agent/UART│
└─────────────────┘                             └─────────────────┘
```

---

## 二、 阶段实战指南与技能联动矩阵

### 1. 硬件设计与器件校验
* **核心目标**：确保原理图网络标号无冲突、引脚分配无重叠、BOM 规范化导出。
* **SOP 规范**：使用 EasyEDA Pro 绘制，重点核验单片机晶振（OSC_IN/OUT）、SWD 下载口（SWCLK/SWDIO）与复位阻容。
* **【联动技能】**：[`easyeda-api`](../../easyeda-api/SKILL.md)
  - *触发示例*：“在嘉立创EDA里把选中的网络标号批量改成 VCC_3V3”、“导出当前工程的物料清单 BOM”。

### 2. 固件架构与工业级编码 (PIA 架构)
* **核心目标**：打破臃肿的 `main.c`，实施 **PIA（渐进式实例驱动架构）** 四层解耦：
  - `BSP`（板级支持包：LED、按键、蜂鸣器）
  - `DEV`（智能外设驱动：OLED/ST7789、传感器、PMIC、电机）
  - `SYS`（中央黑板、状态总线、时间片轮询调度器）
  - `APP`（顶层业务状态机、双端通信协议处理）
* **【联动技能】**：[`embedded-stm32-rules`](../../embedded-stm32-rules/SKILL.md)
  - *触发示例*：“按照 PIA 架构与标准目录规范重构当前工程”、“用 HAL 库写一个双缓冲 UART DMA 接收驱动并检查合规性”。

### 3. 无头构建与硬件探针烧录
* **核心目标**：免除 Keil / IAR 笨重 IDE 打开等待，实现 CLI 秒级固件烧写与锁死芯片解锁。
* **SOP 规范**：
  - 探针识别：支持 ST-Link、CMSIS-DAP、DAPLink；
  - 救砖解锁：当单片机因 Sleep 模式或引脚复用失联时，强制启用 `-M under-reset -e chip`。
* **【联动技能】**：[`cortex-m-pyocd`](../../cortex-m-pyocd/SKILL.md)
  - *触发示例*：“检测一下插在电脑上的 ST-Link 和单片机型号”、“把 build/firmware.bin 烧进单片机 Flash”。

### 4. 工业级串口通信与 VOFA+ 遥测
* **核心目标**：建立可靠的下位机状态回传链路，支持 JustFloat 浮点波形与 RawHex 调试。
* **SOP 规范**：排除蓝牙虚拟串口干扰（`--exclude-bt`），配置 DMA 循环接收 + 空闲中断（IDLE）。
* **【联动技能】**：[`industrial-serial-agent`](../../industrial-serial-agent/SKILL.md)
  - *触发示例*：“扫描当前电脑可用的 COM / ttyUSB 端口”、“监听 COM5 波特率 115200 并抓取遥测数据”。

### 5. 全链路死机排障与工程总控
* **核心目标**：面对 HardFault、Watchdog 复位或协议漂移，执行自底向上的穿透式诊断。
* **【联动技能】**：[`embedded-engineering-master`](../../embedded-engineering-master/SKILL.md)
  - *触发示例*：“板子死机了，帮我全链路排查硬件与固件”、“从原理图引脚核对到串口遥测跑通端到端闭环”。

---

## 三、 实战踩坑手记与经验增量池 (Hard-Won Knowledge)

1. **I2C 总线挂死自愈**：从机在 ACK 阶段拉低 SDA 导致主机死锁。恢复方案：主机强制将 SCL 翻转 9 次并发送 STOP 信号；
2. **ST7789 显存偏移与字节序**：驱动需根据分辨率（如 240x240 / 240x280 / 240x320）补偿 `Row/Col Offset`，RGB565 数据在 SPI 传输时必须为高字节在前（大端传输）；
3. **ArmClang 6 编译冲突**：开启 MicroLIB 时严禁使用标准 C 库的大型 `printf` 浮点支持，避免栈溢出。
