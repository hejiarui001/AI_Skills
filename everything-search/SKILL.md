---
name: everything-search
description: >-
  Searches the user's entire Windows filesystem in sub-milliseconds using the local
  voidtools Everything engine. Use when the user asks to find, locate, or search for files,
  code, project directories, datasheets, SOLIDWORKS models, or documents across their drives
  (e.g., "帮我搜一下电脑里的xx文件", "找一下所有的.ioc工程", "找找看最近修改的固件").
license: Apache-2.0
metadata:
  version: v1.0.0
  author: voidtools-native
---

# Everything Native Desktop Search

This skill provides lightning-fast (<10ms) full-disk search across all local drives (C:, D:, E:, G:, etc.) using the user's running `voidtools Everything` engine.

---

## 1. Operating Procedure (SOP)

When the user asks to search, find, or locate files on their computer:

1. **Execute Search**:
   Call the local native script:
   ```bash
   python "C:\Users\hejia\.gemini\config\skills\everything-search\scripts\search_everything.py" "<search_query>" -n <limit>
   ```

2. **Supported Search Syntax (voidtools syntax)**:
   * **Extension search**: `ext:ioc`, `ext:sldprt`, `ext:c`, `ext:pdf`
   * **Wildcards**: `*.hex`, `*motor*`, `stm32f4*.h`
   * **Combine criteria**: `ext:ioc stm32` (finds .ioc files containing stm32 in path/name)
   * **Path search**: `path:D:\Projects *.c`
   * **Date modified**: `dm:today`, `dm:thisweek`

3. **Presenting Results**:
   Provide clickable local file links using markdown format `[filename.ext](file:///D:/path/to/filename.ext)` so the user can open them with a single click.
