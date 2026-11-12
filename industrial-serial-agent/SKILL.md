---
name: industrial-serial-agent
version: 1.2.0
description: >-
  Industrial-grade serial (UART / COM port) device discovery, command transmission,
  frame parser, and VOFA+ telemetry log capture across Windows and Linux environments.
  Trigger on: "serial", "uart", "com port", "vofa+", "ttyUSB", "ttyACM", "baudrate", "send command".
license: Apache-2.0
metadata:
  version: v1.2.0
  role: Micro Execution Skill
---

# 工业级串口通信与 VOFA+ 遥测控制 (Industrial Serial Agent) v1.2

基于 `pyserial` (`scripts/serial_tool.py`) 实现 Windows (`COM*`) 与 Linux (`/dev/ttyUSB*`, `/dev/ttyACM*`) 跨平台串口扫描、指令下发与数据抓包。

## 1. 跨平台端口发现与避坑规范

* **Windows 11**：自动化扫描必须附加 `--exclude-bt` 过滤 HWID 含 `BTHENUM`/`BLUETOOTH` 的蓝牙虚拟 SPP 串口，防止尝试打开时阻塞超时。
* **Linux (Ubuntu)**：识别 `/dev/ttyUSB*` 与 `/dev/ttyACM*`；遇 `Permission denied` 时引导执行 `sudo usermod -aG dialout $USER` 并重新登录。
* **端口冲突**：若返回串口被占用，先关闭 VOFA+、MobaXterm 或工程 PyQt5 上位机。

## 2. 验证可用的 `scripts/serial_tool.py` 标准子命令

```bash
# 1. 列出真实硬件串口（自动标记并跳过 BTHENUM 蓝牙虚拟口）
python scripts/serial_tool.py list --exclude-bt

# 2. 抓取开机自检或 VOFA+ 启动日志 (默认 115200bps，监听 5 秒)
python scripts/serial_tool.py capture COM5 -b 115200 -d 5.0
python scripts/serial_tool.py capture /dev/ttyACM0 -b 115200 -d 5.0

# 3. 发送 ASCII 文本控制指令并等待回传 JSON 结果 (response_text / response_hex)
python scripts/serial_tool.py send COM5 "PING\r\n" -b 115200 -t 2.0

# 4. 发送 HEX 原始协议帧 (如 25 字节自定义遥控遥测查询帧)
python scripts/serial_tool.py send COM5 "AA 55 02 01 01 00 0D 0A" --hex -b 115200
```

* **VOFA+ `JustFloat` 协议尾帧提示**：多通道浮点二进制协议以 4 字节小端无穷大标志 `\x00\x00\x80\x7F` 结尾，可用 `capture` 或 `send` 返回字段 `response_hex` 核对帧边界。
