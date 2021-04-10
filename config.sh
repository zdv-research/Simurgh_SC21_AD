#!/bin/bash

##########################
### paths
##########################

export SIMURGH_LIB_PATH="libsimurgh.so"
export SIMURGH_UTILS_PATH="simurgh_utils"

# set those according to your SplitFS install
export SPLITFS_PATH="../SplitFS/splitfs"
export SPLITFS_NVP_TREE_FILE_PATH="../SplitFS/splitfs/bin/nvp_nvp.tree"
export SPLITFS_LIB_PATH="../SplitFS/splitfs/libnvp.so"

# set those according to your PMFS build
export PMFS_MODULE_PATH="../PMFS-new/pmfs.ko"

# set this according to the directory of the custom built git 
export GIT_BIN_PATH="../git-master/git"



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
export LINUX_DATA_UNPACKED="../linux"
export LINUX_DATA_PACKED="../linux.tar"
export LINUX_DATA_PACKED_AND_UNPACKED="../linux_plus_linuxtar"