---
name: routeros-network-master
version: 1.1.0
description: >-
  MikroTik RouterOS (v7.x) system maintenance, dual-path automated disaster recovery, SD storage health governance,
  Tailscale P2P mesh & UPnP cone NAT traversal, Clash TUN bypass arbitration, and 192.168.8.x remote lifeline continuous protection.
  Trigger on: "routeros", "ros", "mikrotik", "p2p", "tailscale", "打洞", "中继", "直连", "双栈", "ipv6", "sd卡挂载", "dude", "user-manager", "巡检路由", "远程防失联".
license: Apache-2.0
metadata:
  version: v1.1.0
  author: Antigravity
---

# RouterOS & P2P Mesh Network Master Suite (路由系统运维与穿透网络大师)

本技能覆盖 MikroTik RouterOS (v7.x) 核心架构运维、外置存储寿命保护、双轨灾备脚本部署、P2P 穿透（EasyTier/Tailscale）与二级网关远程命脉连续保护。

---

## 1. 核心铁律（硬核防护红线）

1. **远程命脉通道最高保护原则**：`ether2`（承载 `192.168.8.x` 二级网关）为用户远程接入的唯一控制通道。任何防火墙、路由、NAT 或流控变更，必须置顶放行 `ether2`，且任何网络操作前后**强制执行 `verify_remote_safety.py` 五层探活自检**；
2. **SD 卡写损耗与 FAT32 崩溃物理隔离**：MIPS 架构路由器（如 hEX mmips）严禁将高频写入的 SQLite WAL 数据库（如 User-Manager）置于外置 MicroSD 卡；必须收敛至板载 Flash，并使用双轨 `:do on-error` 容灾脚本；
3. **P2P 穿透与 TUN 代理仲裁标准**：Tailscale / EasyTier 穿透依赖对称端口与 STUN UDP 探测。TUN 代理必须切换为 `mixed` 或 `system` 堆栈，杜绝 `gvisor` 重打包导致源端口漂移。

---

## 2. 内置辅助工具链 (Scripts)

| 脚本工具 | 核心功能 | 调用方法 (Cross-Platform) |
| :--- | :--- | :--- |
| **`verify_remote_safety.py`** | 远程命脉与网络五层探活自检（ARP/Ping/DNS/HTTP/Port） | `python scripts/verify_remote_safety.py` |
| **`diagnose_routeros.py`** | ROS 全系统状态、存储空间与 CPU 负载巡检 | `python scripts/diagnose_routeros.py` |
| **`check_p2p_mesh.py`** | P2P 穿透拓扑、DERP 中继与 Direct 状态诊断 | `python scripts/check_p2p_mesh.py` |

---

## 3. 常见意图与指令映射

* **巡检主路由**：执行 `diagnose_routeros.py`，核验 SD 卡读写状态、内存占用与固件版本；
* **测试远程命脉与断网回滚**：执行 `verify_remote_safety.py`，若出现链路异常立即阻断变更；
* **排查 P2P 穿透打洞**：执行 `check_p2p_mesh.py`，核验是否命中直连或中继。

---

## 4. 深度参考手册

* 📘 **标准排障 SOP 手册**：查阅 [`references/routeros_ops_sop.md`](file:///C:/Users/hejia/.gemini/config/skills/routeros-network-master/references/routeros_ops_sop.md)（含 MicroSD 只读锁死自愈、双轨自动备份脚本代码、MobaXterm 语法报错消除、The Dude 鉴权风暴治理及 IPv6 PD 无前缀委派方案）。
* 🌐 **P2P 串流与穿透架构**：查阅 [`references/ROUTEROS_P2P_GUIDE.md`](file:///C:/Users/hejia/.gemini/config/skills/routeros-network-master/references/ROUTEROS_P2P_GUIDE.md)。
