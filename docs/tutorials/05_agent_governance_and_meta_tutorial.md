# Agent 运行治理、元能力与安全守则教程 (Agent Governance & Meta Tutorial)

> **领域定位**：Antigravity Agent 自进化机制、技能库健康巡检与上游同步、高危破坏拦截、Python 虚拟环境隔离与数据科学规范  
> **联动技能群**：`skills-navigator`、`notebook-data-science`、`accidental-data-loss-prevention`、`managing-python-dependencies`、`skill-repair`  
> **更新机制**：随 Agent 技能扩展、上游同步与环境适配持续循环演进

---

## 一、 Agent 自进化与运行治理闭环

```text
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 1. 技能总控与更新│ ──> │ 2. 高危操作防线 │ ──> │ 3. 依赖隔离治理 │
│ skills-navigator│     │loss-prevention  │     │python-dependenci│
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                                               │
         ▼                                               ▼
┌─────────────────┐                             ┌─────────────────┐
│ 5. 技能修复&演进│ <────────────────────────── │ 4. 严谨数据科学 │
│  skill-repair   │                             │notebook-science │
└─────────────────┘                             └─────────────────┘
```

---

## 二、 阶段实战指南与技能联动矩阵

### 1. 技能库总控、健康巡检与上游更新
* **核心目标**：统一管控全局 23 项专业技能，监控 GitHub 上游官方仓库的增量提交，提供一键同步。
* **【联动技能】**：[`skills-navigator`](../../skills-navigator/SKILL.md)
  - *触发示例*：“技能清单”、“检查技能更新”、“更新 嘉立创EDA技能”。

### 2. 高危破坏性指令拦截防线
* **核心目标**：防范不可逆的数据破坏（SQL DROP/TRUNCATE、跨目录 `rm -rf`、云端存储桶删除）。
* **SOP 规范**：任何不可逆破坏操作前，**强制停止并输出红色警示**，必须获得用户显式人工确认后方可执行。
* **【联动技能】**：[`accidental-data-loss-prevention`](../../accidental-data-loss-prevention/SKILL.md)
  - *触发示例*：“拦截高危 DROP TABLE 或格式化操作”。

### 3. Python 虚拟环境防全局污染
* **核心目标**：严禁向全局环境执行 `pip install`，强制检查当前工作区的 `.venv` 虚拟环境。
* **【联动技能】**：[`managing-python-dependencies`](../../managing-python-dependencies/SKILL.md)
  - *触发示例*：“审计当前项目的虚拟环境与依赖健康度”。

### 4. 数据科学与交互式 Notebook 研发军规
* **核心目标**：规范机器学习实验（分类、聚类、时间序列、统计检验）结构，严禁无序调试代码，产出出版物级可视化图表。
* **【联动技能】**：[`notebook-data-science`](../../notebook-data-science/SKILL.md)
  - *触发示例*：“按照专业数据科学规范重构并审计这个 Jupyter Notebook”。

### 5. 技能清单异常诊断与自动修复
* **核心目标**：诊断损坏的技能 manifest 与依赖死锁，恢复技能索引。
* **【联动技能】**：[`skill-repair`](../../skill-repair/SKILL.md)
  - *触发示例*：“诊断并修复安装失败的技能清单”。

---

## 三、 实战踩坑手记与经验增量池 (Hard-Won Knowledge)

1. **Token 预算防爆炸法则（Progressive Disclosure）**：
   - 技能主文件 `SKILL.md` 必须严控在 80 行以内，只保留关键红线、CLI 命令与状态标签；
   - 详尽的实现代码、SOP 步骤与案例必须下沉至 `references/`，按需调阅，绝不常驻上下文；
2. **三段式版本号演进协议 (SemVer)**：
   - 重大架构重构升 `MAJOR`，功能性新增/新外设支持升 `MINOR`，文档修补与时钟参数微调升 `PATCH`；
3. **双端协同 Git 冲突防御**：
   - 更新技能前必须运行 `git fetch origin main`；
   - 若远端有更新，先执行 `pull` 并在本地完成语义分析与增量融合，确认无误后再 `push`。
