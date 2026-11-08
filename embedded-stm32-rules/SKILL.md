---
name: embedded-stm32-rules
version: 1.10.0
description: >-
  Enforces professional embedded C/C++ development guidelines and PIA (Progressive
  Instance-driven Architecture) for STM32 microcontrollers, ARM Cortex-M architecture,
  and hardware abstraction layer (HAL/LL). Use when writing, reviewing, refactoring,
  or designing STM32 firmware, peripheral drivers (UART, SPI, I2C, DMA, ADC, PWM, CAN),
  cooperative time-sliced task schedulers, FreeRTOS integration, or VOFA+ debugging protocols.
license: Apache-2.0
metadata:
  version: v1.9.0
  source: awesome-cursorrules-embedded & PIA Architecture Standard
---

# Embedded STM32 & MCU Engineering Guidelines (with PIA Architecture)

This skill enforces strict, production-grade embedded C/C++ development practices and the **PIA (Progressive Instance-driven Architecture)** derived from top-tier robotics (RoboMaster, Robocon) and high-reliability aerospace/flight control frameworks (Betaflight, PX4, QP/C).

---

## 1. Core Operating Procedure (SOP)

When generating or reviewing code for STM32 / MCU platforms, the agent must follow these steps:

1. **Architecture & Peripheral Verification**:
   - Confirm MCU family (e.g., F1, F4, G4, H7) and core constraints (Cortex-M0/M3/M4/M7).
   - If targeting Cortex-M7 (H7/F7), verify D-Cache alignment and DMA buffer placement.
2. **Universal Workspace & Progressive Architecture Enforcement (PIA Protocol)**:
   - **Universal Multi-Workflow Directory Baseline**: In heterogeneous projects (CubeMX, Keil, CMake, PlatformIO, PC tools), isolate project concerns into 5 standard zones:
     - `Firmware/`: Holds pure C/C++ embedded code under 4-tier model (`App/`, `Module/`, `Service/`, `BSP/`).
     - `Host/`: Holds PC-side clients (Python/Qt), serial testing tools, and launch scripts.
     - `docs/`: Holds schematics, interface documents, and reference datasheets.
     - `_checkpoints/`: Holds zero-build-cache milestone snapshots (< 400KB).
     - `SOFTWARE_SPEC.md`: Root software specification & handover manual.
     - `<Toolchain_Anchors>`: Toolchain-bound generation anchors (`Core/`, `Drivers/`, `MDK-ARM/`, `CMakeLists.txt`, `cmake/`, `.ioc`, `.vscode/`) remain strictly at root to prevent code re-generation conflicts and IDE breakage.
   - **Dual-Workflow Architecture (MDK-ARM + CMake)**: Support dual-engine projects sharing the same `Firmware/` core. For MDK-ARM, mount `Firmware/` via virtual Groups; for CMake, inject non-invasively via `add_subdirectory(Firmware)`. Ensure CubeMX re-generation safety and GCC/ArmClang portability per [dual_workflow_mdk_cmake_guide.md](./references/dual_workflow_mdk_cmake_guide.md).
   - **4-Tier Directory Layout**: Maintain clean separation across `BSP/` (on-chip peripherals), `Module/` (external devices & algorithms), `Service/` (scheduler, blackboard, protocol), and `App/` (behavior FSM).
   - **Monolithic File Prohibition**: Single `.c` files must not exceed **400 lines**. Actuators, displays, protocols, and state machines must reside in separate files.
   - **Unidirectional Dependency**: `BSP` and `Module` layers must never include `App/` headers.
   - **Instance-Driven Abstraction**: Actuators (motors, valves) and sensors must be encapsulated into handle structs (`Dev_t*`) to allow seamless multi-channel scaling without modifying driver code.
   - **Zero Naked Delays**: Never use `HAL_Delay()` in the main execution path. Use the static cooperative task table (`Service/sys_scheduler.c`) or non-blocking delta ticks (`now - last_tick >= interval`).
   - **Data Blackboard Decoupling**: Avoid scattering bare global `extern` variables across files; route shared data through a unified `SystemBlackboard_t`.
