# PIA 渐进式实例驱动架构规范 (Progressive Instance-driven Architecture)

本规范为嵌入式 C/C++ 固件开发定义了一套**“从极简原型平滑演进到工业/竞赛级高可靠系统”**的代码架构标准。其核心哲学是：**用统一分层避免架构腐化，用极简微核避免过度设计，用句柄与黑板实现功能无损叠加。**

---

## 1. 架构起源与背景

### 1.1 "App + BSP" 双层架构的陷阱
行业中常见的 `App/` + `BSP/` 双层架构极易在中期演进中崩溃：
* **伪 BSP 污染**：将 OLED、电机、传感器等外部器件与片上资源混在一起（例如 `bsp_oled.c` 直接操作 STM32 寄存器），换一颗 MCU 驱动全部报废。
* **App 膨胀为垃圾桶**：通信协议、控制算法、按键扫描、保护逻辑堆砌在同一个文件中（动辄突破千行），模块之间充斥着裸露的全局 `extern` 变量。
* **两极分化陷阱**：遇到复杂问题就直接硬搬重型 RTOS 或庞大框架，导致代码量激增、RAM/ROM 浪费、调试难度倍增。

### 1.2 顶级工程的核心精髓
PIA 架构融合了工业级与顶级机器人竞赛开源项目的底层设计：
* **Betaflight**：静态时间片协同调度器（Cooperative Scheduler），以零栈开销实现微秒级确定性执行，彻底替代 `HAL_Delay` 与裸循环。
* **HNU `basic_framework` & SCUT `srml`**：外设驱动采用**句柄注册制（Instance Model）**，驱动只认句柄指针，天然支持从 1 路无缝扩展至 N 路。
* **PX4 & Meta-Team**：**数据黑板（Blackboard / Topic）**与**离线守护（Daemon）**机制，输入/反馈/状态单向流动，杜绝跨文件变量穿透。
* **QP/C**：明确的有限状态机（FSM）与事件触发机制，杜绝嵌套 `switch-case` 意大利面条代码。

---

## 2. 通用多工作流物理分仓与 4 级单向依赖目录 (Multi-Workflow Directory Isolation Baseline)

### 2.1 跨工作流物理分仓标准 (Universal Workspace Baseline)
嵌入式项目经常涉及多种工具链（STM32CubeMX、Keil MDK、CMake/GCC、PlatformIO）以及与 PC 端上位机（Python/Qt/VOFA+）的协同。若将所有文件平铺在根目录，各工具链的代码重新生成机制与编译缓存将互相污染。

因此，所有工程必须遵循以下 **5 大独立分仓区** 进行物理隔离：

```text
<Project_Root>/
├── Firmware/                 /* 【MCU 固件总仓】纯 C/C++ 嵌入式工程源码，完全收敛 PIA 四层 */
│   ├── App/                  /* 业务行为状态机 (主控任务流程, 安全自锁保护, 交互与UI调度) */
│   ├── Module/               /* 外接设备与独立算法 (电机/阀门模型, OLED屏幕, 传感器滤波, 按键) */
│   ├── Service/              /* 核心服务与中间件 (静态时间片调度器, 数据黑板, 协议解包, 守护) */
│   └── BSP/                  /* 硬件外设适配层 (片上资源封装: adc_bsp, can_bsp, uart_bsp) */
│
├── Host/                     /* 【PC 端上位机总仓】PC 测控客户端、Python 脚本、串口调试工具箱 */
│   ├── Host_App/             /* 上位机 UI 与核心应用 */
│   ├── Tools/                /* 串口助手、字模生成器、协议发包脚本 */
│   └── 启动上位机.bat          /* 一键拉起上位机入口 */
│
├── docs/                     /* 【历史设计资料归档区】硬件原理图、通信帧文档、技术草稿 */
├── _checkpoints/             /* 【里程碑复位快照区】零编译缓存轻量备份 (单节点 < 400KB) */
├── SOFTWARE_SPEC.md          /* 【说明书】根目录唯一权威软硬件交付总纲 */
│
└── <Toolchain_Anchors>/      /* 【工具链锚点区】禁止移动，严格保留在根目录 */
    ├── Core/                 /* (CubeMX) 片上外设时钟/引脚初始化 (main.c, stm32f1xx_it.c) */
    ├── Drivers/              /* (CubeMX) ST 官方 STM32 HAL 库与 CMSIS */
    ├── MDK-ARM/              /* (Keil) uvprojx 工程与编译输出 */
    ├── F103c8t6_qibeng.ioc   /* (CubeMX) 芯片图形化配置 */
    ├── .mxproject            /* (CubeMX) 工具链映射 (隐藏属性) */
    └── .vscode/              /* (VSCode) IDE 编译器索引与任务配置 (隐藏属性) */
```

