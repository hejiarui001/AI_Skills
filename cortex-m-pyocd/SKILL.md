---
name: cortex-m-pyocd
version: 1.1.0
description: >-
  Controls ARM Cortex-M firmware programming, chip erasing, target discovery, and
  hardware debugging using pyOCD across Windows and Linux environments.
  Trigger on: "pyocd", "flash firmware", "st-link", "cmsis-dap", "daplink", "erase chip", "mcu debug", "burn hex".
license: Apache-2.0
metadata:
  version: v1.1.0
  role: Micro Execution Skill
---

# ARM Cortex-M 硬件调试与固件烧录 (pyOCD) v1.1

支持 Windows 11 与 Linux (Ubuntu) 双操作系统无缝自适应调用的硬件探针控制中枢。

---

## 1. 跨平台可执行程序动态定位 (Cross-Platform Execution)

* **Windows 11**：优先使用 `E:\Tools\pyocd\pyocd.exe`；若不存在，降级调用系统 PATH 中的 `pyocd`；
* **Linux (Ubuntu)**：直接调用系统 PATH 中的 `pyocd` 或 `~/.local/bin/pyocd`；
* **Linux 权限前置**：核验用户是否加入 `plugdev` 组并配置 udev 规则（`/etc/udev/rules.d/49-stlinkv2.rules`）。

---

## 2. 核心控制工作流 (SOP)

### 2.1 探测调试器探针与硬件连接
```bash
# Windows (PowerShell)
& "E:\Tools\pyocd\pyocd.exe" list

# Linux (Bash)
pyocd list
```

### 2.2 固件烧录 (Flashing)
```bash
# 烧录 hex 文件 (带芯片型号声明)
pyocd flash -t stm32f407ve "path/to/firmware.hex"

# 烧录 bin 文件 (指定 0x08000000 偏移)
pyocd flash -t stm32f407ve -a 0x08000000 "path/to/firmware.bin"
```

### 2.3 全片擦除与解除低功耗/死锁 (Erase & Unlock)
```bash
pyocd erase -t stm32f407ve --chip
```

### 2.4 复位目标板 (Reset)
```bash
pyocd reset -t stm32f407ve
```
