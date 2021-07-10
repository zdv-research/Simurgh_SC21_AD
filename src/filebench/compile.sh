#!/bin/bash

set -e

cd ../../filebench

libtoolize
aclocal
autoheader
automake --add-missing
autoconf


./configure --prefix $(pwd)/../binaries
make install
#cp filebench ../binaries