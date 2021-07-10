#include <stdio.h>
#include <unistd.h>

// gem5 stuff to dump the stats
#include "../../gem5/include/gem5/m5ops.h"
#include "../../gem5/include/gem5/asm/generic/m5ops.h"

int main()
{
    // warm up the cache
    syscall(436);

    for (int i = 0; i<100; ++i) {
        m5_reset_stats(0,0);
        syscall(436);
        m5_dump_stats(0, 0);
    }
    m5_exit(0);
}
