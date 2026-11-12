---
name: embedded-engineering-master
version: 2.5.0
description: >-
  Flagship full-stack embedded hardware & software engineering orchestrator for STM32, ARM Cortex-M, and ESP32/RISC-V microcontrollers.
  Unifies the complete end-to-end hardware-software pipeline: EasyEDA circuit/pinout verification -> UCA/PIA multi-tier firmware architecture -> Headless compilation (Keil/CMake/idf.py) -> pyOCD/esptool hardware flashing -> industrial serial telemetry (UART/VOFA+) -> milestone checkpointing.
  Featuring Autonomous Architecture Tiering (Compact Mode vs UCA Comprehensive Mode), Blackboard state bus, Policy chain engine, Matrix Break-Before-Make safety, 3-in-1 Unified Protocol, and strict Zero Desktop Intrusion (未获明确允许严禁向宿主桌面落盘快捷方式/文件).
  Trigger when the user asks for end-to-end embedded development, hardware-software co-debugging, full-chain feature delivery, board bring-up, or full lifecycle diagnostics (e.g., "全链路开发", "端到端调通", "从原理图到板子跑通", "板子死机全系统排查", "软硬件全栈闭环").
license: Apache-2.0
metadata:
  version: v2.5.0
  role: Master Orchestrator
---

# 嵌入式软硬件全栈工程大师 (Embedded Engineering Master) v2.5

端到端嵌入式研发编排中枢：打通 **原理图引脚核查 -> 分级架构与双端契约 -> 无头编译 -> 探针烧录 -> 串口/上位机联调 -> 卫生审计与快照归档** 全链路闭环。

---

## 1. 架构自主分级判定 (Autonomous Tiering)

接手工程时先行探测芯片资源并输出三行判定报备：
* **模式 A — 极简紧凑 / PIA 分层 (C99)**：`Flash <= 64KB, RAM <= 16KB` 或纯粹外设板卡。扁平 `App/BSP` 或 PIA 4 层 (`Firmware/{App,Module,Service,BSP}`)，零 `malloc`、零虚表，协作式时间片调度 + VOFA+ `JustFloat`。
* **模式 B — 综合组件模式 UCA (C++17/20)**：`Flash >= 128KB, RAM >= 32KB` 或异构双核/无线网联。5 层组件隔离（`modules/` 禁含 HAL 头文件便于宿主机单测），见 [`references/uca_architecture_spec.md`](references/uca_architecture_spec.md)；含 OSAL + PAL、Blackboard 状态总线、责任链策略引擎、矩阵 **Break-Before-Make** 死区与短路微脉冲探测、三合一协议（遥测/ParamTree/RPC）。

---

## 2. 六阶段全链路标准作业程序 (6-Stage Master Pipeline)

### 阶段 1：硬件图纸、供电与时钟核验 (Hardware Grounding)
1. 阅读工程 `docs/HARDWARE_SPEC.md`、`docs/SOFTWARE_SPEC.md` 或调用 [`easyeda-api`](../easyeda-api/SKILL.md) 核查物理位号、GPIO 复用、极性与多通道防短路互斥。
2. **PMIC 供电与模式核查**：对 MP2672/BQ 等电源管理 IC，I2C 无应答时先用万用表确认 `VIN`(USB 5V) 或 `BATT` 是否供电使内部 `VCC` LDO 建立（仅接 ST-Link 3.3V 时 PMIC 未上电必 NACK），并核实 `CV`/模式引脚拉至 `VCC` 进入 Host-Control 模式。
3. **三方时钟核验与 `.ioc` 防覆写**：对齐“BOM 晶振丝印 ∩ `.ioc` `HSE_VALUE` ∩ 运行时 PLL 寄存器”，所有上下拉/时钟修改必须同步固化到 `.ioc`。

### 阶段 2：双端契约与固件工程 (Contract & Firmware)
1. **契约先行与原子同步**：UI 模式（`UiMode_t`）、遥测帧与控制指令先在中央黑板/通信头文件显式定义；MCU 与 PyQt5 上位机改动必须在同一迭代同步交付，物理清零旧轮播与容错残留。
2. **编码军规与外设要点**：遵循 [`embedded-stm32-rules`](../embedded-stm32-rules/SKILL.md)（单文件 `<=400` 行、`<=0` 动态内存、`9-Clock` I2C 自愈并重设 `AF_OD` + `HAL_I2C_DeInit`、`ST7789` `MADCTL` 与偏移转置/RGB565 高字节先行/差分刷屏与 DMA 分片保护、PyQt5 `sys.excepthook` 异常兜底与 UTF-8 `.bat` 禁用 `::`）。

### 阶段 3：跨平台无头编译 (Headless Build)
* **Keil MDK-ARM**：`UV4.exe -b <proj>.uvprojx -j0`（动态探测 `$env:KEIL_ROOT` 或 `E:\Keil_v5`，严禁硬编码单一路径）；ArmClang 6 注意 `-fshort-enums -fshort-wchar` 与 V5.06 `armlink` 备选。
* **Modern CMake (CubeCLT / GCC)**：优先探测 `$env:STM32CLT_PATH`、`PATH` 或 `/opt/st/stm32cubeclt`，运行 `cmake -B build -G Ninja && cmake --build build`。
* **ESP-IDF**：`idf.py build` 并核查 app 分区余量。全部目标要求 **0 Error(s), 0 Warning(s)**。

### 阶段 4：硬件探针与固件烧录 (Flash & Verify)
联动 [`cortex-m-pyocd`](../cortex-m-pyocd/SKILL.md)（STM32）或 `esptool.py`（ESP32）探测硬件并烧录校验；若遇休眠或 SWD 锁死使用 `pyocd flash -M under-reset`。

### 阶段 5：串口遥测与联调 (Serial Telemetry & Host Launch)
联动 [`industrial-serial-agent`](../industrial-serial-agent/SKILL.md)（`list --exclude-bt` 自动跳过 `BTHENUM` 蓝牙虚拟口，`capture`/`send` 抓包校验帧率与电压/传感器遥测，必要时配合 VOFA+ 验证）。

### 阶段 6：自洁交付审计与快照归档 (DoD Gate)
1. **目录与卫生校验**：清除散落 `.log`/`.tmp`，确保 `docs/`、`Firmware/`、`Host/`、`Tools/Firmware/` 四权分立，严禁未获用户授权在桌面生成 `.lnk`/`.desktop`。
2. **自动化健康检查与快照**：运行工程级健康审计脚本（如 `python Tools/check_project_health.py`）与 [`embedded_checkpoint.py`](../embedded-stm32-rules/scripts/embedded_checkpoint.py)（生成轻量快照与 `RESTORE.ps1` / `RESTORE.sh`），同步更新 `docs/SOFTWARE_SPEC.md` 与根目录 `README.md`。

---

## 3. 子技能调度路由

| 专项任务 | 调用子技能 |
| :--- | :--- |
| 原理图/PCB/BOM 读取与修改 | [`easyeda-api`](../easyeda-api/SKILL.md) |
| STM32 代码审计、PIA 重构与踩坑手册 | [`embedded-stm32-rules`](../embedded-stm32-rules/SKILL.md) |
| 调试器探测、烧录、全片擦除与解锁 | [`cortex-m-pyocd`](../cortex-m-pyocd/SKILL.md) |
| COM/ttyUSB 扫描、协议收发与日志抓取 | [`industrial-serial-agent`](../industrial-serial-agent/SKILL.md) |
