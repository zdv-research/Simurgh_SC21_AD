microcode = '''

def macroop RETP
{
    # Make the default data size of jumps 64 bits in 64 bit mode
    .adjust_env oszIn64Override
    .function_return

    # Change the CS segment to the user segment with CPL 3.

#### All 1s for the segment limit.
###limm t1, "(uint64_t)(-1)", dataSize=8

#### Load sysret cs from the star MSR.
###rdval t3, star
###srli t3, t3, 48, dataSize=8

#### set the rpl to 3 (b11)
###ori t3, t3, 3, dataSize=1

#### Set up cs.
###addi t4, t3, 16, dataSize=8
###wrsel cs, t4

#### Write the base of 0 and limit of 4GB.
###wrbase cs, t0, dataSize=8
###wrlimit cs, t1, dataSize=4

    # Load and write the following attributes for the cs.
    #
    # | dpl | unusable | defaultSize | longMode | avl |
    # | --- | -------- | ----------- | -------- | --- |
    # | 11  | 0        | 0           | 1        | 0   |
    #
    # | granularity | present | type | writable |
    # | ----------- | ------- | ---- | -------- |
    # | 1           | 1       | 0101 | 0        |
    #
    # | readable | expandDown | system |
    # | -------- | ---------- | ------ |
    # | 1        | 0          | 1      |

    limm t4, ((3 << 0)  | (0  << 2)  | (0 << 3)   | \
              (1 << 4)  | (0  << 5)  | (1 << 6)   | \
              (1 << 7)  | (10 << 8)  | (0 << 12)  | \
              (1 << 13) | (0  << 14) | (1 << 15)), dataSize=8
    wrattr cs, t4

#### Reset the SS
###addi t4, t3, 8, dataSize=8
###wrsel ss, t4

    # Jump to the return address.
    ld t1, ss, [1, t0, rsp]
    # Check address of return
    addi rsp, rsp, dsz
    wripi t1, 0
};

'''

