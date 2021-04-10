#include <stdio.h>
#include <linux/kernel.h>
#include <sys/syscall.h>
#include <unistd.h>

// gem5 stuff to dump the stats
#include "../../gem5/include/gem5/m5ops.h"
#include "../../gem5/include/gem5/asm/generic/m5ops.h" 

int main()
{
    m5_reset_stats(0,0);
    syscall(436);
    m5_exit(0);
}
