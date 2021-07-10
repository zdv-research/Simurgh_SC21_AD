INCLUDE := $(GEM5)/include
CC := gcc
CPPFLAGS := -static -I$(INCLUDE) $(GEM5)/util/m5/src/x86/m5op.S  
OBJECTS :=  measure_jump measure_retp measure_syscall
all: $(OBJECTS)
$(objects): %: %.c
	$(CC) $(CPPFLAGS) -o $@ -c $<
clean:
	rm -f $(OBJECTS)
