#!/bin/bash

./unmount.sh

mkdir -p /mnt/fsramdisk
mkdir -p /mnt/pmem_emul

if [[ $TARGET_FS == "SIMURGH" ]]; then
    ./ndctl_reconfigure_DEVDAX.sh
    ./format_simurgh.sh
    echo "Mounted SIMURGH"
fi

if [[ $TARGET_FS == "NOVA" ]]; then
    ./ndctl_reconfigure_FSDAX.sh
    find /mnt/fsramdisk/ -type f -delete
    modprobe -r nova
    modprobe nova inplace_data_updates=1
    mount -t NOVA -o init $NDCTL_DEVICE /mnt/fsramdisk
fi

if [[ $TARGET_FS == "EXT4DAX" ]]; then
    ./ndctl_reconfigure_FSDAX.sh
    yes "" | mkfs -t ext4 $NDCTL_DEVICE
    mount -t ext4 -o dax $NDCTL_DEVICE /mnt/fsramdisk
fi

if [[ $TARGET_FS == "PMFS" ]]; then
    ./ndctl_reconfigure_FSDAX.sh
    insmod $BENCHMARK_REPO_DIR/$PMFS_MODULE_PATH
    mount -t pmfs -o init $NDCTL_DEVICE /mnt/fsramdisk
fi

if [[ $TARGET_FS == "SPLITFS" ]]; then
    ./ndctl_reconfigure_FSDAX.sh
    yes "" | mkfs -t ext4 $NDCTL_DEVICE
    mount -t ext4 -o dax $NDCTL_DEVICE /mnt/pmem_emul
fi

