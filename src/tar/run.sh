#!/bin/bash

tar_path="$BENCHMARK_REPO_DIR/$TAR_BIN_PATH"
linux_kernel_source_path="$BENCHMARK_REPO_DIR/$LINUX_DATA_UNPACKED"

current_date=$(date +"%Y-%m-%d_%H-%M-%S");

set -e


function set_preloads {
    if [[ $TARGET_FS == "SIMURGH" ]]
    then
        export LD_PRELOAD="$BENCHMARK_REPO_DIR/$SIMURGH_LIB_PATH"
    fi
    if [[ $TARGET_FS == "SPLITFS" ]]
    then
        echo "Set preload SPLITFS"

        export LD_LIBRARY_PATH="$BENCHMARK_REPO_DIR/$SPLITFS_PATH"
        export NVP_TREE_FILE="$BENCHMARK_REPO_DIR/$SPLITFS_NVP_TREE_FILE_PATH"
        export LD_PRELOAD="$BENCHMARK_REPO_DIR/$SPLITFS_LIB_PATH"
    fi
}


function unset_preloads {
    if [[ $TARGET_FS == "SIMURGH" ]]
    then
        unset LD_PRELOAD
    fi
    if [[ $TARGET_FS == "SPLITFS" ]]
    then
        echo "UnSet preload SPLITFS"
        unset LD_LIBRARY_PATH
        unset NVP_TREE_FILE
        unset LD_PRELOAD
    fi
}

set_preloads
unset_preloads

mkdir $RAM_DISK || true
umount $RAM_DISK || true
mount -t tmpfs -o size=5g tmpfs $RAM_DISK

for run_i in {1..1}
do

if [[ $TARGET_FS == "SIMURGH" ]]
then
    (cd $BENCHMARK_REPO_DIR/src/bash/ && ./mount.sh)

    repo_path="/pm:"
elif [[ $TARGET_FS == "SPLITFS" ]]
then
    (cd $BENCHMARK_REPO_DIR/src/bash/ && ./mount.sh)
    rm -rf /mnt/pmem_emul/*

    sync; echo 3 > /proc/sys/vm/drop_caches;

    repo_path="/mnt/pmem_emul"

# elif [[ $TARGET_FS == "TMPFS" ]]
# then
#     sync; echo 3 > /proc/sys/vm/drop_caches;
#     preload=""
#     repo_path="/tmp/git_dir_$current_date"

elif [[ $TARGET_FS == "NOVA" ]]
then
    sync; echo 3 > /proc/sys/vm/drop_caches;
    preload=""
    repo_path="/mnt/fsramdisk"

    (cd $BENCHMARK_REPO_DIR/src/bash/ && ./mount.sh)
    rm -rf /mnt/fsramdisk/*
elif [[ $TARGET_FS == "PMFS" ]]
then
    sync; echo 3 > /proc/sys/vm/drop_caches;
    preload=""
    repo_path="/mnt/fsramdisk"

    (cd $BENCHMARK_REPO_DIR/src/bash/ && ./mount.sh)
    rm -rf /mnt/fsramdisk/*
elif [[ $TARGET_FS == "EXT4DAX" ]]
then
    sync; echo 3 > /proc/sys/vm/drop_caches;
    preload=""
    repo_path="/mnt/fsramdisk"

    (cd $BENCHMARK_REPO_DIR/src/bash/ && ./mount.sh)
    rm -rf /mnt/fsramdisk/*
else
    echo "No target fs specified. Abort."
    exit
fi

tar_exec_="$tar_path"
tar_exec="$tar_exec_"
if [[ $2 == "VALGRIND" ]]
then
    tar_exec="valgrind --tool=callgrind --trace-children=yes --callgrind-out-file=callgrind.out $git_exec_"
fi
echo "tar_exec: $tar_exec"

output_folder="output_$TARGET_FS_$current_date"

mkdir "$output_folder"

sync; echo 3 > /proc/sys/vm/drop_caches;

echo "Copy files:"
echo cp -r $linux_kernel_source_path/ $RAM_DISK/ 
if [[ $TARGET_FS == "SIMURGH" ]] ; then set_preloads ; fi
{ (mkdir "$repo_path" || true) ; cp -r $linux_kernel_source_path/ $RAM_DISK/ ; }
if [[ $TARGET_FS == "SIMURGH" ]] ; then unset_preloads ; fi
if [[ $2 == "VALGRIND" ]] ; then mv callgrind.out "$output_folder/callgrind_1_copy_$run_i.out" ; fi

sync; echo 3 > /proc/sys/vm/drop_caches;

echo "Compress:"
echo $tar_exec -cf $repo_path/linux.tar $RAM_DISK/linux-5.6.14
set_preloads
{ time $tar_exec -cf $repo_path/linux.tar $RAM_DISK/linux-5.6.14 ; } 2> $output_folder/2_compress_$run_i.txt
unset_preloads
if [[ $2 == "VALGRIND" ]] ; then mv callgrind.out "$output_folder/callgrind_2_compress_$run_i.out" ; fi
cat $output_folder/2_compress_$run_i.txt
echo ""

sync; echo 3 > /proc/sys/vm/drop_caches;
if [[ $TARGET_FS == "SIMURGH" ]] ; then ../bash/format_simurgh.sh ; fi
rm -rf $RAM_DISK/*

echo "Create compressed file"
echo cp  $BENCHMARK_REPO_DIR/$LINUX_DATA_PACKED $RAM_DISK/linux.tar
if [[ $TARGET_FS == "SIMURGH" ]] ; then set_preloads ; fi
{ (mkdir "$repo_path" || true) ; cp  $BENCHMARK_REPO_DIR/$LINUX_DATA_PACKED $RAM_DISK/linux.tar ; }
if [[ $TARGET_FS == "SIMURGH" ]] ; then unset_preloads ; fi
if [[ $2 == "VALGRIND" ]] ; then mv callgrind.out "$output_folder/callgrind_3_copy_compressed_$run_i.out" ; fi

sync; echo 3 > /proc/sys/vm/drop_caches;

echo "Extract:"
echo $tar_exec -xf $RAM_DISK/linux.tar -C $repo_path
set_preloads
{ time $tar_exec -xf $RAM_DISK/linux.tar -C $repo_path ; } 2> $output_folder/4_extract_$run_i.txt
unset_preloads
if [[ $2 == "VALGRIND" ]] ; then mv callgrind.out "$output_folder/callgrind_4_extract_$run_i.out" ; fi
cat $output_folder/4_extract_$run_i.txt
echo ""

done

echo "DONE."
