import os
import json
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from datetime import datetime
import pprint

# Final settings
worker_indexes_for_barplots = [0, 1, 2, 3, 4, 5]
file_indexes_indexes_for_bar_lineplots = [0]
box_linewidth = 0

markersize = 6
linewidth = 2
edgecolor = "white"
matplotlib.rcParams['hatch.linewidth'] = 0.5

colors = {
    "SIMURGH": "#2271B2",
    "NOVA": "#CD022D",
    "PMFS": "#359B73",
    "EXT4DAX": "#D55E00",
    "SPLITFS": "#FFC33B",
}
hatches = {
    "SIMURGH": "oo",
    "SPLITFS": "///",
    "NOVA": "...",
    "EXT4DAX": "xxx",
    "PMFS": "\\\\\\",
}

# Final settings 
run_descriptions = [
    {
        "directory": "output_microbenchmarks_SIMURGH",
        "title": "Simurgh",
        "bar_plot_hatch": '/',
        "bar_plot_color": "red",
        "line_plot_style": '-',
        "line_plot_marker": 'o',
        "line_plot_color": colors["SIMURGH"]
    },
    {
        "directory": "output_microbenchmarks_NOVA",
        "title": "NOVA",
        "bar_plot_hatch": '\\',
        "bar_plot_color": "blue",
        "line_plot_style": '-',
        "line_plot_marker": 'v',
        "line_plot_color": colors["NOVA"] 
    },
    {
        "directory": "output_microbenchmarks_PMFS",
        "title": "PMFS",
        "bar_plot_hatch": 'x',
        "bar_plot_color": "orange",
        "line_plot_style": '-',
        "line_plot_marker": 'D',
        "line_plot_color": colors["PMFS"]
    },
    {
        "directory": "output_microbenchmarks_EXT4DAX",
        "title": "EXT4-DAX",
        "bar_plot_hatch": 'o',
        "bar_plot_color": "green",
        "line_plot_style": '-',
        "line_plot_marker": 'x',
        "line_plot_color": colors["EXT4DAX"]
    },
     {
         "directory": "output_microbenchmarks_SPLITFS",
         "title": "SplitFS",
         "bar_plot_hatch": 'x',
         "bar_plot_color": "black",
         "line_plot_style": '-',
         "line_plot_marker": '^',
         "line_plot_color": colors["SPLITFS"]
     },

]

# Final settings
benchmark_descriptions = [
    # {
    #     "source_title": "create_close_unlink_file_in_private_dir_MT",
    # },
    # {
    #     "source_title": "create_close_unlink_file_in_private_dir_MP",
    # },
    # {
    #     "source_title": "create_close_unlink_file_in_shared_dir_MP",
    # },
    {
        "source_title": "create_file_in_private_dir_MT",
    },
    # {
    #     "source_title": "create_file_in_private_dir_MP",
    # },
    {
        "source_title": "create_file_in_shared_dir_MT",
    },
    # {
    #     "source_title": "create_file_in_shared_dir_MP",
    # },
    {
        "source_title": "unlink_file_in_private_dir_MT",
    },
    # {
    #     "source_title": "unlink_file_in_private_dir_MP",
    # },
    # {
    #     "source_title": "unlink_file_in_shared_dir_MT",
    # },
    # {
    #     "source_title": "unlink_file_in_shared_dir_MP",
    # },
    # {
    #     "source_title": "open_private_file_in_shared_dir_depth5_MT",
    # },
    # {
    #     "source_title": "open_private_file_in_shared_dir_depth5_MP",
    # },
    # {
    #     "source_title": "open_private_file_in_private_dir_depth5_MT",
    # },
    {
        "source_title": "open_private_file_in_private_dir_depth5_MP",
    },
    # {
    #     "source_title": "open_single_file_depth5_MT",
    # },
    {
        "source_title": "open_single_file_depth5_MP",
    },
    # {
    #     "source_title": "fallocate_private_files_4K_MT",
    # },
    # {
    #     "source_title": "fallocate_private_files_4K_MP",
    # },
    {
        "source_title": "fallocate_private_files_4M_MT",
    },
    # {
    #     "source_title": "fallocate_private_files_4M_MP",
    # },
    {
        "source_title": "append_4K_blocks_to_private_file_MT",
        "legend_loc": "lower right"
    },
    # {
    #     "source_title": "open_and_append_4K_block_to_distinct_file",
    # },
    {
        "source_title": "rename_private_file_in_shared_directory_MT",
    },
    # {
    #     "source_title": "rename_private_file_in_shared_directory_MP",
    # },
    # {
    #     "source_title": "rename_private_dir_with_one_file_in_shared_directory_MT",
    # },
    # {
    #     "source_title": "rename_private_dir_with_one_file_in_shared_directory_MP",
    # },
    # {
    #     "source_title": "create_dir_in_shared_dir_MT",
    # },
    # {
    #     "source_title": "create_dir_in_shared_dir_MP",
    # },
    # {
    #     "source_title": "create_dir_in_private_dir_MT",
    # },
    # {
    #     "source_title": "create_dir_in_private_dir_MP",
    # },
    # {
    #     "source_title": "read_private_2M_block_in_private_file_MT",
    #     "additional_bandwith_plot": True,
    #     "op_size": 2097152
    # },
    {
        "source_title": "read_private_4K_block_in_private_file_MT",
        "additional_bandwith_plot": True,
        "op_size": 4096
    },
    # {
    #     "source_title": "overwrite_private_4K_block_in_private_file_MT",
    #     "additional_bandwith_plot": True,
    #     "op_size": 4096
    # },
    # {
    #     "source_title": "overwrite_private_2M_block_in_shared_file_MT",
    #     "additional_bandwith_plot": True,
    #     "op_size": 2097152
    # },
    # {
    #     "source_title": "overwrite_private_2M_block_in_shared_file_MP",
    #     "additional_bandwith_plot": True,
    #     "op_size": 2097152
    # },
    {
        "source_title": "read_private_4K_block_in_shared_file_MT",
        "additional_bandwith_plot": True,
        "op_size": 4096
    },
    # {
    #     "source_title": "read_private_4K_block_in_shared_file_MP",
    #     "additional_bandwith_plot": True,
    #     "op_size": 4096
    # },
    {
        "source_title": "read_private_2M_block_in_shared_file_MT",
        "additional_bandwith_plot": True,
        "op_size": 2097152
    },
    # {
    #     "source_title": "read_private_2M_block_in_shared_file_MP",
    #     "additional_bandwith_plot": True,
    #     "op_size": 2097152
    # },
    {
        "source_title": "overwrite_private_4K_block_in_shared_file_MT",
        "additional_bandwith_plot": True,
        "op_size": 4096
    },
    # {
    #     "source_title": "overwrite_private_4K_block_in_shared_file_MP",
    #     "additional_bandwith_plot": True,
    #     "op_size": 4096
    # },
    # {
    #     "source_title": "overwrite_private_4k_files_MP",
    #     "additional_bandwith_plot": True,
    #     "op_size": 4096
    # },
    #     {
    #     "source_title": "overwrite_private_4k_files_MT",
    #     "additional_bandwith_plot": True,
    #     "op_size": 4096
    # },
    #     {
    #     "source_title": "read_private_4k_files_MP",
    #     "additional_bandwith_plot": True,
    #     "op_size": 4096
    # },
    #     {
    #     "source_title": "read_private_4k_files_MT",
    #     "additional_bandwith_plot": True,
    #     "op_size": 4096
    # },
    # {
    #     "source_title": "write_large_file_512M_per_op_MT",
    #     "additional_bandwith_plot": True,
    #     "op_size": 536870912*200
    # },

]

