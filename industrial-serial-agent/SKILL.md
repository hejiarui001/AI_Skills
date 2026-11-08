---
name: industrial-serial-agent
version: 1.1.0
description: >-
  Industrial-grade serial (UART / COM port) device discovery, command transmission,
  frame parser, and VOFA+ telemetry log capture across Windows and Linux environments.
  Trigger on: "serial", "uart", "com port", "vofa+", "ttyUSB", "ttyACM", "baudrate", "send command".
license: Apache-2.0
metadata:
  version: v1.1.0
  role: Micro Execution Skill
---

# 工业级串口通信与 VOFA+ 遥测控制 (Industrial Serial Agent) v1.1

基于 Python `pyserial` 驱动，支持 Windows 11 与 Linux (Ubuntu) 双系统自适应串口探测与帧解析通道。

---

## 1. 跨平台串口设备探测 (Port Discovery)

* **Windows 11**：自动扫描 `COM*` 端口（结合设备管理器 VID:PID 识别 CH340, CP2102, FTDI, STM32 Virtual COM）；
* **Linux (Ubuntu)**：自动扫描 `/dev/ttyUSB*` 与 `/dev/ttyACM*`；
  * 若出现 `Permission denied`，提示用户执行：`sudo usermod -aG dialout $USER`。

---

## 2. 核心工作流与 CLI 交互 (SOP)

### 2.1 快速端口扫描
```bash
python scripts/serial_tool.py --list
```

### 2.2 监听遥测并抓取启动日志
```bash
python scripts/serial_tool.py --port COM3 --baud 115200 --duration 10
# Linux 示例:
python scripts/serial_tool.py --port /dev/ttyUSB0 --baud 115200 --duration 10
```

### 2.3 发送控制指令或十六进制数据帧
```bash
python scripts/serial_tool.py --port COM3 --baud 115200 --send "AT+RST\r\n"
```
