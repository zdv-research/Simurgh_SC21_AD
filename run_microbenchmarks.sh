#!/bin/bash

export ALIGNMENT="4k"

source ./config.sh
source ./src/bash/parse_initial_arguments.sh
source ./src/bash/env.sh

(cd ./src/microbenchmarks && ./run.sh)