# 破局重生 Prompt 工业级模板库 (Resumption Prompt Blueprint Library)

> **版本**：v1.0.0 | **所属技能**：`session-checkpoint-advisor`  
> **说明**：当用户在 Antigravity 或大模型界面执行会话回退或新建会话后，直接复制本模板库中的结构化 Prompt 发送给 AI，实现 100% 无缝、零重复劳动、强避坑的断点续接。

---

## 模板 1：嵌入式硬件与底层驱动重构破局 (Embedded Driver Refactoring)

```markdown
【会话回退续接指令 · 嵌入式驱动破局】

1. 物理磁盘代码现实 (Physical Reality Grounding)：
   - 芯片与工程路径：`E:\AI_Workspace\01_Embedded_Development\...` (MCU: STM32F401CCU6)
   - 当前磁盘保留文件：
     * `Inc/bsp_uart.h`：环形缓冲区结构体与协议头已定义完毕，契约锁定，严禁修改！
     * `Src/bsp_uart.c`：上一轮 DMA 中断回调逻辑混乱，需要局部重构接收解析部分。
   - 代码已通过 `git stash` 建立安全备份。

2. 已确立事实与硬件约束 (Hard Facts & Ground Truth)：
   - 晶振与时钟：HSE 8MHz，系统主频 84MHz；USART1 波特率 115200 8-N-1，引脚 PA9(TX) / PA10(RX)；
   - 协议帧头：`0xAA 0x55`，结尾为 CRC16 (MODBUS)。

3. 已验证的失败死路与负面清单 (Negative Constraints / Blacklist)：
   - 严禁尝试在 `USART1_IRQHandler` 中调用耗时的阻塞打印或复杂数据解析（会造成帧丢失）；
   - 严禁将 DMA 接收缓冲区定义在局部函数栈中（会导致指针跑飞与 HardFault）。

4. 本轮唯一行动目标 (Single Focus Action)：
   - 🎯 仅针对 `Src/bsp_uart.c`，使用双缓冲区乒乓 DMA (Double Buffer Ping-Pong) 或空闲中断 (IDLE Line) 重构数据接收，给出纯净驱动实现。
```

---

## 模板 2：长会话彻底膨胀后的“全新会话交接” (Clean-Slate Handover)

```markdown
【全新会话交接指令 · 承前启后全景注入】

> 我们在此前的长会话中已经完成了前期的技术调研与架构设计，为了摆脱长上下文的注意力稀释并提升响应质量，我们开启了当前全新会话。请以本 Prompt 提供的基线事实为唯一指导，无缝继续任务：

1. 项目现状与当前进度 (Project Status & Completed Work)：
   - 当前项目目标：[填写核心目标，如：编写 RouterOS 远程命脉网段防失联自检脚本]
   - 当前宿主系统：Windows 11 (兼顾 Ubuntu 22.04 LTS 跨平台适配)
   - 已完成并保留在磁盘上的核心资产：
     * `Tools/verify_remote_safety.py`：五层网络链路自检框架已写好
     * `docs/NETWORK_TOPOLOGY.md`：网络拓扑与 192.168.8.x 命脉保护契约已固化

2. 关键架构规范与铁律 (Non-Negotiable Constraints)：
   - 统一使用 `pathlib.Path` 解析路径，严禁硬编码绝对路径；
   - 执行网络改动前后必须无条件探活，阻断必须原地自动回滚；
   - 严禁向用户桌面写入任何未经许可的文件。

3. 上次调试中排除的死路 (Lessons Learned / Blacklist)：
   - 不要通过直接 kill 网卡进程的方式重置，这会导致 SSH 连接被彻底切断；
   - RouterOS REST API 在 7.12 之后需要特定 Basic Auth 请求头。

4. 当前待交付的单一里程碑 (Immediate Next Deliverable)：
   - 🎯 请编写自动回滚策略函数 `rollback_firewall_rules()`，确保在检测到延迟超时时能在 3 秒内恢复原状。
```

---

## 模板 3：全栈上下位机双端协议重构 (Dual-End Contract Synchronization)

```markdown
【会话回退续接指令 · 上下位机双端协议重塑】

1. 物理代码现状 (Physical Code Reality)：
   - 下位机固件：`Firmware/Core/Src/sys_blackboard.c`
   - 上位机界面：`Host/ui_main.py`
   - 当前存在问题：上位机新增了遥测字段，但下位机仍在使用旧版结构体，出现数据解析偏移。

2. 权威协议源契约 (Single Source of Truth)：
   - 协议头文件：`Firmware/Core/Inc/proto_telemetry.h`
   - 遥测枚举：严格定义 `UiMode_t`（0=Standby, 1=Auto, 2=Manual, 3=Calibrate），杜绝未经定义的魔数！

3. 本次重构纪律 (Refactoring Discipline)：
   - 先下后上，原子同步：先给出下位机结构体与序列化函数，随后同步给出上位机 `unpack` 解包逻辑；
   - 物理清除所有历史容错补丁（删除过时的模式号映射代码）。

4. 本轮唯一行动目标 (Single Focus Action)：
   - 🎯 原子化重构下位机 `telemetry_pack()` 与上位机 `telemetry_unpack()`，确保双端数据对齐。
```
