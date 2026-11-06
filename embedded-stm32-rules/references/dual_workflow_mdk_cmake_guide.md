# STM32 双工作流工程体系规范 (MDK-ARM + Modern CMake Dual-Engine Guide)

> **适用场景**：既需要使用 CubeMX + VSCode + Keil AC6（传统 MDK 闭环），又需要使用 CubeMX + VSCode + CMake + Ninja / GCC（现代高并发构建与 Clangd 代码补全）的 STM32 研发体系。  
> **核心目标**：实现**同一套工程源码、同一个 `Firmware/` 核心**，同时支持 MDK-ARM 与 CMake 双向一键无头构建，且在 CubeMX 多次重新生成外设代码时，业务架构 100% 免疫覆写。

---

## 1. 痛点分析与解耦设计原则 (Core Principles)

在常规嵌入式开发中，MDK 与 CMake 往往是相互排斥的孤岛：
1. **CubeMX 覆写风险**：CubeMX 重新配置引脚或时钟并点击 `Generate Code` 时，会直接重写根目录的 `CMakeLists.txt` 或覆盖工程配置文件，冲掉开发者手动添加的源文件和编译参数。
2. **工具链与宏定义割裂**：Keil ArmClang (AC6) 与 GNU GCC (`arm-none-eabi-gcc`) 在紧凑结构体 (`__packed`)、内联汇编、CMSIS-DSP 静态库格式（`.lib` vs `.a`）上存在微小语法差异，导致代码难以两套编译器无缝通调。
3. **环境切换成本高**：开发者习惯在 VSCode 中享受现代编辑器的补全与跳转，但受限于团队交付需要提交 `.uvprojx`。

