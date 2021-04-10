import helpers
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
import json 
import subprocess
import shutil

output_save = True
output_show = False

do_checks = 0

# Final settings
ops_amounts_bases = [10]
measurements_per_result = 20
worker_amounts = [1, 2, 4, 6, 8, 10]

# Test settings
# worker_amounts = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 30, 40]

# Final settings
benchmarks = [

    # {       # Not running at the moment...
    #         'prog_filename' : 'create_unlink_file',
    #         'title' : "create_close_unlink_file_in_shared_dir",
    #         'short_title' : "create_close_unlink_file_in_shared_dir",
    #         'compiler_args' : "-Dmode=0",
    #         'other_args' : "",
    #         'ops_amounts_factor': 5000,
    #         'worker_mode': "multithreaded"
    # },  

#     {
#             'prog_filename' : 'create_unlink_file',
#             'title' : "create_close_unlink_file_in_private_dir",
#             'short_title' : "create_close_unlink_file_in_private_dir",
#             'compiler_args' : "-Dmode=1",
#             'other_args' : "",
#             'ops_amounts_factor': 100000,
#             'worker_mode': "multithreaded"
#     },  
#     {
#             'prog_filename' : 'create_unlink_file',
#             'title' : "create_close_unlink_file_in_shared_dir",
#             'short_title' : "create_close_unlink_file_in_shared_dir",
#             'compiler_args' : "-Dmode=0",
#             'other_args' : "",
#             'ops_amounts_factor': 100000,
#             'worker_mode': "multiprocesses"
#     },  
#     {
#             'prog_filename' : 'create_unlink_file',
#             'title' : "create_close_unlink_file_in_private_dir",
#             'short_title' : "create_close_unlink_file_in_private_dir",
#             'compiler_args' : "-Dmode=1",
#             'other_args' : "",
#             'ops_amounts_factor': 100000,
#             'worker_mode': "multiprocesses"
#     }, 
    {
            'prog_filename' : 'create_file',
            'title' : "create_file_in_shared_dir",
            'short_title' : "create_file_in_shared_dir",
            'compiler_args' : "-Dmode=0",
            'other_args' : "",
            'ops_amounts_factor': 5000,
            'worker_mode': "multithreaded"
    },  
    {
            'prog_filename' : 'create_file',
            'title' : "create_file_in_private_dir",
            'short_title' : "create_file_in_private_dir",
            'compiler_args' : "-Dmode=1",
            'other_args' : "",
            'ops_amounts_factor': 5000,
            'worker_mode': "multithreaded"
    },  
#     {
#             'prog_filename' : 'create_file',
#             'title' : "create_file_in_shared_dir",
#             'short_title' : "create_file_in_shared_dir",
#             'compiler_args' : "-Dmode=0",
#             'other_args' : "",
#             'ops_amounts_factor': 5000,
#             'worker_mode': "multiprocesses"
#     },  
    # {
    #         'prog_filename' : 'create_file',
    #         'title' : "create_file_in_private_dir",
    #         'short_title' : "create_file_in_private_dir",
    #         'compiler_args' : "-Dmode=1",
    #         'other_args' : "",
    #         'ops_amounts_factor': 5000,
    #         'worker_mode': "multiprocesses"
    # }, 
    # {
    #         'prog_filename' : 'unlink_file',
    #         'title' : "unlink_file_in_shared_dir",
    #         'short_title' : "unlink_file_in_shared_dir",
    #         'compiler_args' : "-Dmode=0",
    #         'other_args' : "",
    #         'ops_amounts_factor': 5000,
    #         'worker_mode': "multithreaded"
    # },  
    { 
            'prog_filename' : 'unlink_file',
            'title' : "unlink_file_in_private_dir",
            'short_title' : "unlink_file_in_private_dir",
            'compiler_args' : "-Dmode=1",
            'other_args' : "",
            'ops_amounts_factor': 5000,
            'worker_mode': "multithreaded"
    },  
#     {
#             'prog_filename' : 'unlink_file',
#             'title' : "unlink_file_in_shared_dir",
#             'short_title' : "unlink_file_in_shared_dir",
#             'compiler_args' : "-Dmode=0",
#             'other_args' : "",
#             'ops_amounts_factor': 5000,
#             'worker_mode': "multiprocesses"
#     },  
#     {
#             'prog_filename' : 'unlink_file',
#             'title' : "unlink_file_in_private_dir",
#             'short_title' : "unlink_file_in_private_dir",
#             'compiler_args' : "-Dmode=1",
#             'other_args' : "",
#             'ops_amounts_factor': 5000,
#             'worker_mode': "multiprocesses"
#     }, 
#     {
#             'prog_filename' : 'path_resolution',
#             'title' : "open_private_file_in_shared_dir_depth5",
#             'short_title' : "open_private_file_in_shared_dir_depth5",
#             'compiler_args' : "-Dmode=0",
#             'other_args' : "",
#             'ops_amounts_factor': 50000,
#             'worker_mode': "multithreaded"
#     },  
#     {
#             'prog_filename' : 'path_resolution',
#             'title' : "open_private_file_in_shared_dir_depth5",
#             'short_title' : "open_private_file_in_shared_dir_depth5",
#             'compiler_args' : "-Dmode=0",
#             'other_args' : "",
#             'ops_amounts_factor': 50000,
#             'worker_mode': "multiprocesses"
#     },  
#     {
#             'prog_filename' : 'path_resolution',
#             'title' : "open_private_file_in_private_dir_depth5",
#             'short_title' : "open_private_file_in_private_dir_depth5",
#             'compiler_args' : "-Dmode=1",
#             'other_args' : "",
#             'ops_amounts_factor': 50000,
#             'worker_mode': "multithreaded"
#     }, 
    {
            'prog_filename' : 'path_resolution',
            'title' : "open_private_file_in_private_dir_depth5",
            'short_title' : "open_private_file_in_private_dir_depth5",
            'compiler_args' : "-Dmode=1",
            'other_args' : "",
            'ops_amounts_factor': 50000,
            'worker_mode': "multiprocesses"
    }, 
#     {
#             'prog_filename' : 'path_resolution',
#             'title' : "open_single_file_depth5",
#             'short_title' : "open_single_file_depth5",
#             'compiler_args' : "-Dmode=2",
#             'other_args' : "",
#             'ops_amounts_factor': 500000,
#             'worker_mode': "multithreaded"
#     }, 
    {
            'prog_filename' : 'path_resolution',
            'title' : "open_single_file_depth5",
            'short_title' : "open_single_file_depth5",
            'compiler_args' : "-Dmode=2",
            'other_args' : "",
            'ops_amounts_factor': 500000,
            'worker_mode': "multiprocesses"
    }, 
    {
            'prog_filename' : 'append',
            'title' : "append_4K_blocks_to_private_file",
            'short_title' : "append_4K_blocks_to_private_file",
            'compiler_args' : "-Dbytes_per_op=4096 -Dmode=1",
            'other_args' : "",
            'ops_amounts_factor': 10000,
            'worker_mode': "multithreaded"
    }, 
    # {
    #         'prog_filename' : 'append',
    #         'title' : "open_and_append_4K_block_to_distinct_files_of_2K",
    #         'short_title' : "open_and_append_4K_block_to_distinct_file",
    #         'compiler_args' : "-Dbytes_per_op=4096 -Dmode=2",
    #         'other_args' : "",
    #         'ops_amounts_factor': 5000,
    #         'worker_mode': "multithreaded"
    # }, 
        {
            'prog_filename' : 'simple_read_write',
            'title' : "read_private_4K_block_in_private_file",
            'short_title' : "read_private_4K_block_in_private_file",
            'compiler_args' : "-Dbytes_per_op=4096 -Dmode=0",
            'other_args' : "",
            'ops_amounts_factor': 1000,
            'worker_mode': "multithreaded"
    },  
    #     {
    #         'prog_filename' : 'simple_read_write',
    #         'title' : "write_private_4K_block_in_private_file",
    #         'short_title' : "write_private_4K_block_in_private_file",
    #         'compiler_args' : "-Dbytes_per_op=4096 -Dmode=1",
    #         'other_args' : "",
    #         'ops_amounts_factor': 1000,
    #         'worker_mode': "multithreaded"
    #    },  
    #  {
    #          'prog_filename' : 'simple_read_write',
    #          'title' : "read_private_2M_block_in_private_file",
    #          'short_title' : "read_private_2M_block_in_private_file",
    #          'compiler_args' : "-Dbytes_per_op=2097152 -Dmode=0",
    #          'other_args' : "",
    #          'ops_amounts_factor': 1000,
    #          'worker_mode': "multithreaded"
    #  },  
    # {
    #          'prog_filename' : 'simple_read_write',
    #          'title' : "read_private_256K_block_in_private_file",
    #          'short_title' : "read_private_256K_block_in_private_file",
    #          'compiler_args' : "-Dbytes_per_op=262144 -Dmode=0",
    #          'other_args' : "",
    #          'ops_amounts_factor': 1000,
    #          'worker_mode': "multithreaded"
    #  }, 
    #     {
    #          'prog_filename' : 'simple_read_write',
    #          'title' : "write_private_2M_block_in_private_file",
    #          'short_title' : "write_private_2M_block_in_private_file",
    #          'compiler_args' : "-Dbytes_per_op=2097152 -Dmode=1",
    #          'other_args' : "",
    #          'ops_amounts_factor': 1000,
    #          'worker_mode': "multithreaded"
    #  },  
    # {
    #          'prog_filename' : 'simple_read_write',
    #          'title' : "write_private_256K_block_in_private_file",
    #          'short_title' : "write_private_256K_block_in_private_file",
    #          'compiler_args' : "-Dbytes_per_op=262144 -Dmode=1",
    #          'other_args' : "",
    #          'ops_amounts_factor': 1000,
    #          'worker_mode': "multithreaded"
    #  }, 
    #  {
    #          'prog_filename' : 'big_read_write',
    #          'title' : "overwrite_private_2M_block_in_shared_file",
    #          'short_title' : "overwrite_private_2M_block_in_shared_file",
    #          'compiler_args' : "-Dbytes_per_op=2097152 -Dmode=1",
    #          'other_args' : "",
    #          'ops_amounts_factor': 1000,
    #          'worker_mode': "multithreaded"
    #  },  
     {
             'prog_filename' : 'big_read_write',
             'title' : "read_private_2M_block_in_shared_file",
             'short_title' : "read_private_2M_block_in_shared_file",
             'compiler_args' : "-Dbytes_per_op=2097152 -Dmode=0",
             'other_args' : "",
             'ops_amounts_factor': 1000,
             'worker_mode': "multithreaded"
     },  
    #  {
    #          'prog_filename' : 'big_read_write',
    #          'title' : "read_private_2M_block_in_shared_file",
    #          'short_title' : "read_private_2M_block_in_shared_file",
    #          'compiler_args' : "-Dbytes_per_op=2097152 -Dmode=0",
    #          'other_args' : "",
    #          'ops_amounts_factor': 1000,
    #          'worker_mode': "multiprocesses"
    #  },  
    #  {
    #          'prog_filename' : 'big_read_write',
    #          'title' : "overwrite_private_2M_block_in_shared_file",
    #          'short_title' : "overwrite_private_2M_block_in_shared_file",
    #          'compiler_args' : "-Dbytes_per_op=2097152 -Dmode=1",
    #          'other_args' : "",
    #          'ops_amounts_factor': 1000,
    #          'worker_mode': "multiprocesses"
    #  }, 
     {
             'prog_filename' : 'big_read_write',
             'title' : "read_private_4K_block_in_shared_file",
             'short_title' : "read_private_4K_block_in_shared_file",
             'compiler_args' : "-Dbytes_per_op=4096 -Dmode=0",
             'other_args' : "",
             'ops_amounts_factor': 200000,
             'worker_mode': "multithreaded"
     },  
     {
             'prog_filename' : 'big_read_write',
             'title' : "overwrite_private_4K_block_in_shared_file",
             'short_title' : "overwrite_private_4K_block_in_shared_file",
             'compiler_args' : "-Dbytes_per_op=4096 -Dmode=1",
             'other_args' : "",
             'ops_amounts_factor': 200000,
             'worker_mode': "multithreaded"
     },  
    #  {
    #          'prog_filename' : 'big_read_write',
    #          'title' : "read_private_4K_block_in_shared_file",
    #          'short_title' : "read_private_4K_block_in_shared_file",
    #          'compiler_args' : "-Dbytes_per_op=4096 -Dmode=0",
    #          'other_args' : "",
    #          'ops_amounts_factor': 200000,
    #          'worker_mode': "multiprocesses"
    #  },  
    #  {
    #          'prog_filename' : 'big_read_write',
    #          'title' : "overwrite_private_4K_block_in_shared_file",
    #          'short_title' : "overwrite_private_4K_block_in_shared_file",
    #          'compiler_args' : "-Dbytes_per_op=4096 -Dmode=1",
    #          'other_args' : "",
    #          'ops_amounts_factor': 200000,
    #          'worker_mode': "multiprocesses"
    # }, 
    {
            'prog_filename' : 'rename',
            'title' : "rename_private_file_in_shared_directory",
            'short_title' : "rename_private_file_in_shared_directory",
            'compiler_args' : "-Dmode=0",
            'other_args' : "",
            'ops_amounts_factor': 100000,
            'worker_mode': "multithreaded"
    },  
#     {
#             'prog_filename' : 'rename',
#             'title' : "rename_private_file_in_shared_directory",
#             'short_title' : "rename_private_file_in_shared_directory",
#             'compiler_args' : "-Dmode=0",
#             'other_args' : "",
#             'ops_amounts_factor': 100000,
#             'worker_mode': "multiprocesses"
#     }, 
#     {
#             'prog_filename' : 'rename',
#             'title' : "rename_private_dir_with_one_file_in_shared_directory",
#             'short_title' : "rename_private_dir_with_one_file_in_shared_directory",
#             'compiler_args' : "-Dmode=1",
#             'other_args' : "",
#             'ops_amounts_factor': 100000,
#             'worker_mode': "multithreaded"
#     }, 
#     {
#             'prog_filename' : 'rename',
#             'title' : "rename_private_dir_with_one_file_in_shared_directory",
#             'short_title' : "rename_private_dir_with_one_file_in_shared_directory",
#             'compiler_args' : "-Dmode=1",
#             'other_args' : "",
#             'ops_amounts_factor': 100000,
#             'worker_mode': "multiprocesses"
#     }, 
#     {
#             'prog_filename' : 'create_directory',
#             'title' : "create_dir_in_shared_dir",
#             'short_title' : "create_dir_in_shared_dir",
#             'compiler_args' : "-Dmode=0",
#             'other_args' : "",
#             'ops_amounts_factor': 2000,
#             'worker_mode': "multithreaded"
#     },  
#     {
#             'prog_filename' : 'create_directory',
#             'title' : "create_dir_in_shared_dir",
#             'short_title' : "create_dir_in_shared_dir",
#             'compiler_args' : "-Dmode=0",
#             'other_args' : "",
#             'ops_amounts_factor': 2000,
#             'worker_mode': "multiprocesses"
#     },  
#     {
#             'prog_filename' : 'create_directory',
#             'title' : "create_dir_in_private_dir",
#             'short_title' : "create_dir_in_private_dir",
#             'compiler_args' : "-Dmode=1",
#             'other_args' : "",
#             'ops_amounts_factor': 2000,
#             'worker_mode': "multithreaded"
#     }, 
#     {
#             'prog_filename' : 'create_directory',
#             'title' : "create_dir_in_private_dir",
#             'short_title' : "create_dir_in_private_dir",
#             'compiler_args' : "-Dmode=1",
#             'other_args' : "",
#             'ops_amounts_factor': 2000,
#             'worker_mode': "multiprocesses"
#     }, 
#     {
#             'prog_filename' : 'fallocate',
#             'title' : "fallocate_private_files_4K",
#             'short_title' : "fallocate_private_files_4K",
#             'compiler_args' : "-Dmode=0",
#             'other_args' : "",
#             'ops_amounts_factor': 10000,
#             'worker_mode': "multithreaded"
#     }, 
#     {
#             'prog_filename' : 'fallocate',
#             'title' : "fallocate_private_files_4K",
#             'short_title' : "fallocate_private_files_4K",
#             'compiler_args' : "-Dmode=0",
#             'other_args' : "",
#             'ops_amounts_factor': 10000,
#             'worker_mode': "multiprocesses"
#     }, 
    {
            'prog_filename' : 'fallocate',
            'title' : "fallocate_private_files_4M",
            'short_title' : "fallocate_private_files_4M",
            'compiler_args' : "-Dmode=1",
            'other_args' : "",
            'ops_amounts_factor': 100,
            'worker_mode': "multithreaded"
    }, 
#     {
#             'prog_filename' : 'fallocate',
#             'title' : "fallocate_private_files_4M",
#             'short_title' : "fallocate_private_files_4M",
#             'compiler_args' : "-Dmode=1",
#             'other_args' : "",
#             'ops_amounts_factor': 100,
#             'worker_mode': "multiprocesses"
#     }, 


    # {  # not usable: conceptually wrong..
    #         'prog_filename' : 'append',
    #         'title' : "append_to_only_one_file 4K",
    #         'short_title' : "append_to_only_one_file_4K",
    #         'compiler_args' : "-Dbytes_per_op=4096 -Dmode=0",
    #         'other_args' : "",
    #         'ops_amounts_factor': 5000,
    #         'worker_mode': "multithreaded"
    # },  
    #     {
    #         'prog_filename' : 'simple_read_write',
    #         'title' : "overwrite_private_4k_files",
    #         'short_title' : "overwrite_private_4k_files",
    #         'compiler_args' : "-Dbytes_per_op=4096 -Dmode=1",
    #         'other_args' : "",
    #         'ops_amounts_factor': 200000,
    #         'worker_mode': "multiprocesses"
    # }, 
    #         {
    #         'prog_filename' : 'simple_read_write',
    #         'title' : "read_private_4k_files",
    #         'short_title' : "read_private_4k_files",
    #         'compiler_args' : "-Dbytes_per_op=4096 -Dmode=0",
    #         'other_args' : "",
    #         'ops_amounts_factor': 200000,
    #         'worker_mode': "multiprocesses"
    # }, 
    #             {
    #         'prog_filename' : 'simple_read_write',
    #         'title' : "read_private_4k_files",
    #         'short_title' : "read_private_4k_files",
    #         'compiler_args' : "-Dbytes_per_op=4096 -Dmode=0",
    #         'other_args' : "",
    #         'ops_amounts_factor': 200000,
    #         'worker_mode': "multipthreaded"
    # }, 
    #         {
    #         'prog_filename' : 'simple_read_write',
    #         'title' : "overwrite_private_4k_files",
    #         'short_title' : "overwrite_private_4k_files",
    #         'compiler_args' : "-Dbytes_per_op=4096 -Dmode=1",
    #         'other_args' : "",
    #         'ops_amounts_factor': 200000,
    #         'worker_mode': "multithreaded"
    # }, 
]

