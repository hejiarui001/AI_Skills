---
name: p2p-streaming-master
version: 1.0.0
description: >-
  Domestic high-performance P2P mesh networking, Moonlight & Sunshine ultra-low latency game/desktop streaming,
  dual-rail NAT traversal (EasyTier primary + Tailscale fallback), P2P stress testing, and Android tablet remote console.
  Trigger on: "easytier", "tailscale", "p2p", "穿透", "串流", "moonlight", "sunshine", "打洞", "中继", "直连", "压测", "平板串流", "虚拟专网", "mesh".
license: Apache-2.0
metadata:
  version: v1.0.0
  author: Antigravity
---

# P2P Streaming & Mesh Network Master (P2P 穿透与低延迟串流大师)

本技能覆盖基于 **EasyTier 国内高性能 Mesh（主力专网 `10.144.144.0/24`）** 与 **Tailscale（按需备用）** 的双轨低延迟远程桌面/游戏串流（Moonlight/Sunshine）全链路运维、阶梯压力测试与故障排查。

---

## 1. 核心运行原则（红线契约）

1. **双轨分级与自启解耦原则**：
   * 默认以 **EasyTier 为主力专网**（国内骨干中继打洞，实测延迟 < 40ms，0% 丢包）；
   * **Tailscale 解耦开机常驻**（释放 41641/8088 端口），仅作为按需调用的冷备通道；
2. **全链路压力测试与 A+ 评级门禁**：
   * 串流调优以 `p2p_stress_test.py` 阶梯压力测试为基准，严格遵循 A+ 评级门禁（0% 丢包、RTT < 40ms、抖动 < 10ms）；
3. **Sunshine 宿主守护与零桌面入侵**：
   * 确保虚拟显示器驱动在 Headless/锁屏状态下稳定输出；严禁未经允许向用户桌面落盘脚本或图标。

---

## 2. 自动化运维与控制台工具链 (Cross-Platform)

| 操作目标 | Windows 调度方式 | Linux (Ubuntu) 调度方式 | 核心功能说明 |
| :--- | :--- | :--- | :--- |
| **交互式状态总控台** | `03_EasyTier_Mesh/控制台_EasyTier平板专网.bat` | `03_EasyTier_Mesh/控制台_EasyTier平板专网.sh` | 状态监控、启停服务与一键测速 |
| **全链路压力测试** | `python 03_EasyTier_Mesh/p2p_stress_test.py` | `python 03_EasyTier_Mesh/p2p_stress_test.py` | 230 发阶梯压力测试与 A+ 评级 |
| **快速健康探针** | `python scripts/check_p2p_health.py` | `python scripts/check_p2p_health.py` | 平板虚拟 IP 连通性与 Sunshine 状态 |
| **局域网平板 APK 分发** | `03_EasyTier_Mesh/分发平板APK_局域网下载.bat` | `03_EasyTier_Mesh/分发平板APK_局域网下载.sh` | 本地 HTTP 极速推送安装包至平板 |
| **Tailscale 备用通道启停** | `Tools/enable_tailscale_autostart.bat` | `Tools/enable_tailscale_autostart.sh` | 按需激活/注销备用穿透服务 |

---

## 3. 常见指令与意图映射

* **“测试平板串流延迟 / 运行 P2P 压测”**：执行 `p2p_stress_test.py` 并出具丢包率、延迟与评级报告；
* **“检查平板专网连通性”**：执行 `check_p2p_health.py` 探测 `10.144.144.2`；
* **“打开 EasyTier 控制台”**：调出平台对应的 `控制台_EasyTier平板专网` 脚本。

---

## 4. 深度参考手册

* 📘 **P2P 穿透、双重 NAT 映射与 Moonlight 串流调优手册**：查阅 [`references/p2p_streaming_guide.md`](file:///C:/Users/hejia/.gemini/config/skills/p2p-streaming-master/references/p2p_streaming_guide.md)（含 Full Cone / 对称 NAT 打洞原理、Sunshine 4K 码率优化、故障 SOP 与切换备用通道标准）。
