// as -s -o dumpme.o dumpme.s; strip dumpme.o -R .note.gnu.property; ld -static --section-start=.secretflag=0xdeadf00d000 --section-start=.text=0xfeedface000 --section-start=.bss=0x1337babf000 -z separate-code -s dumpme.o -o dumpme
    .bss
    .lcomm _bss, 1
    .section    .secretflag,"a"
    .string    "justCTF{tr4cing_blind_a1nt_that_h4rd}"
    .section    .note.GNU-stack,"",@progbits
    .text
    endbr64
    xor     %esp, %esp
    movl    $231, %eax
    movl    $99, %edi
    syscall
    ret
    .align 4096
