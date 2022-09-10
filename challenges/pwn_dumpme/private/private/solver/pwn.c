#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <sys/personality.h>
#include <sys/user.h>
#include <sys/mman.h>
#include <asm/unistd.h>
#include <linux/auxvec.h>
#include <elf.h>
#include <stdarg.h>

struct user_regs_struct regs0 = {};
pid_t pid;
int fds[2];

long dosyscall(long nargs, long call, ...) {
    struct user_regs_struct regs = {};
    ptrace(PTRACE_SYSCALL, pid, 0, 0);
    wait(NULL);
    ptrace(PTRACE_GETREGS, pid, 0, &regs);
    regs.orig_rax = call;
    regs.rip = regs.rip - 2;
    va_list ap;
    va_start(ap, call);
    if (nargs --> 0)
        regs.rdi = va_arg(ap, long);
    if (nargs --> 0)
        regs.rsi = va_arg(ap, long);
    if (nargs --> 0)
        regs.rdx = va_arg(ap, long);
    va_end(ap);
    ptrace(PTRACE_SETREGS, pid, 0, &regs);
    ptrace(PTRACE_SYSCALL, pid, 0, 0);
    wait(NULL);
    ptrace(PTRACE_GETREGS, pid, 0, &regs);
    return regs.rax;
}

long getpage(unsigned long ptr, void *page) {
    long ret = dosyscall(3, __NR_write, fds[1], ptr & -PAGE_SIZE, PAGE_SIZE);
    if (ret <= PAGE_SIZE)
        read(fds[0], page, ret);
    else {
            errno = -ret;
            if (errno < 0x1000)
                puts(strerror(errno));
    }
    return ret;
}

int main(int argc, char *argv[])
{
    pipe(fds);
    pid = fork();
    if (pid == 0) {
        close(fds[0]);
        ptrace(PTRACE_TRACEME, 0, 0, 0);
        execve(argv[1], &argv[1], NULL);
        puts("exec failed");
        _exit(-1);
    }
    close(fds[1]);
    wait(NULL);
    ptrace(PTRACE_GETREGS, pid, 0, &regs0);

    void *page = mmap(NULL, PAGE_SIZE, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    getpage(regs0.rsp, page);

    unsigned long phdr = 0;
    for (int i = 0; i < PAGE_SIZE; i += sizeof(long)) {
        unsigned long val = *(long*)(page+i);
        if (val == AT_PHDR)
            phdr = ((long*)(page+i))[1];
    }
    printf("Found PHDR at %p\n", (void*)phdr);

    getpage(phdr, page);
    void *page2 = mmap(NULL, PAGE_SIZE, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    long adj = 0;
    for (int i = phdr & (PAGE_SIZE-1); i < PAGE_SIZE; i += sizeof(Elf64_Phdr)) {
        Elf64_Phdr *val = page+i;
        if (val->p_type == PT_LOAD) {
            if (val->p_vaddr == 0) {
                adj = phdr & -PAGE_SIZE;
            }
            printf("PT_LOAD into %p\n", (void*)val->p_vaddr);
            getpage(val->p_vaddr + adj, page2);
            puts(page2);
        }
        if (val->p_type == PT_NULL) break;
    }

    dosyscall(1, __NR_exit_group, 137);
    return 0;
}
