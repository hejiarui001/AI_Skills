---
name: cortex-m-pyocd
version: 1.0.0
description: >-
  Controls ARM Cortex-M firmware programming, chip erasing, target discovery, and
  hardware debugging using pyOCD (located at E:\Tools\pyocd\pyocd.exe). Use when the
  user asks to flash firmware (.bin, .hex, .elf) to STM32 or other Cortex-M microcontrollers,
  detect connected debug probes (ST-Link, CMSIS-DAP, J-Link), erase flash, or read MCU memory.
license: Apache-2.0
metadata:
  version: v1.0.0
  author: ARM-pyOCD
---

# ARM Cortex-M Hardware Flashing & Debugging (pyOCD)

This skill enables the agent to interface with physical hardware, programming and debugging microcontrollers via ST-Link, CMSIS-DAP, or J-Link debug probes.

---

## 1. Tool Path & Environment

* **Executable**: `E:\Tools\pyocd\pyocd.exe`
* **Version**: `0.46.0` (Official ARM release)
* **Supported Probes**: ST-Link (v2, v2-1, v3), CMSIS-DAP / DAPLink, J-Link.

---

## 2. Core Operational Workflows (SOP)

### 2.1 检查调试探针与连接状态
在执行任何烧录或擦除前，必须先检测调试器连接：
```powershell
& 'E:\Tools\pyocd\pyocd.exe' list
```
* 若输出 `No available debug probes are connected`，提示用户检查 ST-Link 是否插好、USB 接口是否松动或驱动是否正常。

### 2.2 固件烧录 (Flashing)
支持 `.bin`、`.hex`、`.elf` 格式直接烧录：
```powershell
# 烧录 hex 文件 (自动处理偏移地址)
& 'E:\Tools\pyocd\pyocd.exe' flash -t stm32f407ve "path\to\firmware.hex"

# 烧录 bin 文件 (需显式指定起始地址，通常为 0x08000000)
& 'E:\Tools\pyocd\pyocd.exe' flash -t stm32f407ve -a 0x08000000 "path\to\firmware.bin"
```

### 2.3 全片擦除与解除死锁 (Erase & Unlock)
当单片机程序跑飞、进低功耗模式失联或写保护锁死时执行：
```powershell
& 'E:\Tools\pyocd\pyocd.exe' erase -t stm32f407ve --chip
```

### 2.4 复位单片机 (Reset)
```powershell
& 'E:\Tools\pyocd\pyocd.exe' reset -t stm32f407ve
```

### 2.5 芯片支持包管理 (Pack Management)
如果目标芯片型号提示不支持，可通过 pyocd 自动安装对应的 CMSIS-Pack：
```powershell
# 查找支持包
& 'E:\Tools\pyocd\pyocd.exe' pack find stm32f407
# 安装对应芯片支持包
& 'E:\Tools\pyocd\pyocd.exe' pack install stm32f407ve
```

---

## 3. 安全防护守则

* 在执行烧录前，先确认目标固件文件的绝对路径存在；
* 若目标 MCU 型号未指明，优先参考用户当前工程的 `.ioc` 芯片定义（例如 STM32F407VET6 -> `stm32f407ve`）。