# worker_amounts = [1, 8]
# benchmarks = [
#      {
#             'prog_filename' : 'snappymicrobench',
#             'title' : "snappymicrobench_8K",
#             'short_title' : "snappymicrobench_8K",
#             'compiler_args' : "-Dbytes_per_op=8192 -Dmode=0",
#             'additional_sources' : "snappy/snappy.c",
#             'other_args' : "",
#             'ops_amounts_factor': 26214,
#             'worker_mode': "multithreaded"
#     },{
#             'prog_filename' : 'snappymicrobench',
#             'title' : "snappymicrobench_16K",
#             'short_title' : "snappymicrobench_16K",
#             'compiler_args' : "-Dbytes_per_op=16384 -Dmode=0",
#             'additional_sources' : "snappy/snappy.c",
#             'other_args' : "",
#             'ops_amounts_factor': 26214,
#             'worker_mode': "multithreaded"
#     },{
#             'prog_filename' : 'snappymicrobench',
#             'title' : "snappymicrobench_32K",
#             'short_title' : "snappymicrobench_32K",
#             'compiler_args' : "-Dbytes_per_op=32768 -Dmode=0",
#             'additional_sources' : "snappy/snappy.c",
#             'other_args' : "",
#             'ops_amounts_factor': 26214,
#             'worker_mode': "multithreaded"
#     },{
#             'prog_filename' : 'snappymicrobench',
#             'title' : "snappymicrobench_128K",
#             'short_title' : "snappymicrobench_128K",
#             'compiler_args' : "-Dbytes_per_op=131072 -Dmode=0",
#             'additional_sources' : "snappy/snappy.c",
#             'other_args' : "",
#             'ops_amounts_factor': 26214,
#             'worker_mode': "multithreaded"
#     }
# ]

