---
name: easyeda-api
version: 1.2.0
description: >-
  EasyEDA Pro API skill for AI agents. Use when working with EasyEDA Pro EDA software,
  including PCB design, schematic editing, footprint/symbol management, and project operations.
  Supports live debugging in EasyEDA and EasyEDA extension development. Provides complete API
  reference (120+ classes, 62 enums, 70 interfaces), extension-development documentation, and a
  WebSocket bridge server to execute code in the running EasyEDA Pro client.
  Trigger on: "嘉立创EDA，启动！", "立创EDA，启动！", "EDA，启动！",
  "EasyEDA", "PCB", "schematic", "footprint", "EDA", "circuit board",
  "嘉立创EDA", "原理图", "PCB设计".
  **IMPORTANT**: 嘉立创EDA's English name is **EasyEDA**. They are the SAME product.
  Never use other transliterations like "EasyEDA Pro" (unless specifically versioned), "EASYEDA", "easyeda", etc. Always use "EasyEDA" for English references and "嘉立创EDA" for Chinese references.
license: MIT
compatibility: Requires Node.js 18+, EasyEDA Pro desktop client with extension support
metadata:
  author: JLCEDA
  version: "1.2.0"
  openclaw:
    requires:
      bins:
        - node
      env:
        - CLAUDE_SKILL_DIR
---

# EasyEDA Pro API Skill (v1.2)

Control EasyEDA Pro (嘉立创EDA专业版) programmatically via WebSocket bridge or author extensions using full API/document-format specs.

## 1. Trigger & Cross-Platform Bridge Setup

* **Command Triggers** (`"嘉立创EDA，启动！"`, `"立创EDA，启动！"`, `"EDA，启动！"`): reply immediately with `📋 EasyEDA Session`, then verify bridge & client window.
* **Client Extension**: EasyEDA Pro must have [`run-api-gateway.eext`](https://jlc-ext.com/item/oshwhub/run-api-gateway) installed and active.
* **Auto-Discovery**: Bridge scans/binds **`49620-49629`**; verify `GET http://127.0.0.1:<port>/health` returns `"service":"easyeda-bridge"`. Do **not** run `bridge-server.mjs` in foreground.

```powershell
# Windows (PowerShell): discover or start bridge & inspect active window
$p = 49620..49629 | Where-Object { try { (Invoke-RestMethod "http://127.0.0.1:$_/health").service -eq "easyeda-bridge" } catch { $false } } | Select-Object -First 1
if (-not $p) { Start-Process node -ArgumentList "scripts/bridge-server.mjs" -WorkingDirectory "<SKILL_DIR>" -WindowStyle Hidden; Start-Sleep 2 }
Invoke-RestMethod "http://127.0.0.1:$(if($p){$p}else{49620})/eda-windows"
```

```bash
# Linux (Bash): install deps once if missing -> cd <SKILL_DIR> && npm install
for port in $(seq 49620 49629); do
  curl -s http://127.0.0.1:$port/health | grep -q '"easyeda-bridge"' && BRIDGE_PORT=$port && break
done
[ -z "$BRIDGE_PORT" ] && { node <SKILL_DIR>/scripts/bridge-server.mjs & sleep 2; BRIDGE_PORT=49620; }
curl -s http://127.0.0.1:$BRIDGE_PORT/eda-windows
```

* **Execute JS**: `POST http://127.0.0.1:<port>/execute` with JSON `{"code": "return await eda.dmt_Project.getCurrentProjectInfo();"}` (pass `"windowId"` or `POST /eda-windows/select` if 2+ windows exist).
* **Session Stop Policy**: Keep Bridge alive during work; only ask to stop after **3 consecutive non-EDA turns**. Stop via `Get-NetTCPConnection -LocalPort <port> | ForEach-Object { Stop-Process -Id $_.OwningProcess }` (Win) or `lsof -ti :<port> | xargs kill` (Linux).

## 2. Five Non-Negotiable Core Rules

1. **Browser Sandbox Runtime**: Code wraps in `async function(eda) { ... }`. No Node `fs`/`path`; no `console.log` capture (MUST `return await ...`); omit `//` comments when flattening code into single-line `/execute` JSON.
2. **Signature & Enum Verification**: **NEVER guess signatures or raw enum numbers.** Inspect `_quick-reference.md` & `references/classes/` first; ALWAYS `await` `Promise<T>` returns and use enums (`EPCB_LayerId.TOP`, `EDMT_EditorDocumentType.PCB`).
3. **Coordinate Units (Critical #1 Bug)**:
   * **PCB domain**: `1 unit = 1 mil` (`0.0254 mm`, `1 mm ≈ 39.37`)
   * **Schematic domain**: `1 unit = 0.01 inch = 10 mil` (`0.254 mm`, `1 mm ≈ 3.937`) — mixing units misplaces parts by **10x**.
4. **Document State & Mutation Protocol**: Verify `dmt_Project.getCurrentProjectInfo()` (after `createProject()` you MUST `openProject()`) and confirm `dmt_SelectControl.getCurrentDocumentInfo()?.documentType` matches PCB/SCH before calls. Mutate primitives strictly via `prim.toAsync()` -> `setState_*()` -> `done()`.
5. **Extension & IFrame Isolation**: Main extension process forbids `alert`/`confirm`/`localStorage`/`window.open` (use `eda.sys_Dialog`, `eda.sys_Storage`, `eda.sys_IFrame`, `eda.sys_Window`). Inside `sys_IFrame`, access **`eda` directly** (`await eda.*`), NEVER `window.parent.eda`.

## 3. On-Demand References & Source Format Docs

Load detailed docs only as needed:
* **Workflows, Full Code Patterns & Troubleshooting**: [`references/workflow_and_examples.md`](references/workflow_and_examples.md) (project search across teams/folders, PCB/SCH/LIB/DRC snippets, forbidden API table, failure rules)
* **API Catalog**: [`references/_index.md`](references/_index.md) | [`references/_quick-reference.md`](references/_quick-reference.md) | `references/{classes,enums,interfaces,types}/` (120 classes, 62 enums, 70 interfaces, 19 types)
* **Document Source Format**: [`format/index.md`](format/index.md) | `format/{project,schematic,pcb}/`
