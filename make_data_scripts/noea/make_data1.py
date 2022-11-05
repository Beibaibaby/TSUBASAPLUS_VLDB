import pandas as pd
import os
import numpy as np

import csv

os.system('/usr/local/bin/wget -r -np -l 1 -A txt https://www.ncei.noaa.gov/pub/data/uscrn/products/hourly02/2020/')

path = './www.ncei.noaa.gov/pub/data/uscrn/products/hourly02/2020/'

n=9
for filename in filter(lambda p: p.endswith("txt"), os.listdir(path)):
    filepath = os.path.join(path, filename)
    #print(filepath)
    dataframe1 = pd.read_csv(filepath, delim_whitespace=True)
    dataframe1.to_csv(filepath, index=None)
    #z = np.loadtxt(filename, usecols=10)
    with open(filepath, mode='r') as in_file:
        stripped = (line.strip() for line in in_file)

        lines = (line.split(",") for line in stripped if line)

        with open(filename+'.csv', 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(lines)

matrix=[]

matrix=np.zeros((2,8000))

for filename in filter(lambda p: p.endswith("csv"), os.listdir('./')):
    filepath = os.path.join('./', filename)


    result=[]
    reader = csv.reader(open(filepath, "rt"), delimiter=",")
    for row in reader:
        #print(row)
        while True:
            try:
                result.append(float(row[n]))
                break
            except ValueError:
                result.append(20)
                break

    result=np.asarray(result)
    print(result[:8000])

    matrix = np.append(matrix, [result[:8000]], axis=0)
    print(matrix.shape)
    np.save('./data_prepared', matrix)
    print('pass')


print(matrix)