# Test settings
worker_indexes_for_barplots = range(11)
run_descriptions = [
    {
        "directory": "output_microbenchmarks_SIMURGH_20210325_15-05-36",
        "title": "Simurgh",
        "bar_plot_hatch": '/',
        "bar_plot_color": "red",
        "line_plot_style": '-',
        "line_plot_marker": 'o',
        "line_plot_color": colors["SIMURGH"]
    },
    {
        "directory": "output_microbenchmarks_NOVA_20210325_16-06-21",
        "title": "NOVA",
        "bar_plot_hatch": '\\',
        "bar_plot_color": "blue",
        "line_plot_style": '-',
        "line_plot_marker": 'v',
        "line_plot_color": colors["NOVA"] 
    },
]
benchmark_descriptions = [
    {"source_title": "create_file_in_private_dir_MT"},
    {"source_title": "create_file_in_shared_dir_MT"},
    {"source_title": "create_file_in_private_dir_MP"},
    {"source_title": "create_file_in_shared_dir_MP"},
    {"source_title": "create_file_in_private_dir_10x_MT"},
    {"source_title": "create_file_in_shared_dir_10x_MT"},
    {"source_title": "create_file_in_private_dir_10x_MP"},
    {"source_title": "create_file_in_shared_dir_10x_MP"},
]

now = datetime.now()
date = now.strftime("%Y%m%d_%H-%M-%S")
output_dir = "output_merged_" + date
os.mkdir(output_dir)
def plot_save_show(plot, title, zero_pad_inches=True):
    if zero_pad_inches is True:
        plot.savefig(output_dir+"/"+title+".pdf", dpi=300, bbox_inches='tight', pad_inches=0)
    else:
        plot.savefig(output_dir+"/"+title+".pdf", dpi=300, bbox_inches='tight')
    print()
    #plt.show()

def load_single_result (directory, source_title):
    found = False
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            if filename.startswith(source_title):
                json_file_name = filename
                found = True
                break

    if not found:
        return None

    if json_file_name is None:
        print("Error: " + source_title + " in " + directory + " not found!")

    with open(directory + "/" + json_file_name) as json_file:
        return json.load(json_file)


def to_mega_ops (time_complete_ms, n_ops):
    if time_complete_ms == 0:
        time_complete_ms = 10000
    return (n_ops/time_complete_ms)/1000

def to_gbps (time_complete_ms, n_ops, op_size):
    if time_complete_ms == 0:
        return 0
    return ((float(op_size)/1000000000.0)*n_ops)/(time_complete_ms/1000.0)

def autolabel(rects, ax):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{:.2f}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 1),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

def customlabel(rects, ax, values, format_string, append_string, x_off=0, y_off=0):
        i = 0
        for rect in rects:
            height = rect.get_height()
            ax.annotate(format_string.format(values[i]) + append_string,
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0+x_off, 1+y_off),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)
            
            i += 1
    

### Main

# Read data
benchmarks = []
for benchmark_description in benchmark_descriptions:
    benchmark = {
        "benchmark_description": benchmark_description,
        "runs":[]
    }

    for run_description in run_descriptions:
        run = {
            "run_description": run_description,
            "result": load_single_result(run_description["directory"], benchmark_description["source_title"])
        }
        benchmark["runs"].append(run)

    benchmarks.append(benchmark)


# Create plots