#### 各分仓隔离机制与约束边界：
* **CubeMX 零破坏原则**：CubeMX 强制以 `.ioc` 所在目录为根路径并维护 `Core` 与 `Drivers`。通过将用户代码放入 `Firmware/`，CubeMX 在二次生成代码（Re-generate Code）时永远触碰不到用户固件，绝不产生代码冲刷或工程分裂。
* **IDE 配置不失效原则**：VSCode 强制要求 `.vscode/` 必须在工作区最顶层。将其设为系统隐藏属性，既保障代码智能提示与快捷任务 100% 正常，又保持资源管理器视觉清爽。
* **上位机环境解耦原则**：PC 端 Python 虚拟环境（`.venv`）与巨型依赖包全部隔离在 `Host/` 内，单片机工程扫描与快照备份时彻底剔除上位机垃圾缓存。

---

### 2.2 PIA 4 级单向无环依赖原则

在 `Firmware/` 内部，无论项目大小，目录结构自始至终保持统一，禁止随项目变大而重构目录：

```
[Firmware/App] ──────► [Firmware/Service] ──────► [Firmware/Module] ──────► [Firmware/BSP] ──► [MCU HAL/LL]
      │                        │                          │
      └────────────────────────┴──────────────────────────┘ (允许跨层向下调用，严禁反向引用)
```
* **禁止反向包含**：`BSP` 和 `Module` 头文件严禁 include `App/` 下的文件。
* **禁止业务渗透**：`BSP` 中不得出现具体业务变量或具体外接设备逻辑（如 `bsp_gpio.c` 只提供 `BSP_GPIO_Set()`，不能叫 `BSP_Pump_On()`）。
* **高内聚单文件限制**：单个 `.c` 源文件代码行数严格控制在 **400 行以内**，超过必须根据职责拆分至 Module、Service 或 App。

---

## 3. 三阶平滑演进模型 (Progressive Ladders)

AI 在编写或重构嵌入式代码时，遵循以下三个阶梯逐步往上搭建：

```
[Level 3: 综合协同期] ──► 数据黑板池 + 离线Daemon守护 + 无缝切入RTOS
         ▲
         │ (多路外设/双协议/状态分支增多时)
[Level 2: 模块解耦期] ──► 驱动句柄化(多实例) + 协议帧与业务解耦 + 独立状态机
         ▲
         │ (初始极简原型)
[Level 1: 极简启动期] ──► 统一4目录 + 静态时间片调度表 (零RTOS开销，5分钟闭环)
```

---

### Level 1: 极简启动期 (Minimal Seed)
* **适用**：轻量 MCU（STM32F0/F1/G0）、单路控制、引脚点亮、原型快速调通。
* **核心动作**：
  1. 片上资源只封装最简单的 `BSP` 函数。
  2. 引入仅 30 行 C 代码的**静态时间片调度表**，彻底淘汰裸循环和 `HAL_Delay`。

#### 静态时间片调度器实现模板 (`Service/sys_scheduler.c/.h`)
```c
/* Service/sys_scheduler.h */
#ifndef __SYS_SCHEDULER_H
#define __SYS_SCHEDULER_H
#include <stdint.h>

typedef struct {
    void (*task_func)(void);  /* 任务函数指针 */
    uint32_t interval_ms;     /* 任务执行周期 (ms) */
    uint32_t last_tick;       /* 上次执行时间戳 (ms) */
} TaskNode_t;

void Sys_Scheduler_Init(void);
void Sys_Scheduler_Run(void);
#endif
```

```c
/* Service/sys_scheduler.c */
#include "sys_scheduler.h"
#include "main.h"

/* 声明任务函数 (由 App 或 Module 提供) */
extern void App_Sensor_Process(void);
extern void App_Control_Process(void);
extern void App_Telemetry_Process(void);
extern void App_Heartbeat_Process(void);

/* 静态任务注册表: 周期与优先级一目了然 */
static TaskNode_t s_tasks[] = {
    { App_Sensor_Process,     5,   0 },   /* 200Hz 传感器采集与保护 */
    { App_Control_Process,    10,  0 },   /* 100Hz 核心控制回路 */
    { App_Telemetry_Process,  50,  0 },   /* 20Hz 遥测数据发送 */
    { App_Heartbeat_Process,  500, 0 },   /* 2Hz LED心跳 */
};

#define TASK_NUM (sizeof(s_tasks) / sizeof(TaskNode_t))

void Sys_Scheduler_Init(void) {
    uint32_t now = HAL_GetTick();
    for (uint32_t i = 0; i < TASK_NUM; i++) {
        s_tasks[i].last_tick = now;
    }
}

void Sys_Scheduler_Run(void) {
    uint32_t now = HAL_GetTick();
    for (uint32_t i = 0; i < TASK_NUM; i++) {
        if (now - s_tasks[i].last_tick >= s_tasks[i].interval_ms) {
            s_tasks[i].last_tick = now;
            s_tasks[i].task_func();
        }
    }
}
```
* **主循环契约**：`main.c` 内部的 `while(1)` 仅有一行 `Sys_Scheduler_Run();`。