3. **Deterministic Real-Time Execution**:
   - Enforce **zero dynamic allocation** (`malloc`/`free`) in real-time execution paths.
   - Enforce **strict non-blocking patterns** (use state machines, DMA, or hardware timers).
   - Use explicit fixed-width integers from `<stdint.h>` (`uint8_t`, `int32_t`, etc.).
4. **Interrupt Safety (ISR)**:
   - Keep ISRs fast and minimal (< 10 µs).
   - Never call `printf`, `HAL_Delay`, or blocking transmit functions inside ISRs or callbacks.
   - Mark all shared global flags/variables as `volatile`.
5. **Milestone Checkpoint & Rollback**:
   - Before major refactoring, protocol modifications, or after successfully verifying a new hardware feature, create a lightweight milestone checkpoint in `_checkpoints/` using [embedded_checkpoint.py](./scripts/embedded_checkpoint.py).
   - Filter intermediate build caches (`*.o`, `*.crf`, `*.d`, etc.) to achieve >99% disk space reduction while guaranteeing 1-click restore (`RESTORE.ps1`).
6. **Software Specification Delivery (with Handover Guide)**:
   - For every project or significant milestone, generate or synchronize `SOFTWARE_SPEC.md` in the project root following [software_spec_standard.md](./references/software_spec_standard.md).
   - Document executive project overview, architecture deep dive (code map, lifecycle sequence, data flow), electrical pinout, cooperative task schedules, statecharts, handover/extension guide (how to add channels/commands, pitfalls), and pre-allocated upgrade partitions (IAP/Flash map & reserved fields).
7. **ADC Sampling & Filtering Selection Protocol**:
   - For analog sampling, select filtering strategy according to load and dynamics:
     - **Option A (Inductive / Motor Loads)**: Deploy **Adaptive Composite Filter** (DMA spatial trimmed-mean outlier rejection + temporal adaptive dual-rate IIR + zero deadband) to eliminate brush sparks while maintaining < 10ms trip latency for overload protection.
     - **Option B (Resistive / Slow Sensors or Low Compute)**: Fall back to **Low-Quantization Bit-Shift Filter** (power-of-2 window bit-shift + fixed-point IIR) for zero-multiplier, microsecond-level execution.
8. **Compiler & DSP Toolchain Compatibility (ArmClang 6 vs CMSIS-DSP & MicroLIB)**:
   - When building STM32 (H7/F4/G4) projects linking precompiled CMSIS-DSP `.lib` files under ArmClang 6:
     - Enforce `-fshort-enums -fshort-wchar` in `MiscControls` to prevent `L6242E` attribute collisions (`wchart-16/32`, `packed-enum/enum_is_int`).
     - If ArmClang 6.20-6.24 `armlink.exe` crashes with `mc_w.l:2982 Error: L6907E: Expected an expression`, switch the linker stage to `ARMCC\bin\armlink.exe` (Linker V5.06) or decouple wide characters from MicroLIB.
     - In headless CLI compilation, assemble `startup_stm32xxxx.s` with `--pd "__MICROLIB SETA 1"` and match the exact FPU target (`--cpu=Cortex-Mx.fp.sp`) to avert `L6218E` undefined `__use_two_region_memory` and `L6366E` VFP attribute clashes.
     - Replace missing GCC builtins (`__builtin_arm_smuad`) with inline assembly in `cmsis_armclang.h`.
     - Full resolution guide: [armclang_cmsis_dsp_compatibility.md](./references/armclang_cmsis_dsp_compatibility.md).
9. **Validation**:
   - Run the linting script [check_c_embedded_rules.py](./scripts/check_c_embedded_rules.py) against generated files when needed to ensure zero rule violations.