# benchmarks = [
#     {
#         'prog_filename' : 'large_file_read_write',
#         'title' : "read_large_file_512M_per_op",
#         'short_title' : "read_large_file_512M_per_op",
#         'compiler_args' : "-Dbytes_per_op_M=512 -Dmode=0",
#         'other_args' : "",
#         'worker_mode': "multithreaded"
#     }, 
#     {
#         'prog_filename' : 'large_file_read_write',
#         'title' : "write_large_file_512M_per_op",
#         'short_title' : "write_large_file_512M_per_op",
#         'compiler_args' : "-Dbytes_per_op_M=512 -Dmode=1",
#         'other_args' : "",
#         'worker_mode': "multithreaded"
#     }, 

# ]

Y_axis_label = "time [ms]"
X_axis_label = "n operations"


### helpers

error_summary_single_try = {}
def add_error_single_try(title):
    if title in error_summary_single_try:
        error_summary_single_try[title] = error_summary_single_try[title] + 1
    else:
        error_summary_single_try[title] = 1

error_summary_all_tries = {}
def add_error_all_tries(title):
    if title in error_summary_all_tries:
        error_summary_all_tries[title] = error_summary_all_tries[title] + 1
    else:
        error_summary_all_tries[title] = 1

error_summary_complete_run = {}
def add_error_complete_run(title):
    if title in error_summary_complete_run:
        error_summary_complete_run[title] = error_summary_complete_run[title] + 1
    else:
        error_summary_complete_run[title] = 1