---

### Level 2: 模块解耦期 (Component Scaling)
* **适用**：控制通道从 1 路扩展至多路、外接 OLED/按键、引入 CAN/串口双通信协议。
* **核心动作**：
  1. **驱动句柄化（Instance Model）**：执行器与传感器抽为结构体句柄，驱动只接受指针，支持实例化多对象。
  2. **协议解包与业务分流**：通信解析只产生“命令事件”，不直接操作执行器硬件。
  3. **独立状态机（FSM）**：建立 `app_fsm.c`，把复杂模式切换收拢为清晰状态。

#### 句柄化设备模型模板 (`Module/actuator_channel.h/.c`)
```c
/* Module/actuator_channel.h */
#ifndef __ACTUATOR_CHANNEL_H
#define __ACTUATOR_CHANNEL_H
#include "main.h"

typedef struct {
    GPIO_TypeDef* pump_port;
    uint16_t      pump_pin;
    GPIO_TypeDef* valve_port;
    uint16_t      valve_pin;
    uint8_t       channel_id;
    uint8_t       cur_pump_state;
    uint8_t       cur_valve_state;
    uint32_t      pulse_vent_end_tick;
} ActuatorChannel_t;

void Actuator_Init(ActuatorChannel_t* dev, uint8_t id, GPIO_TypeDef* p_port, uint16_t p_pin, GPIO_TypeDef* v_port, uint16_t v_pin);
void Actuator_SetOutput(ActuatorChannel_t* dev, uint8_t pump_on, uint8_t valve_on);
void Actuator_TriggerPulseVent(ActuatorChannel_t* dev, uint16_t duration_ms);
void Actuator_Update(ActuatorChannel_t* dev, uint32_t now_ms);
#endif
```
* **无损扩展效果**：增加通道只需在 App 中定义 `ActuatorChannel_t g_channels[3];`，并在初始化时绑定引脚，底层驱动代码不需要改写任何一行。

---

### Level 3: 综合协同期 (System Enterprise)
* **适用**：复杂系统交互（通信、显示、主控频繁共享变量）、外设多节点网络、高可靠安全离线自保、无缝切入 RTOS。
* **核心动作**：
  1. **统一数据黑板（Blackboard Pool）**：消灭各模块之间散落的 `extern` 全局变量，数据流动分为：`输入 -> 黑板 -> 控制 -> 黑板 -> 输出`。
  2. **离线守护计数器（Daemon）**：为所有外部输入绑定心跳计时器，一旦失联自动切断输出并告警。
  3. **平滑 RTOS 映射**：由于 `s_tasks[]` 已经是纯周期函数，随时可直接包装为 `xTaskCreate`。

#### 数据黑板实现模板 (`Service/sys_blackboard.h`)
```c
/* Service/sys_blackboard.h */
#ifndef __SYS_BLACKBOARD_H
#define __SYS_BLACKBOARD_H
#include <stdint.h>

/* 权限规约:
 * input:    仅由通信解析 (CAN/UART/按键) 写入
 * feedback: 仅由传感器/驱动采集 (ADC/编码器) 写入
 * status:   仅由主控业务状态机 (FSM) 写入
 * telemetry:仅由上报任务读取
 */
typedef struct {
    struct {
        uint8_t  target_pump[3];
        uint8_t  target_valve[3];
        uint8_t  cmd_mode;
        uint16_t overload_threshold_mv;
    } input;

    struct {
        uint16_t voltage_mv[3];
        uint8_t  fault_latch[3];
        uint8_t  comm_online;
    } feedback;

    struct {
        uint8_t  sys_state;
        uint8_t  oled_page;
        uint32_t uptime_sec;
    } status;
} SystemBlackboard_t;

extern SystemBlackboard_t g_blackboard;
#endif
```

