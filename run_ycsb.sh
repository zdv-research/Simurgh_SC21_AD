#!/bin/bash

export ALIGNMENT="2M"

source ./config.sh
source ./src/bash/parse_initial_arguments.sh
source ./src/bash/env.sh

(cd ./src/ycsb && ./run.sh)