def print_error_summary():
    print("####### ERROR SUMMARY Start #######")
    print("Single try errors")
    for title in error_summary_single_try:
        print("  " + title + ": " + str(error_summary_single_try[title]))
    print("All try per run errors")
    for title in error_summary_all_tries:
        print("  " + title + ": " + str(error_summary_all_tries[title]))
    print("Complete run errors")
    for title in error_summary_complete_run:
        print("  " + title + ": " + str(error_summary_complete_run[title]))
    print("####### ERROR SUMMARY End #######")


def run_single_measurement(processes, threads, operations):
    tries = 0
    while True:
        if tries == 5:
            add_error_all_tries(short_title)
            return 0
        tries = tries + 1

        print("")
        print_error_summary()
        print("")
        print("####### BENCHMARK RUN (" + str(runs_done_amount) + "/" + str(overall_run_amount) + "): " + title + " #######")
        print("")

        args =  ' --processes=' + str(int(processes))
        args += ' --threads=' + str(int(threads))
        args += ' --operations=' + str(int(operations))
        args += ' --do_checks=' + str(do_checks)
        args += ' --root=' + helpers.get_root(target)
        args += " " + other_args

        if helpers.get_drop_caches(target) is True:
            args +=  ' --drop_caches=1'
        else:
            args +=  ' --drop_caches=0'

        helpers.do_cleanup(target)

        if processes == 1:
            args +=  ' --process_id=' + str(0)

            command_to_run = helpers.get_LD_PRELOAD(target) + ' ./'+prog_filename+'.o' + args
            print(command_to_run)
            output = os.popen(command_to_run).read()    

            print("")
            print(output)
            time = helpers.parse_Time(output)
            if time:
                return time
            else:
                add_error_single_try(short_title)

        else:

            print("#### PREPARARE ####")
            command_to_run = helpers.get_LD_PRELOAD(target) + ' ./'+prog_filename+'.o' + args + ' --only_prepare_run=1'
            output = os.popen(command_to_run).read() 
            print(output)

            error_in_any_process = False

            print("#### MEASURE ####")
            process_list = []
            times = []
            for process_id in range(processes):
                p = subprocess.Popen(helpers.get_LD_PRELOAD(target) + ' ./'+prog_filename+'.o' + args + ' --process_id=' + str(process_id) + ' --only_measurement_run=1', shell=True, stdout=subprocess.PIPE)
                process_list.append((p, process_id))

            for p, process_id in process_list:
                p.wait()
                print("")
                print("Process " + str(process_id) +" collected output:")
                out, err = p.communicate()
                output = out.decode("utf-8")
                print(out.decode("utf-8"))
                time = helpers.parse_Time(output)
                if time == 0:
                    add_error_single_try(short_title)
                    error_in_any_process = True
                times.append(helpers.parse_Time(output))

            max_time = max(times)
            print("Max process time: " + str(max_time))

            print("#### POSTPARE ####")
            command_to_run = helpers.get_LD_PRELOAD(target) + ' ./'+prog_filename+'.o' + args + ' --only_postpare_run=1'
            output = os.popen(command_to_run).read() 
            print(output)

            if error_in_any_process is not True:
                return max_time

