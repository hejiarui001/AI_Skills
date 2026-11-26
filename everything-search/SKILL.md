---
name: everything-search
version: 1.0.0
description: "voidtools Everything 本地全盘毫秒级极速文件检索。Trigger on: 搜一下文件, 找工程, 找.ioc, 搜索本地文件。"
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
