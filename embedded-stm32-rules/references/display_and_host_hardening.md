# ST7789/SPI 显示驱动与 PyQt5 上位机工程加固规约

> **适用场景**：STM32 / ESP32-C6 SPI TFT 显示屏（ST7789 等）几何校准与局部刷新优化，以及 Windows/Linux PyQt5 工业测控上位机的防闪退、串口过滤与启动脚本加固。

---

## 1. ST7789 / SPI TFT 驱动与刷新铁律

### 1.1 `MADCTL (0x36)` 方向矩阵与宽高/偏移耦合
改变屏幕旋转方向 (`Dir 0~3`) 时，必须同步切换逻辑 `width`/`height` 与显存坐标偏移 `x_offset`/`y_offset`（一旦 `MV=1` 发生行列交换，分辨率与偏移必须成对转置）：

| `dir` | 物理方向 | `MADCTL (0x36)` | 位含义 (`MY, MX, MV`) | 分辨率 (以 240x320 为例) |
| :---: | :--- | :---: | :--- | :---: |
| `0` | 0° 竖屏 | `0x00` | `MY=0, MX=0, MV=0` | `240 x 320` |
| `1` | 90° 横屏 | `0x70` | `MY=0, MX=1, MV=1` (`ML=0`) | `320 x 240` |
| `2` | 180° 倒置竖屏 (PCB 常用) | `0xC0` | `MY=1, MX=1, MV=0` | `240 x 320` |
| `3` | 270° 横屏 | `0xA0` | `MY=1, MX=0, MV=1` | `320 x 240` |

* **颜色极性与通道顺序**：IPS 面板通常需开启反色 `0x21`（非 IPS 用 `0x20`）；若红蓝反色，将 `MADCTL` 位 `[3]` (`BGR = 0x08`) 取反。
* **8-bit SPI RGB565 字节序**：在 `COLMOD (0x3A) = 0x55`（16-bit/pixel）8 位 SPI 总线下，必须**先发高字节 `(uint8_t)(color >> 8)`，再发低字节 `(uint8_t)(color & 0xFF)`**。
* **片选释放时序**：`BSP_SPI_SetCS(1)` 拉高 `CS` 前必须等待硬件 `SPI_FLAG_BSY == 0`，防止尾像素在移位寄存器尚未发完时被截断。

### 1.2 差分局部刷新与 DMA 分片上限保护
1. **脏矩形/状态差分渲染 (`app_ui.c`)**：UI 主循环（如 20Hz `Task_UI`）禁止全屏 `ST7789_Clear()` 重绘导致闪烁与带宽浪费；必须通过 `static last_*` 记录上一次选中项或遥测数值，仅对变更区域调用 `ST7789_SetWindow(x1 + x_offset, y1 + y_offset, ...)` 局部重绘。
2. **SPI DMA 单次事务上限保护**：若使用带硬件 DMA 单包长度限制的 MCU（如 ESP32-C6 GPSPI 单次事务上限 `32 KB` / `SPI_DMA_CHUNK_SIZE`），全屏帧缓冲传输必须自动分块循环提交。
3. **单帧 vs 双帧内存权衡**：Wi-Fi/BLE 等大堆场景优先保留 `FRAME_BUFFER_COUNT = 1` + 串行同步刷新，避免双缓冲额外占用几十 KB 静态 RAM 挤占协议栈 DMA 堆；切换异步双缓冲前必须重新设计缓冲所有权锁定机制。
4. **单模式枚举契约 (`UiMode_t`)**：显示模式与菜单状态必须在中央黑板或协议头文件中用枚举显式定义，架构重整后物理删除历史轮播模式与旧状态映射代码。

---

## 2. PyQt5 工业上位机防闪退与启动加固规范

### 2.1 启动锚定与 `pythonw.exe` 全局异常兜底 (`main.py`)
1. **强制锁定工作目录**：入口首行执行：
   ```python
   current_dir = os.path.dirname(os.path.abspath(__file__))
   os.chdir(current_dir)
   ```
   防止从外部脚本或其它工作目录拉起时，相对路径找不到 `.ui`、样式表或配置文件。
2. **`pythonw.exe` 空流保护与 `sys.excepthook`**：无控制台运行时 `sys.stdout`/`sys.stderr` 可能为 `None`，需先检查或重定向；同时注册 `sys.excepthook`，将未捕获异常追加写入 `crash.log`，优先弹出 `QMessageBox.critical`，若 Qt 尚未就绪则降级调用 `ctypes.windll.user32.MessageBoxW` 报错，彻底杜绝无黑框静默闪退。

### 2.2 蓝牙虚拟串口过滤 (`BTHENUM`)
Windows 设备管理器常存在蓝牙虚拟 SPP COM 口（HWID 含 `BTHENUM` / `BLUETOOTH`，描述含 `蓝牙` / `Bluetooth`），在 Qt/pyserial 探测扫描时极易阻塞卡死。上位机下拉扫描与 CLI 探测均应过滤或显式标记此类端口：
```python
if "BTHENUM" in hwid or "BLUETOOTH" in hwid or "Bluetooth" in desc or "蓝牙" in desc:
    continue
```

### 2.3 Windows Batch / PowerShell 启动脚本铁律
1. **UTF-8 `.bat` 禁令**：使用 `chcp 65001 >nul` 后**严禁使用 `::` 写注释**（Windows CMD 在 UTF-8 下易解析错位报错 `'cho' is not recognized` 并闪退），统一使用 `REM`。
2. **`requirements.txt` 编码**：必须保存为 **UTF-8 无 BOM**，防止 `pip install -r requirements.txt` 解析首包名失败。
3. **自动 `.venv` 引导与 `--console` 兜底**：`run_app.bat` 检测到 `.venv` 缺失时自动执行 `python -m venv .venv && .venv\Scripts\pip install -r requirements.txt`，并保留 `--console` / `-c` 参数切换前台调试输出。
4. **桌面零入侵**：所有 `.bat` / `.ps1` / `.vbs` 启动脚本收敛于 `Host/` 目录，未经用户明确指令严禁向操作系统桌面创建 `.lnk` 或 `.desktop` 快捷方式。
