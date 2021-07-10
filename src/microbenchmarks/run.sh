#!/bin/bash

(cd $BENCHMARK_REPO_DIR/src/bash/ && ./mount.sh)

python3 micro_benchmark_runner.py --target=$TARGET_FS