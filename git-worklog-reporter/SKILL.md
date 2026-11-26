---
name: git-worklog-reporter
version: 1.0.0
description: "Git 研发日报/周报生成器：自动提取本地 Git 提交与文件变更统计并输出高管级结构化汇报。Trigger on: 日报, 周报, 总结代码, 汇报工作进展。"
license: Apache-2.0
metadata:
  version: v1.0.0
  author: git-standup-reporter
---

# Git Engineering Worklog & Report Generator

This skill leverages local Git version control history (inspired by `kamranahmedse/git-standup`, 7.9k+ ⭐) to automatically extract code changes and synthesize professional, high-impact daily and weekly engineering reports.

---

## 1. Core Operating Procedure (SOP)

When the user requests an engineering daily/weekly report or work recap:

1. **Identify Target Repository & Time Range**:
   - Determine repo path: Current working directory by default, or the path specified by the user.
   - Determine time window:
     - Daily report / standup: `--days 1` (or 2 if Monday)
     - Weekly report: `--days 7`
     - Custom: user-specified day count

2. **Extract Git Activity**:
   Execute the extractor script:
   ```bash
   python "C:\Users\hejia\.gemini\config\skills\git-worklog-reporter\scripts\git_reporter.py" -p "<repo_path>" -d <days>
   ```

3. **Synthesize & Elevate Report**:
   - Parse the JSON output (`summary`, `commits`, `file_types`).
   - **Do not simply copy-paste commit subjects**:
     - Group related commits by subsystem (e.g., Drivers, Algorithms, Protocols, Configs).
     - Elevate technical details into clear engineering achievements (e.g., "Fixed timer bug" -> "Resolved TIM2 counter overflow edge case, stabilizing PWM output").
     - Highlight file impact and lines modified when relevant.

4. **Format Output**:
   Format the result using the structured templates in [Report Templates](./references/report_templates.md):
   - **Daily Report**: Highlights, Technical Hurdles & Fixes, Next Day Plan.
   - **Weekly Report**: Core Milestones, Detailed Task Status Table, Risks/Blockers, Next Week Objectives.
