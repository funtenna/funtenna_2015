.text
.equ raw_gpio_write_func, 0x02F4EF4
.equ clutch_gpio_struct, 0x1601948
.equ engine_power_gpio_struct, 0x1601188
@ 0x0 spin period, rf output @ 25.92Mhz
@for fsk, 7 works
.equ spin_period, 0x5
@for dog whistle
@.equ spin_period, 0x6ff
@.equ spin_period, 0xfffff
.equ all_p1mp, 0xffffffff
@wrong. these are for LEDs
.equ gpio_10_addr, 0x1600ee8
.equ gpio_11_addr, 0x1600ee8
.equ gpio_12_addr, 0x1600f08
.equ gpio_13_addr, 0x1600f28
.equ gpio_14_addr, 0x1600f48

.equ gpio_bank_a_off_addr, 0xFD040020
.equ gpio_bank_b_off_addr, 0xF8040020
.equ gpio_bank_c_off_addr, 0xF8041020
.equ gpio_bank_d_off_addr, 0xF8042020

.equ gpio_struct_a, 0x3c1860
.equ gpio_struct_b, 0x3C1AE0
.equ gpio_struct_c, 0x3c1d60
.equ gpio_struct_d, 0x3c1fe0

.equ gpio_sensor_addr, 0x1600e28
@old_version
.equ gpio_open_func, 0x02F3520
@new version
@.equ gpio_open_func, 0x2FB064

.equ gpio_8_addr, 0x01600EA8
.equ gpio_9_addr, 0x01600EC8
.equ symbol_duration, 0xfffff

.equ xmit_msg_word, 0b10101010101010101010101010101010
.equ xmit_msg_word, 0b11011101111011101101000101010011

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

    MOV  R0, #0x0
    LDR  R1, =gpio_struct_a
    MOV  R2, #0x20
    BL   _func_gpio_open

    MOV  R0, #0x1
    LDR  R1, =gpio_struct_b
    MOV  R2, #0x20
    BL   _func_gpio_open

    MOV  R0, #0x2
    LDR  R1, =gpio_struct_c
    MOV  R2, #0x20
    BL   _func_gpio_open

    MOV  R0, #0x3
    LDR  R1, =gpio_struct_d
    MOV  R2, #0x1a
    BL   _func_gpio_open


_loopy:
    LDR     R5, =all_p1mp
    LDR     R1, =gpio_bank_a_off_addr
    LDR     R2, =gpio_bank_b_off_addr   
    LDR     R3, =gpio_bank_c_off_addr
    LDR     R4, =gpio_bank_d_off_addr   
    MOV     R6, #0x0 @ counter
    MOV     R7, #0x0 @ freq flag
    LDR     R8, =symbol_duration

_load_xmit_word:
    LDR     R9, =xmit_msg_word
    B       _reset_symbol    

_doloopy:
    CMP     R9, #0x0
    BEQ     _load_xmit_word

    CMP     R7, #0x1
    BEQ     _spin1_off
_spin1_on:
    LDR     R0, =spin_period
    B       _spin1
_spin1_off:
    MOV     R0, #0x0
_spin1:
    BL      _funcspin

    STR     R5, [R1]
    STR     R5, [R2]
    STR     R5, [R3]
    STR     R5, [R4]

    CMP     R7, #0x1
    BEQ     _spin2_off
_spin2_on:
    LDR     R0, =spin_period
    B       _spin2
_spin2_off:
    MOV     R0, #0x0
_spin2:
    BL      _funcspin

    STR     R5, [R1, #0x4]
    STR     R5, [R2, #0x4]
    STR     R5, [R3, #0x4]
    STR     R5, [R4, #0x4]

    ADD     R6, #0x1
    CMP     R6, R8
    BHI     _reset_symbol
    B       _doloopy

_reset_symbol:
    MOV     R6, #0x0
    TST     R9, #1
    LSR     R9, R9, #0x1
    BEQ     _set_symbol_one
_set_symbol_zero:
    MOV     R7, #0x0
    B       _doloopy
_set_symbol_one:
    MOV     R7, #0x1
    B       _doloopy

_doneFlipping:
    ADD     SP, SP, #0x40
    LDMFD   SP!, {R4-R12, LR}
    BX      LR

_func_gpio_open:
    STMFD   SP!, {R4-R12, LR}
    SUB     SP, SP, #0x40

    STR     R0, [SP, #0x20] @ gpio bank
    STR     R1, [SP, #0x24] @ data structure
    STR     R2, [SP, #0x2c] @ max pins
    MOV R0,    #0x0
    STR R0,    [SP, #0x14] @ 0x14 = counter

_gpio_open:
    LDR     R0, [SP, #0x14]
    LDR     R1, [SP, #0x2c] @ max pins
    CMP     R0, R1
    BGE     _done_gpio_open

    MOV     R1, #0x14
    MUL     R1, R0
    LDR     R0, [SP, #0x24]
    ADD     R0, R1

    LDR     R1, [SP, #0x20] @ bank number
    LDR     R2, [SP, #0x14] @ pin number
    MOV     R3, #0x1
    STR     R3, [SP, #0x0]
    STR     R3, [SP, #0x4]
    LDR     R12, =gpio_open_func
    BLX     R12

    LDR     R0, [SP, #0x14]
    ADD     R0, #0x1
    STR     R0, [SP, #0x14]
    B       _gpio_open
_done_gpio_open:
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

.align
.ltorg    
    MOV        LR,LR
    NOP
    MOV        LR,LR
    NOP
