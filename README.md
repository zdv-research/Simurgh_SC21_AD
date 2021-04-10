[![DOI](https://zenodo.org/badge/356302456.svg)](https://zenodo.org/badge/latestdoi/356302456)
# SimurghAD
Simurgh is a user level file system library for NVMMs. We proposes the concept of protected functions to provide hardware assisted security to user level libraries without direct OS involvement. Using protected functions Simurgh is able to provide fine grained security to user level code. The repository contains setups, instructions and benchmarks to produce results presented in SC21 submission. The experiments are divided into Simurgh file system library and the modified gem5 simulator and the ISA extensions for the proposed hardware instructions. 

## Contents

* [Repository structure](#repository-structure)
* [Prerequisites](#prerequisites)
  + [Environment](#environment)
    - [ndctl](#ndctl)
    - [Simurgh](#simurgh)
    - [NOVA](#nova)
    - [EXT4DAX](#ext4dax)
    - [PMFS](#pmfs)
    - [SplitFS](#splitfs)
  + [Applications](#applications)
    - [Git](#git)
    - [Filebench](#filebench)
    - [Tar](#tar)
    - [YCSB](#ycsb)
  + [Data](#data)
  + [System](#system)
* [Running Benchmarks](#running-benchmarks)
  + [Benchmark details](#benchmark-details)
    - [Microbenchmarks](#microbenchmarks)
    - [Git](#git-1)
    - [Filebench](#filebench-1)
    - [Recovery times](#recovery-times)
    - [Tar](#tar-1)
    - [YCSB](#ycsb-1)
* [Gem5 benchmark](#gem5-benchmark)
  + [Building gem5](#building-gem5)
  + [Testing the instruction](#testing-the-instruction)

## Repository structure
The repository contains a global `config.sh` and following scripts to run the file system benchmarks:
```bash
run_microbenchmarks.sh
run_filebench.sh
run_git.sh
run_recovery.sh
```

The `src` directory contains the actual scripts and workloads to perform the benchmarks. They are either executed by the scripts above or manually using instructions below.

Simurgh is provided as pre-compiled binaries found at the top level of the repository.  

`gem5` folder contains the modified version of the [gem5 simulator](https://github.com/gem5/gem5). `gem5_kernel` contains ready to use modified kernel images.


## Prerequisites

All file system experiments are performed on CentOS 8.2 running Linux kernel `5.1.0`, unless stated otherwise.  
Some benchmarks are compiled on the fly by their corresponding scripts.  
The required `gcc` and `g++` version is `8.3.1`.
Some benchmarks use python (version `3.6.8`) to be scheduled and `matplotlib` for their output.

### Environment

#### ndctl
[`ndctl`](https://github.com/pmem/ndctl) for managing persistent memory devices has to be available. Our benchmarks use version `67`.  
A namespace has to be setup:
```
ndctl create-namespace -f -m devdax -a 4096
```
The returned `dev` name (e.g. `namespace0.0`) has to be set in the `config.sh` as `NDCTL_NAMESPACE`. `NDCTL_DEV` has to be the pmem device (e.g. `/dev/pmem0`).
`ndctl` then is used by the benchmark scripts automatically. For example, `NOVA` benchmarks reconfigure to `fsdax` mode, `SIMURGH` benchmarks reconfigure to `devdax` mode.

#### Simurgh

Applications can use Simurgh by preloading the Simurgh file system library (`LD_PRELOAD=libsimurgh.so`).
The shared DRAM and persistent address space can be formatted using the `simurgh_utils` binary with `f` argument. 
For benchmarks, that are performed by our supplied bash scripts, a manual preload or format is not required.

#### NOVA
Our benchmarks use [`NOVA`](https://github.com/NVSL/NOVA) version `5.1` within kernel `5.1.0`. The kernel has to be build with NOVA modules enabled.  
Please follow the build and install instructions in `NOVA`'s repository. We configured NOVA with inline writes.

#### EXT4DAX
Our benchmarks use `ext4` file system in `DAX` mode of kernel `5.1.0`, which has to be enabled while kernel compilation.

#### PMFS
Our benchmarks use [`PMFS-new`](https://github.com/NVSL/PMFS-new) inside kernel `4.18.19`.  
Please see the build and install instructions in `PMFS-new`'s repository. The path to the built module has to be be set in the `config.sh` as `PMFS_MODULE_PATH`.

#### SplitFS
Our benchmarks use [`SplitFS`](https://github.com/utsaslab/SplitFS/) with the suggested kernel version `4.13`.  
Please see the build and install instructions in `SplitFS`'s repository.  
Paths to the built libraries has to be set our `config.sh`.

### Applications

#### Git
Our benchmarks use `git` version `2.28.0`. Due to some libc functions getting inlined, git has to be custom compiled.  
Therefore lines `1177` and `1178` of `Makefile` have to be modified with `no-inline` flags:  
```Makefile
CFLAGS = -g -O2 -Wall -fno-inline -fno-inline-small-functions
LDFLAGS = -fno-inline-small-functions -fno-inline
```

`GIT_BIN_PATH` in `config.sh` needs to be set accordingly (e.g. `../git-master/git`).

#### Filebench
[Filebench version `1.5-alpha3`](https://github.com/filebench/filebench/tree/1.5-alpha3) needs to be installed. 

#### Tar
`tar` version `1.3` is used by our benchmarks.

#### YCSB
We used the `YCSB` benchmark and workload generator supplied with SplitFS. The source code is available in the `SplitFS` repository. Their run script has to be modified to preload `libsimurgh.so`.


### Data
The `git`, `tar` and `recovery` benchmarks use the Linux source code files.  
Our runs use the `linux-5.6.14` source code.
The `config.sh` needs to be configured with the correct paths.  
`LINUX_DATA_UNPACKED` needs to point to the directory containing the source code.  
`LINUX_DATA_PACKED` points to a packed tar file containing the source code. 
`LINUX_DATA_PACKED_AND_UNPACKED`, should point to a directory similar to `LINUX_DATA_UNPACKED`, that contains also a copy of the packed tar file.


### System
We ran the benchmarks on a single socket server equipped with a 10 cores Xeon Gold 5212 processor running at 2.5GHz, 192 GB DRAM and 746 GB Optane DC persistent memory across 6 DIMMs.
The benchmarks require at least 64GB DRAM and 256GB NVMM.
To clear caches, mount or unmount file systems, provided scripts have to be run with root privilege.

## Running Benchmarks

To run the benchmark scripts inside the repository, an argument specifying the target file system (`SIMURGH`, `NOVA`, `EXT4DAX`, `PMFS`, `SPLITFS`) has to be passed.  
Example:
```bash
./run_microbenchmarks.sh SIMURGH
```

In the first step, the correct kernels have to be prepared and booted.  
Outputs will be generated in the `src` directory of the corresponding benchmark or printed on the standard output.
For some benchmarks, no running script is provided. In this case, the detail section below contains easy to follow steps.

### Benchmark details

Between different measurements, file system caches are cleared. In case of independent iterations, file systems are formatted between runs.
The provided scripts will take care of that. If run manually (e.g. for `tar` or `YCSB` measurements), clearing caches can be done by
```
sync; echo 3 > /proc/sys/vm/drop_caches;
```

#### Microbenchmarks
The microbenchmarks presented in the paper are executed after each other. For default, each benchmark is performed 20 times with different thread counts (up to 10). Iteration times and thread counts can be adjusted in `src/microbenchmarks/micro_benchmark_runner.py` with the fields `measurements_per_result` and `worker_amounts`.

Use `./run_microbenchmarks.sh [file system]` to perform. 

#### Git
Within this benchmark, the full source code of Linux kernel together with a tar packed copy of the source code is copied into an empty git repository, that is created inside the target file system. We measure git `add`, `commit` and `reset` times.

Use `./run_git.sh [file system]` to perform. 

#### Filebench
We used `varmail`, `webserver`, `webproxy`, and `fileserver` workloads. The default configuration for all workloads was used and only the directory for creating the files was modified.

Use `./run_filebench.sh [file system]` to perform. 

#### Recovery times
For this benchmark, we copied the full source code of Linux kernel into our file system.

Within the benchmark, a full recovery procedure is performed. The Simurgh library includes a dedicated entry point for this. The recovery split in two parts: scanning and repairing the persistent data, and rebuilding the shared memory data structures. The time reported in the paper consists of the sum of those two parts.

Use `./run_recovery.sh SIMURGH` to perform. 

#### Tar
To measure the performance of file systems on Tar, We copied the full source code of Linux kernel into the file system. Then, the buffer cache of the OS is flushed and cleared. Next, we used the following command to create the tar file and measured the execution time.

```bash
tar cf linux.tar linux-5.1.0
```

Next, we removed the source directory, and flushed the cache and used the following command to extract files.

```bash
tar xf linux.tar
```

Before executing the commands above, the used file system has to preloaded or mounted. Scripts in `src/bash` can be used for that.


#### YCSB
To achieve a fair comparison, we used the same source code and workflow proposed by SplitFS to run YCSB. The details of running the benchmark and obtaining the results can be found in [this](https://github.com/utsaslab/SplitFS/blob/master/experiments.md) link.

For the execution time breakdown, we ran the YCSB script with the following prefix command. 

```bash
perf record -F 9999 --call-graph dwarf [command]
```

Next, we used `perf report` to read the output and extract numbers.

## Gem5 benchmark

The benchmarks and the pipeline analysis were conducted using gem5 version `20.0.0.2`. The `src/gem5/fs.py` script is used to boot a Gentoo RootFS on top of the provided kernel images. The kernel images inside the `gem5_kernel` directory were modified to include the PTEditor module. A dummy syscall was added to the kernel which executes no code, to allow measuring the overhead of the linux system call mechanism. The DerivO3CPU CPU type with caches and L2 caches enabled was specified to be used with the `fs.py` script to boot gem5.

### Building gem5

The steps to measure the performance of the proposed instructions, measuring the overhead of an empty syscall and the standard function call are listed below. 


1. Compile the modified `gem5` version. See the [gem5 documentation](https://www.gem5.org/documentation/general_docs/building) for more information. On Ubuntu you can install all the required packages using the below command:

```
sudo apt install build-essential git m4 scons zlib1g zlib1g-dev libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev python-dev python
```
2. Build our `gem5` code. The command below in gem5 directory creates an opt file which is an optimized binary with debug symbols.
```
scons -D PYTHON_CONFIG=PYTHON_CONFIG_PATH build/X86/gem5.opt -j [NUM_PROCESSORS]
```
3. To start the Linux system you need to provide a Linux disk image. A disk image can be either [built](https://www.gem5.org/project/2020/03/09/boot-tests.html) or [downloaded](http://www.cs.utexas.edu/~parsec_m5/x86root-parsec.img.bz2).


### Testing the instruction

We ran the benchmarks on gem5 full system mode (FS-mode).
FS-Mode simulates a complete environment for running an operating system including support for interrupts, exceptions, privilege levels etc. Depending on the ISA,
it is possible to boot a complete Linux operating system inside gem5. 

The benchmarks measures the cycle count required for the `jmpp`/`pret`, `SYSCALL_64`/`SYSRET_TO_64` instructions and a complete Linux system call from user space. All measurement are divided into related execution blocks, to show the cycle count required for each relevant part of an instruction. The `m5_reset_stats` and `m5_dump_stats` pseudo instructions allow measuring the cycle count. To achieve minimal measurement overhead, the parameters required to be passed to these instructions in the `rdi` and `rsi` registers were hardcoded. That way, a single macro-op is enough to reset or dump the statistics. Each measurement was performed 100 times to account for caching or speculative execution effects.

The benchmarks need to be compiled using the m5 utilities to be able to run using the gem5 simulator. The folder `src/gem5` contains the tests to measure the overhead of the new instructions and also an empty system call on the modified gem5. The file `src/gem5/test_code_measure_stats.c` performs 100 iterations of the `jmpp` and `pret` instructions. To compile it for a Linux target machine run:
```
gcc -o test_instruction src/gem5/benchmarks/test_code_measure_stats.c -I src/gem5/benchmarks/include/ gem5/util/m5/src/x86/m5op.S
```
Run the compiled tests from within the `gem5` directory:
```
build/X86/gem5.opt ../src/gem5/fs.py --disk-image=[DISK_IMAGE_PATH] --kernel=[KERNEL_IMAGE_PATH] --script=test_instruction
```
After the simulator has loaded you can run the below command inside the gem5 shell
```
m5 readfile > /tmp/test_instruction && chmod +x /tmp/test_instruction && /tmp/test_instruction
```
To measure the overhead of an empty syscall you can run the `syscall_dummy` benchmark in the `gem5_config` folder according to the above instructions. 


