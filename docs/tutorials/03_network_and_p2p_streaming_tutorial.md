# 路由系统、P2P专网穿透与低延迟串流实战教程 (Network & P2P Streaming Tutorial)

> **领域定位**：MikroTik RouterOS 主路由运维、堡垒防火墙、192.168.8.x 远程命脉五层自检、EasyTier 国内高速 P2P 虚拟专网、Moonlight/Sunshine 4K 串流调优与双轨 NAT 穿透  
> **联动技能群**：`routeros-network-master`、`p2p-streaming-master`、`google-sync-guard`  
> **更新机制**：随网络拓扑割接、P2P 压测与穿透实测持续演进

---

## 一、 网络与串流双轨架构全景 (Architecture Topology)

```text
       ┌────────────────────────────────────────────────────────┐
       │              外网接入 / 校园网 PPPoE 拨号                │
       └──────────────────────────┬─────────────────────────────┘
                                  │
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │   一级硬件主路由: MikroTik hEX RB750Gr3 (RouterOS v7)   │
       │   [routeros-network-master]                           │
       │   • 堡垒防火墙 (Fortress Firewall)                      │
       │   • UPnP Full Cone NAT                                 │
       │   • 128G MicroSD 卡存储保护与 Flash 双轨容灾备份         │
       └──────────────┬──────────────────────────┬──────────────┘
                      │                          │
       (ether2: 命脉通道)                   (LAN: 局域网终端)
                      ▼                          ▼
       ┌────────────────────────┐      ┌────────────────────────┐
       │ 二级网关: 192.168.8.1   │      │ 本地开发机: PC Host    │
       │ (远程运维最高优先级保护) │      │ • Sunshine 串流服务    │
       └────────────────────────┘      └───────────┬────────────┘
                                                   │
                   ┌───────────────────────────────┴───────────────────────────────┐
                   │                                                               │
     (主力专网: 低延迟/国内直连打洞)                                  (按需备用: 解耦常驻/冷备通道)
                   ▼                                                               ▼
┌──────────────────────────────────────┐                       ┌──────────────────────────────────────┐
│ EasyTier Mesh 虚拟专网 (10.144.144.0) │                       │ Tailscale 穿透网络 (100.x.y.z)       │
│ [p2p-streaming-master]               │                       │ [p2p-streaming-master]               │
│ • PC 节点: 10.144.144.1              │                       │ • PC 节点: 100.117.118.91            │
│ • Android 平板: 10.144.144.2         │                       │ • Android 平板: 100.115.83.85        │
│ • 实测 RTT: 36.2 ms (0% 丢包 / A+)   │                       │ • 平时完全关闭，释放 41641/8088 端口 │
└──────────────────┬───────────────────┘                       └──────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│ Moonlight 4K/60fps 极限无感远程串流  │
└──────────────────────────────────────┘
```

---

## 二、 阶段实战指南与技能联动矩阵

### 1. MikroTik RouterOS 主路由运维与命脉保护
* **核心目标**：保障硬件主路由高可用，杜绝因防火墙误改或磁盘崩溃导致远程失联。
* **三大铁律**：
  1. **192.168.8.x 命脉通道最高保护**：`ether2` 二级网关为远程控制生命线，任何网络规则变更前后**强制运行 `verify_remote_safety.py` 五层自检**（ARP、Ping、DNS、HTTP、Port），出现异常立即阻断回滚；
  2. **MicroSD 卡 FAT32 崩溃物理隔离**：MIPS 架构严禁将 SQLite WAL 高频写入库（如 User-Manager）放在 SD 卡上，必须收敛至 Flash，并启用 `:do on-error` 双轨自动灾备；
  3. **私密日志物理隔离**：网络检测日报与拓扑日志强制输出至外部 `E:\Internet\Messages\`，绝对禁止保存在 AI 工作区，严禁 Git 纳管。
* **【联动技能】**：[`routeros-network-master`](../../routeros-network-master/SKILL.md)
  - *触发示例*：“巡检主路由运行状态与 SD 卡健康度”、“执行 192.168.8.x 远程命脉与网络五层全链路自检”。

### 2. EasyTier 国内高速 P2P 专网与低延迟串流
* **核心目标**：突破复杂 NAT（Full Cone 与移动蜂窝对称型 NAT），实现平板与 PC 间的点对点高速打洞。
* **SOP 规范**：
  - 虚拟网规划：`10.144.144.0/24`，PC 固定为 `.1`，平板固定为 `.2`；
  - 串流调优：Sunshine 强制绑定虚拟网，Moonlight 码率配置为 `30~50 Mbps`，编码器强制选择 `HEVC` 或 `AV1`；
  - 双端控制台：Windows 通过批处理自动请求 UAC 管理员提权；Linux 通过 systemd 注册 `easytier.service`；
  - 快速分发：平板首次接入通过本地 HTTP 8888 端口极速下载 APK。
* **【联动技能】**：[`p2p-streaming-master`](../../p2p-streaming-master/SKILL.md)
  - *触发示例*：“打开 EasyTier 平板专网控制台”、“启动本地局域网平板 APK 分发服务”。

### 3. 全链路阶梯压力测试与 A+ 评级门禁
* **核心目标**：在正式串流前，通过 `p2p_stress_test.py` 实施 230 发全梯度负载压力测试。
* **评级门禁**：
  - **A+ (卓越)**：丢包率 `0.0%`，平均 RTT `< 40ms`，抖动 `< 10ms`（满足 4K/60fps 极限竞技与精密操作）；
  - **低于 A 级处理**：立即检查是否受 2.4GHz Wi-Fi 干扰，排查主路由端口映射。
* **【联动技能】**：[`p2p-streaming-master`](../../p2p-streaming-master/SKILL.md)
  - *触发示例*：“测试平板 Moonlight 串流延迟与 P2P 链路健康度”、“运行 EasyTier 230 发阶梯压力测试”。

### 4. Tailscale 备用通道与自启解耦
* **核心目标**：解除 Tailscale 开机自启常驻（释放 41641/8088 端口），仅在海外中继或专网调试时一键启用。
* **【联动技能】**：[`p2p-streaming-master`](../../p2p-streaming-master/SKILL.md)
  - *触发示例*：“临时切换到 Tailscale 备用通道”、“禁用 Tailscale 开机自启”。

### 5. Google 云端协同防断网网关
* **核心目标**：在访问 Google Workspace 时实时监测代理可用性，网络抖动时启动写前缓存队列（Write-Ahead Cache）。
* **【联动技能】**：[`google-sync-guard`](../../google-sync-guard/SKILL.md)
  - *触发示例*：“探测当前 Google 云端网络连通性”、“检查离线暂存队列是否有未同步的日志”。

---

## 三、 实战踩坑手记与经验增量池 (Hard-Won Knowledge)

1. **Sunshine Headless 锁屏崩溃**：PC 处于无物理显示器状态时，必须启用虚拟显示器驱动（固定 2560x1600@60Hz），否则视频编码器抓屏失败闪退；
2. **TUN 代理导致 P2P 无法打洞**：Clash Verge 的 gVisor 堆栈会重新打包 UDP 源端口导致端口漂移，必须将网络堆栈设为 `mixed` 或在规则中将 STUN UDP `3478` 与 EasyTier UDP `11010` 直连放通；
3. **MobaXterm 登录 ROS 语法报错**：禁用 MobaXterm 的“Auto-detect terminal size”，避免其发送 `ESC[6n` 探针触发 CLI 报错。
