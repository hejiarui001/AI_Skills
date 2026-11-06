---
name: zotero-assistant
description: >-
  Connects to and searches the user's local Zotero reference library (zotero.sqlite)
  in read-only mode, locates full-text PDF attachments, and extracts research metadata.
  Use when the user asks about their papers, literature, citations, datasheets, or documents
  stored in Zotero (e.g., "查一下我Zotero里的论文", "找找我文献库里的STM32资料").
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
