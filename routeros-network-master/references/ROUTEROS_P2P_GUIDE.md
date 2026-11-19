# RouterOS v7 & Tailscale P2P 实战踩坑与配置全景指南

> **文档性质**：实战工程经验沉淀与权威避坑手册  
> **适用平台**：MikroTik RouterOS v7.x (RB750Gr3 等) + Tailscale + Clash Verge Rev  

---

## 一、 RouterOS 存储与稳定性踩坑复盘

### 1. FAT32 目录损坏与不可逆只读锁定
- **问题起因**：路由器在未安全卸载或突发断电时，FAT32 文件系统目录项发生损坏。若外置存储上运行高频写入进程（如 User-Manager SQLite 数据库），WAL 写入会导致单文件膨胀并出现几百 GB 的“幽灵文件”（甚至显示为 3.9 EB），Linux 内核随后触发 `-EIO` 强制把整卡设为 `Read-Only`。
- **排查命令**：
  ```routeros
  /disk/print
  /log/print where message~"file operation error"
  ```
- **核心规约**：
  - 严禁将 User-Manager 数据库置于 MicroSD 卡！必须移至板载 Flash：
    ```routeros
    /user-manager/database/set db-path=flash/user-manager5
    ```
  - The Dude 监控数据属于非关键可重建数据，可保留在 `sd1-part1/dude`。
  - mmips / 256MB 内存机型缺少 `rose-storage` 扩展包，无法格式化为 ext4，必须格式化为 FAT32。

### 2. 双轨自动化容灾备份
为防止 MicroSD 卡掉载导致日常备份任务全面中断，必须在定时调度器（Scheduler）中部署带错误捕获的脚本：
```routeros
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

---

## 二、 协议兼容与客户端冲突治理

### 1. MobaXterm SFTP 导致 SSH 脚本语法错误
- **报错特征**：`executing script from sshd failed: syntax error (line 1 column 7)`
- **原因分析**：MobaXterm 连接任何 SSH 服务器时，默认尝试通过 SFTP 列目录，并注入 `ls` / `pwd` 命令。RouterOS 的交互式 Shell 并不支持此类标准 POSIX 指令，导致每次建立连接都在系统日志中刷一条红字语法错误。
- **解决方案**：在 MobaXterm Session 设置中将 `SSH-browser type` 设为 `None`，并取消勾选 `X11-Forwarding`。

### 2. The Dude 轮询鉴权失败
- **报错特征**：`login failure for user admin from 192.168.188.1 via winbox`
- **原因分析**：The Dude 在扫描拓扑时，默认启用 Winbox (8291) 探针，但探针内部保存的密码为空或旧密码。
- **解决方案**：在 The Dude 客户端中右键路由器设备 -> `Settings` -> 更新 `Credentials`，或者全局关闭未授权设备的自动探针。

---

## 三、 Tailscale P2P 穿透与 Clash TUN 仲裁

### 1. Endpoints: None 根因排查
- 当执行 `tailscale status --json` 发现某个 peer 的 `Endpoints: null` 时：
  - **90% 概率是对端开启了 TUN 代理**，导致 STUN 探测包（UDP 3478）未能返回物理公网 IP:Port；
  - **10% 概率是对端系统休眠**，系统回收了后台 UDP 监听套接字。

### 2. Clash Verge Rev (PC 端) 黄金配置
在 TUN 模式下，必须防范 `gvisor` 协议栈重新打包 UDP 报文：
- **堆栈选型**：首选 `mixed` 或 `system`；
- **必备加白规则**：
  ```yaml
  prepend:
    - PROCESS-NAME,tailscaled.exe,DIRECT
    - PROCESS-NAME,tailscale.exe,DIRECT
    - DST-PORT,3478,DIRECT
    - DST-PORT,41641,DIRECT
    - DOMAIN-SUFFIX,tailscale.com,DIRECT
    - DOMAIN-SUFFIX,ts.net,DIRECT
    - IP-CIDR,100.64.0.0/10,DIRECT,no-resolve
    - IP-CIDR6,fd7a:115c:a1e0::/48,DIRECT,no-resolve
  ```

### 3. Android 端应用分流
安卓端不要尝试写复杂的正则规则，直接在代理 App（Clash Meta for Android / Flclash）的「网络」->「应用访问控制」中选择「绕过模式」，把 **Tailscale** 勾选排除即可。
