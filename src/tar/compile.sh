#!/bin/bash

set -e

cd ../../tar
./configure
make
cp src/tar ../binaries