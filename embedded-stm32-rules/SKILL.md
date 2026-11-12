---
name: embedded-stm32-rules
version: 1.11.0
description: >-
  Enforces professional embedded C/C++ development guidelines and PIA (Progressive
  Instance-driven Architecture) for STM32 microcontrollers, ARM Cortex-M architecture,
  and hardware abstraction layer (HAL/LL). Use when writing, reviewing, refactoring,
  or designing STM32 firmware, peripheral drivers (UART, SPI, I2C, DMA, ADC, PWM, CAN),
  cooperative time-sliced task schedulers, FreeRTOS integration, or VOFA+ debugging protocols.
license: Apache-2.0
metadata:
  version: v1.11.0
  source: awesome-cursorrules-embedded & PIA Architecture Standard
---

# Embedded STM32 & MCU Engineering Guidelines (v1.11)

Production-grade C/C++ standards and **PIA (Progressive Instance-driven Architecture)** for STM32 / ARM Cortex-M platforms.

---

## 1. Workspace Layout & Dual-Workflow Separation

Isolate concerns strictly while leaving CubeMX/IDE anchors at project root (`Core/`, `Drivers/`, `MDK-ARM/`, `CMakeLists.txt`, `cmake/`, `.ioc`):
* **`Firmware/`**: Pure embedded code structured into `BSP/` -> `Module/` -> `Service/` -> `App/` (never reverse-include `App/` from `BSP`/`Module`).
* **`Host/`**: PC GUI/CLI clients (`Host_App/`) and host launch scripts only (Desktop Zero-Intrusion: no unauthorized `.lnk`/`.desktop`).
* **`Tools/Firmware/`**: MCU build, flash, font generation & health scripts (never pollute `Host/`).
* **`docs/`**: Single authoritative `SOFTWARE_SPEC.md`, `HARDWARE_SPEC.md`, protocol specs; root holds `README.md` index.
* **`_checkpoints/`**: Lightweight milestone snapshots (<400 KB) with dual-OS restore scripts (`RESTORE.ps1` + `RESTORE.sh`).

---

## 2. Core Coding & Verification Mandates

1. **Modularity & Contracts**: Single `.c`/`.cpp` file `<= 400 lines` (split huge font/init arrays into `*_cfg.h`). Define UI modes, commands, and frame structs first in central blackboard/protocol headers (`SystemBlackboard_t`, `UiMode_t`), synchronizing MCU + Host atomically.
2. **Real-Time & ISR Safety**: Zero `malloc`/`free` in runtime paths; explicit `<stdint.h>` widths (`uint8_t`, `int32_t`); zero naked `HAL_Delay()` in main/task loops (use cooperative scheduler or delta ticks); ISRs `< 10 us` with `volatile` shared flags and no `printf` / `HAL_Delay`.
3. **Peripheral & Hardware Safety**:
   * **Handle Encapsulation**: Multi-channel drivers take handle structs (`Dev_t*`), no duplicated channel functions and no hardcoded PC host strings (`COM5`) in MCU UI.
   * **Cortex-M7 (H7/F7)**: Align DMA buffers and manage D-Cache coherency.
   * **CubeMX `.ioc` Sync & Clock Triangulation**: Never rely solely on hand-edits in `Core/Src/`; lock pull-ups, open-drain, and `HSE_VALUE` into `.ioc`, verifying BOM crystal x `.ioc` x runtime PLL registers.
   * **Scaffolding Pruning**: Physically remove temporary test loops, multi-resolution carousels, and obsolete command fallbacks immediately once hardware specs are locked.
4. **Validation & Snapshot Gate**:
   * Lint code & PIA hierarchy: `python scripts/check_c_embedded_rules.py <workspace_or_file>`
   * Save pre-refactor / verified snapshots: `python scripts/embedded_checkpoint.py <workspace> create <tag> "<note>"`

---

## 3. On-Demand Specialized References

Load detailed implementation guides only for the domain you are actively working on:

| Domain | Trigger / Focus | Reference Manual |
| :--- | :--- | :--- |
| **PIA Architecture** | 4-tier layout, <50-line cooperative scheduler, handle instances, blackboard | [`progressive_architecture_pia.md`](./references/progressive_architecture_pia.md) |
| **Dual Build (MDK + CMake)** | Shared `Firmware/` across Keil AC6 + CMake/Ninja/GCC, dynamic CubeCLT paths | [`dual_workflow_mdk_cmake_guide.md`](./references/dual_workflow_mdk_cmake_guide.md) |
| **ArmClang 6 & CMSIS-DSP** | `-fshort-enums -fshort-wchar`, MicroLIB `--pd`, L6907E V5.06 armlink, builtins | [`armclang_cmsis_dsp_compatibility.md`](./references/armclang_cmsis_dsp_compatibility.md) |
| **I2C Recovery & PMIC Traps** | 9-clock recovery, `AF4` remapping + `HAL_I2C_DeInit`, MP2672 `CV`/`VCC` check | [`i2c_bus_recovery_and_pwr_traps.md`](./references/i2c_bus_recovery_and_pwr_traps.md) |
| **ST7789 TFT & PyQt5 Host** | `MADCTL` orientation/offset swap, RGB565 byte order, dirty-rect & chunked DMA, PyQt crash hook, `BTHENUM` filter, UTF-8 `.bat` no-`::` rule | [`display_and_host_hardening.md`](./references/display_and_host_hardening.md) |
| **CubeMX Sync & Pruning** | Overwrite immunity, clock triangulation, physical scaffolding removal | [`cubemx_ioc_sync_and_scaffolding_rules.md`](./references/cubemx_ioc_sync_and_scaffolding_rules.md) |
| **UART DMA & VOFA+** | `HAL_UARTEx_ReceiveToIdle_DMA`, ring buffers, `JustFloat`/`FireWater` frames | [`stm32_uart_dma_pattern.md`](./references/stm32_uart_dma_pattern.md) / [`vofa_protocol.md`](./references/vofa_protocol.md) |
| **ADC Filtering** | Option A: motor composite trimmed-mean+IIR vs Option B: bit-shift IIR | [`adc_filtering_patterns.md`](./references/adc_filtering_patterns.md) |
| **HardFault Debug** | MSP/PSP stack frame dump handlers, CFSR/HFSR register decode | [`hardfault_diagnostics.md`](./references/hardfault_diagnostics.md) |
| **Spec Standard** | `SOFTWARE_SPEC.md` template, memory map, pinout, handover guide | [`software_spec_standard.md`](./references/software_spec_standard.md) |
