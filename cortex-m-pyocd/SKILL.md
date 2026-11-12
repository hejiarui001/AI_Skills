---
name: cortex-m-pyocd
version: 1.2.0
description: >-
  Controls ARM Cortex-M firmware programming, chip erasing, target discovery, and
  hardware debugging using pyOCD across Windows and Linux environments.
  Trigger on: "pyocd", "flash firmware", "st-link", "cmsis-dap", "daplink", "erase chip", "mcu debug", "burn hex".
license: Apache-2.0
metadata:
  version: v1.2.0
  role: Micro Execution Skill
---

# ARM Cortex-M 硬件调试与固件烧录 (pyOCD) v1.2

支持 Windows 11 与 Linux (Ubuntu) 双平台的 ARM Cortex-M 探针发现、固件烧录、芯片擦除与 SWD 锁死救援。

## 1. 跨平台可执行程序动态解析

* **Windows (PowerShell)**：依次探测 `$env:PYOCD_EXE` -> `E:\Tools\pyocd\pyocd.exe` -> 系统 PATH `pyocd` -> `python -m pyocd`：
  ```powershell
  $PYOCD = @($env:PYOCD_EXE, "E:\Tools\pyocd\pyocd.exe", (Get-Command pyocd -ErrorAction SilentlyContinue | ForEach-Object Source)) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
  if (-not $PYOCD) { $PYOCD = "python"; $PYOCD_PREFIX = @("-m", "pyocd") } else { $PYOCD_PREFIX = @() }
  ```
* **Linux (Bash)**：使用 `pyocd` 或 `python3 -m pyocd`；前置核验用户在 `plugdev` 组并已加载 udev 规则（如 `/etc/udev/rules.d/49-stlinkv2.rules`）。

## 2. 核心 CLI 指令 (SOP)

```bash
# 1. 探测已连接调试探针 (ST-Link / CMSIS-DAP / DAPLink) 与支持的芯片名
pyocd list
pyocd list --targets   # 查询精确 target 标识符

# 2. 烧录固件 (.hex 自带基址；.bin 需附 -a；非内置芯片可附 --pack <file.pack>)
pyocd flash -t stm32f407ve "path/to/firmware.hex"
pyocd flash -t stm32f103c8 -a 0x08000000 "path/to/firmware.bin"

# 3. SWD 失联 / 休眠 / 引脚复用锁死救援 (Under-Reset 连接 + 擦除)
pyocd flash -t stm32f103c8 -M under-reset -e chip "path/to/firmware.hex"
pyocd erase -t stm32f407ve --chip -M under-reset

# 4. 硬件复位目标板
pyocd reset -t stm32f407ve
```

## 3. 常见故障快速定位

| 现象 | 排查与处置 |
| :--- | :--- |
| `No connected debug probes` | 检查 USB 线供电/接触；关闭占用探针的 Keil / STM32CubeProgrammer |
| `TransferFault` / SWD 连不上 | 芯片进入低功耗休眠或复用了 PA13/PA14：改用 `-M under-reset` 并确认 NRST 接线或短接复位上电 |
| 烧录前电压检测失败 | 探针 VREF/TVCC 需接目标板 3.3V，不能悬空 |
