import os
import pprint

folder_to_parse="."

files_to_parse=["3_add_timing", "6_commit_timing", "11_reset_timing"]

timings = {}

for folder in next(os.walk(folder_to_parse))[1]:
    print(folder)
    title = folder.split("_")[1].split("_")[0]
    timings[title] = []

    for file_ in files_to_parse:

        _counter = 0.0
        _sum = 0.0

        for filenumber in range (1, 3):

            file = file_ + "_" + str(filenumber) + ".txt"
            print(file)

            with open(os.path.join(folder_to_parse, folder, file)) as fp:
                line = fp.readline()
                while line:
                    if "real" in line:
                        print(line)
                        _sum += float(line.split("m")[1].split("s")[0])
                        _counter += 1
                    line = fp.readline()

        timings[title].append(_sum/_counter)


    print(" ")

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(["add", "commit", "reset"])
pp.pprint(timings)


