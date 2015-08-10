.text
.equ dst_func, 0x03C1644
    MOV        LR,LR
    NOP
    MOV        LR,LR
    NOP
    STMFD   SP!, {R4-R12, LR}
    SUB     SP, SP, #0x40

    BL      dst_func

    ADD     SP, SP, #0x40
    LDMFD   SP!, {R4-R12, LR}
    BX      LR

    MOV        LR,LR
    NOP
    MOV        LR,LR
    NOP
