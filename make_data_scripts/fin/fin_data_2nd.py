import csv
import numpy as np
import pandas as pd
import functools
import pickle

fin_data = pd.read_csv("/localdisk3/TSUBASAPLUS/origindata.csv")
#fin_data = pd.read_csv("/u/yxu103/TSUBASAPLUS/datasets/sample.csv")
#print(fin_data)
print("finish###loading")
com_name = fin_data['COMNAM']
com = com_name.drop_duplicates(keep='first', inplace=False)
comlist = com.values.tolist()
print("Company_names_picked")
dateinfo=[]



k=2000
#First Scan: Find the common dates for all the companys

fin_sub_1=fin_data[(fin_data['COMNAM']==com_name[2])] #The frame of a specific
date_of_this_company=fin_sub_1['date'].tolist()
std_dates=np.asarray(date_of_this_company)
lll=len(comlist)
print(len(comlist))

print('start')
common_we_need=[]
dateinfo=[]
count=0
for i in comlist:
    fin_sub = fin_data[(fin_data['COMNAM'] == i)]  # The frame of a specific
    fin_sub_date=fin_sub.loc[fin_sub['date'].isin(date_of_this_company)]#Select the frames with common dates
    fin_sub_date_data = np.intersect1d(np.asarray(fin_sub_date['date'].tolist()),std_dates)
    with open('/u/yxu103/TSUBASAPLUS/logs/log_formal.txt', 'w') as f:
             f.write(str(count/lll))
    count=count+1
    #print(fin_sub_date)
    if np.size(fin_sub_date_data)>k:
        common_we_need.append(i)
        std_dates=fin_sub_date_data
        print(fin_sub_date_data.shape)
        dateinfo.append(fin_sub_date_data)
        print(fin_sub_date_data[0])
        print(fin_sub_date_data[-1])
        print("NiuNiu")
        print(i)

        
        #with open("/u/yxu103/TSUBASAPLUS/output/fin_dates", "wb") as fp:
             #pickle.dump(dateinfo, fp)
        #common_date=list(functools.reduce(set.intersection, map(set,dateinfo)))
        #cd=np.asarray(common_date)
        #print(np.size(cd))
        np.save('/u/yxu103/TSUBASAPLUS/output/common_dates_np',std_dates)
        #price_of_this_company=fin_sub_date['OPENPRC'].tolist()


common_date=list(functools.reduce(set.intersection, map(set,dateinfo)))
print("common_date get")
print(common_date)

with open("/u/yxu103/TSUBASAPLUS/output/fin_common_dates", "wb") as fp:
        pickle.dump(common_date, fp)
        
print("finish_date_selection")


priceinfo=[]
print("std size")
print(std_dates.shape)
std_size=np.size(std_dates)
lll=len(common_we_need)
count=0
for i in common_we_need:
    fin_sub = fin_data[(fin_data['COMNAM'] == i)]  # The frame of a specific
    fin_sub_date=fin_sub.loc[fin_sub['date'].isin(std_dates)]
    with open('/u/yxu103/TSUBASAPLUS/logs/log_formal_2nd.txt', 'w') as f:
             f.write(str(count/lll))
    count=count+1
    #Select the frames with common dates
    if len(fin_sub_date)==std_size:
        print(fin_sub_date)
        price_of_this_company=np.asarray(fin_sub_date['OPENPRC'].tolist())
        priceinfo.append(price_of_this_company)

result=np.asarray(priceinfo)
np.save('/u/yxu103/TSUBASAPLUS/output/fin_dataset',result)
print(result)


