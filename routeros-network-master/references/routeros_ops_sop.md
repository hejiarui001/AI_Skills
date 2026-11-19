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