for benchmark in benchmarks:
    print(benchmark)
    valid_runs_amount = 0
    for i in range(0, len(benchmark["runs"])):
        if benchmark["runs"][i]["result"] is not None:
            valid_runs_amount = valid_runs_amount + 1

    # Bar plot
    
    # worker_indexes = worker_indexes_for_barplots
    # worker_amounts = len(worker_indexes)

    # file_indexes = file_indexes_indexes_for_bar_lineplots
    
    # pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(benchmark)
    # print("")

    # labels = [] # X Axis Label: Operation Amount
    # for f in range(0, len(file_indexes)):
    #     labels.append(benchmark["runs"][0]["result"]["ops_amounts"][file_indexes[f]])

    # fig, axs = plt.subplots(1, worker_amounts, sharex='col', sharey='row', gridspec_kw={'wspace': 0.05})
    # rect_series = []
    # x_label_pos = np.arange(len(labels))
    # width = 0.25

    # #fig.suptitle(benchmark["benchmark_description"]["source_title"])
    # fig.text(0.5, 0.02, '# of operations', ha='center')
    # fig.text(0.02, 0.5, 'Throughput [Mops/s]', va='center', rotation='vertical')

    # for t in range(0, worker_amounts):
    #     if worker_amounts is 1:
    #         t_axs = axs
    #     else:
    #         t_axs = axs[t]

    #     label_pos_index_t = 0
    #     for i in range(0, len(benchmark["runs"])):
    #         if benchmark["runs"][i]["result"] is None:
    #             continue
    #         values = []
    #         real_file_indexes = file_indexes
    #         if "custom_file_indexes_for_bar_lineplots" in benchmark["runs"][i]["run_description"]:
    #             real_file_indexes = benchmark["runs"][i]["run_description"]["custom_file_indexes_for_bar_lineplots"]

    #         for f in range(0, len(real_file_indexes)):
    #             values.append(to_mega_ops(
    #                 benchmark["runs"][i]["result"]["results"][worker_indexes[t]][real_file_indexes[f]], 
    #                 benchmark["runs"][i]["result"]["ops_amounts"][real_file_indexes[f]]
    #                 ))
    #         barlist = t_axs.bar(
    #             x_label_pos + (-valid_runs_amount/2+label_pos_index_t)*width, 
    #             values, 
    #             width, 
    #             label=(benchmark["runs"][i]["run_description"]["title"]),
    #             hatch=(benchmark["runs"][i]["run_description"]["bar_plot_hatch"]),
    #             color=(benchmark["runs"][i]["run_description"]["bar_plot_color"]),
    #             edgecolor=edgecolor, linewidth=box_linewidth
    #             )
    #         label_pos_index_t = label_pos_index_t + 1
        
    #     t_axs.set_title("workers: " + str(benchmark["runs"][i]["result"]["worker_amounts"][worker_indexes[t]]), fontsize=10)
    #     t_axs.set_xticks(x_label_pos)
    #     t_axs.set_xticklabels(labels)
    
    # plt.legend(prop={'size': 9}, )

    # if save_plots:
    #     fig.set_size_inches(6, 4)
    #     plot_save_show(plt, benchmark["benchmark_description"]["source_title"]+"_merged_barplot")


    # Line plot

    def do_line_plot(type):
        
        worker_indexes = worker_indexes_for_barplots
        worker_amounts = len(worker_indexes)

        file_indexes = file_indexes_indexes_for_bar_lineplots
        file_indexes_amounts = len(file_indexes)

        labels = []
        #for ops_amount in benchmark["runs"][0]["result"]["worker_amounts"]:
            #labels.append(ops_amount)
        for w in range(0, worker_amounts):
            labels.append(benchmark["runs"][0]["result"]["worker_amounts"][worker_indexes[w]])
        x_label_pos = np.arange(len(labels))

        fig, axs = plt.subplots(1, file_indexes_amounts, sharex='col', sharey='row', gridspec_kw={'wspace': 0.05})

        #fig.suptitle(benchmark["benchmark_description"]["source_title"])
        fig.text(0.5, -0.04, '# of workers', ha='center')
        if type == "absolute":
            fig.text(0, 0.5, 'Throughput [Mops/s]', va='center', rotation='vertical')
        if type == "relative":
            fig.text(0, 0.5, 'Scalability factor', va='center', rotation='vertical')
        if type == "bandwidth":
            fig.text(0, 0.5, 'Bandwidth [Gb/s]', va='center', rotation='vertical')

        for f in range(0, file_indexes_amounts):
            if file_indexes_amounts is 1:
                t_axs = axs
            else:
                t_axs = axs[f]



            for i in range(0, len(benchmark["runs"])):
                if benchmark["runs"][i]["result"] is None:
                    continue

                real_file_indexes = file_indexes
                if "custom_file_indexes_for_bar_lineplots" in benchmark["runs"][i]["run_description"]:
                    real_file_indexes = benchmark["runs"][i]["run_description"]["custom_file_indexes_for_bar_lineplots"]

                def correct_time (time_complete_ms, n_ops, worker_amount):
                    overhead_ms = 0.0000184 # 46 cycles * 0.4 ns
                    return time_complete_ms + overhead_ms * n_ops / worker_amount

                scalability_values = []
                #for w in range(0, len(benchmark["runs"][0]["result"]["worker_amounts"])):
                for w in range(0, worker_amounts):    
                    time = benchmark["runs"][i]["result"]["results"][worker_indexes[w]][real_file_indexes[f]]
                    ops_amount = benchmark["runs"][i]["result"]["ops_amounts"][real_file_indexes[f]]
                    worker_amount = benchmark["runs"][i]["result"]["worker_amounts"][worker_indexes[w]]
                    
                    if benchmark["runs"][i]["run_description"]["title"] == "Simurgh":
                        time = correct_time(time, ops_amount, worker_amount)

                    if type == "absolute":
                        scalability_values.append(to_mega_ops(
                            time,
                            ops_amount
                            ))
                    if type == "relative":
                        if time == 0:
                            time = 10000
                        scalability_values.append(benchmark["runs"][i]["result"]["results"][0][real_file_indexes[f]] / time)
                    if type == "bandwidth":
                        scalability_values.append(to_gbps(
                            time,
                            ops_amount,
                            benchmark["benchmark_description"]["op_size"]
                            ))

                t_axs.plot(
                    scalability_values, 
                    label=(benchmark["runs"][i]["run_description"]["title"]),
                    linestyle=(benchmark["runs"][i]["run_description"]["line_plot_style"]),
                    marker=(benchmark["runs"][i]["run_description"]["line_plot_marker"]),
                    color=(benchmark["runs"][i]["run_description"]["line_plot_color"]),
                    markersize=markersize,
                    linewidth=linewidth
                    )

            #t_axs.set_title("# of operations: " + str(benchmark["runs"][0]["result"]["ops_amounts"][real_file_indexes[f]]), fontsize=10)
            #t_axs.set_title(benchmark["benchmark_description"]["source_title"], fontsize=10)
            
            t_axs.set_xticks(x_label_pos)
            t_axs.set_xticklabels(labels)
            #t_axs.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))

        loc = "best"
        if "legend_loc" in benchmark["benchmark_description"]:
            loc = benchmark["benchmark_description"]["legend_loc"]

        plt.legend(prop={'size': 8}, ncol=2, loc=loc)

        fig.set_size_inches(4, 2)
        if type == "absolute":
            plot_save_show(plt, benchmark["benchmark_description"]["source_title"]+"_merged_absolute", zero_pad_inches=False)
        if type == "relative":
            plot_save_show(plt, benchmark["benchmark_description"]["source_title"]+"_merged_scalability", zero_pad_inches=False)
        if type == "bandwidth":
            plot_save_show(plt, benchmark["benchmark_description"]["source_title"]+"_merged_bandwidth", zero_pad_inches=False)

    
    #do_line_plot("relative")
    if "additional_bandwith_plot" in benchmark["benchmark_description"]:
        do_line_plot("bandwidth")
    else:
        do_line_plot("absolute")


# # Create File History Plot (Single Thread, 5000 files)

# labels = ["PMFS k.", "PMFS k.\nlarge fn.", "PMFS u.s.\nw/o journal",  "Simurgh"]
# times_st = [round(200.0/1133, 3), round(1133.0/1133, 3),           round(130.0/1133, 3),                      round(22.0/1133, 3)]

# fig, axs = plt.subplots()

# x_pos = [i for i, _ in enumerate(labels)]

# width = 0.4

# rect = plt.bar(x_pos, times_st, edgecolor=edgecolor, linewidth=box_linewidth, color="gainsboro")

# axes = plt.gca()
# axes.set_ylim([0,1.1])

# plt.xticks(x_pos, labels)

# autolabel(rect, axs)

# fig.set_size_inches(4, 2.3)
# plt.savefig(output_dir+"/history_create_file"+date+".pdf", dpi=300, bbox_inches='tight')

def to_mops(arr):
    for i in range(0, len(arr)):
        arr[i] = arr[i] /1000000

def normalize(arr, norm_arr):
    for i in range(0, len(norm_arr)):
        arr[i] = arr[i]/norm_arr[i]
        
# LevelDB Plots

