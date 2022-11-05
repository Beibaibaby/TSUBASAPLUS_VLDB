import numpy as np
import pandas as pd
import functools
import matplotlib.pyplot as plt
import math
fin_data = pd.read_csv("./origindata.csv", index_col=None)
#print(fin_data)
size_bw = int(20)
com_name = fin_data['COMNAM']
com = com_name.drop_duplicates(keep='first', inplace=False)
comlist = com.values.tolist()

dateinfo=[]
#First Scan: Find the common dates for all the companys
for i in comlist:
    fin_sub=fin_data[(fin_data['COMNAM']==i)] #The frame of a specific
    date_of_this_company=fin_sub['date'].tolist()
    dateinfo.append(date_of_this_company)
common_date=list(functools.reduce(set.intersection, map(set,dateinfo))) #common dates for all companys
priceinfo=[]
#Second Scan: Construct the list of series(Prize)
for i in comlist:
    fin_sub = fin_data[(fin_data['COMNAM'] == i)]  # The frame of a specific
    fin_sub_date=fin_sub.loc[fin_sub['date'].isin(common_date)] #Select the frames with common dates
    price_of_this_company=fin_sub_date['OPENPRI'].tolist()
    priceinfo.append(price_of_this_company)

result=np.asarray(priceinfo)
np.save('fin_result',result)
#print(result)

size_sliding=50
thre=0.5

def create_basic_window_matrix(ts_matrix,size_bw):
    num_ts = ts_matrix.shape[0]  # number of time series
    len_ts = ts_matrix.shape[1]  # length of time series
    num_bw = int(len_ts / size_bw)  # number of basic window
    length_pro=num_bw*size_bw
    ts_splited=ts_matrix[:, : length_pro].reshape((num_ts,num_bw,size_bw))
    return ts_splited
    #The return vaule here is a 3-d array: 1. num_ts 2.num_bs 3. size_bw

def sketch_computation_1(ts_splited):#function for computing sigma and delta
    sigma_matrix = np.zeros((ts_splited.shape[0],ts_splited.shape[1]))
    delta_matrix = np.zeros((ts_splited.shape[0], ts_splited.shape[1]))
    for i in range(ts_splited.shape[0]):
        mean=np.mean(ts_splited[i])
        for j in range (ts_splited.shape[1]):
            sigma_matrix[i,j]=np.std(ts_splited[i][j])
            delta_matrix[i,j]=np.mean(ts_splited[i][j])-mean
    return sigma_matrix, delta_matrix


def corr_pair(x,y):
    if x.shape != y.shape:
        raise Exception("Error, the time seris for correlation computation are in different shape")
    list=[]
    sigma_list_x = np.zeros(x.shape[0])
    delta_list_x=np.zeros(x.shape[0])
    sigma_list_y = np.zeros(x.shape[0])
    delta_list_y=np.zeros(x.shape[0])
    mean_x=np.mean(x)

    for i in range(x.shape[0]):
        sigma_list_x[i]=np.std(x[i])
        delta_list_x[i]=np.mean(x[i])-mean_x

    mean_y=np.mean(y)
    for i in range(y.shape[0]):
        sigma_list_y[i]=np.std(y[i])
        delta_list_y[i]=np.mean(y[i])-mean_y

    for i in range(x.shape[0]):
        corr=np.corrcoef(x[i],y[i])
        list.append(corr[0,1])

    cor_list=np.asarray(list)
    numerator=0
    denumerator_1=0
    denumerator_2=0
    for i in range(x.shape[0]):
        #print(sigma_list_x[i])
        numerator += (x[i].size *(sigma_list_x[i]*sigma_list_y[i]*cor_list[0] + delta_list_x[i]*delta_list_y[i]))
        denumerator_1 += x[i].size * (sigma_list_x[i]**2 + delta_list_x[i]**2)
        denumerator_2 += y[i].size * (sigma_list_y[i]**2 + delta_list_y[i]**2)

    denumerator_1=math.sqrt(denumerator_1)
    denumerator_2 =math.sqrt(denumerator_2)

    return np.asarray(numerator/(denumerator_1*denumerator_2))