### PIA 双引擎解耦架构
通过将构建系统视为外壳、将业务逻辑收敛进 [`Firmware/`](file:///Firmware/)，实现如下架构拓扑：

```
Project_Root/
├── Core/                      <-- [CubeMX 原厂桩] 仅包含 main.c, stm32h7xx_it.c, 外设初始化
├── Drivers/                   <-- [原厂 BSP/HAL] CMSIS 核心库与 HAL 驱动库
├── MDK-ARM/                   <-- [工作流 1 入口] *.uvprojx 工程与无头脚本 build.ps1
├── cmake/                     <-- [工作流 2 工具链] gcc-arm-none-eabi.cmake 交叉编译配置
├── CMakeLists.txt             <-- [工作流 2 入口] 顶级 CMake 配置（CubeMX 托管）
├── Firmware/                  <-- [PIA 纯净核心] 业务与驱动代码，两套工具流完全共享
│   ├── App/                   <-- 系统状态机与核心业务编排
│   ├── Module/                <-- 传感器/执行器实例句柄驱动（OLED, DDS, 编码器等）
│   ├── Service/               <-- 时间片调度器、VOFA+ 遥测、算法滤波、信号分析
│   ├── BSP/                   <-- 片上外设轻量原子抽象（GPIO, UART, ADC 差分接口）
│   └── CMakeLists.txt         <-- [Firmware 专属构建] 声明独立的静态库或源码注入
├── SOFTWARE_SPEC.md           <-- 软件规格说明书（接口定义、引脚分配、任务周期）
└── TASK.md                    <-- 任务流与调试指令看板
```

---

## 2. 工作流 1：MDK-ARM (Keil AC6) 配置标准

适用于需要使用 MicroLIB 超轻量化运行时、需要交付标准 Keil 工程或使用 Keil 专用硬件调试器的场景。

### 2.1 UVPROJX 虚拟 Group 挂载
在 `MDK-ARM/*.uvprojx` 中，为 `Firmware` 创建 4 个虚拟 Group：
- `Firmware/App`
- `Firmware/Module`
- `Firmware/Service`
- `Firmware/BSP`
头文件包含路径加入：
```text
../Firmware/App;../Firmware/Module;../Firmware/Service;../Firmware/BSP
```

### 2.2 自动化无头构建脚本 (`build.ps1`)
在 `MDK-ARM/` 目录下放置专用 PowerShell 构建脚本，直接调用 ArmClang 6 编译器进行高速无头构建并生成 `.hex`：

```powershell
# 工具链路径常量（对齐本地环境）
$ARMCLANG = "E:\Keil ARM\MDK_ARM\ARM\ARMCLANG\Bin\armclang.exe"
$ARMASM   = "E:\Keil ARM\MDK_ARM\ARM\ARMCLANG\Bin\armasm.exe"
$ARMLINK  = "E:\Keil ARM\MDK_ARM\ARM\ARMCC\bin\armlink.exe"  # 使用 Linker V5.06 规避 L6907E
$FROMELF  = "E:\Keil ARM\MDK_ARM\ARM\ARMCLANG\Bin\fromelf.exe"

# 编译参数
$CFLAGS = @("-xc", "-std=c99", "--target=arm-arm-none-eabi", "-mcpu=cortex-m7", "-mfpu=fpv5-sp-d16", "-mfloat-abi=hard", "-c", "-fno-rtti", "-funsigned-char", "-fshort-enums", "-fshort-wchar", "-D__MICROLIB", "-DSTM32H750xx", "-DUSE_HAL_DRIVER", "-O2")
```

---

## 3. 工作流 2：Modern CMake (GCC + Ninja) 配置标准

适用于日常沉浸式开发、毫秒级增量编译构建、VSCode `clangd` 高精度语法智能提示、以及 CI/CD 自动化流水线。

### 3.1 交叉编译工具链定义 (`cmake/gcc-arm-none-eabi.cmake`)
```cmake
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)

# 自动绑定本地 STM32CubeCLT 工具链或环境变量路径
if(NOT TOOLCHAIN_PREFIX)
    if(EXISTS "E:/Tools/STM32CubeCLT_1.22.0/GNU-tools-for-STM32/bin/arm-none-eabi-gcc.exe")
        set(TOOLCHAIN_PREFIX "E:/Tools/STM32CubeCLT_1.22.0/GNU-tools-for-STM32/bin/arm-none-eabi-")
    else()
        set(TOOLCHAIN_PREFIX "arm-none-eabi-")
    endif()
endif()

set(CMAKE_C_COMPILER "${TOOLCHAIN_PREFIX}gcc.exe")
set(CMAKE_ASM_COMPILER "${TOOLCHAIN_PREFIX}gcc.exe")
set(CMAKE_CXX_COMPILER "${TOOLCHAIN_PREFIX}g++.exe")
set(CMAKE_OBJCOPY "${TOOLCHAIN_PREFIX}objcopy.exe")
set(CMAKE_SIZE "${TOOLCHAIN_PREFIX}size.exe")

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
```

### 3.2 根目录 `CMakeLists.txt` 的解耦挂载
无论根目录 `CMakeLists.txt` 是手写还是 CubeMX 生成，在文件末尾通过非侵入方式接入 `Firmware`：

```cmake
# ==============================================================================
# PIA Architecture User Firmware Injection (Safe from CubeMX Regeneration)
# ==============================================================================
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/Firmware/CMakeLists.txt")
    add_subdirectory(Firmware)
    target_link_libraries(${CMAKE_PROJECT_NAME} PRIVATE Firmware_Core)
endif()
```

### 3.3 `Firmware/CMakeLists.txt` 模块定义
在 `Firmware/CMakeLists.txt` 中自给自足地收集所有业务代码与头文件路径：

```cmake
add_library(Firmware_Core STATIC)

file(GLOB_RECURSE FIRMWARE_SOURCES
    "${CMAKE_CURRENT_SOURCE_DIR}/App/*.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/Module/*.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/Service/*.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/BSP/*.c"
)

target_sources(Firmware_Core PRIVATE ${FIRMWARE_SOURCES})

target_include_directories(Firmware_Core PUBLIC
    "${CMAKE_CURRENT_SOURCE_DIR}/App"
    "${CMAKE_CURRENT_SOURCE_DIR}/Module"
    "${CMAKE_CURRENT_SOURCE_DIR}/Service"
    "${CMAKE_CURRENT_SOURCE_DIR}/BSP"
    "${CMAKE_CURRENT_SOURCE_DIR}/../Core/Inc"
    "${CMAKE_CURRENT_SOURCE_DIR}/../Drivers/STM32H7xx_HAL_Driver/Inc"
    "${CMAKE_CURRENT_SOURCE_DIR}/../Drivers/CMSIS/Device/ST/STM32H7xx/Include"
    "${CMAKE_CURRENT_SOURCE_DIR}/../Drivers/CMSIS/Include"
)
```

---

## 4. 编译器跨平台代码编写规约 (Portability Rules)

为保证一套 C 代码在 ArmClang (AC6) 与 GNU GCC 下均能无告警编译，必须遵循以下规约：

### 4.1 紧凑结构体 (`packed`) 统一写法
严禁使用 Keil 特有的 `__packed struct Foo { ... };`。统一采用 CMSIS 标准宏或 GCC 标准属性：
```c
#include "cmsis_compiler.h"

// 方案 A：使用 CMSIS 标准包装宏
__PACKED_STRUCT PacketHeader {
    uint8_t frame_head;
    uint16_t length;
};

// 方案 B：使用标准属性定义
struct __attribute__((packed)) TelemetryFrame {
    uint8_t id;
    float value;
};
```

### 4.2 强制内联与对齐
- 统一使用 `__STATIC_FORCEINLINE` 或 `__STATIC_INLINE`（由 `cmsis_compiler.h` 跨平台支持）。
- 内存对齐统一使用 `__ALIGNED(4)`，例如 DMA 缓冲区：
```c
uint8_t dma_rx_buffer[256] __ALIGNED(32); // Cortex-M7 D-Cache 32字节对齐
```

### 4.3 阻塞式 IO 桩函数解耦
严禁重写 `fputc(int ch, FILE *f)` 或 `__io_putchar(int ch)` 挂死单一编译器。统一在 `Firmware/BSP/bsp_uart.c` 中提供纯净的 `BSP_UART_SendString(const char *str)` 及 `vofa_telemetry.c` 二进制打包器。

---

## 5. CubeMX 重新生成代码的安全工作流 (Regeneration SOP)

当需要修改引脚、开启新的硬件定时器或修改系统主频时：

1. **CubeMX 操作**：
   - 在 `.ioc` 中完成硬件配置修改；
   - 点击 `GENERATE CODE`（无论选择生成 MDK-ARM 还是 CMake）。
2. **安全隔离检查**：
   - `Core/Src/main.c` 中的初始化注入点必须严格写在 `/* USER CODE BEGIN 2 */` 与 `/* USER CODE END 2 */` 之间：
     ```c
     /* USER CODE BEGIN 2 */
     AllIn_App_Init();
     /* USER CODE END 2 */
     ```
   - `while (1)` 中的调度执行点严格写在 `/* USER CODE BEGIN 3 */` 与 `/* USER CODE END 3 */` 之间：
     ```c
     /* USER CODE BEGIN WHILE */
     while (1)
     {
         AllIn_App_Task();
     /* USER CODE END WHILE */
     /* USER CODE BEGIN 3 */
     }
     /* USER CODE END 3 */
     ```
   - 检查顶级 `CMakeLists.txt` 末尾是否依然包含 `add_subdirectory(Firmware)`，若被 CubeMX 还原，只需单行恢复。
3. **双构建验证**：
   - 运行 MDK 构建：`powershell ./MDK-ARM/build.ps1`
   - 或运行 CMake 构建：`cmake --build build -j`
   - 确保两套构建流程输出的固件功能 100% 对齐。
