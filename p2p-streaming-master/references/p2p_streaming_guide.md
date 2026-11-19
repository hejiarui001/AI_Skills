# P2P 穿透、EasyTier 虚拟专网与 Moonlight 串流指南 (P2P Streaming Guide)

本文档承载 `p2p-streaming-master` 技能的深层网络拓扑、NAT 穿透原理、Sunshine/Moonlight 串流参数调优与故障处理 SOP。

---

## 1. 架构演进与方案分级定位 (Architecture Evolution & Dual-Rail Tiers)

工作区确立了以 **EasyTier 国内高性能 Mesh 为主力专网、Tailscale 为按需安全备用通道** 的双轨体系：

```text
┌────────────────────────────────────────────────────────────────────────┐
│             Moonlight / Sunshine 低延迟串流传输层                      │
├───────────────────────────────────┬────────────────────────────────────┤
│   主力专网: EasyTier Mesh         │   按需备用: Tailscale DERP/Direct  │
│   (低延迟/国内中继/打洞能力极强)   │   (高安全性/海外备用/开机自启解耦) │
├───────────────────────────────────┼────────────────────────────────────┤
│ • 虚拟网段: 10.144.144.0/24       │ • 虚拟网段: 100.x.y.z              │
│ • 宿主 PC: 10.144.144.1           │ • 宿主 PC: 100.117.118.91          │
│ • Android平板: 10.144.144.2       │ • Android平板: 100.115.83.85       │
│ • 实测 RTT: ~36.2 ms (0% 丢包)    │ • 解耦常驻，释放系统 41641/8088 端口│
│ • 状态: 开机自启 / 系统服务守护   │ • 状态: 独立启停，故障时一键切换   │
└───────────────────────────────────┴────────────────────────────────────┘
```

---

## 2. 核心穿透原理与技术铁律

### 2.1 Full Cone NAT vs 对称型 NAT 碰撞法则
* **Full Cone NAT (全锥型)**：RouterOS 开启 UPnP 并置顶放行端口后，外部任何节点可向已建立映射的本地端口发送数据；
* **对称型 NAT (Symmetric NAT - 5G移动蜂窝网)**：移动数据网络每次向不同外部 IP 发起连接时，NAT 外部端口动态随机分配；
* **解决方案**：EasyTier 采用内置的国内骨干中继中转节点协助打洞，在两端建立直接 UDP 连接；一旦打洞失败，自动平滑无缝降级为国内节点高速中继，杜绝 Tailscale 绕美导致的 300ms+ 高延迟。

### 2.2 双重 NAT 端口映射与防火墙放行
* **Moonlight / Sunshine 传输端口**：
  - TCP: `47984, 47989, 48010`（服务握手、HTTP 通信、Web 管理）
  - UDP: `47998, 47999, 48000, 48002, 48010`（音视频流传输、控制流）
* **EasyTier 专网通信端口**：
  - UDP/TCP: `11010`（Mesh 节点互联通信与 STUN 探针）

### 2.3 Sunshine 宿主进程 Headless 崩溃红线
* **问题特征**：PC 处于锁屏、无显示器（Headless）或远程桌面断开时，Sunshine 捕获显卡画面可能抛出 `Failed to duplicate output` 崩溃；
* **解决方案**：必须在 PC 端启用虚拟显示器驱动（Virtual Display Driver, 如 IddSampleDriver）或插入物理 HDMI 诱骗插头，分辨率固定为平板原生分辨率（如 `2560x1600 @ 60Hz`）。

---

## 3. 全链路压力测试套件评估标尺 (Stress Test Rubric)

运行 `p2p_stress_test.py` 时的综合打分准则：

| 评级等级 | 丢包率 (Packet Loss) | 平均往返延迟 (RTT) | 延迟抖动 (Jitter) | 适用场景与质量描述 |
| :---: | :---: | :---: | :---: | :--- |
| **A+ (卓越)** | **`0.0%`** | **`< 40.0 ms`** | **`< 10.0 ms`** | 4K/60fps 极限无感串流，竞技游戏与精密操作 |
| **A (优良)** | `< 1.0%` | `< 60.0 ms` | `< 15.0 ms` | 1080P/60fps 顺畅串流，常规办公与视频播放 |
| **B (可用)** | `< 3.0%` | `< 100.0 ms` | `< 25.0 ms` | 轻量桌面远程控制，存在偶发丢帧 |
| **C (受限)** | `> 5.0%` | `> 120.0 ms` | `> 30.0 ms` | 中继劣化，需排查物理网络或重启节点服务 |

---

## 4. 故障处理标准作业程序 (SOP)

### SOP-01: 平板连接不上 EasyTier 专网
1. 检查 PC 端服务状态：执行 `查看状态_Windows.bat`，核验自身虚拟 IP 是否为 `10.144.144.1`；
2. 检查平板 EasyTier APP：核验网络名称（`easytier`）、网络密码与节点连接状态；
3. 执行局域网 APK 分发：若平板未安装，运行 `分发平板APK_局域网下载.bat`，平板浏览器访问 `http://PC_IP:8888` 极速下载。

### SOP-02: 串流卡顿、跳帧或高延迟诊断
1. 运行压力测试：`python E:\AI_Workspace\05_Network_Development\03_EasyTier_Mesh\p2p_stress_test.py`；
2. 若评级低于 A，检查 WiFi 频段：确保 PC 与平板均处于 5GHz / 6GHz Wi-Fi，远离 2.4GHz 干扰；
3. 检查 Sunshine 码率：建议平板端 Moonlight 码率限制在 `30 ~ 50 Mbps`，编码器强制选择 `HEVC (H.265)` 或 `AV1`。

### SOP-03: 切换至备用通道 (Tailscale Fallback)
1. 临时启动 Tailscale：运行 `E:\AI_Workspace\Tools\enable_tailscale_autostart.bat`；
2. 平板打开 Tailscale APP 连接；
3. Moonlight 中添加 PC 的 Tailscale IP（`100.117.118.91`）作为备用连接入口。
