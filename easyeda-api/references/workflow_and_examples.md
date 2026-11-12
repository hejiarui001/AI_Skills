# EasyEDA Pro API Workflows, Patterns & Troubleshooting

Complete code patterns, extension constraints, failure rules, and communication protocol details offloaded from [`SKILL.md`](../SKILL.md) for on-demand lookup.

---

## 1. Architecture & Bridge Protocol

```text
┌───────────┐   HTTP/WS     ┌─────────────────┐   WebSocket   ┌───────────┐
│ AI Agent  │ ◄───────────► │  Bridge Server  │ ◄───────────► │  EasyEDA  │
│           │  49620-49629  │  (Node.js)      │  49620-49629  │  (Client) │
└───────────┘               └─────────────────┘               └───────────┘
```

### Port Discovery & Handshake
- Bridge auto-binds the first free port in **`49620-49629`**.
- **HTTP Health**: `GET http://127.0.0.1:<port>/health` returns `{ "service": "easyeda-bridge", "edaConnected": bool, ... }`. Always verify `"service": "easyeda-bridge"` before using a port.
- **WebSocket Handshake**: Server sends `{ "type": "handshake", "service": "easyeda-bridge" }` on connect.
- **Extension Gateway**: Install `run-api-gateway.eext` inside EasyEDA from `https://jlc-ext.com/item/oshwhub/run-api-gateway`.

### Message Format
| Field | Type | Description |
| :--- | :--- | :--- |
| `type` | `"execute" \| "result" \| "error" \| "ping" \| "pong" \| "handshake"` | Message type |
| `id` | `string` | Request UUID for correlation |
| `code` | `string` | JS code to execute (`type: "execute"`) |
| `result` | `any` | Execution return value (`type: "result"`) |
| `error` | `string` | Error string (`type: "error"`) |
| `service` | `string` | `"easyeda-bridge"` (`type: "handshake"`) |
| `timestamp` | `number` | Unix milliseconds |

---

## 2. Multi-Window & Session Lifecycle

### Multi-Window Operations
Only re-check window selection on the **first operation** or on **window disconnected** errors (if only 1 window is connected, it is auto-selected):

```json
// GET /eda-windows response example
{
  "windows": [
    { "windowId": "abc-123", "connected": true, "active": true },
    { "windowId": "def-456", "connected": true, "active": false }
  ],
  "activeWindowId": "abc-123",
  "count": 2
}
```
- **0 windows**: Instruct the user to load `run-api-gateway.eext` in EasyEDA.
- **2+ windows**: List IDs and ask the user before switching via `POST /eda-windows/select` with `{"windowId": "abc-123"}`, or pass `"windowId"` in `POST /execute`.

### Detecting Topic Changes & Stopping the Bridge
Do **NOT** close the Bridge automatically between tasks. Only ask the user if the conversation moves away from EasyEDA/PCB/schematic for **3 consecutive turns**:
> "I notice we've moved on from EasyEDA. The Bridge server is still running in the background. Would you like me to stop it to free up resources?"

Stop only upon confirmation (scanning `49620..49629` via `Get-NetTCPConnection` + `Stop-Process` on Windows, or `lsof -ti :$port` / `kill` on Linux).

---

## 3. Code Execution Context & Extension Constraints

Code executes in EasyEDA Pro's browser runtime wrapped inside `async function(eda) { ... }`:
- No Node.js APIs (`fs`, `path`, etc.).
- No `console.log` capture — always `return await ...`.
- Omit inline JS comments (`//`) when collapsing snippets into single-line `/execute` payloads.

### Forbidden Browser APIs in Main Extension Process
`localStorage`, `window`, and `document` are available **inside `sys_IFrame`** panels, **NOT** in the main extension process:

| Purpose | Forbidden in Main | Use Instead (`eda.sys_*`) |
| :--- | :--- | :--- |
| Text input / selection | Native prompts | `eda.sys_Dialog.showInputDialog()` / `showSelectDialog()` |
| Alerts & confirms | `alert()` / `confirm()` | `eda.sys_Dialog.showInformationMessage()` / `showConfirmationMessage()` |
| Toast message | DOM manipulation | `eda.sys_Message.showToastMessage()` |
| Persistent config | `localStorage` | `eda.sys_Storage.setExtensionUserConfig(key, value)` |
| Custom HTML UI | Host DOM / `showInformationMessage(html)` | `eda.sys_IFrame.openIFrame()` |
| External link | `window.open()` | `eda.sys_Window.open()` |
| Hardware Web APIs (`navigator.serial`) | Main process | Run inside `sys_IFrame` |

