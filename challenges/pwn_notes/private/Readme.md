# notes

Easy "menu" style heap task, where player can add/delete/view his notes. Leak via unsorted bin then arbitrary write via fastbin dup on GLIBC 2.31 (tcache).
