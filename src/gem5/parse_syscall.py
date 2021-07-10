#!/usr/bin/python3

import os
import argparse
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

SIM_START_KEYWORDS = ["Begin", "Simulation", "Statistics"]
SIM_END_KEYWORDS = ["End", "Simulation", "Statistics"]

class Statistic(object):
    """
    One single statistic.
    """
    def __init__(self, name, value, description):
        self.name = name
        self.value = value
        self.description = description

    @classmethod
    def from_line(cls, line):
        """
        Create and return a statistics object from a raw line.
        """
        components = line.split(maxsplit=2)
        if len(components) != 3:
            return None

        name = components[0].strip()
        value = float(components[1])
        description = components[2][1:].strip()
        return cls(name, value, description)


    def __str__(self):
        return f"{self.name}\t{self.value}\t{self.description}"

class Simulation(object):
    """
    A simulation instance.
    """
    def __init__(self):
        self.statistics = {}

    def add_statistic(self, stat):
        self.statistics[stat.name] = stat

    def remove_statistic(self, stat):
        del self.statistics[stat.name]

    def get_statistic(self, name):
        return self.statistics[name]

    def __getitem__(self, key):
        return self.statistics.get(key)

    def __setitem__(self, key, value):
        self.statistics[key] = value

def parse_args():
    """
    Setup the command line arguments.
    return: the parsed arguments
    """
    def str2bool(v):
        if isinstance(v, bool):
           return v
        if v.lower() in ("yes", "true", "t", "y", "1"):
            return True
        elif v.lower() in ("no", "false", "f", "n", "0"):
            return False
        raise argparse.ArgumentTypeError("Boolean value expected.")

    parser = argparse.ArgumentParser()
    parser.add_argument(dest="files", type=str, help="Path to the gem5 statistics file.", nargs='+')
    parser.add_argument("--title", type=str, help="Figure title.")
    parser.add_argument("--plot", type=str2bool, nargs='?', const=True, default=False,
                        help="Show a bar plot with the different values.")
    parser.add_argument("--skip_first", type=str2bool, nargs='?', const=True, default=False,
                        help="Skip the first data point.")
    parser.add_argument("--skip_last", type=str2bool, nargs='?', const=True, default=False,
                        help="Skip the last data point.")
    parser.add_argument("--clean_name", type=str2bool, nargs='?', const=True, default=False,
                        help="Try to cleanup the name by replacing _ with spaces.")
    return parser.parse_args()

def parse_statistics(path):
    """
    """
    def is_sim_begin(line):
        """
        param line: the line to check
        return: True if this line is the "Begin Simulation" line. False otherwise.
        """
        return all([k in line.split() for k in SIM_START_KEYWORDS])

    def is_sim_end(line):
        """
        param line: the line to check
        return: True if this line is the "End Simulation" line. False otherwise.
        """
        return all([k in line.split() for k in SIM_END_KEYWORDS])

    # Parse the statistics file
    try:
        simulations = []
        cur_sim = None
        with open(path) as f:
            for line in f.readlines():
                if line.strip() == "":
                    continue
                elif is_sim_begin(line):
                    cur_sim = Simulation()
                elif is_sim_end(line):
                    simulations.append(cur_sim)
                elif stat := Statistic.from_line(line):
                    cur_sim.add_statistic(stat)
                else:
                    print(f"Could not parse line: {line}")
        return simulations

    except FileNotFoundError:
        print(f"Could not open file {path}")


def get_syscall_stat(simulations, statistic, cpu="switch_cpus", skip_last=True, num_iter=100, num_dumps=6):
    """
    Read the number of cycles only for the specified cpu.
    param cpu: the cpu type to use ("cpu", "switch_cpu")
    param num_iter: the number
    return: average cycle number.
    """
    stats = []
    start_idx = len(simulations)-num_iter * num_dumps - int(skip_last)
    simulations = simulations[start_idx:len(simulations) - int(skip_last)]

    # Group all values in num_dumps tuple and calculate the difference
    # between each pair.
    group = []
    last_value = 0
    for i, sim in enumerate(simulations, 1):
        if stat_obj := sim[f"system.{cpu}.{statistic}"]:
            #print(f"Simulation {i}: {stat_obj}")
            group += [stat_obj.value-last_value]
            last_value = stat_obj.value

            if len(group) == num_dumps:
                stats.append(group)

                group = []
                last_value = 0

    return stats


def main_syscall_result():
    args = parse_args()
    files = args.files

    # Read the data of all files into a dictionary
    data = {}
    for file in files:
        # All dumps are placed inside `entry_SYSCALL_64`.
        # Since we calculate the delta between each steps the labels should be:
        labels = ["syscall wrapper", "swapgs", "SWITCH_TO_KERNEL_CR3", "Construct pt_regs", "do_syscall_64",
                  "find return path", "syscall_return_via_sysret", "USERGS_SYSRET64"]

        simulations = parse_statistics(file)
        stats = get_syscall_stat(simulations, statistic="numCycles", cpu="switch_cpus",
                                 skip_last=True, num_iter=100, num_dumps=len(labels))

        # Additionally we caluclate the time for "SYSCALL_64" and "SYSRET_TO_64"
        # We needs these values to reason about the kernel time as well
        values = zip(*stats)
        data = dict(zip(labels, values))

        # Convert the data into a pandas dataframe
        df = pd.DataFrame(data)

        print(df.describe(percentiles=[0.5, 0.95]).to_string())

        # Plot the data
        if args.plot:
            sns.set_style("darkgrid")
            swarm = sns.swarmplot(data=df)

            # draw the medians
            ax = swarm.axes
            ax.set_ylabel("Cycle Count")
            ax.set_xlabel("Section")

            # add a second ax to the right side
            medians = list(df.median().unique())

            median_ax = ax.twinx()
            median_ax.set_ylabel("Median")
            median_ax.set_ylim(ax.get_ylim())
            median_ax.set_yticks(medians)
            median_ax.set_zorder(-1)

            for mid in medians:
                swarm.axhline(mid, ls="--", linewidth=1)

            plt.title(args.title)
            plt.show()


main_syscall_result()
