# STM32 UART + DMA + IDLE Ring Buffer Pattern

This pattern implements zero-copy or minimal-copy serial reception using STM32 HAL with DMA and IDLE interrupt.

---

## 1. 结构与环形缓冲区实现 (Ring Buffer)

```c
#ifndef INC_RING_BUFFER_H_
#define INC_RING_BUFFER_H_

#include <stdint.h>
#include <stdbool.h>

#define RING_BUFFER_SIZE 512

typedef struct {
    uint8_t buffer[RING_BUFFER_SIZE];
    volatile uint16_t head;
    volatile uint16_t tail;
} RingBuffer_t;

static inline void RingBuffer_Init(RingBuffer_t *rb) {
    rb->head = 0;
    rb->tail = 0;
}

static inline bool RingBuffer_IsEmpty(const RingBuffer_t *rb) {
    return rb->head == rb->tail;
}

static inline bool RingBuffer_IsFull(const RingBuffer_t *rb) {
    return ((rb->head + 1) % RING_BUFFER_SIZE) == rb->tail;
}

static inline bool RingBuffer_Write(RingBuffer_t *rb, uint8_t byte) {
    uint16_t next = (rb->head + 1) % RING_BUFFER_SIZE;
    if (next == rb->tail) return false; // Full
    rb->buffer[rb->head] = byte;
    rb->head = next;
    return true;
}

static inline bool RingBuffer_Read(RingBuffer_t *rb, uint8_t *byte) {
    if (rb->head == rb->tail) return false; // Empty
    *byte = rb->buffer[rb->tail];
    rb->tail = (rb->tail + 1) % RING_BUFFER_SIZE;
    return true;
}

#endif /* INC_RING_BUFFER_H_ */
```

---

## 2. STM32 HAL RxEvent 现代接口 (HAL 1.25+)

STM32 HAL 推荐使用 `HAL_UARTEx_ReceiveToIdle_DMA` 替代繁琐的手动清除空闲标志。

```c
#define RX_RAW_BUF_SIZE 128
static uint8_t rx_raw_buffer[RX_RAW_BUF_SIZE];
static RingBuffer_t rx_ring_buffer;

void Serial_Init(UART_HandleTypeDef *huart) {
    RingBuffer_Init(&rx_ring_buffer);
    HAL_UARTEx_ReceiveToIdle_DMA(huart, rx_raw_buffer, RX_RAW_BUF_SIZE);
    // 禁用 DMA 半传输中断以减少不必要的上下文切换
    __HAL_DMA_DISABLE_IT(huart->hdmarx, DMA_IT_HT);
}

void HAL_UARTEx_RxEventCallback(UART_HandleTypeDef *huart, uint16_t Size) {
    if (huart->Instance == USART1) {
        // 将接收到的数据快速搬运至环形队列
        for (uint16_t i = 0; i < Size; i++) {
            RingBuffer_Write(&rx_ring_buffer, rx_raw_buffer[i]);
        }
        // 重新开启下一次接收
        HAL_UARTEx_ReceiveToIdle_DMA(huart, rx_raw_buffer, RX_RAW_BUF_SIZE);
        __HAL_DMA_DISABLE_IT(huart->hdmarx, DMA_IT_HT);
    }
}
```
