.inst
    _start: add &0, $2, $3 # comment
    nope
    sub &2, $4, $5
    addi &2, 20
    sll &2, $2, 4
    jump _start
    div $2, $3