10. **I2C Bus Deadlock Recovery & PMIC Mode Verification Protocol**:
   - When driving I2C peripherals (sensors, EEPROM, battery chargers, PMICs), implement 9-clock bus recovery (`I2C_Bus_Recover()`) to clear slave SDA deadlock before initializing I2C hardware.
   - **Dual Trap Prevention**: After emitting 9 pulses, explicitly re-initialize GPIO pins to `GPIO_MODE_AF_OD` (`GPIO_AF4_I2C1`) and call `HAL_I2C_DeInit()` to restore the HAL state machine to `HAL_I2C_STATE_RESET` before invoking `HAL_I2C_Init()`.
   - **PMIC Hardware Mode Pin Check**: When interfacing PMICs (e.g., MP2672, BQ series), verify mode selection pins (e.g. `CV` pin) are pulled up to internal VCC for Host-Control mode; pull-downs force standalone autonomous mode where I2C slave is completely disabled and returns NACK.
   - Full protocol guide: [i2c_bus_recovery_and_pwr_traps.md](./references/i2c_bus_recovery_and_pwr_traps.md).
11. **CubeMX `.ioc` Dual-Directional Synchronization & Anti-Overwrite Protocol**:
    - Never rely on manual code patches in generated toolchain directories (`Core/Src/gpio.c`, `Core/Src/i2c.c`, etc.).
    - All electrical pin attributes (Internal Pull-Up, Open-Drain, Speed) and peripheral clock parameters must be explicitly committed back into the `.ioc` configuration file.
    - Ensure that running CubeMX "GENERATE CODE" will never wipe out hardware critical setups or cause floating bus/pin states.
12. **Scaffolding Deconstruction & Physical Code Pruning Standard**:
    - During hardware bring-up, auxiliary scaffolding (multi-resolution carousels, test patterns, probing loops) may be introduced.
    - Once the physical hardware specification is confirmed or the user instructs negative pruning ("把其他模式删掉"), all temporary tables, test routines, and obsolete commands must be physically removed from production code within the same delivery cycle.
    - Keep driver files modularized under 400 lines (offload large init arrays to `*_cfg.h`), and never hardcode host environment strings (e.g. `COM5`) into device displays.


---

## 2. On-Demand Specialized References

Refer to the following guides for concrete implementations and protocol details:

* **Software Specification Standard**:
  See [Software Specification Standard](./references/software_spec_standard.md) for firmware documentation templates with memory maps, pinout tables, task schedules, statecharts, and upgrade planning.
* **PIA Progressive Software Architecture**:
  See [PIA Architecture Reference](./references/progressive_architecture_pia.md) for 4-tier directory patterns, static cooperative task scheduler (< 50 lines), instance handle registration, system blackboard, and daemon heartbeats.
* **VOFA+ Protocol & Telemetry**:
  See [VOFA+ Protocol Reference](./references/vofa_protocol.md) for ready-to-use C struct definitions and packet encoders for `JustFloat` (tail: `0x00 0x00 0x80 0x7F`) and `FireWater`.
* **UART + DMA + IDLE Ring Buffer**:
  See [UART DMA Pattern](./references/stm32_uart_dma_pattern.md) for circular buffer implementations and modern `HAL_UARTEx_ReceiveToIdle_DMA` workflows.
* **ADC Sensor & Power Sampling Patterns**:
  See [ADC Filtering Patterns](./references/adc_filtering_patterns.md) for dual-option filtering specification (Composite anti-spike adaptive IIR vs Low-quantization bit-shift) and macro switch templates.
* **I2C Bus Recovery & PMIC Mode Traps**:
  See [I2C Bus Recovery & PMIC Traps Guide](./references/i2c_bus_recovery_and_pwr_traps.md) for 9-clock bus deadlock clearing, AF4 alternate function re-mapping traps, and PMIC standalone vs host-control mode pins.
