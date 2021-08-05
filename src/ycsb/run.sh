#!/bin/bash

leveldb_build_dir="$BENCHMARK_REPO_DIR/leveldb/build"

current_date=$(date +"%Y-%m-%d_%H-%M-%S");

set -e


function set_preloads {
    if [[ $TARGET_FS == "SIMURGH" ]]
    then
        export LD_PRELOAD="$BENCHMARK_REPO_DIR/libfs_ycsb.so"
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

function run_workload {
    echo "run $1"
    export trace_file=$BENCHMARK_REPO_DIR/leveldb/workloads/$1

    sync; echo 3 > /proc/sys/vm/drop_caches;
    if [[ $TARGET_FS == "SIMURGH" ]] ; then ../bash/format_simurgh.sh ; fi

    echo $leveldb_build_dir/db_bench --use_existing_db=1 --benchmarks=ycsb,stats,printdb --db=$repo_path --threads=1 --open_files=1000
    set_preloads
    mkdir -p $repo_path
    cp $BENCHMARK_REPO_DIR/$YCSB_DATA/* $repo_path
    unset_preloads
    sync; echo 3 > /proc/sys/vm/drop_caches;

    set_preloads
    $leveldb_build_dir/db_bench --use_existing_db=1 --benchmarks=ycsb,stats,printdb --db=$repo_path --threads=1 --open_files=1000  2>&1 | tee $output_folder/$1
    unset_preloads


}
set_preloads
unset_preloads


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

export trace_file=$BENCHMARK_REPO_DIR/leveldb/workloads/loada_5M

output_folder="output_$TARGET_FS_$current_date"

export output_folder

mkdir "$output_folder"

sync; echo 3 > /proc/sys/vm/drop_caches;

echo "Load A"
echo "$leveldb_build_dir/db_bench --use_existing_db=0 --benchmarks=ycsb,stats,printdb --db=$repo_path --threads=1 --open_files=1000"
set_preloads
mkdir -p $repo_path
$leveldb_build_dir/db_bench --use_existing_db=0 --benchmarks=ycsb,stats,printdb --db=$repo_path --threads=1 --open_files=1000  2>&1 | tee $output_folder/loada
unset_preloads

run_workload runa_5M_5M

run_workload runb_5M_5M

run_workload runc_5M_5M

run_workload rund_5M_5M

sync; echo 3 > /proc/sys/vm/drop_caches;

echo "Load E"
export trace_file=$BENCHMARK_REPO_DIR/leveldb/workloads/loade_5M

if [[ $TARGET_FS == "SIMURGH" ]] ; then ../bash/format_simurgh.sh ; fi

echo "$leveldb_build_dir/db_bench --use_existing_db=0 --benchmarks=ycsb,stats,printdb --db=$repo_path --threads=1 --open_files=1000"
set_preloads
mkdir -p $repo_path
$leveldb_build_dir/db_bench --use_existing_db=0 --benchmarks=ycsb,stats,printdb --db=$repo_path --threads=1 --open_files=1000  2>&1 | tee $output_folder/loade
unset_preloads

run_workload rune_5M_1M

run_workload runf_5M_5M

echo " "
done

echo "DONE."