# labels = ["fileserver", "varmail", "webproxy", "webserver"] # removed fileserver for now. We will fix issues for it beeing slow.
# results_NOVA = [481770, 828886, 996040, 1.34926e+06]
# results_PMFS = []
# results_SIMURGH = [406309, 1.40966e+06, 1.11623e+06, 1.36814e+06]
labels = ["LoadA", "RunA", "RunB", "RunC", "RunD", "LoadE", "RunE", "RunF"]
#results_SIMURGH = [21.790, 94.727, 146.652, 193.949, 205.031, 34.560, 18.216, 116.230]
results_SIMURGH = [30.953, 79.226, 152.522, 190.147, 222.524, 31.139, 17.934, 96.594]
results_NOVA_5 = [17.198, 41.380, 122.349, 156.342, 196.350, 17.137, 15.085, 60.544]
results_NOVA_4 = [11.300, 28.051, 110.360, 131.645, 131.645, 11.287, 12.316, 53.169]
results_PMFS = [21.791, 53.516, 132.266, 160.104, 184.842, 21.675, 14.723, 82.975]
results_PMFS_4 = [18.196, 44.760, 115.384, 135.462, 165.148, 18.211, 12.493, 83.092]
results_EXDAXT = [13.019, 30.269, 120.662, 154.879, 180.496, 12.865, 15.595, 60.680]
results_EXDAXT_4 = [11.637, 30.784, 122.438, 151.060, 169.096, 11.717, 13.152, 57.821]
results_SPLITFS = [28.109, 58.083, 130.254, 175.604, 187.890, 28.131, 15.509, 78.392]

results_SIMURGH_for_labels = [30.953, 79.226, 152.522, 190.147, 222.524, 31.139, 17.934, 96.594]

normalize(results_SIMURGH, results_SPLITFS)
normalize(results_NOVA_5, results_SPLITFS)
normalize(results_NOVA_4, results_SPLITFS)
normalize(results_PMFS, results_SPLITFS)
normalize(results_PMFS_4, results_SPLITFS)
normalize(results_EXDAXT, results_SPLITFS)
normalize(results_EXDAXT_4, results_SPLITFS)
normalize(results_SPLITFS, results_SPLITFS)
# to_mops(results_NOVA)
# to_mops(results_PMFS)
# to_mops(results_EXDAXT)
# to_mops(results_SIMURGH)
#to_mops(results_SPLITFS)

# fig, axs = plt.subplots(1, 3, sharex='col', sharey='row', gridspec_kw={'wspace': 0.00})

# fig.text(0.5, 0.00, 'Threads', ha='center')
# fig.text(0.01, 0.5, 'Avg. system calls number per op.', va='center', rotation='vertical')

fig, axs = plt.subplots()

x_label_pos = np.arange(len(labels))

width = 1/6

