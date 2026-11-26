---
name: zotero-assistant
version: 1.0.0
description: "本地 Zotero 文献库 (zotero.sqlite) 只读检索、芯片 Datasheet 与 PDF 附件元数据提取。Trigger on: Zotero, 查论文, 找文献, 查芯片资料。"
license: Apache-2.0
metadata:
  version: v1.0.0
  author: Antigravity
---

# Zotero Local Literature Assistant

This skill gives the agent read-only access to the user's local Zotero library, enabling instant document retrieval, literature synthesis, and PDF discovery without requiring third-party API keys or cloud syncing.

---

## 1. Core Operating Procedure (SOP)

When the user inquires about literature, research papers, datasheets, or citations in their Zotero library:

1. **Search Zotero Library**:
   Execute the local Python CLI:
   ```bash
   python "C:\Users\hejia\.gemini\config\skills\zotero-assistant\scripts\zotero_cli.py" search "<keyword>" --limit 5
   ```
   Or list recent items if no keyword is specified:
   ```bash
   python "C:\Users\hejia\.gemini\config\skills\zotero-assistant\scripts\zotero_cli.py" recent --limit 5
   ```
2. **Inspect Metadata & Attachments**:
   If a specific item needs deeper analysis, call `get`:
   ```bash
   python "C:\Users\hejia\.gemini\config\skills\zotero-assistant\scripts\zotero_cli.py" get <itemID>
   ```
   Check the `pdf_paths` field in the JSON response.
3. **Full-Text Analysis**:
   If a valid local PDF path exists (e.g., in `C:\Users\hejia\Zotero\storage\...`), use `read_file` to read the document content and answer the user's research, mathematical, or firmware questions directly.
4. **Safety Guarantee**:
   All database connections use `file:...mode=ro` (read-only SQLite). Never execute write or mutate queries against `zotero.sqlite`.

---

## 2. Reference Documentation

For database architecture and schema details, see [Zotero Guide](./references/zotero_guide.md).
