---
name: routeros-network-master
version: 1.0.0
description: >-
  MikroTik RouterOS (v7.x) system maintenance, dual-path automated disaster recovery,
  SD storage health governance, Tailscale P2P mesh & UPnP cone NAT traversal, Clash TUN
  bypass arbitration, and 192.168.8.x remote lifeline continuous protection.
  Trigger on: "routeros", "ros", "mikrotik", "p2p", "tailscale", "打洞", "中继", "直连",
  "双栈", "ipv6", "sd卡挂载", "dude", "user-manager", "巡检路由", "远程防失联".
license: Apache-2.0
metadata:
  version: v1.0.0
  author: Antigravity
---

# RouterOS & P2P Mesh Network Master Suite (路由系统运维与穿透网络大师)

> **归属领域**：`03_Cloud_Sync_Gateway` (网络与云端协同域)  
> **适用平台**：跨平台自适应 (Windows 11 / Linux Ubuntu)  
> **核心使命**：提供工业级 MikroTik RouterOS (v7.x) 路由器全生命周期运维保障、双轨容灾备份机制、SD 卡文件系统硬故障防损坏治理、Tailscale P2P 网状组网与 NAT 穿透诊断、Clash TUN 代理冲突深度治理，以及远程接入命脉链路防失联自检协议。

---

## 1. 核心架构与设计原则

```mermaid
flowchart TD
    subgraph WAN [外网出入口]
        PPPoE["PPPoE (CERNET 公网 IPv4: 59.68.x.x)"]
        IPv6_WAN["IPv6 SLAAC (/64 单接口地址)"]
    end

    subgraph RouterOS [MikroTik hEX (v7.25.1)]
        REST["REST API (Port 80)"]
        Winbox["Winbox (Port 8291)"]
        Dude["The Dude (sd1-part1/dude)"]
        UM["User-Manager v5 (flash/user-manager5)"]
        DualBackup[":do {SD备份} on-error={Flash备份}"]
        UPnP["UPnP Full Cone NAT"]
    end

    subgraph Lifeline [远程命脉网段]
        L2_Router["二级网关 (192.168.8.1) / ether2"]
        PC["本地开发机 (192.168.8.2)"]
    end

    subgraph P2P_Mesh [Tailscale P2P 穿透网]
        TS_PC["PC Node (100.117.118.91)"]
        TS_Tablet["Android Node (100.115.83.85)"]
        Clash_Bypass["TUN 规则放行 (STUN 3478 / WG 41641)"]
    end

    PPPoE --> REST
    PPPoE --> Winbox
    REST --> UPnP
    UPnP --> TS_PC
    TS_PC <-->|Direct UDP Punch| TS_Tablet
    Clash_Bypass -.->|Bypass gVisor| TS_PC
    L2_Router --> PC
    RouterOS -->|ether2 永远放行| L2_Router
```

### 核心铁律
1. **远程命脉通道最高保护原则**：`ether2`（承载 `192.168.8.x` 二级网关）为用户远程接入的唯一控制通道。任何防火墙、路由、NAT 或流控策略，必须置顶放行 `ether2`，且所有网络变更前后必须执行 `verify_remote_safety.py` 五层探活自检。
2. **SD 卡写损耗与 FAT32 崩溃物理隔离**：MIPS 架构路由器（如 hEX mmips）严禁将高频写入的 SQLite WAL 数据库（如 User-Manager）置于外置 MicroSD 卡；必须收敛至板载 Flash，并使用双轨 `:do on-error` 容灾脚本。
3. **P2P 穿透与 TUN 代理仲裁标准**：Tailscale 穿透依赖对称端口与 STUN UDP `3478`。TUN 代理必须切换为 `mixed` 或 `system` 堆栈，杜绝 `gvisor` 重打包导致源端口漂移。

---

## 2. 关键排障标准作业程序 (SOP)

### SOP-01: MicroSD 卡 FAT32 损坏与只读锁死自愈
- **故障特征**：系统日志突发 `file operation error (:export; line 4)`，磁盘显示存在大于卡物理容量的幽灵文件，内核处于 `-EIO` 只读锁。
- **根因**：异常断电导致 FAT32 目录表项断裂，叠加 User-Manager SQLite 高频写放大。
- **治理标准流程**：
  1. 停止依赖进程：`/dude/set enabled=no`；
  2. 剥离高频写数据库：`/user-manager/database/set db-path=flash/user-manager5`；
  3. 执行非交互式格式化：`/disk/format-drive numbers=[find slot=sd1-part1] file-system=fat32`；
  4. 恢复监控目录：`/dude/set data-directory=sd1-part1/dude enabled=yes`；
  5. 验证读写能力：创建测试文件并立即删除。

