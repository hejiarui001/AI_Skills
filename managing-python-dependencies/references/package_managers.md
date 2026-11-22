# Python 包管理器检测与多工具链速查手册 (Python Dependency Manager Reference)

> **版本**：v1.1.0 | **所属技能**：`managing-python-dependencies`  
> **说明**：在执行任何 Python 包安装前，必须按优先级检测项目既有的包管理工具，禁止破坏既有生态。

---

## 1. 复合预检探测命令 (Pre-Flight Composite Probe)

严禁执行多条分散的探测命令，必须通过复合探针一条命令完成环境探测：

```bash
# Linux / macOS
python3 -c "import sys, importlib.util; print(f'Python {sys.version.split()[0]}'); [(print(f'{pkg}: {__import__(pkg).__version__}') if importlib.util.find_spec(pkg) else print(f'{pkg}: not found')) for pkg in ['pyspark', 'google.cloud.bigquery']]"

# Windows PowerShell
python -c "import sys, importlib.util; print(f'Python {sys.version.split()[0]}'); [(print(f'{pkg}: {__import__(pkg).__version__}') if importlib.util.find_spec(pkg) else print(f'{pkg}: not found')) for pkg in ['pyspark', 'google.cloud.bigquery']]"
```

包管理器锁定文件一键复合扫描：
```bash
# 统一扫描命令
ls uv.lock poetry.lock Pipfile.lock requirements.txt pyproject.toml environment.yml 2>/dev/null
```

---

## 2. 依赖管理工具检测与优先级矩阵 (Priority Matrix)

按以下**严格优先级顺序**检测项目既有配置：

| 优先级 | 特征文件 / 信号 (Signal) | 识别工具 (Tool) | 依赖安装命令 (Install) | 环境初始化命令 (Setup) |
| :---: | :--- | :---: | :--- | :--- |
| **1** | `uv.lock` 或 `pyproject.toml` 包含 `[tool.uv]` | **uv** | `uv add <package>` | `uv sync` |
| **2** | `pyproject.toml` 包含 `[tool.poetry]` | **Poetry** | `poetry add <package>` | `poetry install` |
| **3** | `Pipfile` | **Pipenv** | `pipenv install <package>` | `pipenv install` |
| **4** | `environment.yml` | **Conda** | `conda install <package>` | `conda env create -f environment.yml` |
| **5** | 仅 `requirements.txt` | **venv + pip** | `.venv/bin/pip install <pkg>` | `.venv/bin/pip install -r requirements.txt` |
| **6** | 无任何上述配置文件 | **venv + pip** *(默认)* | `.venv/bin/pip install <pkg>` | `.venv/bin/pip install -r requirements.txt` |

---

## 3. 标准 venv + pip 工作流 (Windows / Linux 对照)

当未检测到更高级的包管理工具时，强制采用标准虚拟环境隔离：

### Linux (Bash)
```bash
# 1. 创建虚拟环境
python3 -m venv .venv

# 2. 显式路径安装依赖
.venv/bin/pip install <package>

# 3. 固化依赖状态
.venv/bin/pip freeze > requirements.txt
```

### Windows (PowerShell)
```powershell
# 1. 创建虚拟环境
python -m venv .venv

# 2. 显式路径安装依赖
.\.venv\Scripts\pip.exe install <package>

# 3. 固化依赖状态
.\.venv\Scripts\pip.exe freeze > requirements.txt
```
