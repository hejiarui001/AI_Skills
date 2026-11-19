# AI Skills 领域实战精炼教程与技能联动体系 (Domain Master Tutorials)

> **定位**：Antigravity Agent 领域作战全景地图、实战心法与技能双向联动中枢  
> **设计哲学**：**“技能保持精炼锋利（低 Token 消耗执行单项武器），教程写透全景与联动（高密度沉淀领域流水线与实操心法）”**  
> **演进机制**：随实际项目进行持续增量沉淀，形成 **“实战项目踩坑 -> 教程吸收沉淀 -> 技能升级进化 -> 赋能新项目”** 的永续闭环。

---

## 一、 五大核心领域实战教程快速索引

| 序号 | 领域教程文档 | 覆盖核心业务与技术栈 | 核心联动技能群 |
| :---: | :--- | :--- | :--- |
| **01** | [**嵌入式软硬件全栈实战教程**](./01_embedded_hardware_tutorial.md) | STM32 / ESP32 电路设计、PIA 分层架构、无头固件构建、pyOCD 烧录与 VOFA+ 遥测 | `easyeda-api`<br>`embedded-stm32-rules`<br>`cortex-m-pyocd`<br>`industrial-serial-agent`<br>`embedded-engineering-master` |
| **02** | [**系统运维、科研学术与财务报销教程**](./02_system_academic_finance_tutorial.md) | Windows 40 款兵器运维、Everything 毫秒搜盘、Zotero 文献手册库、高校发票报销 11 列总账、Git 汇报与多维发散调研 | `pc-maintenance-master`<br>`everything-search`<br>`zotero-assistant`<br>`invoice-audit-master`<br>`git-worklog-reporter`<br>`divergent-search-guide` |
| **03** | [**路由系统、P2P专网穿透与低延迟串流教程**](./03_network_and_p2p_streaming_tutorial.md) | MikroTik RouterOS 堡垒路由、192.168.8.x 命脉五层自检、EasyTier 国内高速 Mesh 专网、Moonlight 4K 串流与压测 | `routeros-network-master`<br>`p2p-streaming-master`<br>`google-sync-guard` |
| **04** | [**云原生大数据、数据流与治理教程**](./04_gcp_bigdata_engineering_tutorial.md) | Google Cloud ADC 认证合规、BigQuery 高性能数仓/BQML、GCS 存储分层与 FUSE、Airflow 2/3 调度总成、dbt/Dataform | `bigquery-master`<br>`gcs-storage-suite`<br>`gcp-airflow-composer-suite`<br>`gcp-data-engineering`<br>`gcp-governance-assets` |
| **05** | [**Agent 运行治理、元能力与安全守则教程**](./05_agent_governance_and_meta_tutorial.md) | 全量技能健康巡检与上游同步、高危破坏拦截防线、Python 环境隔离、数据科学 Notebook 军规与 SemVer 演进 | `skills-navigator`<br>`notebook-data-science`<br>`accidental-data-loss-prevention`<br>`managing-python-dependencies`<br>`skill-repair` |

---

## 二、 教程与 Skills 双向联动机制 (Bidirectional Symbiosis)

```text
┌────────────────────────────────────────────────────────┐
│           领域实战教程 (Domain Master Tutorial)        │
│   • 讲解业务全景、系统拓扑、阶段 SOP 与实战踩坑手记      │
│   • 在关键实战阶段显式标注并嵌入对应技能及标准 Prompt    │
└──────────────────────────┬─────────────────────────────┘
                           │
                 【阶段驱动】调起对应技能
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│               专业原子技能 (Specialized Skill)          │
│   • 保持 < 80 行极低 Token 消耗，纯粹执行具体指令       │
│   • 头部反向索引所属领域教程链接，便于随时深入调阅      │
└──────────────────────────┬─────────────────────────────┘
                           │
                 【实战踩坑】反哺增量经验
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│              实战经验增量池 (Hard-Won Knowledge)       │
│   • 随真实项目调试解决的硬故障，持续追加至教程增量章节  │
│   • 当沉淀出通用规约时，升段升级 Skill 并推送云端       │
└────────────────────────────────────────────────────────┘
```

---

## 三、 持续演进准则 (Continuous Evolution Protocol)

1. **教程高密度原则**：教程拒绝虚泛说教，直击物理本质、寄存器位域、网络拓扑图与参数对照表；
2. **零日常 Token 负荷**：教程文件收敛在 `docs/tutorials/` 独立目录中，日常任务中仅由 Agent 在需要了解全链路架构或学习时按需调阅，绝不随 `SKILL.md` 常驻上下文；
3. **版本演进联动**：每当在实际项目中突破重大技术难点并扩充教程内容时，对应的领域技能按 SemVer 规范升级版本号，并在 `CHANGELOG.md` 中记录演进台账。
