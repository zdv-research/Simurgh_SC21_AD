#!/bin/bash

if [[ $1 == "SIMURGH" ]]; then
    export TARGET_FS="SIMURGH"
fi

if [[ $1 == "NOVA" ]]; then
    export TARGET_FS="NOVA"
fi

if [[ $1 == "EXT4DAX" ]]; then
    export TARGET_FS="EXT4DAX"
fi

if [[ $1 == "PMFS" ]]; then
    export TARGET_FS="PMFS"
fi

if [[ $1 == "SPLITFS" ]]; then
    export TARGET_FS="SPLITFS"
fi