# VOFA+ Protocol Reference

This document provides exact specifications and reference C implementations for VOFA+ communication protocols.

---

## 1. JustFloat 协议

### 1.1 协议格式
* 数据类型：标准 IEEE 754 32位单精度浮点数（float），小端模式（Little Endian）。
* 数据通道：支持 1 至 N 个通道。
* 帧尾标记：固定 4 字节：`0x00, 0x00, 0x80, 0x7F`（即浮点数正无穷大 `+inf` 的二进制小端形式）。

### 1.2 标准 C 结构体与发送函数

```c
#ifndef INC_VOFA_JUSTFLOAT_H_
#define INC_VOFA_JUSTFLOAT_H_

#include <stdint.h>
#include <string.h>

#define VOFA_JUSTFLOAT_CHANNELS 4

#pragma pack(push, 1)
typedef struct {
    float channels[VOFA_JUSTFLOAT_CHANNELS];
    uint8_t tail[4];
} Vofa_JustFloat_Packet_t;
#pragma pack(pop)

static inline void Vofa_JustFloat_Init(Vofa_JustFloat_Packet_t *pkt) {
    if (!pkt) return;
    memset(pkt->channels, 0, sizeof(pkt->channels));
    pkt->tail[0] = 0x00;
    pkt->tail[1] = 0x00;
    pkt->tail[2] = 0x80;
    pkt->tail[3] = 0x7F;
}

static inline void Vofa_JustFloat_Set(Vofa_JustFloat_Packet_t *pkt, uint8_t ch, float val) {
    if (pkt && ch < VOFA_JUSTFLOAT_CHANNELS) {
        pkt->channels[ch] = val;
    }
}

#endif /* INC_VOFA_JUSTFLOAT_H_ */
```

---

## 2. FireWater 协议

* 格式：以逗号分隔的 ASCII 字符，以换行符 `\n` 或 `\r\n` 结尾。
* 示例：`"12.5,3.14,-0.82\n"`
* 建议：为了避免 `printf`/`sprintf` 在中断或高频任务中产生过大开销，高频打印（>50Hz）建议优先采用 **JustFloat** 协议。
