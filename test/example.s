.data
    .word 4, 5
    .space 2
    _ten: .word 10
    .byte 5
    .ascii "abc"

.inst
    _start: add &0, $2, $3 # comment
    nope
    sub &2, $4, $5
    addi &2, 20
    sll &2, $2, 4
    _test: jr $4