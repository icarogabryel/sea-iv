.data
    .word 4, 5
    .space 2
    _ten: .word 10
    .byte 5
    .ascii "abc"

.inst
    add &0, $2, $3 # comment
    _loop: sub &2, $4, $5
