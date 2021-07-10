#!/bin/bash

linux_kernel_source_path="$BENCHMARK_REPO_DIR/$LINUX_DATA_UNPACKED"

gcc -shared -fPIC -o dummylib.so dummylib.cpp
g++ -fPIC main.cpp -o main.o -I . -L. dummylib.so
g++ -fPIC main2.cpp -o main2.o

function set_preloads {
    export LD_LIBRARY_PATH=.
    export LD_PRELOAD="$BENCHMARK_REPO_DIR/$SIMURGH_LIB_PATH"
} 

function unset_preloads {
    unset LD_LIBRARY_PATH
    unset LD_PRELOAD
} 

cur_dir=$(pwd)
(cd $BENCHMARK_REPO_DIR/src/bash/ && ./mount.sh)

echo "Copy over files:"
set_preloads
mkdir "/pm:/"
unset_preloads
for i in {1..10}
do
    set_preloads
    mkdir "/pm:/$i"
    time cp -r $linux_kernel_source_path "/pm:/$i"
    unset_preloads
done
echo ""

echo "Run meta data recovery:"
echo ./main.o
set_preloads
time ./main.o
unset_preloads
echo ""

echo "Clear SHM:"
dd if=/dev/zero of=/dev/shm/simurgh-shm bs=1M count=1024

echo "Run shm build up:"
echo ./main2.o
set_preloads
time ./main2.o
unset_preloads
echo ""

echo "DONE."