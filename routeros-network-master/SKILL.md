---
name: routeros-network-master
version: 1.3.0
description: >-
  MikroTik RouterOS (v7.x) system maintenance, dual-path automated disaster recovery, SD storage health governance,
  Tailscale P2P mesh & UPnP cone NAT traversal, Clash TUN bypass arbitration, 192.168.8.x remote lifeline continuous protection,
  Bridge Port Horizon hardware-offload isolation, and strict Principle of Least Privilege (PoLP) / IAM group hardening.
  Trigger on: "routeros", "ros", "mikrotik", "p2p", "tailscale", "打洞", "中继", "直连", "双栈", "ipv6", "sd卡挂载", "dude", "user-manager", "巡检路由", "远程防失联", "最小权限", "agent-operator", "horizon", "硬件隔离".
license: Apache-2.0
metadata:
  version: v1.3.0
  author: Antigravity
---

# RouterOS & P2P Mesh Network Master Suite (路由系统运维与穿透网络大师)

本技能覆盖 MikroTik RouterOS (v7.x) 核心架构运维、外置存储寿命保护、双轨灾备脚本部署、二层硬件端口隔离 (Bridge Horizon)、P2P 穿透（EasyTier/Tailscale）与二级网关远程命脉连续保护。

---

## 1. 核心铁律（硬核防护红线）

1. **远程命脉通道最高保护原则**：`ether2`（承载 `192.168.8.x` 二级网关）为用户远程接入的唯一控制通道。任何防火墙、路由、NAT 或流控变更，必须置顶放行 `ether2`，且任何网络操作前后**强制执行 `verify_remote_safety.py` 五层探活自检**；
2. **SD 卡写损耗与 FAT32 崩溃物理隔离**：MIPS 架构路由器（如 hEX mmips）严禁将高频写入的 SQLite WAL 数据库（如 User-Manager）置于外置 MicroSD 卡；必须收敛至板载 Flash，并使用双轨 `:do on-error` 容灾脚本；
3. **P2P 穿透与 TUN 代理仲裁标准**：Tailscale / EasyTier 穿透依赖对称端口与 STUN UDP 探测。TUN 代理必须切换为 `mixed` 或 `system` 堆栈，杜绝 `gvisor` 重打包导致源端口漂移；
4. **工业级最小权限控制与严禁过度授权红线 (PoLP & IAM Hardening)**：
   * 自动化运维账号必须绑定受限组（`agent-operator`），严格放行 `ssh,read,write,test,sensitive,api,rest-api`，绝对封死 `!reboot,!policy,!password,!sniff,!winbox,!web`；
   * 备份操作优先使用 PoLP 兼容的 `/export` 文本导出，二进制 `.backup` 涉及全凭据哈希留交管理员手动或本地调度；
5. **二层硬件端口隔离与规则有效性铁律 (Bridge Horizon & Zero Invalid Policy)**：
   * 同网桥物理从属端口之间严禁使用三层 IP Filter 假隔离（被硬件卸载绕过且触发 invalid），强制配置二层 **Bridge Port Horizon** (`horizon=10`) 实现芯片线速隔离；
   * 防火墙从属口匹配必须采用主网桥 (`bridge-lan`) 结合源/目的 IP 地址，严禁直接匹配从属物理口；
   * 自动化巡检必须嵌入 `invalid == true` 拦截与核心规则零命中 (`packets == 0`) 审计门禁。

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
* **排查 P2P 穿透打洞**：执行 `check_p2p_mesh.py`，核验是否命中直连或中继；
* **排查网桥端口隔离与无效规则**：查阅 `references/hardware_offload_vs_firewall_pitfalls.md`。

---

## 4. 深度参考手册

* 📘 **标准排障 SOP 手册**：查阅 [`references/routeros_ops_sop.md`](file:///C:/Users/hejia/.gemini/config/skills/routeros-network-master/references/routeros_ops_sop.md)（含 MicroSD 只读自愈、双轨灾备、PoLP 权限规约与 SOP-08 硬件隔离审计）。
* ⚡ **二层硬件卸载与端口隔离避坑手册**：查阅 [`references/hardware_offload_vs_firewall_pitfalls.md`](file:///C:/Users/hejia/.gemini/config/skills/routeros-network-master/references/hardware_offload_vs_firewall_pitfalls.md)。
* 🌐 **P2P 串流与穿透架构**：查阅 [`references/ROUTEROS_P2P_GUIDE.md`](file:///C:/Users/hejia/.gemini/config/skills/routeros-network-master/references/ROUTEROS_P2P_GUIDE.md)。
