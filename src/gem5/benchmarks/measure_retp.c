// If everything is working as expected you should see the following output:
// Jump!
// I'm back!
//
// If you set the SET_SEC_BIT flag to 0, you should see a general protection fault.
// That's it. Nothing too fancy, I know.

#include <stdio.h>
#include <unistd.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>

// PTEditor to modify the PTEs.
#include "include/secure_bit.h"
#include "include/pprint.h"

// Use these magic opcodes. This allows measuring inside
// the asm volatile. This way the mov is not measured
// and we minimize measurement overhead.
// IMPORTANT:
// Make sure that you either place 0,0 in rsi and rdi
// or modify Gem5 to always pass 0,0 !!!!
// Otherwise this will lead to undefined behaviour.
#define M5_EXIT  ".byte 0x0F, 0x04; .word 0x21\r\n"
#define M5_RESET ".byte 0x0F, 0x04; .word 0x40\r\n"
#define M5_DUMP  ".byte 0x0F, 0x04; .word 0x41\r\n"


#define SET_SEC_BIT 1

// Just a test
char code[] = "\x0F\xA7";  //         retp (0x0F 0xA7)

int NUM_ITER = 1;

void jmp_dst() {
    // Dump the stats after a jump
    __asm__ volatile(M5_DUMP);

    // Exit after 100 iterations
    if (NUM_ITER == 0) {
        __asm__ volatile (M5_EXIT);
    }

    // Decrease the counter
    NUM_ITER -= 1;

    // Jump!
    __asm__ volatile (
        "mov %[func], %%rax\r\n"
        M5_RESET
        ".byte 0x48, 0x0F, 0xA6, 0xC0" /* jmpp */
        :                              /* output */
        : [func]"r"(jmp_dst+4)         /* input */
        : "%rax"                       /* clobbered register */
    );
}

void jmp_dst_for_retp() {
    __asm__ volatile (
        M5_RESET
        ".byte 0x48, 0x0F, 0xA7" /* retp */
    );
}


int main() {
    unsigned long *mem_loc, *ptr;
    int flags, prot, ret;

    // Setup a page where we want to palce the target code.
    // Make sure that the page offset (lower 12 bits)
    // correspond to one of the entry points:
    // 0x000, 0x400, 0x800, 0xC00
    // Choose 0x000 in this case.
    mem_loc = (unsigned long *)0x10000;
    prot = PROT_READ | PROT_WRITE | PROT_EXEC;
    flags = MAP_FIXED | MAP_ANON | MAP_PRIVATE;
    ptr = mmap(mem_loc, sizeof(code), prot, flags, -1, 0);

    // Check if the page setup was successfull.
    if (*ptr != *mem_loc) {
        printf(TAG_FAIL "Error: Could not map code to memory location: %p\n", mem_loc);
        exit(-1);
    }

    // Copy the actual code to the memory address.
    memcpy(ptr, code, sizeof(code));

    #if SET_SEC_BIT

    // Init the pteditor kernel module.
    if (ptedit_init()) {
        printf(TAG_FAIL "Error: Could not initalize PTEditor, did you load the kernel module?\n");
        return 1;
    }

    // Set the secure bit for the corresponding code page.
    if (ret = setSecureBit((void *)(jmp_dst+4)) != 0) {
        printf(TAG_FAIL "Error: Could not set the secure bit.\n");
        return 1;
    }

    // We need this for retp measurements.
    if (ret = setSecureBit((void *)(jmp_dst_for_retp+4)) != 0) {
        printf(TAG_FAIL "Error: Could not set the secure bit.\n");
        return 1;
    }

    // Depending on the measurement we might need this
    if (ret = setSecureBit((void *)mem_loc) != 0) {
        printf(TAG_FAIL "Error: Could not set the secure bit.\n");
        return 1;
    }
    #endif

    // Jump to the target code.
    printf(TAG_OK "Jump!\n");

// Use this to measure a JMPP.
//    __asm__ volatile (
//        M5_RESET
//        "mov %[func], %%rax\r\n"
//        ".byte 0x48, 0x0F, 0xA6, 0xC0"      /* jmpp */
//        :                                   /* output */
//        : [func]"r"(jmp_dst+4)     /* input */
//        : "%rax"
//    );

__asm__ volatile (M5_RESET);
// Use this to measure a RETP call.
    for (int i = 0; i < 100; ++i) {
        __asm__ volatile (
            "mov %[func], %%rax\r\n"
            ".byte 0x48, 0x0F, 0xA6, 0xC0\r\n" /* jmpp */
            M5_DUMP
            :                              /* output */
            : [func]"r"(jmp_dst_for_retp+4)         /* input */
            : "%rax"
        );
    }

// Use this to measure single components of JMPP where wrip is not called.
// Note: You need to modify the gem5 JMPP source before executing this code.
//    for (int i = 0; i < 100; ++i) {
//        __asm__ volatile (
//            "mov %[func], %%rax\r\n"
//            M5_RESET
//            ".byte 0x48, 0x0F, 0xA6, 0xC0\r\n" /* jmpp */
//            M5_DUMP
//            :                              /* output */
//            : [func]"r"(mem_loc)
//            : "%rax"
//        );
//    }

// Use this to measure the overhead for a nop.
//    for (int i = 0; i < 100; ++i) {
//        __asm__ volatile (
//            M5_RESET
//            "nop\r\n"
//            M5_DUMP
//        );
//    }

    // Stop the simulation.
    __asm__ volatile(M5_EXIT);


    // Never called.

    printf(TAG_OK "I'm back!\n");

    // Cleanup PTEditor if the module was loaded.
    #if SET_SEC_BIT
    ptedit_cleanup();
    #endif

    // Cleanup the mapped code
    if (ret = munmap(ptr, sizeof(code)) != 0) {
        printf(TAG_FAIL "Error: unmap() = %d\n", ret);
        return 1;
    }

    return 0;
}
