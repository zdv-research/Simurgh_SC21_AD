#ifndef SECURE_BIT_H_INCLUDED
#define SECURE_BIT_H_INCLUDED

#include "ptedit_header.h"

#define SEC_BIT PTEDIT_PAGE_BIT_SOFTW2

// Set the secure bit to true for a specific page at a given virtual address.
static int inline setSecureBit(void *ptr) {
    pid_t pid = getpid();

    ptedit_entry_t entry = ptedit_resolve(ptr, 0);

    // Set the secure bit for all levels of PTEs
    if (!(entry.valid & PTEDIT_VALID_MASK_PTE)) {
        return 1;
    }

    // Change page table entry if it exists
    entry.valid = PTEDIT_VALID_MASK_PTE;
    entry.pte |= (1ull << SEC_BIT);

    // Change page global directory entry if it exists
    /*if (ptedit_paging_definition.has_pgd) {
        entry.valid |= PTEDIT_VALID_MASK_PGD;
        entry.pgd |= (1ull << SEC_BIT);
    }*/

    // Change level 5 pte if it exists
    if (ptedit_paging_definition.has_p4d) {
        entry.valid  |= PTEDIT_VALID_MASK_P4D;
        entry.p4d |= (1ull << SEC_BIT);
    }

    // Change page middle directory entry if it exists
    if (ptedit_paging_definition.has_pmd) {
        entry.valid  |= PTEDIT_VALID_MASK_PMD;
        entry.pmd |= (1ull << SEC_BIT);
    }

    // Change page upper directory entry if it exists
    if (ptedit_paging_definition.has_pud) {
        entry.valid  |= PTEDIT_VALID_MASK_PUD;
        entry.pud |= (1ull << SEC_BIT);
    }

    ptedit_update(ptr, pid, &entry);

    // Check if we successfully set the secure bit.
    entry = ptedit_resolve(ptr, pid);
    unsigned char success = !!(entry.pte & (1ull << SEC_BIT));
    //if (ptedit_paging_definition.has_pgd) success = success && !!(entry.pgd & (1ull << SEC_BIT));
    if (ptedit_paging_definition.has_p4d) success = success && !!(entry.p4d & (1ull << SEC_BIT));
    if (ptedit_paging_definition.has_pud) success = success && !!(entry.pud & (1ull << SEC_BIT));
    if (ptedit_paging_definition.has_pmd) success = success && !!(entry.pmd & (1ull << SEC_BIT));

    if (success != 1) {
        return 1;
    }

    return 0;
}


#endif // SECURE_BIT_H_INCLUDED
