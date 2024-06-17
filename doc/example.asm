.include "test"

.data
    .word 4, 5, 6
    .space 3
    _ten: .word 10
    .byte 5
    .ascii "nome"

.inst
    add &0, $2, $3 # comment
    _loop: sub &2, $4, $5
