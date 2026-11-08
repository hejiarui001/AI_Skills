---
name: gcs-storage-suite
version: 3.0.0
description: >-
  Google Cloud Storage (GCS) Master Suite: Secure bucket architecture and provisioning,
  object lifecycle management, high-performance Cloud Storage FUSE POSIX mounts (gcsfuse),
  and comprehensive GCS security & IAM audit (SAIF compliance).
  Trigger on: "GCS", "Cloud Storage", "storage bucket", "gcsfuse", "FUSE mount",
  "gsutil", "gcloud storage", "bucket security", "bucket design".
license: Apache-2.0
metadata:
  version: v3.0.0
  role: Master Suite
---

# Google Cloud Storage 统一存储中枢 (GCS Storage Suite) v3.0

整合原 `google-cloud-storage-basics`、`google-cloud-storage-bucket-architect`、`google-cloud-storage-fuse` 与 `gcs-security-assessment` 四大存储技能，形成 GCS 架构、挂载、传输与安全合规全景套件。

---

## 1. 存储桶架构设计与开箱声明 (Bucket Architect)
* **默认安全原则**：强制开启统一存储桶级访问权限（Uniform Bucket-Level Access）；开启公共访问阻止（Public Access Prevention）；
* **存储类别与生命周期**：根据读写频率设计分层（Standard -> Nearline -> Coldline -> Archive），利用 Lifecycle Rules 自动沉降或清理过期版本；
* **软删除与数据保护**：配置 Soft Delete 窗口（默认 7 天）与版本控制（Object Versioning）防御意外覆写与恶意删除。

---

## 2. 对象读写、并发传输与 CLI 最佳实践 (Basics)
* 统一使用现代化 `gcloud storage` CLI，全面替代旧版 `gsutil`；
* 大文件与海量文件并发传输：开启多线程多进程分块传输 (`gcloud storage rsync -r`)；
* 预签名 URL 生成：`gcloud storage sign-url ...` 支持免凭据临时受限访问。

---

## 3. 高性能 POSIX 文件系统挂载 (Cloud Storage FUSE)
* **适用场景**：AI/ML 训练数据读取、Checkpoint 周期性快照落盘；
* **缓存与性能调优**：
  * 读密集型：开启大容量文件缓存与元数据缓存（`--file-cache:max-size-mb=...`，`--stat-cache-capacity=...`）；
  * 写 Checkpoint：启用原子重命名支持与关闭时刷新（Close-time finalization）；
* **Kubernetes (GKE) 集成**：使用 GKE GCS FUSE CSI Driver 与 Workload Identity。

---

## 4. 存储安全水位与 IAM 权限审计 (Security Assessment)
* 运行 `scripts/` 内置脚本自动化评估存储桶暴露风险：
  * 检查是否存在 `allUsers` 或 `allAuthenticatedUsers` 越权策略；
  * CMEK 自主密钥加密合规校验；
  * VPC Service Controls 边界与审计日志配置验证。