### Extension <-> IFrame Communication & Direct `eda` Access
- **Pass state** via `eda.sys_Storage.setExtensionUserConfig('myKey', JSON.stringify(data))` / `getExtensionUserConfig('myKey')`.
- **Call APIs inside iframe**: EasyEDA injects `eda` directly into `sys_IFrame`. **Always use `await eda.dmt_Project.getCurrentProjectInfo()` directly — NEVER `window.parent.eda`**.

---

## 4. API Modules Overview

| Prefix | Domain | Key Classes |
| :--- | :--- | :--- |
| `DMT_` | Document management | Board, EditorControl, Folder, Panel, Pcb, Project, Schematic, SelectControl, Team, Workspace |
| `PCB_` | PCB & Footprint | Document, Drc, Event, Layer, Net, Primitive, PrimitiveComponent, PrimitiveLine, PrimitivePad, PrimitivePour, PrimitiveVia, SelectControl |
| `SCH_` | Schematic | Document, Event, Primitive, PrimitiveComponent, PrimitiveWire, SelectControl |
| `LIB_` | Library | 3DModel, Cbb, Classification, Device, Footprint, LibrariesList, PanelLibrary, SelectControl, Symbol |
| `SYS_` | System | Dialog, Environment, FileManager, FileSystem, FontManager, HeaderMenu, I18n, IFrame, LoadingAndProgressBar, Log, Message, MessageBox, MessageBus, PanelControl, Setting, ShortcutKey, Storage, Timer, ToastMessage, WebSocket, Window |
| `IPCB_` / `ISCH_` | Primitive interfaces | PrimitiveArc, PrimitiveComponent, PrimitivePad, PrimitiveFill, PrimitivePour, PrimitiveRegion, PrimitiveVia, PrimitiveWire, PrimitiveText, PrimitiveRectangle |
| `EPCB_` / `ESCH_` | Enums | PrimitiveType, LayerId (`EPCB_LayerId`), PadType, DocumentType (`EDMT_EditorDocumentType`) |

---

## 5. Common Code Patterns

### Project, Board & Open by Name
`dmt_Project.getAllProjectsUuid()` is **not** a global no-arg enumerator; iterate `dmt_Team` -> team projects -> `dmt_Folder` projects. Note `openProject(uuid)` may discard unsaved changes in the active project.

```javascript
// Find project by name across teams and folders, then open its first schematic page
const targetProjectName = 'NE555 Circuit';
const teams = await eda.dmt_Team.getAllTeamsInfo();
const seenProjectUuid = new Set();
let targetProjectUuid = null;

for (const team of teams || []) {
  for (const projectUuid of (await eda.dmt_Project.getAllProjectsUuid(team.uuid)) || []) {
    if (seenProjectUuid.has(projectUuid)) continue;
    seenProjectUuid.add(projectUuid);
    const info = await eda.dmt_Project.getProjectInfo(projectUuid);
    if ((info?.friendlyName || info?.name || '') === targetProjectName) {
      targetProjectUuid = projectUuid; break;
    }
  }
  if (targetProjectUuid) break;
  for (const folderUuid of (await eda.dmt_Folder.getAllFoldersUuid(team.uuid)) || []) {
    for (const projectUuid of (await eda.dmt_Project.getAllProjectsUuid(team.uuid, folderUuid)) || []) {
      if (seenProjectUuid.has(projectUuid)) continue;
      seenProjectUuid.add(projectUuid);
      const info = await eda.dmt_Project.getProjectInfo(projectUuid);
      if ((info?.friendlyName || info?.name || '') === targetProjectName) {
        targetProjectUuid = projectUuid; break;
      }
    }
    if (targetProjectUuid) break;
  }
  if (targetProjectUuid) break;
}
if (!targetProjectUuid) throw new Error(`Project not found: ${targetProjectName}`);
if (!await eda.dmt_Project.openProject(targetProjectUuid)) throw new Error(`Failed to open: ${targetProjectName}`);

const schematics = await eda.dmt_Schematic.getAllSchematicsInfo();
const firstSchematic = schematics?.[0];
const pages = await eda.dmt_Schematic.getAllSchematicPagesInfo();
const firstPage = (pages || []).find((p) => p.parentSchematicUuid === firstSchematic?.uuid) || firstSchematic?.page?.[0];
if (!firstPage) throw new Error('No schematic page found');
const tabId = await eda.dmt_EditorControl.openDocument(firstPage.uuid);
return { projectUuid: targetProjectUuid, schematicUuid: firstSchematic.uuid, pageUuid: firstPage.uuid, tabId };
```

