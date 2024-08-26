.data
    .word 4
.inst
    _start: add &0, $2, $3 # comment
    nope
    sw &2, _start[5]
