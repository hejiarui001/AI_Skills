# 统一嵌入式组件架构规范 (UCA - Unified Component Architecture)

## 1. 架构总则与设计哲学

UCA 旨在消除芯片架构（ARM Cortex-M vs RISC-V / Xtensa）、操作系统（裸机时间片 vs FreeRTOS）以及编程范式（纯 C99 vs 现代 C++20）之间的壁垒，实现**“业务积木完全纯净、硬件平台即插即拔、上下位机一套通吃”**。

```
MyProject_Root/
├── app/                             # [Layer 5] 业务胶水与生命周期装配
├── modules/                         # [Layer 4] 核心业务积木（100% 跨平台，零硬件包含）
│   ├── blackboard/                  # 全局状态总线（单一真理源）
│   ├── policy_engine/               # 动作与安全责任链引擎
│   ├── matrix_controller/           # 矩阵控制与先断后合引擎
│   └── ui_engine/                   # 零堆分配屏幕/按键交互
├── framework/                       # [Layer 2~3] 跨平台基础设施
│   ├── osal/                        # 操作系统抽象（裸机双模 / RTOS）
│   ├── pal/                         # 平台外设抽象（GPIO/UART/I2C/SPI/CAN）
│   └── protocol/                    # 统一通信中枢（遥测 + 参数树 + 指令 RPC）
├── bsp/                             # [Layer 1] 板级硬件引脚对照与器件驱动
└── host/                            # 上位机工具（VOFA+ 预设、Python 自动化脚本）
```

---

## 2. 四大核心积木组件规范

### 2.1 状态总线 (Blackboard - 单一真理源)
* **原则**：所有连续物理量（电压、电流、温度、转速）收敛至单一结构体；
* **写入规约**：生产者（ADC、I2C 采样任务）通过原子锁或关中断写入；
* **读取规约**：消费者（UI、通信、保护逻辑）只读快照副本，杜绝跨模块直接穿透指针。

### 2.2 动作策略链引擎 (Policy Engine - 责任链)
* **原则**：所有执行器（继电器、MOS、功率输出）禁止直接暴露控制接口；
* **规约**：统一通过 `PolicyEngine::request(op, source)` 提交。执行器开通前，依次执行已注册策略的 `can_execute()` 校验：
  - `ShortCircuitDetectPolicy`（短路阶梯探测）
  - `ProtectPolicy`（过压、过流、过温阈值）
  - `CooldownPolicy`（防抖与冷却时间窗口）
  - `InterlockPolicy`（上位机/按键互锁）
  所有策略校验一致放行后，方可驱动物理硬件。

### 2.3 矩阵控制引擎 (Matrix Engine - 安全二分图)
* **拓扑抽象**：采用 `uint16_t` / `uint64_t` **位图（Bitmask）**记录全矩阵通道通断，通信与存储仅占 2~8 字节；
* **排他性规则表（Exclusion Matrix）**：
  - **单源独占**：同一列（Column）只允许 1 个交叉点导通，彻底杜绝多路电源并联倒灌硬短路；
  - **容量超载拦截**：全矩阵激活通道数超过硬件驱动线圈功率上限时强行拒止；
* **先断后合状态机（Break-Before-Make, BBM）**：
  状态切换严禁一步到位，强制走四拍原子事务：
  `计算差异 -> 切断旧通道 -> 硬件死区延时(Dead-time) -> 导通新通道`。

### 2.4 上下位机三合一协议引擎与双端原子演进 (Protocol Engine & Dual-End Co-Evolution)
* **遥测通道 (Telemetry)**：定长二进制/浮点帧直通 **VOFA+ JustFloat** 或上位机波形控件；
* **参数树通道 (Parameter Tree)**：基于 Key-Value / TLV 索引树，支持上位机动态标定，并联动单片机 Flash/NVS 掉电持久化；
* **指令通道 (RPC Command)**：操作码 + 状态响应，直接对接策略链引擎；
* **双端原子同步与技术债务清零**：通信协议是上下位机唯一契约。下位机扩展 UI 模式或遥测字段时，上位机 UI、解析器与命令发送端必须同版本交付；重构后必须彻底物理清除旧过渡模式（如旧轮播模式、旧模式号容错与已废弃函数命名），杜绝上下位机语义漂移。

---

## 3. 架构分级模式对照表

| 维度 | 【极简紧凑模式】 | 【综合组件模式】(UCA) |
|:---|:---|:---|
| **适用芯片** | Flash $\le$ 64KB, RAM $\le$ 16KB *(STM32F0/G0, CH32V)* | Flash $\ge$ 128KB, RAM $\ge$ 32KB *(STM32F4/G4/H7, ESP32)* |
| **代码目录** | 扁平单层（`main.c`, `app.c/h`, `bsp.c/h`） | 5 层组件化目录（`app`, `modules`, `framework`, `bsp`, `host`） |
| **编程语言** | 纯 C99，禁止 C++ 虚函数与动态内存 | 现代 C++20 / C++17，RAII 智能守卫，模板与类多态 |
| **并发系统** | 裸机 SysTick 协同时间片轮询 | OSAL 多任务（FreeRTOS / 抢占式 RTOS） |
| **脱机测试** | 纯 C 逻辑单函数验证 | MinGW/GTest 宿主机 100% 覆盖测试 |