### PCB Operations & `toAsync()` Primitive Mutation Pattern
```javascript
// Create copper line (PCB coordinates: 1 unit = 1 mil; layer MUST use EPCB_LayerId enum)
await eda.pcb_PrimitiveLine.create('GND', EPCB_LayerId.TOP, 0, 0, 1000, 0, 10, false);

// Modify any existing PCB/SCH primitive (toAsync -> setState_* -> done)
const prim = await eda.pcb_PrimitiveVia.get([viaId]);
const asyncPrim = prim.toAsync();
asyncPrim.setState_X(newX);
asyncPrim.setState_Y(newY);
asyncPrim.setState_Diameter(diameter);
asyncPrim.done();
```

### Schematic, Library, System & DRC Snippets
```javascript
// Create schematic component (SCH coordinates: 1 unit = 0.01 inch = 10 mil; component MUST be {libraryUuid, uuid})
await eda.sch_PrimitiveComponent.create(
  { libraryUuid: '...', uuid: 'device-uuid-from-library' },
  5000, 5000, '', 0, false, true, true
);
const schIds = eda.sch_SelectControl.getAllSelectedPrimitives_PrimitiveId();
const pcbIds = eda.pcb_SelectControl.getAllSelectedPrimitives_PrimitiveId();

// Libraries
const libs = await eda.lib_LibrariesList.getAllLibrariesList();
const devs = await eda.lib_Device.search('STM32');
const sym = await eda.lib_Symbol.get(symbolUuid);

// FileSystem & Dialog (extension sandbox)
const ok = await eda.sys_Dialog.showConfirmationMessage('Proceed?');
const txt = await eda.sys_FileSystem.readFileFromFileSystem(path);
await eda.sys_FileSystem.saveFileToFileSystem(path, content);

// Run DRC
const passed = await eda.pcb_Drc.check(true, true, false);
```

---

## 6. Common Mistakes, Verification & Failure Handling

### Top 5 AI Errors
1. **Missing `await`**: Methods returning `Promise<T>` return `<pending>` if not `await`ed.
2. **Raw integer enums**: Never write layer `1`; look up `references/enums/EPCB_LayerId.md` (`EPCB_LayerId.TOP`).
3. **Coordinate Unit Mixup**: PCB = `1 mil` (`0.0254 mm`), Schematic = `0.01 inch = 10 mil` (`0.254 mm`). Mixing them places components **10x too far**!
4. **Skipping Document State Check**: After `createProject()`, you MUST `openProject()` and verify active document before `PCB_*` / `SCH_*` calls:
   ```javascript
   const project = await eda.dmt_Project.getCurrentProjectInfo();
   if (!project) return 'Error: No project opened.';
   const doc = await eda.dmt_SelectControl.getCurrentDocumentInfo();
   if (doc?.documentType !== EDMT_EditorDocumentType.PCB) return 'Error: Active document is not PCB.';
   ```
5. **Guessing `create()` vs `modify()` signatures**: Parameter ordering often differs; always read `references/classes/<Class>.md`.

### Troubleshooting & Failure Rules
| Situation | Action |
| :--- | :--- |
| Bridge not found on `49620-49629` | Start background server (`bridge-server.mjs`) and check `/health` |
| 0 connected windows | Confirm `run-api-gateway.eext` is installed & enabled in EasyEDA |
| 30s timeout or `null` | Verify open project, active document type matching domain, or split batch calls |
| Method not in `references/classes/` | **Stop immediately** — do not hallucinate APIs; inform the user |
| Signature uncertain | **Stop** — re-read `references/classes/`, `enums/`, and `interfaces/` |
| Permission blocked error | Valid signature consistently fails due to EDA license/project restrictions — inform user |
| Forbidden browser API | Auto-replace with `eda.sys_*` (`sys_Dialog`, `sys_Storage`, `sys_IFrame`) |
| Extension menu ID conflict | Prefix menu IDs uniquely (`my-plugin-home`, `my-plugin-sch`) |

### Standard Execution Workflow
1. Identify domain (`PCB` / `SCH` / `LIB` / `DMT`) -> 2. Check active project & document type -> 3. Lookup exact signature in `references/_quick-reference.md` + `references/classes/` -> 4. Verify enums/interfaces -> 5. Execute single-line JS via `POST /execute` -> 6. Validate result & iterate.
