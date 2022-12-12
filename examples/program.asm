prog:
    XOR rax, rax    ; clear rax
    ADD rax, 0x42   ; add 0x42 to rax
    CALL prog       ; recursive call prog