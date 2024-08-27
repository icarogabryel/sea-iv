.data
    .word 4
.inst
    _start: add &0, $2, $3 # comment
    nope
    swap $4, $5
    call _start
    ret
