# 专有交换芯片二层硬件卸载、Bridge Horizon 端口隔离与网桥从属口失效陷阱复盘手册

> **归属技能**：`routeros-network-master` (v1.3.0)  
> **生效环境**：MikroTik RouterOS v7.x (所有搭载硬件交换芯片的机型，如 MT7621A / Atheros / Marvell)  
> **核心主题**：二层交换数据平面与三层防火墙分离机制、Bridge Port Horizon 隔离原理与网桥从属口 (Slave Port) 语法失效排查

---

## 一、 核心技术陷阱与底层根因剖析

### 1. 陷阱一：二层硬件卸载 (Hardware Offload) 绕过三层 IP Firewall
* **典型错误设计**：在同一个网桥（如 `bridge-lan`）下有两个物理端口（如 `ether2` 和 `ether3`），误以为在三层防火墙配置 `chain=forward in-interface=ether2 out-interface=ether3 action=drop` 即可实现相互隔离；
* **底层真实机理**：
  1. **硬件线速转发机制**：在搭载硬件交换芯片（Switch Core ASIC）的路由器上，网桥默认开启硬件卸载（`hw-offload=true`）。同网段（同广播域）的跨端口流量直接由交换芯片根据内部 MAC 地址表完成二层转发；
  2. **完全旁路 CPU 与 Netfilter**：该流量根本**不会被上送至 CPU 内核协议栈**，更不会进入 IP Firewall 的 Conntrack 与 Forward 链；
  3. **假阳性掩盖**：若下挂设备本身带有 NAT（如二级路由器 WAN 口 Masquerade），从外部本来就 Ping 不通内网设备，导致工程师产生“规则已生效”的致命误判；
  4. **排查证据**：查看该 Filter 规则的统计计数器，必呈现 `bytes=0, packets=0`（从未被命中）。

---

### 2. 陷阱二：网桥从属接口 (Slave Port) 在 IP Firewall 中被标记为 Invalid
* **典型错误设计**：在 `/ip firewall filter` 或 `/ip firewall raw` 中直接指定网桥从属物理口，例如：
  `add chain=input in-interface=ether2 action=accept`
* **RouterOS v7 报错**：
  规则被系统强制置为 **`invalid: true`**，控制台报错：
  > `in/out-interface matcher not possible when interface (ether2) is slave - use master instead (bridge-lan)`
* **底层真实机理**：
  在 RouterOS v7 内核模型中，物理接口加入 Bridge 成为 Slave Port 后，其三层 IP 属性被网桥总接口（Master）剥夺并统一接管。三层 IP 协议栈只能识别 `bridge-lan`，直接匹配物理从属口会导致规则解析器判定为非法语法而静默跳过执行。

---

## 二、 工业级标准解决方案 (Best Practices)

### 方案 1：二层硬件级端口隔离 —— Bridge Port Horizon (强烈推荐)
依据官方文档规范（`https://mikrotikdocs.fyi/bridge/bridge-port-isolation/`），在网桥端口属性中为需要隔离的物理接口分配**相同的非零 Horizon 值**（Private VLAN / Split Horizon 机制）：

```routeros
# 将 ether2 与 ether3 划入同一硬件隔离域 (horizon=10)
/interface bridge port
set [find interface=ether2] horizon=10
set [find interface=ether3] horizon=10

# 其余管理口与网维专机端口保持默认 (horizon=none)
set [find interface=ether4] horizon=none
set [find interface=ether5] horizon=none
```

#### 转发控制矩阵逻辑：
| 源端口 Horizon | 目的端口 Horizon | 交换芯片处理动作 | 适用场景 |
| :---: | :---: | :---: | :--- |
| `H = 10` | `H = 10` | 🚫 **物理硬件绝对丢弃** | `ether2` 与 `ether3` 之间互阻（单播/组播/广播全禁） |
| `H = 10` | `H = none` | 🟢 **允许线速转发** | `ether2` 访问 `ether4` (网维专机) 或工作站 |
| `H = 10` | `CPU (bridge-lan)`| 🟢 **允许三层转发** | 终端正常访问主路由网关、DNS 与出海外网 |

* **核心优势**：
  - 由交换芯片 ASIC 硬件执行，**CPU 占用率 0%**；
  - 维持硬件卸载（Hw-Offload），不牺牲千兆 FastPath 性能；
  - 彻底杜绝 ARP 广播泛洪与跨端口二层嗅探。

---

### 方案 2：网桥从属口在 IP Firewall 的标准放通语义
若必须在三层防火墙针对特定端口下挂的设备进行访问控制，**必须将 `in-interface` 设定为主网桥 `bridge-lan`，并搭配 `src-address` 进行精确约束**：

```routeros
# 正确写法：主网桥 + 静态 IP / 网段
/ip firewall filter
add chain=input in-interface=bridge-lan src-address=192.168.188.249 action=accept \
    comment="SAFETY-CRITICAL: ether2 (AX3 Pro) Always Allow Management"

add chain=forward in-interface=bridge-lan src-address=192.168.188.249 out-interface-list=WAN action=accept \
    comment="SAFETY-CRITICAL: ether2 (AX3 Pro) Always Allow Internet"
```

---

## 三、 自动化巡检与防线断言规约 (Audit Assertions)

在开发与执行 RouterOS 自动化运维脚本时，必须嵌入以下两条硬核断言逻辑：

1. **Invalid 状态红线阻断 (Zero Invalid Rule Policy)**：
   ```python
   # 规则有效性硬核门禁
   invalid_rules = [r for r in ros_rules if r.get('invalid') == 'true']
   if invalid_rules:
       raise SystemError(f"CRITICAL: 发现 {len(invalid_rules)} 条无效规则！必须排查从属口与语法冲突！")
   ```
2. **零命中异常旁路审计 (Zero-Hit Traffic Audit)**：
   对投产超过 24 小时的关键安全与隔离规则进行流量审计：
   - 若 `packets == "0"` 且规则包含 `ISOLATION` 或 `DROP`，必须触发警告：**“规则命中为零，疑似已被二层交换芯片硬件卸载绕过或前置放通，需排查是否应迁移至 Bridge Horizon”**。
