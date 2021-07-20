#!/bin/bash

##########################
### paths
##########################

export SIMURGH_LIB_PATH="libfs.so"
export SIMURGH_LIB_FB_PATH="libfs_filebench.so"
export SIMURGH_UTILS_PATH="simurgh"

# set those according to your SplitFS install
export SPLITFS_PATH="../SplitFS/splitfs"
export SPLITFS_NVP_TREE_FILE_PATH="../SplitFS/splitfs/bin/nvp_nvp.tree"
export SPLITFS_LIB_PATH="../SplitFS/splitfs/libnvp.so"

# set those according to your PMFS build
export PMFS_MODULE_PATH="../PMFS-new/pmfs.ko"


export GIT_BIN_PATH="./git-2.28.0/git"
export FILEBENCH_BIN_PATH="./binaries/bin/filebench"
export TAR_BIN_PATH="./binaries/tar"



##########################
### system
##########################

# set this according to your ndctl namespace creation
export NDCTL_DEVICE="/dev/pmem0"
export NDCTL_NAMESPACE="namespace0.0"



##########################
### data
##########################

# set this according your prepared data location
export LINUX_DATA_PACKED="./data/linux.tar"
export LINUX_DATA_UNPACKED="./data/linux-5.6.14"
export RAM_DISK="/mnt/ramdisk"
export YCSB_DATA="./data/ycsb"
