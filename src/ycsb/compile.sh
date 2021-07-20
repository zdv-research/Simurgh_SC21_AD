#!/bin/bash

mkdir -P $BENCHMARK_REPO_DIR/leveldb/build
cd $BENCHMARK_REPO_DIR/leveldb/build

cmake -DCMAKE_BUILD_TYPE=Release .. && make -j4

cd $BENCHMARK_REPO_DIR/ycsb
mvn install -DskipTests