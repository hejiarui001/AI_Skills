---
name: managing-python-dependencies
version: 1.1.0
description: >-
  Ensures proper Python dependency management, avoiding global pip install, enforcing
  virtual environment isolation, and adhering to project-specific tooling (uv, poetry, pipenv, conda, venv).
  Trigger on: "pip install", "python dependency", "requirements.txt", "virtualenv", "venv", "poetry", "uv add".
license: Apache-2.0
metadata:
  version: v1.1.0
  author: Antigravity
---

# Python Dependency & Environment Isolation Rule

本技能强制规范 Python 运行环境与依赖治理，杜绝全局 `pip install` 污染宿主操作系统。

---

## 1. 核心铁律与防御准则 (Non-Negotiable Rules)

1. **严禁全局安装 (Global Install Prohibited)**：
   * 绝对禁止在宿主全局环境中直接运行裸 `pip install <package>`；
   * 必须在项目根目录探测或创建虚拟环境（`.venv`）。
2. **工具链优先级探测 (Respect Project Tooling)**：
   * 安装任何依赖前，必须探测既有配置文件，严禁用不同工具覆盖项目既有生态；
   * 探测顺序：**uv (`uv.lock`) $\to$ Poetry (`[tool.poetry]`) $\to$ Pipenv (`Pipfile`) $\to$ Conda (`environment.yml`) $\to$ venv (`requirements.txt`)**；
   * 统一使用复合探测命令：`ls uv.lock poetry.lock Pipfile.lock requirements.txt pyproject.toml 2>/dev/null`。
3. **默认工作流规范 (Default venv + pip)**：
   * 若无专属管理器，默认使用显式虚拟环境路径调用：
     - **Linux**: `.venv/bin/pip install <pkg> && .venv/bin/pip freeze > requirements.txt`
     - **Windows**: `.\.venv\Scripts\pip.exe install <pkg>; .\.venv\Scripts\pip.exe freeze > requirements.txt`
4. **复合预检探针 (Composite Pre-Flight Probe)**：
   * 禁止多条分散的探测命令，必须通过一条复合单行 Python 指令核验 Python 版本与关键库。

---

## 2. 深度参考手册

* 📘 **包管理器检测大表与多平台对照**：查阅 [`references/package_managers.md`](file:///C:/Users/hejia/.gemini/config/skills/managing-python-dependencies/references/package_managers.md)。
