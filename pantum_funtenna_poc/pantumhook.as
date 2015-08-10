.text
.equ printf, 0x05F414
.equ dst_func, 0x03C1540
    MOV        LR,LR
    NOP
    MOV        LR,LR
    NOP
BL dst_func
    MOV        LR,LR
    NOP
    MOV        LR,LR
    NOP
