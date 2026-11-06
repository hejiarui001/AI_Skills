# Industrial Serial Reference & Best Practices

This guide describes how to operate COM ports safely and reliably when interacting with microcontrollers and embedded devices.

---

## 1. 端口互斥与安全原则 (Port Exclusivity)

* Windows 下串口句柄是排他的（Exclusive Lock）。同一时间只有一个进程能打开特定的 COM 口。
* **VOFA+ 与终端协同**：
  * 当用户正在使用 VOFA+ 查看波形或使用 MobaXterm 时，COM 口会被占用。
  * `serial_tool.py` 严格遵循 **即开、即测、即关** 原则，在 `finally` 块中确保端口被释放，绝不长期霸占 COM 口。
  * 若出现 `Access is denied` 或端口打开失败，优先提示用户检查 VOFA+ 是否处于连接状态。

---

## 2. 常见硬件识别特征

* **ST-Link VCP**: 描述通常包含 `STMicroelectronics STLink Virtual COM Port`，VID 为 `0x0483`。
* **CH340 / CH341**: 描述通常为 `USB-SERIAL CH340`，VID 为 `0x1A86`。
* **CP210x**: 描述通常为 `Silicon Labs CP210x USB to UART Bridge`，VID 为 `0x10C4`。
* **FTDI**: 描述通常包含 `FT232R` 或 `USB Serial Port`，VID 为 `0x0403`。