* **HardFault Diagnostics**:
  See [HardFault Diagnostics Reference](./references/hardfault_diagnostics.md) for assembly exception dump handlers and root cause register analysis.
* **ArmClang 6 & CMSIS-DSP Toolchain Compatibility**:
  See [ArmClang CMSIS-DSP Guide](./references/armclang_cmsis_dsp_compatibility.md) for resolving `L6242E` attribute clashes, `L6907E` linker selection script locks, `L6218E` MicroLIB symbol missing, and GCC builtins substitution (`__builtin_arm_smuad`).
* **Dual-Workflow Architecture (MDK-ARM + Modern CMake)**:
  See [Dual-Workflow Guide](./references/dual_workflow_mdk_cmake_guide.md) for configuring dual-engine projects sharing the same `Firmware/` core, CubeMX regeneration safe protocols, and cross-compiler portability rules (ArmClang 6 vs GCC).
* **CubeMX `.ioc` Sync & Scaffolding Pruning Standard**:
  See [CubeMX IOC Sync & Scaffolding Rules](./references/cubemx_ioc_sync_and_scaffolding_rules.md) for overwrite immunity SOP, clock triangulation rules (BOM + IOC + Register), immediate scaffolding physical deconstruction, and driver decoupling under 400 lines.

---

## 3. Tool Verification Checklist

Before presenting embedded code to the user, verify:
- [ ] Project directory structure conforms to Universal Workspace Baseline (`Firmware/` enclosing PIA 4-tier `BSP/`, `Module/`, `Service/`, `App/`, plus `Host/`, `docs/`, `_checkpoints/`). Toolchain generation roots (`Core/`, `Drivers/`, `MDK-ARM/`, `.ioc`) remain at root.
- [ ] Major feature milestones or refactoring steps are checkpointed in `_checkpoints/` with `CHECKPOINT_NOTE.md` and `RESTORE.ps1`.
- [ ] Single `.c` file length <= 400 lines (modularized into Module/Service/App).
- [ ] No reverse dependency (BSP/Module never includes App headers).
- [ ] No `HAL_Delay()` inside interrupt callbacks, ISRs, or recurring loops (use cooperative scheduler).
- [ ] No `malloc()` / `free()` calls.
- [ ] All hardware registers and interrupt-shared variables are declared `volatile`.
- [ ] Multi-channel peripherals use handle-based structs (`Actuator_t*`) rather than duplicate hardcoded functions.
- [ ] ADC sampling applies appropriate filtering pattern (Option A: Adaptive composite for motors vs Option B: Low-quantization bit-shift for resistive/slow signals).
- [ ] I2C bus recovery includes 9-clock pulse clearing, explicit `GPIO_MODE_AF_OD` remapping, and `HAL_I2C_DeInit()` state reset; PMIC mode pins are verified before assuming bus/IC hardware damage.
- [ ] Project root contains or synchronizes `SOFTWARE_SPEC.md` documenting task schedules, electrical pinouts, and upgrade partitions.
- [ ] Peripheral clock is enabled before peripheral registers are accessed.
- [ ] Status return value `HAL_StatusTypeDef` is checked on critical initializations.
- [ ] For ArmClang 6 projects linking CMSIS-DSP precompiled libraries, `-fshort-enums -fshort-wchar` is configured in `MiscControls` to avert ABI clashes; in headless CLI, `startup_stm32xxxx.s` includes `--pd "__MICROLIB SETA 1"` and links via ARM Linker V5.06 if L6907E occurs.
- [ ] CubeMX `.ioc` is strictly synchronized with code: pin pull-ups, open-drain, and clock trees match so that code re-generation is non-destructive.
- [ ] Hardware clock source is triangulated against BOM silk screen, `.ioc` HSE_VALUE, and runtime PLL registers.
- [ ] All temporary hardware bring-up scaffolding (carousels, test patterns, unneeded driver branches) has been physically pruned upon hardware specification confirmation.
