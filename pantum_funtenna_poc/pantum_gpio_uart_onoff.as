.text
.equ uart_regaddr, 0xFD060000
.equ uart_reg2addr, 0x15F0A70
.equ func_uart_send, 0x302F4C
.equ uart_conf_reg, 0xFD060000
.equ symbol_duration_one,  0x219999
.equ symbol_duration_zero, 0xd4ccc
.equ spin_val,             0xffffff
.equ xmit_msg_word, 0b10101010101010101010101010101010
@.equ xmit_msg_word, 0b11011101111011101101000101010011

    MOV        LR,LR
    NOP
    MOV        LR,LR
    NOP

    STMFD   SP!, {R4-R12, LR}
    SUB     SP, SP, #0x40

    @ disable interrupts
    mrs r0, CPSR
    orr r0, r0, #0x80
    msr CPSR, r0
    mrs r0, CPSR
    orr r0, r0, #0x40
    msr CPSR, r0

    @ set BREAK bit to force SOUT to low
    MOV    R1, #0x43
    LDR    R2, =uart_conf_reg
    STR    R1, [R2, #0xc]
    MOV    R1, #0x23
    MOV    R3, #0x33
    LDR    R5, =xmit_msg_str

_load_xmit_word:
    MOV      R4, #0x0 @reset bit counter
    LDR      R9, [R5]
    ADD      R5, R5, #0x4   
    CMP      R9, #0x0
    BNE      _doloopy
    LDR      R5, =xmit_msg_str
    B        _load_xmit_word   

_doloopy:
    LDR     R0, =spin_val
    BL      _funcspin
    
    CMP     R4, #0x1f
    BHI     _load_xmit_word

_start_xmit_word:
    TST     R9, #1
    LSR     R9, R9, #0x1
    ADD     R4, #0x1 @ increment bit counter
    BEQ     _set_symbol_one

_set_symbol_zero:
    BL      _do_xmit_one
    B       _doloopy
_set_symbol_one:
    BL      _do_xmit_zero
    B       _doloopy

_doneFlipping:
    ADD     SP, SP, #0x40
    LDMFD   SP!, {R4-R12, LR}
    BX      LR


_funcspin:
    MOV     R12, #0x0
_doSpin:
    cmp     R12, R0
    BHI     _doneSpin
    ADD     R12, #0x1
    B       _doSpin
_doneSpin:
    BX      LR

_do_xmit_one:
    STMFD   SP!, {R0-R12, LR}
    SUB     SP, SP, #0x40
    MOV     R0, #0x0
    LDR     R6, =symbol_duration_one

_xmit_one_loop:
    CMP    R0, R6
    BHI    _done_xmit_one
    STR    R1, [R2, #0x10]
    STR    R3, [R2, #0x10]
    ADD    R0, #0x1
    B      _xmit_one_loop

_done_xmit_one:
    ADD     SP, SP, #0x40
    LDMFD   SP!, {R0-R12, LR}
    BX      LR

_do_xmit_zero:
    STMFD   SP!, {R0-R12, LR}
    SUB     SP, SP, #0x40
    MOV     R0, #0x0
    LDR     R6, =symbol_duration_zero

_xmit_zero_loop:
    CMP    R0, R6
    BHI    _done_xmit_zero
    STR    R1, [R2, #0x10]
    STR    R3, [R2, #0x10]
    ADD    R0, #0x1
    B      _xmit_zero_loop

_done_xmit_zero:
    ADD     SP, SP, #0x40
    LDMFD   SP!, {R0-R12, LR}
    BX      LR


@xmit_msg_str:   .asciz "\xffUABCDEFGHIJKLMNOPQRSTUVWXYZ!\xff\xff\x00\x00\x00\x00"
xmit_msg_str: .byte 0b11111111, 0b11111111, 0b01010101, 0b01010101, 0b01000101, 0b01010000, 0b10010000, 0b11110101, 0b00000100, 0b00010000, 0b11111001, 0b01000110, 0b01000001, 0b00010001, 0b00010100, 0b00000100, 0b10011111, 0b00001010, 0b11101000, 0b11111111, 0b11111111, 0b01010101, 0b01010101, 0b00110000, 0b10000011, 0b00100010, 0b00101000, 0b11000000, 0b11011110, 0b11111000, 0b00000100, 0b00111100, 0b00000011, 0b10000101, 0b00011010, 0b11011010, 0b01100100, 0b10010110, 0b11111111, 0b11111111, 0b01010101, 0b01010101, 0b11011110, 0b10000001, 0b01010010, 0b00011101, 0b00100101, 0b10100000, 0b01111000, 0b00000000, 0b00000001, 0b10100001, 0b10010000, 0b00000000, 0b00101100, 0b10100000, 0b01110011, 0b11111111, 0b11111111, 0b01010101, 0b01010101, 0b11010100, 0b00011000, 0b01100011, 0b10001100, 0b00110001, 0b0, 0b0, 0b0, 0b0

.align
.ltorg    
    MOV        LR,LR
    NOP
    MOV        LR,LR
    NOP