rects = plt.bar(x_label_pos-3*width, results_SIMURGH, width, label="Simurgh", hatch=hatches["SIMURGH"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["SIMURGH"])
plt.bar(x_label_pos-2*width, results_NOVA_5, width, label="NOVA", hatch=hatches["NOVA"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["NOVA"])
#plt.bar(x_label_pos-3*width, results_NOVA_4, width, label="NOVA-4", hatch="\\", edgecolor=edgecolor, linewidth=box_linewidth, color="green")
plt.bar(x_label_pos-1*width, results_PMFS, width, label="PMFS", hatch=hatches["PMFS"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["PMFS"])
#plt.bar(x_label_pos-width, results_PMFS_4, width, label="PMFS-4", hatch="\\", edgecolor=edgecolor, linewidth=box_linewidth, color="red")
plt.bar(x_label_pos, results_EXDAXT, width, label="EXT4-DAX", hatch=hatches["EXT4DAX"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["EXT4DAX"])
#plt.bar(x_label_pos+width, results_EXDAXT_4, width, label="EXT4-DAX-4", hatch="o", edgecolor=edgecolor, linewidth=box_linewidth, color="orange")
#plt.bar(x_label_pos+1.5*width, results_SPLITFS, width, label="SplitFS", hatch="/", edgecolor=edgecolor, linewidth=box_linewidth, color="purple")
plt.bar(x_label_pos+1*width, results_SPLITFS, width, label="SplitFS", hatch=hatches["SPLITFS"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["SPLITFS"])

#     t_axs = axs[i]
#     t_axs.bar(r1, futex_numbers[i], width, label='futex', hatch="x", edgecolor=edgecolor, linewidth=box_linewidth, color="gainsboro")
#     t_axs.bar(r1, brk_numbers[i], width, bottom=futex_numbers[i], label='brk', hatch="/", edgecolor=edgecolor, linewidth=box_linewidth, color="silver")
#     t_axs.bar(r1, others_numbers[i], width, bottom=np.add(brk_numbers[i], futex_numbers[i]), label='others', hatch="o", edgecolor=edgecolor, linewidth=box_linewidth, color="gainsboro")
#     t_axs.set_xticks(r1)
#     t_axs.set_xticklabels(labels)
#     t_axs.set_title(titles[i], fontsize=10)

axs.set_xticks(x_label_pos)
axs.set_xticklabels(labels)
axs.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))

axs.set_ylabel('Throughput [normalized]')

plt.legend(prop={'size': 9},  loc='lower center', ncol=5)

fig.set_size_inches(13.5, 2)

plt.ylim(ymin = 0, ymax = 1.53)
customlabel(rects, axs, results_SIMURGH_for_labels, "{:.2f}", " Kops/s")

plot_save_show(plt, "leveldb")


# # Filebench Plots

# # labels = ["fileserver", "varmail", "webproxy", "webserver"] # removed fileserver for now. We will fix issues for it beeing slow.
# # results_NOVA = [481770, 828886, 996040, 1.34926e+06]
# # results_PMFS = []
# # results_SIMURGH = [406309, 1.40966e+06, 1.11623e+06, 1.36814e+06]
# labels = ["varmail", "webserver", "webproxy", "fileserver"]
# results_SIMURGH = [1.40966e+06, 1.36814e+06, 1.11623e+06, 479927]
# results_NOVA = [828886, 1.34926e+06, 996040, 481770]
# results_PMFS = [763191, 1.35431e+06, 303490, 383137]
# results_EXDAXT = [285702, 1.38821e+06, 791102, 345272]
# #results_SPLITFS = [3712, 0, 0, 0]

# def to_mops(arr):
#     for i in range(0, len(arr)):
#         arr[i] = arr[i] /1000000

# to_mops(results_NOVA)
# to_mops(results_PMFS)
# to_mops(results_EXDAXT)
# to_mops(results_SIMURGH)
# #to_mops(results_SPLITFS)

# fig, axs = plt.subplots()

# x_label_pos = np.arange(len(labels))

# width = 0.2

# plt.bar(x_label_pos-1.5*width, results_NOVA, width, label="NOVA", hatch="\\", edgecolor=edgecolor, linewidth=box_linewidth, color="blue")
# plt.bar(x_label_pos-width/2, results_PMFS, width, label="PMFS", hatch="x", edgecolor=edgecolor, linewidth=box_linewidth, color="orange")
# plt.bar(x_label_pos+width/2, results_EXDAXT, width, label="EXT4-DAX", hatch="o", edgecolor=edgecolor, linewidth=box_linewidth, color="green")
# #plt.bar(x_label_pos+1.5*width, results_SPLITFS, width, label="SplitFS", hatch="/", edgecolor=edgecolor, linewidth=box_linewidth, color="purple")
# plt.bar(x_label_pos+1.5*width, results_SIMURGH, width, label="Simurgh", hatch="/", edgecolor=edgecolor, linewidth=box_linewidth, color="red")


# axs.set_xticks(x_label_pos)
# axs.set_xticklabels(labels)
# axs.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))

# fig.text(0.02, 0.5, 'Throughput [Mops/s]', va='center', rotation='vertical')

# plt.legend(prop={'size': 9}, )

# fig.set_size_inches(6, 3)
# plot_save_show(plt, "filebench")

# def norm(x):
#     base = x[0]
#     for i in range(0, len(x)):
#         x[i] = x[i]/base

# for i in range(0, 3):
#     pmfs_throughput[0][i] = to_mega_ops(pmfs_throughput[0][i], 50000)
#     pmfs_throughput[1][i] = to_mega_ops(pmfs_throughput[1][i], 50000)
#     #pmfs_throughput[2][i] = to_mega_ops(pmfs_throughput[2][i], 100000)
#     nova_throughput[0][i] = to_mega_ops(nova_throughput[0][i], 50000)
#     nova_throughput[1][i] = to_mega_ops(nova_throughput[1][i], 50000)
#     #nova_throughput[2][i] = to_mega_ops(nova_throughput[2][i], 100000)
    

# # for x in range(0, 3):
# #     norm(pmfs_throughput[x])
# #     norm(nova_throughput[x])

# width = 0.4
# r1 = np.arange(len(pmfs_throughput[1]))

# fig, axs = plt.subplots(2, 2, sharex='col', gridspec_kw={'wspace': 0.45})

# fig.text(0.5, 0.00, 'Threads', ha='center')
# fig.text(0.01, 0.5, 'Throughput [Mops/s]', va='center', rotation='vertical')

# fig.text(0.94, 0.7, 'NOVA', ha='center')
# fig.text(0.94, 0.3, 'PMFS', ha='center')

# #plt.ylim(0, 1.1)


# for i in range(0, 2):
#     t_axs = axs[0][i]
#     #t_axs.bar(r1-width/2, pmfs_throughput[i], width, label='PMFS', hatch="x", edgecolor=edgecolor, linewidth=box_linewidth, color="gainsboro")
#     t_axs.bar(r1, nova_throughput[i], width, label='NOVA', hatch="/", edgecolor=edgecolor, linewidth=box_linewidth, color="silver")
#     t_axs.set_xticks(r1)
#     t_axs.set_xticklabels(labels)
#     t_axs.set_title(titles[i], fontsize=10)
#     #t_axs.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))


# for i in range(0, 2):
#     t_axs = axs[1][i]
#     t_axs.bar(r1, pmfs_throughput[i], width, label='PMFS', hatch="x", edgecolor=edgecolor, linewidth=box_linewidth, color="gainsboro")
#     #t_axs.bar(r1+width/2, nova_throughput[i], width, label='NOVA', hatch="/", edgecolor=edgecolor, linewidth=box_linewidth, color="silver")
#     t_axs.set_xticks(r1)
#     t_axs.set_xticklabels(labels)
#     #t_axs.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))

# fig.set_size_inches(6, 3)

# plot_save_show(plt, "throughput_scalability")


# # Application results plot: RocksDB

# labels = ["EXT4-DAX   ", "PMFS", "NOVA", "Simurgh"]
# results_SIMURGH = [1/28.9580011, 1/8.2511306, 1/10.2069825, 1/7.6526013]

# fig, axs = plt.subplots()

# x_label_pos = np.arange(len(labels))

# width = 0.6

# barlist = plt.bar(x_label_pos, results_SIMURGH, width, label="Simurgh", hatch="\\", edgecolor=edgecolor, linewidth=box_linewidth, color="whitesmoke")

# barlist[0].set_hatch('o')
# barlist[0].set_fc('green')

# barlist[1].set_hatch('x')
# barlist[1].set_fc('orange')

# barlist[2].set_hatch('\\')
# barlist[2].set_fc('blue')

# barlist[3].set_hatch('/')
# barlist[3].set_fc('red')

# #axs.set_title("dummy values")
# axs.set_xticks(x_label_pos)
# axs.set_xticklabels(labels)
# axs.set_ylabel('Throughput [Mops/s]')
# #axs.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))

# #plt.legend(prop={'size': 9}, )

# #plt.xticks(rotation=-20, ha="left")

# fig.set_size_inches(3, 3)
# plt.tight_layout()
# plot_save_show(plt, "app_rocksdb")


# # Application results plot: Exim

# labels = ["1 thread", "5 threads", "10 threads"]
# results_SIMURGH = [1281.10, 1281.10, 1281.10]
# results_NOVA = [1000, 1000, 1000]


# fig, axs = plt.subplots()

# x_label_pos = np.arange(len(labels))

# width = 0.3

# plt.bar(x_label_pos-0.5*width, results_NOVA, width, label="NOVA", hatch="/", edgecolor=edgecolor, linewidth=box_linewidth, color="gainsboro")
# plt.bar(x_label_pos+0.5*width, results_SIMURGH, width, label="Simurgh", hatch="\\", edgecolor=edgecolor, linewidth=box_linewidth, color="whitesmoke")

# axs.set_title("dummy values")
# axs.set_xticks(x_label_pos)
# axs.set_xticklabels(labels)
# axs.set_ylabel('Messages per core per sec')

# #plt.legend(prop={'size': 9}, )

# fig.set_size_inches(4, 3)
# plt.tight_layout()
# plot_save_show(plt, "app_exim")

# # Application results plot: Tar

# labels = ["EXT4-DAX   ", "PMFS", "NOVA", "Simurgh"]
# results_SIMURGH = [71779/0.99, 71779/0.96, 71779/0.92, 71779/0.71]

# to_mops(results_SIMURGH)

# fig, axs = plt.subplots()

# x_label_pos = np.arange(len(labels))

# width = 0.6

# barlist = plt.bar(x_label_pos, results_SIMURGH, width, label="Simurgh", hatch="\\", edgecolor=edgecolor, linewidth=box_linewidth, color="whitesmoke")

# barlist[0].set_hatch('o')
# barlist[0].set_fc('green')

# barlist[1].set_hatch('x')
# barlist[1].set_fc('orange')

# barlist[2].set_hatch('\\')
# barlist[2].set_fc('blue')

# barlist[3].set_hatch('/')
# barlist[3].set_fc('red')


# TAR plots

def normalize_tar(arr):
    for i in range(0, len(arr)):
        arr[i] = 71779/arr[i]/1000

labels = ["Pack", "Unpack"]

results_SIMURGH = [0.79, 1.20]
results_NOVA_5 = [1.066, 2.397]
# results_NOVA_4 = [11.300, 28.051, 110.360, 131.645, 131.645, 11.287, 12.316, 53.169]
results_PMFS = [0.931, 2.273]
# results_PMFS_4 = [18.196, 44.760, 115.384, 135.462, 165.148, 18.211, 12.493, 83.092]
results_EXDAXT = [1.337, 2.933]
results_SPLITFS = [1.40, 3.59]
# results_EXDAXT_4 = [11.637, 30.784, 122.438, 151.060, 169.096, 11.717, 13.152, 57.821]
# results_SPLITFS = [28.109, 58.083, 130.254, 175.604, 187.890, 28.131, 15.509, 96.411]

normalize_tar(results_SIMURGH)
normalize_tar(results_NOVA_5)
# normalize(results_NOVA_4, results_SPLITFS)
normalize_tar(results_PMFS)
# normalize(results_PMFS_4, results_SPLITFS)
normalize_tar(results_EXDAXT)
normalize_tar(results_SPLITFS)
# normalize(results_EXDAXT_4, results_SPLITFS)
# normalize(results_SPLITFS, results_SPLITFS)


fig, axs = plt.subplots()

x_label_pos = np.arange(len(labels))

width = 1.0/(5+1)

plt.bar(x_label_pos-2*width, results_SIMURGH, width, label="Simurgh", hatch=hatches["SIMURGH"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["SIMURGH"])
plt.bar(x_label_pos-width, results_NOVA_5, width, label="NOVA-5", hatch=hatches["NOVA"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["NOVA"])
# plt.bar(x_label_pos-3*width, results_NOVA_4, width, label="NOVA-4", hatch="\\", edgecolor=edgecolor, linewidth=box_linewidth, color="green")
plt.bar(x_label_pos, results_PMFS, width, label="PMFS", hatch=hatches["PMFS"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["PMFS"])
# plt.bar(x_label_pos-width, results_PMFS_4, width, label="PMFS-4", hatch="\\", edgecolor=edgecolor, linewidth=box_linewidth, color="red")
plt.bar(x_label_pos+width, results_EXDAXT, width, label="EXT4-DAX", hatch=hatches["EXT4DAX"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["EXT4DAX"])
# plt.bar(x_label_pos+width, results_EXDAXT_4, width, label="EXT4-DAX-4", hatch="o", edgecolor=edgecolor, linewidth=box_linewidth, color="orange")
plt.bar(x_label_pos+2*width, results_SPLITFS, width, label="SplitFS", hatch=hatches["SPLITFS"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["SPLITFS"])

# axs.set_title("dummy values")
axs.set_xticks(x_label_pos)
axs.set_xticklabels(labels)
axs.set_ylabel('Throughput [Kops/s]')

# #axs.set_title("dummy values")
# axs.set_xticks(x_label_pos)
# axs.set_xticklabels(labels)
# axs.set_ylabel('Throughout [MBytes/s]')
plt.legend(prop={'size': 9}, ncol=3)

fig.set_size_inches(6, 2)
# plt.tight_layout()
plot_save_show(plt, "app_tar")

# # Application results plot: Tar

# labels = ["EXT4-DAX   ", "PMFS", "NOVA", "Simurgh"]
# results_SIMURGH = [71779/0.99, 71779/0.96, 71779/0.92, 71779/0.71]

# to_mops(results_SIMURGH)

# fig, axs = plt.subplots()

# x_label_pos = np.arange(len(labels))

# width = 0.6

# barlist = plt.bar(x_label_pos, results_SIMURGH, width, label="Simurgh", hatch="\\", edgecolor=edgecolor, linewidth=box_linewidth, color="whitesmoke")

# barlist[0].set_hatch('o')
# barlist[0].set_fc('green')

# barlist[1].set_hatch('x')
# barlist[1].set_fc('orange')

# barlist[2].set_hatch('\\')
# barlist[2].set_fc('blue')

# barlist[3].set_hatch('/')
# barlist[3].set_fc('red')

# #axs.set_title("dummy values")
# axs.set_xticks(x_label_pos)
# axs.set_xticklabels(labels)
# axs.set_ylabel('Throughput [Mfiles/s]')

# #plt.legend(prop={'size': 9}, )

# fig.set_size_inches(3, 3)
# plt.tight_layout()
# plot_save_show(plt, "app_tar")

# Application results plot: Snappy 1 thread

def convert_snappy_to_throughput(in_array):
    for i in range(len(in_array)):
        if in_array[i] == 0:
            continue
        in_array[i] = 262144.0/in_array[i]

def convert_to_data_per_second(in_array):
    input_op_size = [8*1024.0, 16*1024.0, 32*1024.0, 128*1024.0]
    target_data_size = 1024*1024.0
    convert_snappy_to_throughput(in_array)
    for i in range(len(in_array)):
        if in_array[i] == 0:
            continue
        in_array[i] = in_array[i] * input_op_size[i] / target_data_size

labels = ["8KB", "16KB", "32KB", "128KB"]
# results_SIMURGH = [232, 533, 793, 1073]
# results_NOVA = [199, 513, 740, 1040]
# results_PMFS = [0, 0, 0, 0]
# results_EXDAXT = [79, 250, 408, 789]
# results_SPLITFS = [92, 286, 469, 857]

# results_SIMURGH = [9047, 15736, 21145, 62533] OLD
results_SIMURGH = [6.005, 8.575, 11.679, 32.296]
results_NOVA = [9.309, 11.717, 14.882, 33.385]
#results_PMFS = [896754, 936083, 940961, 962741]
results_EXDAXT = [26.613, 33.594, 41.105, 85.003]
results_SPLITFS = [22.652, 29.270, 35.719, 78.254]

convert_to_data_per_second(results_SIMURGH)
#convert_to_data_per_second(results_PMFS)
convert_to_data_per_second(results_NOVA)
convert_to_data_per_second(results_EXDAXT)
convert_to_data_per_second(results_SPLITFS)

fig, axs = plt.subplots()

x_label_pos = np.arange(len(labels))

width = 0.2

#plt.bar(x_label_pos-2*width, results_PMFS, width, label="PMFS", hatch="x", edgecolor=edgecolor, linewidth=box_linewidth, color="orange")
plt.bar(x_label_pos-1.5*width, results_SIMURGH, width, label="Simurgh", hatch=hatches["SIMURGH"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["SIMURGH"])
plt.bar(x_label_pos-0.5*width, results_NOVA, width, label="NOVA", hatch=hatches["NOVA"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["NOVA"])
plt.bar(x_label_pos+0.5*width, results_EXDAXT, width, label="EXT4-DAX", hatch=hatches["EXT4DAX"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["EXT4DAX"])
plt.bar(x_label_pos+1.5*width, results_SPLITFS, width, label="SplitFS", hatch=hatches["SPLITFS"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["SPLITFS"])



#axs.set_title("dummy values")
axs.set_xticks(x_label_pos)
axs.set_xticklabels(labels)
axs.set_ylabel('Throughout [MBytes/s]')

plt.legend(prop={'size': 9}, )

fig.set_size_inches(3, 2.5)
plt.tight_layout()
plot_save_show(plt, "app_snappy_one_process")

# Application results plot: Snappy 1 thread

def convert_snappy_to_throughput(in_array):
    for i in range(len(in_array)):
        if in_array[i] == 0:
            continue
        in_array[i] = 262144.0/in_array[i]

def convert_to_data_per_second(in_array):
    input_op_size = [8*1024.0, 16*1024.0, 32*1024.0, 128*1024.0]
    target_data_size = 1024*1024.0
    convert_snappy_to_throughput(in_array)
    for i in range(len(in_array)):
        if in_array[i] == 0:
            continue
        in_array[i] = in_array[i] * input_op_size[i] / target_data_size

labels = ["8KB", "16KB", "32KB", "128KB"]

# eight thread
# results_SIMURGH = [2290, 2912, 3464, 9218] OLD
results_SIMURGH = [1.728, 2.170, 2.362, 4.934]
results_NOVA = [3.589, 3.792, 4.068, 5.566]
#results_PMFS = [896754, 936083, 940961, 962741]
results_EXDAXT = [10.631, 16.007, 11.921, 14.199]
results_SPLITFS = [7.770, 8.435, 8.913, 13.873]

convert_to_data_per_second(results_SIMURGH)
#convert_to_data_per_second(results_PMFS)
convert_to_data_per_second(results_NOVA)
convert_to_data_per_second(results_EXDAXT)
convert_to_data_per_second(results_SPLITFS)

fig, axs = plt.subplots()

x_label_pos = np.arange(len(labels))

width = 0.2

#plt.bar(x_label_pos-2*width, results_PMFS, width, label="PMFS", hatch="x", edgecolor=edgecolor, linewidth=box_linewidth, color="orange")
plt.bar(x_label_pos-1.5*width, results_SIMURGH, width, label="Simurgh", hatch=hatches["SIMURGH"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["SIMURGH"])
plt.bar(x_label_pos-0.5*width, results_NOVA, width, label="NOVA", hatch=hatches["NOVA"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["NOVA"])
plt.bar(x_label_pos+0.5*width, results_EXDAXT, width, label="EXT4-DAX", hatch=hatches["EXT4DAX"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["EXT4DAX"])
plt.bar(x_label_pos+1.5*width, results_SPLITFS, width, label="SplitFS", hatch=hatches["SPLITFS"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["SPLITFS"])


#axs.set_title("dummy values")
axs.set_xticks(x_label_pos)
axs.set_xticklabels(labels)
axs.set_ylabel('Throughout [MBytes/s]')

plt.legend(prop={'size': 9}, )

fig.set_size_inches(3, 2.5)
plt.tight_layout()
plot_save_show(plt, "app_snappy_eight_process")

# # Optimizations Plot: Hashblock-size performance

# labels = ["16K", "32K", "64K", "128K", "256K"]
# results_SIMURGH = [0.3, 0.4, 0.5, 0.6, 0.7]


# fig, axs = plt.subplots()

# x_label_pos = np.arange(len(labels))

# width = 0.6

# plt.bar(x_label_pos, results_SIMURGH, width, label="Simurgh", hatch="\\", edgecolor=edgecolor, linewidth=box_linewidth, color="whitesmoke")

# axs.set_title("dummy values")
# axs.set_xticks(x_label_pos)
# axs.set_xticklabels(labels)
# axs.set_ylabel('Throughput [Mops/s]')

# #plt.legend(prop={'size': 9}, )

# fig.set_size_inches(3, 3)
# plt.tight_layout()
# plot_save_show(plt, "optimizations_hashblock_perf")

# # Optimizations Plot: Hashblock-size memory

# labels = ["16K", "32K", "64K", "128K", "256K"]
# results_SIMURGH = [-20, -10, 0, 8, 16]


# fig, axs = plt.subplots()

# x_label_pos = np.arange(len(labels))

# width = 0.6

# plt.bar(x_label_pos, results_SIMURGH, width, label="Simurgh", hatch="\\", edgecolor=edgecolor, linewidth=box_linewidth, color="whitesmoke")

# axs.set_title("dummy values")
# axs.set_xticks(x_label_pos)
# axs.set_xticklabels(labels)
# axs.set_ylabel('Overhead [%]')

# #plt.legend(prop={'size': 9}, )

# fig.set_size_inches(3, 3)
# plt.tight_layout()
# plot_save_show(plt, "optimizations_hashblock_mem")


# # Optimizations Plot: valid bit


# fig, axs = plt.subplots()

# labels = ["1", "2", "4", "6", "8", "10"]
# results_VALIDBIT = [108.92766666666667, 66.23156666666667, 37.41076666666667, 28.027500000000003, 23.1444, 21.2007] #create_file_in_private_dir_MT_20200506_19-42-04.json 
# results_BITMAP = [90, 60, 45, 40, 38, 37] 

# def to_mops(arr):
#     for i in range(0, len(arr)):
#         arr[i] = to_mega_ops(arr[i], 50000)

# to_mops(results_VALIDBIT)
# to_mops(results_BITMAP)

# x_label_pos = np.arange(len(labels))

# axs.plot(
#     results_VALIDBIT, 
#     label="valid bit",
#     linestyle="-",
#     marker='o',
#     color='black',
#     markersize=markersize,
#     linewidth=linewidth
#     )

# axs.plot(
#     results_BITMAP, 
#     label="bitmap",
#     linestyle="-",
#     marker='v',
#     color='dimgrey',
#     markersize=markersize,
#     linewidth=linewidth
#     )

# axs.set_title("dummy values")
# axs.set_xticks(x_label_pos)
# axs.set_xticklabels(labels)
# axs.set_ylabel('Throughput [Mops/s]')
# axs.set_xlabel('# of workers')

# plt.legend(prop={'size': 9}, )

# fig.set_size_inches(4, 3)
# plt.tight_layout()
# plot_save_show(plt, "optimizations_validbit")


# Git plot

# labels = ['add', 'status', 'commit', 'reset']
# results = {   'EXT4DAX': [18.217, 0.2405, 0.846, 7.4925],
#     'NOVA': [17.3475, 0.237, 0.7505, 6.4030000000000005],
#     'PMFS': [16.8005, 0.2355, 0.6445000000000001, 6.0055],
#     'SIMURGH': [15.994, 0.2505, 0.4335, 6.1615],
#     'SPLITFS': [18.545, 0.46950000000000003, 0.9575, 7.872]}

labels = ['add', 'commit', 'reset']
results = {   'EXT4DAX': [18.217, 0.846, 7.4925],
    'NOVA': [17.3475, 0.7505, 6.4030000000000005],
    'PMFS': [16.8005, 0.6445000000000001, 6.0055],
    'SIMURGH': [15.994, 0.4335, 6.1615],
    'SPLITFS': [18.545, 0.9575, 7.872]}

results_SIMURGH_for_labels = [67290.0/1000/15.994, 67290.0/1000/0.4335, 67290.0/1000/6.1615]


# for x in range(0, len(labels)):
#     timings = []
#     for key in results.keys():
#         timings.append(results[key][x])
#     norm_timing = results["SIMURGH"][x] # max(timings)
#     for key in results.keys():
#         results[key][x] = results[key][x]/norm_timing


for x in range(0, len(labels)):
    timings = []
    for key in results.keys():
        timings.append(results[key][x])
    norm_timing = results["SPLITFS"][x] # max(timings)
    for key in results.keys():
        results[key][x] = norm_timing/results[key][x]


fig, axs = plt.subplots()

x_label_pos = np.arange(len(labels))

width = 1/(len(results.keys())+1)

rects = plt.bar(x_label_pos-2*width, results["SIMURGH"], width, label="Simurgh", hatch=hatches["SIMURGH"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["SIMURGH"])
plt.bar(x_label_pos-1*width, results["NOVA"], width, label="NOVA", hatch=hatches["NOVA"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["NOVA"])
plt.bar(x_label_pos+0*width, results["PMFS"], width, label="PMFS", hatch=hatches["PMFS"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["PMFS"])
plt.bar(x_label_pos+1*width, results["EXT4DAX"], width, label="EXT4-DAX", hatch=hatches["EXT4DAX"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["EXT4DAX"])
plt.bar(x_label_pos+2*width, results["SPLITFS"], width, label="SplitFS", hatch=hatches["SPLITFS"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["SPLITFS"])

axs.set_xticks(x_label_pos)
axs.set_xticklabels(labels)
#axs.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))

axs.set_ylabel('Throughput [normalized]')

plt.ylim(ymin = 0, ymax = 2.5)
customlabel(rects, axs, results_SIMURGH_for_labels, "{:.2f}", " Kops/s", 2, 0)


plt.legend(prop={'size': 9}, ncol=2)
fig.set_size_inches(6, 2.2)
plot_save_show(plt, "git")

# Filebench Plots

labels = ['fileserver', 'varmail', 'webproxy', 'webserver']
results = {   'EXT4DAX': [338886.1835, 285493.0915, 798252.8822, 1389553.4159],
    'NOVA': [477923.2077, 835282.5385, 1000823.5584000001, 1354271.9274999998],
    'PMFS': [381781.25920000003, 756693.0183, 303521.68319999997, 1334808.3538],
    'SIMURGH': [   483406.71766666666,
                   1412492.2999999998,
                   1116856.991,
                   1370045.0036666666],
    }

def sort_custom(arr):
    temp_array = []
    temp_array.append(arr[1])
    temp_array.append(arr[3])
    temp_array.append(arr[2])
    temp_array.append(arr[0])
    return temp_array.copy()

results["EXT4DAX"] = sort_custom(results["EXT4DAX"])
results["NOVA"] = sort_custom(results["NOVA"])
results["PMFS"] = sort_custom(results["PMFS"])
results["SIMURGH"] = sort_custom(results["SIMURGH"])
labels = sort_custom(labels)


#results_SPLITFS = [3712, 0, 0, 0]

def to_mops(arr):
    for i in range(0, len(arr)):
        arr[i] = arr[i] /1000000

to_mops(results["EXT4DAX"])
to_mops(results["NOVA"])
to_mops(results["PMFS"])
to_mops(results["SIMURGH"])
#to_mops(results["SPLITFS"])

fig, axs = plt.subplots()

x_label_pos = np.arange(len(labels))

width = 1/(len(results.keys())+1)

plt.bar(x_label_pos-1.5*width, results["SIMURGH"], width, label="Simurgh", hatch=hatches["SIMURGH"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["SIMURGH"])
plt.bar(x_label_pos-0.5*width, results["NOVA"], width, label="NOVA", hatch=hatches["NOVA"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["NOVA"])
plt.bar(x_label_pos+0.5*width, results["PMFS"], width, label="PMFS", hatch=hatches["PMFS"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["PMFS"])
plt.bar(x_label_pos+1.5*width, results["EXT4DAX"], width, label="EXT4-DAX", hatch=hatches["EXT4DAX"], edgecolor=edgecolor, linewidth=box_linewidth, color=colors["EXT4DAX"])
#plt.bar(x_label_pos+width, results["SPLITFS"], width, label="SplitFS", hatch="/", edgecolor=edgecolor, linewidth=box_linewidth, color="purple")


axs.set_xticks(x_label_pos)
axs.set_xticklabels(labels)
#axs.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))

fig.text(0.02, 0.5, 'Throughput [Mops/s]', va='center', rotation='vertical')

plt.legend(prop={'size': 9}, )

fig.set_size_inches(6, 2)
plot_save_show(plt, "filebench")

# LevelDB Breakdown

labels = ['LoadA', 'RunA', 'RunB', 'RunC', 'RunD', 'LoadE', 'RunE', 'RunF']

application = [67.33, 68.45, 67.93, 63.05, 68.83, 66.45, 59.88, 69.48]
data = [22.63, 23.05, 24.04, 26.72, 22.64, 23.87, 33.77, 21.08]
filesystem = [10.04, 8.5, 8.03, 9.78, 8.53, 9.68, 6.35, 8.72]

width = 0.6
r1 = np.arange(len(application))

fig, axs = plt.subplots()

axs.set_ylabel('Time Percentage')


t_axs = axs
t_axs.bar(r1, application, width, label='application', hatch=hatches["SIMURGH"], edgecolor=edgecolor, color=colors["SIMURGH"], linewidth=box_linewidth)
t_axs.bar(r1, data, width, bottom=application, label='data', hatch=hatches["PMFS"], edgecolor=edgecolor, color=colors["PMFS"], linewidth=box_linewidth)
t_axs.bar(r1, filesystem, width, bottom=np.add(data, application), label='filesystem', hatch=hatches["EXT4DAX"], edgecolor=edgecolor, color=colors["EXT4DAX"], linewidth=box_linewidth)
t_axs.set_xticks(r1)
t_axs.set_xticklabels(labels) #, rotation=310)
#t_axs.set_title("AAA", fontsize=10)

fig.set_size_inches(6, 2)

plt.legend(prop={'size': 9}, ncol=3)
plot_save_show(plt, "syscallnumber")

