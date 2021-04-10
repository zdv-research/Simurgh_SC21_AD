#!/bin/bash

$BENCHMARK_REPO_DIR/$SIMURGH_UTILS_PATH f
echo 'Clear simurgh-shm:'
dd if=/dev/zero of=/dev/shm/simurgh-shm bs=1M count=1024