---
name: industrial-serial-agent
description: >-
  Provides industrial-grade serial (UART / COM port) device discovery, command transmission,
  and log capture using pyserial (3.5k+ stars). Use when the user asks to scan available COM
  ports, test communication with a microcontroller (STM32, ESP32, Arduino), send AT commands
  or custom data frames, or capture and diagnose MCU serial boot logs.
license: Apache-2.0
metadata:
  version: v1.0.0
  author: pyserial-industrial
---

# Industrial Serial Diagnostic Agent

This skill enables the agent to interface with physical hardware over serial/UART COM ports safely and reliably, adhering to strict port exclusivity rules so as not to interfere with external tools like VOFA+ or MobaXterm.

---

## 1. Operating Procedures (SOP)

### 1.1 扫描检测可用端口
```bash
python "C:\Users\hejia\.gemini\config\skills\industrial-serial-agent\scripts\serial_tool.py" list
```
* 自动输出系统内所有 COM 端口、硬件描述（如 ST-Link VCP, CH340）与 VID/PID。

### 1.2 发送指令并等待回显 (Send & Receive)
```bash
# 默认 115200 波特率发送 ASCII 指令
python "C:\Users\hejia\.gemini\config\skills\industrial-serial-agent\scripts\serial_tool.py" send COM3 "AT\r\n" -b 115200 -t 2.0

# 发送十六进制数据帧
python "C:\Users\hejia\.gemini\config\skills\industrial-serial-agent\scripts\serial_tool.py" send COM3 "AA BB 01 02 FF" --hex -b 115200
```

### 1.3 捕获运行日志 (Capture Log Stream)
在固件刚烧录完成或单片机刚复位时，抓取启动日志：
```bash
python "C:\Users\hejia\.gemini\config\skills\industrial-serial-agent\scripts\serial_tool.py" capture COM3 -b 115200 -d 3.0
```
* 抓取完成后自动安全关闭端口，并将日志文本返回供 Agent 分析是否有 HardFault 或初始化异常。

---

## 2. 关键防护与协同

* **即开即关**：操作完成后端口立即释放，确保用户随时可以打开 VOFA+ 继续看波形。
* **冲突提示**：若打开端口失败，提示用户检查是否在其他串口助手中打开了该端口。
