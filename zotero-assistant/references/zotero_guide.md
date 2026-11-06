# Zotero Local SQLite Reference Guide

This document describes how the AI Agent interacts with the local Zotero SQLite library on Windows.

---

## 1. Local Database Architecture

* **Database Path**: `C:\Users\hejia\Zotero\zotero.sqlite`
* **Storage Path**: `C:\Users\hejia\Zotero\storage\<KEY>\<filename>`
* **Access Policy**: **Read-Only (`mode=ro`)** via SQLite URI. Never execute `INSERT`, `UPDATE`, `DELETE` directly on the database to prevent Zotero data corruption.

---

## 2. CLI Tool Usage (`scripts/zotero_cli.py`)

### 2.1 搜索文献
```bash
python scripts/zotero_cli.py search "STM32" --limit 5
```
返回格式：
```json
[
  {
    "itemID": 11,
    "key": "RSZJNUY8",
    "title": "an2606-introduction-to-system-memory-boot-mode-on-stm32-mcus-stmicroelectronics",
    "pdf_paths": [
      "C:\\Users\\hejia\\Zotero\\storage\\RSZJNUY8\\an2606-introduction-to-system-memory-boot-mode-on-stm32-mcus-stmicroelectronics.pdf"
    ]
  }
]
```

### 2.2 获取详细元数据
```bash
python scripts/zotero_cli.py get 11
```

### 2.3 查看最近添加/修改文献
```bash
python scripts/zotero_cli.py recent --limit 10
```

---

## 3. 关联阅读与全文本检索
当获取到 `pdf_paths` 后，Agent 可以使用内建工具 `read_file` 直接读取目标 PDF 或抽取其文本内容进行深度论文解读、公式对比或引文生成。
