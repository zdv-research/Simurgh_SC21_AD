import os
import pprint

folder_to_parse="."

files_to_parse=["loada", "runa_5M_5M", "runb_5M_5M", "runc_5M_5M", "rund_5M_5M", "loade", "rune_5M_1M", "runf_5M_5M"]

timings = {}

for folder in next(os.walk(folder_to_parse))[1]:
    if not folder.startswith("output"):
        continue
    print(folder)
    title = folder.split("_")[1].split("_")[0]
    timings[title] = []

    for file_ in files_to_parse:

        _counter = 0.0
        _sum = 0.0


        file = file_ 
        print(file)

        with open(os.path.join(folder_to_parse, folder, file)) as fp:
            line = fp.readline()
            while line:
                if "Thread 0: Ops/s" in line:
                    print(line)
                    _sum += float(line.split("=")[1].split("Kops")[0].strip())
                    _counter += 1
                line = fp.readline()

        timings[title].append(_sum/_counter)


    print(" ")

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(["loada", "runa_5M_5M", "runb_5M_5M", "runc_5M_5M", "rund_5M_5M", "loade", "rune_5M_1M", "runf_5M_5M"])
pp.pprint(timings)


