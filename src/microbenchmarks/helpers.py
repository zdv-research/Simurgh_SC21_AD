import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description='A tutorial of argparse!')
parser.add_argument("--target", required=True, type=str, help="", choices=["SIMURGHLOCAL", "SIMURGH", "SPLITFS", "NOVA", "EXT4DAX", "XFSDAX", "PMFS"])
args = parser.parse_args()

def get_target():
    return args.target

def is_user_space_target(target):
    if target == "SIMURGH" or target == "SIMURGHLOCAL" or target == "SPLITFS":
        return True
    return False

def get_drop_caches(target):
    #if target == "SIMURGH" or target == "SIMURGHLOCAL":
    #    return False
    return True

def get_root(target):
    if target == "SIMURGH" or target == "SIMURGHLOCAL":
        return "/pm:"
    if target == "SPLITFS":
        return "/mnt/pmem_emul/"
    return "/mnt/fsramdisk/"


def get_LD_PRELOAD (target):
    if target == "SIMURGH" or target == "SIMURGHLOCAL":
        return 'LD_PRELOAD='+os.environ['BENCHMARK_REPO_DIR']+'/'+os.environ['SIMURGH_LIB_PATH']
    if target == "SPLITFS":
        return 'LD_LIBRARY_PATH='+os.environ['BENCHMARK_REPO_DIR']+'/'+os.environ['SPLITFS_PATH']+' NVP_TREE_FILE='+os.environ['BENCHMARK_REPO_DIR']+'/'+os.environ['SPLITFS_NVP_TREE_FILE_PATH']+' LD_PRELOAD='+os.environ['BENCHMARK_REPO_DIR']+'/'+os.environ['SPLITFS_LIB_PATH']
    return ''

def do_cleanup (target):
    os.popen('rm -rf /tmp/*').read()
    if target == "SIMURGH" or target == "SIMURGHLOCAL":
        subprocess.call(''+os.environ['BENCHMARK_REPO_DIR']+'/src/bash/format_simurgh.sh', shell=True)
    if target == "SPLITFS":
        os.popen('find /mnt/pmem_emul/ -type f -delete').read()
        os.popen('rm -rf /mnt/pmem_emul/*').read()
    if target == "NOVA" or target == "EXT4DAX" or target == "XFSDAX" or target == "PMFS":
        os.popen('find /mnt/fsramdisk/ -type f -delete').read()
        os.popen('rm -rf /mnt/fsramdisk/*').read()

def parse_Time (text):
    for line in text.split("\n"):
        if line.startswith("Time: "):
            return line.split(" ")[1]
    return ""

def is_float(value):
  try:
    float(value)
    return True
  except ValueError:
    return False