def corr_pair_complete(x,y):
    if x.shape != y.shape:
        raise Exception("Error, the time seris for correlation computation are in different shape")
    list=[]
    sigma_list_x = np.zeros(x.shape[0])
    delta_list_x=np.zeros(x.shape[0])
    sigma_list_y = np.zeros(x.shape[0])
    delta_list_y=np.zeros(x.shape[0])
    mean_x=np.mean(x)
    for i in range(x.shape[0]):
        sigma_list_x[i]=np.std(x[i])
        delta_list_x[i]=np.mean(x[i])-mean_x

    mean_y=np.mean(y)
    for i in range(y.shape[0]):
        sigma_list_y[i]=np.std(y[i])
        delta_list_y[i]=np.mean(y[i])-mean_y

    for i in range(x.shape[0]):
        #print(x[i])
        corr=np.corrcoef(x[i],y[i])
        #print(corr)
        list.append(corr[0,1])

    cor_list=np.asarray(list)
    numerator=0
    denumerator_1=0
    denumerator_2=0
    for i in range(x.shape[0]):
        #print(sigma_list_x[i])
        numerator += (x[i].size *(sigma_list_x[i]*sigma_list_y[i]*cor_list[0] + delta_list_x[i]*delta_list_y[i]))
        denumerator_1 += x[i].size * (sigma_list_x[i]**2 + delta_list_x[i]**2)
        denumerator_2 += y[i].size * (sigma_list_y[i]**2 + delta_list_y[i]**2)

    denumerator_1=math.sqrt(denumerator_1)
    denumerator_2 =math.sqrt(denumerator_2)

    return np.asarray(numerator/(denumerator_1*denumerator_2)), cor_list



def corr_pair_query(x,y,starting,len_sliding):
    return corr_pair(x[starting:starting+len_sliding], y[starting:starting+len_sliding])



def jumping(x,y,t,size_sliding):
    corr_ini=corr_pair_query(x,y,t,size_sliding)
    a,c = corr_pair_complete(x[t:t+size_sliding], y[t:t+size_sliding])
    if a>thre:
        print('jumped step', str(0))
        #print(a)
        #print(t)
        return 0

    for i in range(size_sliding):
        corr_ini+= (1 - c[i])/size_sliding
        if corr_ini>thre:
             print('jumped step',str(i))
             return i
    print('jumped step',str(size_sliding))
    return size_sliding



list=[]
basic_window_matrix=create_basic_window_matrix(result,size_bw)

def do_sliding(result,size_bw,size_sliding):
    basic_window_matrix = create_basic_window_matrix(result, size_bw)
    time_len=basic_window_matrix.shape[1]-size_sliding+1
    correlation_matrix=np.zeros((basic_window_matrix.shape[1]-size_sliding+1,basic_window_matrix.shape[0],basic_window_matrix.shape[0]))
    for i in range(basic_window_matrix.shape[0]):
        for j in range(basic_window_matrix.shape[0]):
              if i!=j:
                  t = 0
                  x = basic_window_matrix[i]
                  y = basic_window_matrix[j]
                  while t <= time_len - 1:
                      jumped_step = jumping(x, y, t, size_sliding)
                      if jumped_step == 0:
                          corr = corr_pair_query(x, y, t, size_sliding)
                          correlation_matrix[t, i, j] = corr
                          t = t + 1
                      else:
                          t = t + jumped_step
                          if t <= time_len - 1:
                              corr = corr_pair_query(x, y, t, size_sliding)
                              correlation_matrix[t, i, j] = corr
                          else:
                              break
              else:
                  correlation_matrix[:, i, j]=1
    return correlation_matrix
fd_result=do_sliding(result[100:105],size_bw,size_sliding)
np.save('fd_result',fd_result)
print(fd_result)

def do_sliding_gt(result,size_bw,size_sliding):
    basic_window_matrix = create_basic_window_matrix(result, size_bw)
    time_len=basic_window_matrix.shape[1]-size_sliding+1
    correlation_matrix=np.zeros((basic_window_matrix.shape[1]-size_sliding+1,basic_window_matrix.shape[0],basic_window_matrix.shape[0]))
    for i in range(basic_window_matrix.shape[0]):
        for j in range(basic_window_matrix.shape[0]):
              if i!=j:
                  t = 0
                  x = basic_window_matrix[i]
                  y = basic_window_matrix[j]
                  while t <= time_len - 1:
                              corr = corr_pair_query(x, y, t, size_sliding)
                              correlation_matrix[t, i, j] = corr
                              t=t+1

              else:
                  correlation_matrix[:, i, j]=1
    return correlation_matrix
gt_fd_result=do_sliding_gt(result[100:105],size_bw,size_sliding)
np.save('gt_result',gt_fd_result)
print(gt_fd_result)