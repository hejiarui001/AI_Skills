# 技能异常诊断与 Manifest 修复指南 (Skill Repair & Manifest Restoration Guide)

> **版本**：v1.9.0 | **所属技能**：`skills-navigator`  
> **定位**：当本地或插件技能在安装、更新或解析过程中发生损坏、缺失依赖或 `manifest.json` 报错时，提供精准的手术式排查与修复流程。

---

## 1. 核心上下文要素 (Skill Context)

在处理损坏的技能前，确认以下 4 个关键路径与标识：
* **Skill ID**：技能的唯一标识符（例如 `easyeda-api`、`routeros-network-master`）。
* **Source Path**：技能的源码仓库路径（如 `C:\Users\hejia\.gemini\config\skills\<skill_name>` 或 Linux 对应目录）。
* **Installed Path**：技能在宿主环境中的安装或映射路径。
* **Manifest Path**：技能清单 `manifest.json`（或 `.datacloud_skills_manifest`）的绝对路径。

---

## 2. 标准化修复 SOP (Standard Repair Procedure)

1. **错误根因定位 (Analyze Error)**：
   * 调阅提示词或控制台报错日志，排查是 YAML frontmatter 语法错误、缺少 `SKILL.md`、换行符问题还是 Python 依赖导入失败。
2. **源码与安装路径修复 (Fix Installed Path)**：
   * 检查技能根目录下的全部文件，修复语法错误或补全缺失的 `references/`、`scripts/` 文件；
   * 确保 `SKILL.md` 包含标准三段式版本号（`version: MAJOR.MINOR.PATCH`）与合规的 description。
3. **更新 Manifest 状态 (Update Manifest)**：
   * 打开对应清单文件（`manifest.json`），在 `skills` 对象中定位对应的 Skill ID；
   * 将 `"status"` 设置为 `"installed"`；
   * 清除 `"error"` 字段（将其设为 `null` 或直接删除）；
   * 将 `"disabled"` 设置为 `false`。
4. **验证与状态刷新 (Verification)**：
   * 运行 `python check_skills_status.py` 验证技能健康度是否转为全绿（Normal）。

---

## 3. Manifest 结构示例 (Manifest Example)

```json
{
  "skills": {
    "my-skill": {
      "status": "installed",
      "disabled": false,
      "error": null
    }
  }
}
```