#### 极简离线守护实现模板 (`Service/sys_daemon.c/.h`)
```c
/* Service/sys_daemon.h */
#ifndef __SYS_DAEMON_H
#define __SYS_DAEMON_H
#include <stdint.h>

typedef struct {
    uint32_t counter;
    uint32_t timeout_reload;
    uint8_t  is_offline;
    void (*offline_callback)(void);
} DaemonNode_t;

void Daemon_Feed(DaemonNode_t* node);
void Daemon_Tick(DaemonNode_t* node, uint32_t step_ms);
#endif
```

---

## 4. AI 编码戒律与静态规约检查

为保证 AI 生成的工程始终具备高内聚低耦合的架构品质，必须强制执行以下军规：

| 检查项 | 强制标准 | 违反后果与处置 |
| :--- | :--- | :--- |
| **单文件行数限制** | 单个 `.c` 文件代码行数严禁超过 **400 行** | 必须拆分为独立的设备驱动（`Module/`）或服务（`Service/`）。 |
| **单向依赖规约** | `BSP` 与 `Module` 严禁 `#include "app_*.h"` | 立即阻断，改由句柄传参或黑板数据解耦。 |
| **零裸延时** | 禁止在任何非初始化阶段调用 `HAL_Delay` | 必须改用非阻塞时间戳差值或时间片调度器。 |
| **禁止散落 extern** | 业务模块间严禁直接 `extern` 对方私有变量 | 统一纳入 `SystemBlackboard_t` 集中管理。 |
| **全通道防呆互锁** | 执行器（如气泵与泄气阀）在驱动层必须具备物理互锁保护 | 软件层强制自保，杜绝硬件直通损坏。 |

---

## 5. 工程完整物理布局与轻量化节点备份规约

### 5.1 严苛的工程目录物理结构
未来所有单片机工程必须严格遵守以下目录与文件布局，禁止在根目录下散落临时代码：

```text
Project_Root/
├── BSP/                  /* 片上硬件外设适配层 (bsp_gpio, bsp_can, bsp_uart, bsp_dma...) */
├── Module/               /* 外接设备句柄对象与独立算法 (执行器、传感器、屏幕驱动、按键、PID) */
├── Service/              /* 核心服务层 (sys_scheduler 任务表、sys_blackboard 黑板、sys_daemon 守护) */
├── App/                  /* 业务逻辑状态机 (app_fsm 状态机、app_safety 安全保护、app_ui) */
├── Core/                 /* CubeMX 初始生成的片上初始化代码 (main.c, stm32f1xx_it.c 等) */
├── Drivers/              /* STM32 原厂 HAL 驱动库与 ARM CMSIS 头文件 */
├── _checkpoints/         /* 关键功能逐个跑通与大变动前的节点复位快照区 */
├── SOFTWARE_SPEC.md      /* 规范化软件说明书 (含引脚映射、调度表、状态机与升级规划) */
└── [ProjectName].ioc     /* STM32CubeMX 芯片引脚与时钟树硬件配置文件 */
```

### 5.2 轻量化节点复位快照机制 (Milestone Checkpoint)
为了在功能逐个调试跑通以及重大重构前“完美保留节点进度”，同时杜绝数百兆编译缓存造成的磁盘膨胀，采用**轻量化选择性快照机制**：

1. **触发时机**：
   * **功能逐个跑通时**：如调通了 ADC DMA 连续采样、调通了 CAN 0x501 闭环控制、调通了 OLED 页面刷新后，立即留痕；
   * **执行重大破坏性重构前**：如单文件重构为多模块、变更通信协议结构体前。
2. **过滤膨胀缓存 (节省 99%+ 空间)**：
   * 严禁打包 Keil/GCC 编译产生的海量临时文件（`*.o`, `*.crf`, `*.d`, `*.axf`, `*.htm`, `*.map`, `.ipch`）以及 `.git`, `.venv`。
   * 单个节点体积由通常的 150~300 MB 缩减至 **200~400 KB**。
3. **快照包核心内容**：
   * 源码目录快照：`App/`, `Module/`, `Service/`, `BSP/`, `Core/Inc/`, `Core/Src/`；
   * 硬件工程定义：`*.ioc`, 项目工程文件 (`.uvprojx`, `CMakeLists.txt`)；
   * 编译固件：只保留已测通过的单一最终发布固件 (`*.hex` 或 `*.bin`)；
   * 节点说明书：`CHECKPOINT_NOTE.md`（包含功能测试结论与关键修改项）；
   * 一键复位脚本：自动生成 `RESTORE.ps1`，双击或单行命令即可秒级无损还原工作区。
4. **自动化命令**：
   * 创建节点：`python embedded_checkpoint.py <workspace> create <tag_name> [note]`
   * 查看节点：`python embedded_checkpoint.py <workspace> list`

