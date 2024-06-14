.data
    .word 4, 5, 6
    _x: .word 10
    _nome: .ascii "nome"

.inst
    add &0, $2, $3 # comment
    _loop: sub &2, $4, $5
