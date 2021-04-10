#ifndef PPRINT_H_INCLUDED
#define PPRINT_H_INCLUDED

// Pretty print. These are just helper variables
// to make the print output a little bit nicer.

#define COLOR_RED "\x1b[31m"
#define COLOR_GREEN "\x1b[32m"
#define COLOR_YELLOW "\x1b[33m"
#define COLOR_RESET "\x1b[0m"

#define TAG_OK COLOR_GREEN "[+]" COLOR_RESET " "
#define TAG_FAIL COLOR_RED "[-]" COLOR_RESET " "
#define TAG_PROGRESS COLOR_YELLOW "[~]" COLOR_RESET " "

#endif // PPRINT_H_INCLUDED
