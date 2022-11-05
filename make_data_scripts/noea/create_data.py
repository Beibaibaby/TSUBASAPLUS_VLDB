import os
import numpy as np
path = '.'
import csv
files_content = []



#z = np.loadtxt("filename.txt", usecols=2)

for filename in filter(lambda p: p.endswith("txt"), os.listdir(path)):
    filepath = os.path.join(path, filename)
    print(filepath)
    #z = np.loadtxt(filename, usecols=10)
    with open(filepath, mode='r') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split(",") for line in stripped if line)
        with open(filename+'.csv', 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerow(('title', 'intro'))
            writer.writerows(lines)


