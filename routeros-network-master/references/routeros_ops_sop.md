# RouterOS 关键排障标准作业程序 (SOP) 与脚本手册

本文档承载 `routeros-network-master` 技能的深层网络排障作业程序（SOP）、RouterOS 终端脚本及特定协议治理方案。

---

## SOP-01: MicroSD 卡 FAT32 损坏与只读锁死自愈
* **故障特征**：系统日志突发 `file operation error (:export; line 4)`，磁盘显示存在大于卡物理容量的幽灵文件，内核处于 `-EIO` 只读锁。
* **根因**：异常断电导致 FAT32 目录表项断裂，叠加 User-Manager SQLite 高频写放大。
* **治理标准流程**：
  1. 停止依赖进程：`/dude/set enabled=no`；
  2. 剥离高频写数据库：`/user-manager/database/set db-path=flash/user-manager5`；
  3. 执行非交互式格式化：`/disk/format-drive numbers=[find slot=sd1-part1] file-system=fat32`；
  4. 恢复监控目录：`/dude/set data-directory=sd1-part1/dude enabled=yes`；
  5. 验证读写能力：创建测试文件并立即删除。

---

## SOP-02: 双轨自动化容灾备份部署
* **设计标准**：首选 MicroSD 卡，降级保板载 Flash，严防因外置介质脱机导致系统无备份。

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
}
```

---

## SOP-03: MobaXterm 与终端 SSH 语法报错清除
* **故障特征**：SSH 终端登录时弹出 `bad command name m (line 1 column 1)`。
* **根因**：MobaXterm 勾选了“Auto-detect terminal size”，在连接初期发送了转义探针 `ESC[6n`，被 RouterOS CLI 解释为命令报错。
* **治理方案**：进入 Session Settings -> Terminal settings -> 禁用自动探针与增强终端模式。

---

## SOP-04: The Dude 轮询鉴权失败风暴治理
* **故障特征**：Dude 服务突发每 5 秒生成一条 `login failure for user admin from 127.0.0.1 via local` 日志，塞满存储日志。
* **治理方案**：
  ```routeros
  /dude/set default-agent-user=admin default-agent-password=""
  /dude/agent/reset
  ```

---

## SOP-05: Tailscale P2P 直连与 Clash TUN 深度解绑
* **治理标准**：
  1. RouterOS 开启 UPnP 并在防火墙放通 STUN UDP `3478` 与默认 WireGuard UDP `41641`；
  2. Clash Verge 切换网络堆栈至 `mixed`，禁用 `gvisor` 对本地 UDP 源端口的双重重打包；
  3. 运行 `check_p2p_mesh.py` 核验 Android 平板与 PC 间的 `direct: true` 直连状态。

---

## SOP-06: 校园网/宽带 IPv6 无前缀委派 (PD) 路由限制诊断
* **故障特征**：PPPoE 下发了单个 `/64` 地址，但下级局域网设备无法通过 DHCPv6-PD 获取公网 IPv6 前缀。
* **治理方案**：在 RouterOS 启用 NDP 代理与 IPv6 Relay，或切换为 IPv6 NAT66 模式穿透局域网。

---

## SOP-07: 工业级最小权限控制 (PoLP) 与自动化运维账号 IAM 固化
* **核心原则**：严禁向用户索要或提议赋予 `full` 组等全量管理员权限；自动化运维必须收敛在专用受限组。
* **RouterOS `agent-operator` 组规约**：
  1. **组策略配置**：
     ```routeros
     /user/group/add name=agent-operator policy=ssh,read,write,test,sensitive,api,rest-api
     ```
  2. **权限白名单与黑名单对照**：
     * **放行 (Whitelist)**：`ssh,read,write,test,sensitive,api,rest-api`（满足 REST API 状态采集、`/export` 配置导出与受限指令执行）；
     * **剥离 (Blacklist)**：`!local,!telnet,!ftp,!reboot,!policy,!winbox,!password,!web,!sniff,!romon`（阻断硬重启、用户组修改、敏感密码哈希读取与网络抓包）；
  3. **备份权限边界治理**：
     * `/system/backup/save` 在 RouterOS v7 中因包含全系统用户密码哈希，执行必须具备 `password` 或 `policy` 策略，故 `agent-operator` 执行时会报 `not enough permissions (9)`；
     * 严禁通过将账号提升至 `full` 组来消除该报错；
     * 自动化备份统一调用 `/export file=...` 导出纯文本配置脚本（受 `sensitive` 放行支持），具备 100% 灾难恢复能力且不触碰系统密码哈希；
     * 若必须生成二进制 `.backup` 镜像，必须交由 RouterOS 原生计划任务（Scheduler 以管理员身份触发）或由网络管理员手动登录生成。


---

## SOP-08: 网桥从属端口二层 Horizon 隔离与规则失效审计
* **故障特征**：
  1. 在三层 Filter 配置端口隔离规则（如 `in-interface=ether2 out-interface=ether3 action=drop`），但数据包依然可以二层互通或计数器显示 `0 packets`；
  2. 规则被系统标记为红字或 `invalid: true`，报错 `use master instead (bridge-lan)`。
* **根因**：物理端口加入 Bridge 后三层属性被剥夺；且同网桥流量被交换芯片硬件卸载（Hw-Offload）直接二层线速交换，根本不上送 CPU 内核三层协议栈。
* **治理标准流程**：
  1. **二层硬件隔离生效**：
     ```routeros
     /interface/bridge/port/set [find interface=ether2] horizon=10
     /interface/bridge/port/set [find interface=ether3] horizon=10
     ```
  2. **三层从属口语法修复**：
     将所有在 `/ip firewall filter` 中直接指定物理从属口的规则，统一修正为 `in-interface=bridge-lan` 搭配 `src-address=<目标IP>`；
  3. **清理失效规则**：移除原三层无用的 L3 跨网桥端口双向丢弃规则；
  4. **运行全量健康断言**：运行自动化巡检，确认全表 `invalid: true` 数量彻底归零。
