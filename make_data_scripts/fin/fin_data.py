import csv
import numpy as np
import pandas as pd
import functools
import pickle
with open("/u/yxu103/TSUBASAPLUS/output/fin_dates", "rb") as fp:
    b=pickle.load(fp)
print(b)

fin_data = pd.read_csv("/localdisk3/TSUBASAPLUS/origindata.csv")
#fin_data = pd.read_csv("/u/yxu103/TSUBASAPLUS/datasets/sample.csv")
#print(fin_data)
print("finish###loading")
com_name = fin_data['COMNAM']
com = com_name.drop_duplicates(keep='first', inplace=False)
comlist = com.values.tolist()
print("Company_names_picked")
dateinfo=[]

#First Scan: Find the common dates for all the companys
for i in comlist:
    print(i)
    fin_sub=fin_data[(fin_data['COMNAM']==i)] #The frame of a specific
    date_of_this_company=fin_sub['date'].tolist()
    dateinfo.append(date_of_this_company)
print("finish_date_selection")
with open("/u/yxu103/TSUBASAPLUS/output/fin_dates", "wb") as fp:
    pickle.dump(dateinfo, fp)
    
common_date=list(functools.reduce(set.intersection, map(set,dateinfo))) #common dates for all companys

with open("/u/yxu103/TSUBASAPLUS/output/fin_dates", "rb") as fp:
    b=pickle.load(fp)
print(b)

priceinfo=[]
#Second Scan: Construct the list of series(Prize)
for i in comlist:
    fin_sub = fin_data[(fin_data['COMNAM'] == i)]  # The frame of a specific
    fin_sub_date=fin_sub.loc[fin_sub['date'].isin(common_date)] #Select the frames with common dates
    price_of_this_company=fin_sub_date['OPENPRI'].tolist()
    priceinfo.append(price_of_this_company)

result=np.asarray(priceinfo)
print(result)


