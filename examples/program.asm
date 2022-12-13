section .data
    A: 0x1234
    B: 0x4321
    C: 0
    D: "Hello World"

section .text
    XOR %rax, %rax      ; clear rax
    MOV %rdx, 0          ; clear rdx
    LD %rax, #A         ; load #A into %rax
    LD %rdx, #B         ; load #B into %rdx
    ADD #C, %rax, %rdx  ; save sum of %rax and %rdx into #C
