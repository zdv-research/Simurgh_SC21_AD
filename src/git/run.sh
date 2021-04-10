#!/bin/bash

git_path="$BENCHMARK_REPO_DIR/$GIT_BIN_PATH"
linux_kernel_source_path="$BENCHMARK_REPO_DIR/$LINUX_DATA_PACKED_AND_UNPACKED"
linux_kernel_source_folder_name=$(basename $linux_kernel_source_path)

current_date=$(date +"%Y-%m-%d_%H-%M-%S");

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

for run_i in {1..1}
do

echo "RUN $run_i ..."

rm -rf /tmp/*

if [[ $TARGET_FS == "SIMURGH" ]]
then
    echo TEST
    (cd $BENCHMARK_REPO_DIR/src/bash/ && ./mount.sh)

    repo_path="/pm:/git_dir"
elif [[ $TARGET_FS == "SPLITFS" ]]
then
    (cd $BENCHMARK_REPO_DIR/src/bash/ && ./mount.sh)
    rm -rf /mnt/pmem_emul/*

    sync; echo 3 > /proc/sys/vm/drop_caches;

    repo_path="/mnt/pmem_emul/git_dir"

# elif [[ $TARGET_FS == "TMPFS" ]]
# then
#     sync; echo 3 > /proc/sys/vm/drop_caches;
#     preload=""
#     repo_path="/tmp/git_dir_$current_date"

elif [[ $TARGET_FS == "NOVA" ]]
then
    sync; echo 3 > /proc/sys/vm/drop_caches;
    preload=""
    repo_path="/mnt/fsramdisk/git_dir"

    (cd $BENCHMARK_REPO_DIR/src/bash/ && ./mount.sh)
    rm -rf /mnt/fsramdisk/*
elif [[ $TARGET_FS == "PMFS" ]]
then
    sync; echo 3 > /proc/sys/vm/drop_caches;
    preload=""
    repo_path="/mnt/fsramdisk/git_dir"

    (cd $BENCHMARK_REPO_DIR/src/bash/ && ./mount.sh)
    rm -rf /mnt/fsramdisk/*
elif [[ $TARGET_FS == "EXT4DAX" ]]
then
    sync; echo 3 > /proc/sys/vm/drop_caches;
    preload=""
    repo_path="/mnt/fsramdisk/git_dir"

    (cd $BENCHMARK_REPO_DIR/src/bash/ && ./mount.sh)
    rm -rf /mnt/fsramdisk/*
else
    echo "No target fs specified. Abort."
    exit
fi

git_exec_="$git_path --git-dir=$repo_path/.git --work-tree=$repo_path"
git_exec="$git_exec_"
if [[ $2 == "VALGRIND" ]]
then
    git_exec="valgrind --tool=callgrind --trace-children=yes --callgrind-out-file=callgrind.out $git_exec_"
fi
echo "git_exec: $git_exec"

output_folder="output_$TARGET_FS_$current_date"

mkdir "$output_folder"

sync; echo 3 > /proc/sys/vm/drop_caches;

echo "Init repo:"
echo $git_exec init $repo_path
if [[ $TARGET_FS == "SIMURGH" ]] ; then set_preloads ; fi
{ time $git_exec init $repo_path ; } 2> $output_folder/1_init_timing_$run_i.txt
if [[ $TARGET_FS == "SIMURGH" ]] ; then unset_preloads ; fi
if [[ $2 == "VALGRIND" ]] ; then mv callgrind.out "$output_folder/callgrind_1_init_timing_$run_i.out" ; fi
cat $output_folder/1_init_timing_$run_i.txt
echo ""

# echo "Git config file:"
# if [[ $TARGET_FS == "SIMURGH" ]] ; then set_preloads ; fi
# cat $repo_path/.git/config
# if [[ $TARGET_FS == "SIMURGH" ]] ; then unset_preloads ; fi
# echo ""

sync; echo 3 > /proc/sys/vm/drop_caches;

echo "Copy over files:"
echo cp -r $linux_kernel_source_path $repo_path
if [[ $TARGET_FS == "SIMURGH" ]] ; then set_preloads ; fi
{ time cp -r $linux_kernel_source_path $repo_path ; } 2> $output_folder/2_copy_timing_$run_i.txt
if [[ $TARGET_FS == "SIMURGH" ]] ; then unset_preloads ; fi
cat $output_folder/2_copy_timing_$run_i.txt
echo ""

sync; echo 3 > /proc/sys/vm/drop_caches;

echo "Do ADD:"
echo $git_exec add $linux_kernel_source_folder_name
set_preloads
{ time $git_exec add $linux_kernel_source_folder_name ; } 2> $output_folder/3_add_timing_$run_i.txt
unset_preloads
if [[ $2 == "VALGRIND" ]] ; then mv callgrind.out "$output_folder/callgrind_3_add_timing_$run_i.out" ; fi
cat $output_folder/3_add_timing_$run_i.txt
echo ""

echo "Do UPDATE INDEX before commit:"
echo $git_exec update-index
set_preloads
{ time $git_exec update-index ; } 2> $output_folder/4_update_index_before_commit_timing_$run_i.txt
unset_preloads
if [[ $2 == "VALGRIND" ]] ; then mv callgrind.out "$output_folder/callgrind_4_update_index_before_commit_timing_$run_i.out" ; fi
cat $output_folder/4_update_index_before_commit_timing_$run_i.txt
echo ""

sync; echo 3 > /proc/sys/vm/drop_caches;

echo "Do STATUS before commit:"
echo $git_exec status
set_preloads
{ time $git_exec status >> /dev/null ; } 2> $output_folder/5_status_before_commit_timing_$run_i.txt
unset_preloads
if [[ $2 == "VALGRIND" ]] ; then mv callgrind.out "$output_folder/callgrind_5_status_before_commit_timing_$run_i.out" ; fi
cat $output_folder/5_status_before_commit_timing_$run_i.txt
echo ""

# sync; echo 3 > /proc/sys/vm/drop_caches;

# echo "Do set GC OFF:"
# echo $git_exec config gc.autodetach false
# set_preloads
# $git_exec config gc.autodetach false
# unset_preloads
# echo ""

sync; echo 3 > /proc/sys/vm/drop_caches;

echo "Do COMMIT:"
echo $git_exec commit -m "yeah"
set_preloads
{ time $git_exec commit -q -m "yeah" ; } 2> $output_folder/6_commit_timing_$run_i.txt
unset_preloads
if [[ $2 == "VALGRIND" ]] ; then mv callgrind.out "$output_folder/callgrind_6_commit_timing_$run_i.out" ; fi
cat $output_folder/6_commit_timing_$run_i.txt
echo ""

sync; echo 3 > /proc/sys/vm/drop_caches;

echo "Do UPDATE INDEX after commit:"
echo $git_exec update-index
set_preloads
{ time $git_exec update-index ; } 2> $output_folder/7_update_index_after_commit_timing_$run_i.txt
unset_preloads
if [[ $2 == "VALGRIND" ]] ; then mv callgrind.out "$output_folder/callgrind_7_update_index_after_commit_timing_$run_i.out" ; fi
cat $output_folder/7_update_index_after_commit_timing_$run_i.txt
echo ""

sync; echo 3 > /proc/sys/vm/drop_caches;

echo "Do STATUS after commit:"
echo $git_exec status
set_preloads
{ time $git_exec status >> /dev/null ; } 2> $output_folder/8_status_after_commit_timing_$run_i.txt
unset_preloads
if [[ $2 == "VALGRIND" ]] ; then mv callgrind.out "$output_folder/callgrind_8_status_after_commit_timing_$run_i.out" ; fi
cat $output_folder/8_status_after_commit_timing_$run_i.txt
echo ""

sync; echo 3 > /proc/sys/vm/drop_caches;

echo "Do LOG after commit:"
echo $git_exec log
set_preloads
{ time $git_exec log ; } 2> $output_folder/9_log_after_commit_timing_$run_i.txt
unset_preloads
if [[ $2 == "VALGRIND" ]] ; then mv callgrind.out "$output_folder/callgrind_9_log_after_commit_timing_$run_i.out" ; fi
cat $output_folder/9_log_after_commit_timing_$run_i.txt
echo ""

sync; echo 3 > /proc/sys/vm/drop_caches;

echo "Remove files:"
echo rm -rf "$repo_path/$linux_kernel_source_folder_name"
if [[ $TARGET_FS == "SIMURGH" ]] ; then set_preloads ; fi
{ time rm -rf "$repo_path/$linux_kernel_source_folder_name" ; } 2> $output_folder/10_remove_files_timing_$run_i.txt
if [[ $TARGET_FS == "SIMURGH" ]] ; then set_preloads ; fi
cat $output_folder/10_remove_files_timing_$run_i.txt
echo ""

sync; echo 3 > /proc/sys/vm/drop_caches;

echo "Do RESET:"
echo $git_exec reset HEAD --hard
set_preloads
{ time $git_exec reset HEAD --hard ; } 2> $output_folder/11_reset_timing_$run_i.txt
unset_preloads
if [[ $2 == "VALGRIND" ]] ; then mv callgrind.out "$output_folder/callgrind_11_reset_timing_$run_i.out" ; fi
cat $output_folder/11_reset_timing_$run_i.txt
echo ""

done

echo "DONE."