def serialize():
    json_obj = {}
    json_obj["title"] = title
    json_obj["short_title"] = short_title
    json_obj["Y_axisLabes"] = Y_axis_label
    json_obj["X_axis_label"] = X_axis_label
    json_obj["grouped_label"] = grouped_label
    json_obj["ops_amounts"] = ops_amounts
    json_obj["worker_amounts"] = worker_amounts
    json_obj["worker_mode"] = worker_mode
    json_obj["results"] = results
    json_obj["date"] = date

    json_file = open("output_temp/"+filename+".json", "w")
    json_file.write(json.dumps(json_obj, indent=4, separators=(',', ': ')))
    json_file.close()



### main

if output_save:
    shutil.rmtree("output_temp", ignore_errors=True)
    os.mkdir("output_temp")


# calculate amount of runs
overall_run_amount = len(ops_amounts_bases) * len(worker_amounts) * len(benchmarks) * measurements_per_result
runs_done_amount = 0

target = helpers.get_target()


for benchmark in benchmarks:

    labels = []
    results = []
    date = ""
    filename = ""

    prog_filename = benchmark['prog_filename']
    title = benchmark['title']
    short_title = benchmark['short_title']
    other_args = benchmark['other_args']
    compiler_args = benchmark['compiler_args']

    worker_mode = 'multithreaded' # default value
    if 'worker_mode' in benchmark:
        worker_mode = benchmark['worker_mode'] 

    if worker_mode == 'multithreaded':
        title_postfix = 'MT'
        grouped_label = 'Threads'
    else:
        title_postfix = 'MP'
        grouped_label = 'Processes'

    title += ' ' + title_postfix
    short_title += '_' + title_postfix

    ops_amounts = []
    for ops_amounts_base in ops_amounts_bases:
        if "ops_amounts_factor" in benchmark:
            ops_amounts.append(ops_amounts_base*benchmark['ops_amounts_factor'])
        else:
            ops_amounts.append(1)

    additional_sources = ""
    if 'additional_sources' in benchmark:
        additional_sources = benchmark['additional_sources']

    print(os.popen('g++ -g -pthread ./'+prog_filename+'.cpp '+additional_sources+' '+compiler_args+' -fpermissive -o ./'+prog_filename+'.o').read())

    for op_number in ops_amounts:
        labels.append(str(op_number))

    for worker_number in worker_amounts:
        result = []
        for op_number in ops_amounts:
            measurements = []
            for single_measurement in range(measurements_per_result):
                if worker_mode == 'multithreaded':
                    single_measurement = run_single_measurement(1, worker_number, op_number)
                    if single_measurement != 0 and helpers.is_float(single_measurement):
                        measurements.append(float(single_measurement))
                else:
                    single_measurement = run_single_measurement(worker_number, 1, op_number)
                    if single_measurement != 0 and helpers.is_float(single_measurement):
                        measurements.append(float(single_measurement))
                runs_done_amount+=1

            if len(measurements) == 0:
                add_error_complete_run(short_title)
                result.append(0)
            else:
                result.append(sum(measurements) / len(measurements))

        results.append(result)

    now = datetime.now()
    date = now.strftime("%Y%m%d_%H-%M-%S")
    filename = short_title + "_" + date

    if output_save:
        serialize()

    x = np.arange(len(labels))  # the label locations
    width = 0.15  # the width of the bars

    fig, ax = plt.subplots()
    rect_series = []
    for i in range(0, len(worker_amounts)):
        rect_series.append(ax.bar(x + (-len(worker_amounts)/2+i)*width, results[i], width, label=(grouped_label + ': ' + str(worker_amounts[i]))))

    ax.set_ylabel('time [ms]')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


    for i in range(0, len(worker_amounts)):
        autolabel(rect_series[i])

    #fig.tight_layout()

    if output_save:
        plt.savefig("output_temp/"+filename+".pdf")


helpers.do_cleanup(target)
os.popen('rm -rf temp').read()

if output_save:
    now = datetime.now()
    date = now.strftime("%Y%m%d_%H-%M-%S")
    os.rename("output_temp", "output_microbenchmarks_" + target + "_" + date)

print_error_summary()

if output_show:
    plt.show()


