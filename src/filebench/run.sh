# pmem size 40G

workload_dir="./"

if [ $TARGET_FS == SIMURGH ]; then 
    root_dir="/pm:"
    root_dir_esc="\/pm:"
    cleanup=" "
fi
if [ $TARGET_FS == NOVA ]; then 
    root_dir="/mnt/fsramdisk"
    root_dir_esc="\/mnt\/fsramdisk"
    cleanup="rm -rf /mnt/fsramdisk/*"
fi
if [ $TARGET_FS == EXT4DAX ]; then 
    root_dir="/mnt/fsramdisk"
    root_dir_esc="\/mnt\/fsramdisk"
    cleanup="rm -rf /mnt/fsramdisk/*"
fi
if [ $TARGET_FS == PMFS ]; then 
    root_dir="/mnt/fsramdisk"
    root_dir_esc="\/mnt\/fsramdisk"
    cleanup="rm -rf /mnt/fsramdisk/*"
fi
if [ $TARGET_FS == SPLITFS ]; then 
    echo "SPLITFS is not working with filebench.."
    root_dir="/mnt/pmem_emul"
    root_dir_esc="\/mnt\/pmem_emul"
    cleanup="rm -rf /mnt/pmem_emul/*"
fi

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

for workload in fileserver varmail webproxy webserver
do

for value in $(seq 1 $2)
do

echo "RUN WORKLOAD $workload for $TARGET_FS $value"

echo "cleanup.."
eval $cleanup
rm -f "$workload_dir/$workload.temp.f"
rm -f "output_filebench_$workload_$TARGET_FS.txt"

echo "mount"
(cd $BENCHMARK_REPO_DIR/src/bash/ && ./mount.sh)

echo "do workload.."

# create temp worload file
rm -f "$workload_dir/$workload.temp.f"
cp "$workload_dir/$workload.f" "$workload_dir/$workload.temp.f"

# replace variables
dir_line_number() {
    grep -n 'set $dir' "$workload_dir/$workload.temp.f" | cut -d : -f 1
}
echo "$workload_dir/$workload.temp.f line $(dir_line_number)" 
replace_dir() {
    sed -i "$(dir_line_number)s/.*/set\ \$dir=$root_dir_esc/" "$workload_dir/$workload.temp.f"
}
replace_dir

echo mkdir $root_dir
set_preloads
mkdir $root_dir
filebench -f "$workload_dir/$workload.temp.f" >> "$workload_dir/output_filebench_$TARGET_FS-$workload.txt"
unset_preloads

done

done