### SOP-02: 双轨自动化容灾备份部署
- **设计标准**：首选 MicroSD 卡，降级保板载 Flash，严防因外置介质脱机导致系统无备份。
```routeros
# Dual-Path Auto-Backup Script
:local dateStr [/system clock get date];
:local fileName ("AutoBackup-" . $dateStr);
:do {
    /system backup save name=("sd1-part1/backup/" . $fileName);
    /export file=("sd1-part1/backup/" . $fileName);
    :log info ("DualBackup: Successfully saved to SD card (" . $fileName . ")");
} on-error={
    :log warning ("DualBackup: SD card write failed, falling back to Flash!");
    /system backup save name=("flash/" . $fileName);
    /export file=("flash/" . $fileName);
    :log info ("DualBackup: Fallback save to Flash completed.");
};
```

### SOP-03: MobaXterm 与终端 SSH 语法报错清除
- **故障特征**：SSH 登录后系统日志记录 `executing script from sshd failed: syntax error (line 1 column 7)`。
- **根因**：MobaXterm 默认开启 SFTP 侧边栏，后台向 RouterOS 非标准 shell 注入 `ls -la` / `pwd` 探针。
- **治理方法**：进入 MobaXterm Session 设置 -> `Advanced SSH settings` -> 将 `SSH-browser type` 设为 `None`，并取消勾选 `X11-Forwarding`。

### SOP-04: The Dude 轮询鉴权失败风暴治理
- **故障特征**：日志每 10 秒刷屏 `system, error, critical login failure for user admin from 192.168.188.1 via winbox`。
- **根因**：The Dude 自动发现或探针配置了错误的全局/设备凭证轮询自身 Winbox 端口。
- **治理方法**：在 The Dude 客户端中更新 Device Credentials，确保与 RouterOS `admin` / 专用监控账户密码严格一致；关闭无效设备的 Winbox 探测服务。

### SOP-05: Tailscale P2P 直连与 Clash TUN 深度解绑
- **故障特征**：PC 具备公网 IPv4 Cone NAT，但移动设备连接报 `active; relay "sfo"` / `Endpoints: null`，延迟几秒且打不通直连。
- **治理四要素**：
  1. **TUN 堆栈转换**：将 Clash Verge / Mihomo 的 TUN 堆栈由 `gvisor` 改为 `mixed` 或 `system`（防止 UDP 端口重打包）；
  2. **关键端口放行**：在代理规则顶部放行 `DST-PORT,3478,DIRECT`（STUN 探测）与 `DST-PORT,41641,DIRECT`（WG 监听）；
  3. **虚拟网段放行**：放行 `IP-CIDR,100.64.0.0/10,DIRECT` 与 `IP-CIDR6,fd7a:115c:a1e0::/48,DIRECT`；
  4. **移动端分流**：安卓客户端使用「应用访问控制」，在黑名单模式中将 Tailscale 排除（或白名单模式中不要勾选）。

### SOP-06: 校园网/宽带 IPv6 无前缀委派 (PD) 路由限制诊断
- **故障特征**：WAN 口获取到 `2001:da8:.../64`，内网 Bridge 分配了 ULA（`fd00:...`），Windows 终端显示有 IPv6，但公网丢包 100%。
- **治理依据**：核查 `/ipv6/pool/print` 与 `/ipv6/dhcp-client/print`。若上游 BRAS 未下发 Delegated Prefix 且不路由外网 IPv6 ICMP，内网 ULA 无法跨公网通信。此时系统应自动锁定以 **公网 IPv4 + UPnP Full Cone NAT** 为唯一骨干打洞路径，避免因 IPv6 超时拖慢连接。

---

## 3. 内置辅助工具链 (Scripts)

技能自带跨平台辅助脚本（位于 `scripts/` 目录）：
1. **`verify_remote_safety.py`**：五层安全自检网关（网段核查 -> 二级网关 -> 一级主路由管理端口 -> 骨干 DNS -> 端到端外网通信）。
2. **`check_p2p_mesh.py`**：Tailscale 节点拓扑、端点状态、DERP 中继与直连连通性实时诊断。
3. **`diagnose_routeros.py`**：通过 REST API 自动化采集 RouterOS 7.x 硬件资源、存储卡健康度、IPv4/IPv6 路由与最新错误日志。

---

## 4. 常见指令映射

- *“巡检一下我的主路由状态”* -> 调用 `diagnose_routeros.py` 自动化读取 CPU/RAM/SD卡/日志。
- *“检查 Tailscale 为什么还在走中继”* -> 调用 `check_p2p_mesh.py` 分析双端 STUN 端点与 TUN 冲突。
- *“执行网络安全自检”* -> 调用 `verify_remote_safety.py` 执行五层链路探活。
- *“部署 RouterOS 双轨容灾备份”* -> 输出带 `:do on-error` 保护机制的备份脚本。
