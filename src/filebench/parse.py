import os
import pprint

folder_to_parse="./"

workloads_to_parse=["fileserver", "varmail", "webproxy", "webserver"]
fs_to_parse=["SIMURGH", "SPLITFS", "NOVA", "EXT4DAX", "PMFS"]

timings = {}

for fs in fs_to_parse:
    timings[fs] = []
    print(fs)

    for workload in workloads_to_parse:
        filename = "output_filebench_" + fs + "-" + workload + ".txt"

        _counter = 0.0
        _sum = 0.0
        
        print(workload)

        with open(os.path.join(folder_to_parse, filename)) as fp:
            line = fp.readline()
            while line:
                if "IO Summary" in line:
                    print(line)
                    _sum += float(line.split("ops ")[1].split(" ops/s")[0])
                    _counter += 1.0
                line = fp.readline()

        timings[fs].append(_sum/_counter)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(workloads_to_parse)
pp.pprint(timings)


