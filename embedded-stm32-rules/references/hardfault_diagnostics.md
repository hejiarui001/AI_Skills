# STM32 HardFault Diagnostics Reference

When a HardFault occurs on Cortex-M3/M4/M7, use this assembly/C triage pattern to extract the stack frame and crash registers.

---

## 1. 异常处理汇编桩 (Keil / GCC 兼容)

```c
void HardFault_Handler_C(uint32_t *hardfault_args);

__attribute__((naked)) void HardFault_Handler(void) {
    __asm volatile(
        "tst lr, #4\n"
        "ite eq\n"
        "mrseq r0, msp\n"
        "mrsne r0, psp\n"
        "b HardFault_Handler_C\n"
    );
}

void HardFault_Handler_C(uint32_t *hardfault_args) {
    volatile uint32_t stacked_r0  = hardfault_args[0];
    volatile uint32_t stacked_r1  = hardfault_args[1];
    volatile uint32_t stacked_r2  = hardfault_args[2];
    volatile uint32_t stacked_r3  = hardfault_args[3];
    volatile uint32_t stacked_r12 = hardfault_args[4];
    volatile uint32_t stacked_lr  = hardfault_args[5];
    volatile uint32_t stacked_pc  = hardfault_args[6];
    volatile uint32_t stacked_psr = hardfault_args[7];

    volatile uint32_t cfsr = SCB->CFSR;
    volatile uint32_t hfsr = SCB->HFSR;
    volatile uint32_t bfar = SCB->BFAR;

    (void)stacked_r0; (void)stacked_r1; (void)stacked_r2; (void)stacked_r3;
    (void)stacked_r12; (void)stacked_lr; (void)stacked_pc; (void)stacked_psr;
    (void)cfsr; (void)hfsr; (void)bfar;

    // 断点停止，在调试器中查看 stacked_pc 即为崩溃执行代码行
    __BKPT(0);
    while (1);
}
```

## 2. 崩溃根因快速排查表

| 寄存器标志位 | 含义 | 常见原因 |
| :--- | :--- | :--- |
| **PRECISERR** (CFSR.BFSR) | 精确数据访问越界 | 解引用了野指针、非法外设基地址或数组严重越界 |
| **UNDEFINSTR** (CFSR.UFSR) | 执行了未定义指令 | 函数指针未初始化被调用，或者代码段被意外擦写 |
| **UNALIGNED** (CFSR.UFSR) | 非对齐内存访问 | 对未对齐指针进行 32 位访问 |
| **STKOF** | 栈溢出 | 局部数组过大，或深层递归调用 |
