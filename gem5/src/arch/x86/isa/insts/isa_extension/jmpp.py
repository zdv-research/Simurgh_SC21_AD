### TODO: If the code spawns more than one page:
### - Introduce a size parameter and check all pages.
### - We assume the pages are continous.
### TODO: Change the kernel to respect interrupts


microcode = '''

def macroop JMPP_R
{
    # Make the default data size of jumps 64 bits in 64 bit mode
    .adjust_env oszIn64Override
    .function_call

    # Make sure that a valid page offset is provided.
    # Lower 12 bit of the virtual address are the page offset.
    # 2^12 = 4096, Divided into four entry points:
    #
    # 0000 0000 0000 = 0x000 = 0
    # 0100 0000 0000 = 0x400 = 1024
    # 1000 0000 0000 = 0x800 = 2048
    # 1100 0000 0000 = 0xC00 = 3072
    #
    # There is still a possible attack vector left:
    # Assume:
    # The code inside the ep page spawns more than one
    # chunk (1024 bit) beginng on 0x000. It would now
    # be possible for an attacker to jump to position 2024
    # and execute the code there.
    # It would be nice to disallow to. E.g
    # Lets say if the beginng of an entry point is a nop
    # throw a general protection fault.
    #
    # This is VERY VERY complicated to accomplish.
    # I don't even know if this is possible.
    # We only know the instruction at a give location, when
    # the program counter loads the instruction.
    # At that point we don't know if we are currently
    # executing a code block which spawns more than one page
    # or if an attacker tried to jump to this location.
    #
    # Another possible solution to the problem would be:
    # Introduce an addition PTE field that defines the number
    # of entry points for a page. We could then add an
    # instruction to the TLB that checks if the virtual addr
    # is valid. The only problem: There are no unused bits
    # inside a PTE left. One bit could be enough if we just
    # provide a toggle between 2 or 4 entry points or something
    # like that.
    #
    # Give a page size of 4096 bytes,
    # we divide the page in 4 1024 blocks.
    # It holds true:
    #     vaddr[0:12] % 1024 == 0
    # <=> vaddr % 1024 == 0
    # <=> vaddr[0:10] == 0 (we check this)
    # 0x3FF = 1023 = 0b1111111111
    ##limm t1, 0x3FF, dataSize=2
    ##and t0, reg, t1, flags=(EZF,), dataSize=2
    ##fault "std::make_shared<GeneralProtection>(0)", flags=(nCEZF,)

    # if the ep-bit is set, EZF will be 1, otherwise 0
    rdep reg, flags=(EZF,), atCPL0=True
    # if EZF is 0 throw a general protection fault
    fault "std::make_shared<GeneralProtection>(0)", flags=(nCEZF,)

    # Read the instruction pointer into t1
    rdip t1
    # Store t1 into rsp (general purpose register)
    stis t1, ss, [0, t0, rsp], "-env.dataSize"
    # Subtract the stacksize from rsp
    subi rsp, rsp, ssz
    
    # Change the CS DPL value => Change CPL

#### Change the cs segment to the kernel segment with CPL 0.

#### All 1s for the segment limit.
###limm t1, "(uint64_t)(-1)", dataSize=8

#### Read the syscall cs from the star MSR.
###rdval t3, star
###srli t3, t3, 32, dataSize=8
###andi t3, t3, 0xFC, dataSize=1

#### Set up cs.
###wrsel cs, t3

#### Write the base of 0 and limit of 4GB.
###wrbase cs, t0, dataSize=8
###wrlimit cs, t1, dataSize=4

    # Load and write the following attributes for the cs.
    #
    # | dpl | unusable | defaultSize | longMode | avl |
    # | --- | -------- | ----------- | -------- | --- |
    # | 00  | 0        | 0           | 1        | 0   |
    #
    # | granularity | present | type | writable |
    # | ----------- | ------- | ---- | -------- |
    # | 1           | 1       | 0101 | 0        |
    #
    # | readable | expandDown | system |
    # | -------- | ---------- | ------ |
    # | 1        | 0          | 1      |

    limm t4, ((0 << 0)  | (0  << 2)  | (0 << 3)   | \
              (1 << 4)  | (0  << 5)  | (1 << 6)   | \
              (1 << 7)  | (10 << 8)  | (0 << 12)  | \
              (1 << 13) | (0  << 14) | (1 << 15)), dataSize=8
    wrattr cs, t4

#### The SS DPL must match the CPL
#### => We need to change to the kernel SS
#### https://unix.stackexchange.com/questions/510960/why-does-linux-have-two-data-segments-one-for-user-mode-and-another-for-kernel

###addi t3, t3, 8
###wrsel ss, t3
###wrbase ss, t0, dataSize=8
###wrlimit ss, t1, dataSize=4
#### Writable, readable, not expandDown,
#### dpl=0, defaultSize=0, not long mode
###limm t4, ((0 << 0)  | (0  << 2)  | (1 << 3)   | \
###           (0 << 4)  | (0  << 5)  | (1 << 6)   | \
###           (1 << 7)  | (2  << 8)  | (1 << 12)  | \
###           (1 << 13) | (0  << 14) | (1 << 15)), dataSize=8
###wrattr ss, t4

    wripi reg, 0
};

def macroop JMPP_M
{
    panic "JMPP_M not implemented"
};

def macroop JMPP_P
{
    panic "JMPP_M not implemented"
};

'''
