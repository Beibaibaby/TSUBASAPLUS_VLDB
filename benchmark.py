import numpy as np
import math
import random

# def draft_ts(mu_mean, std_mean, mu_std, std_std, num_bw):
#     ts=[]
#     for i in range(num_ts):
#         single_ts=[]
#         single_ts=np.asarray(single_ts)
#         mean_paras = np.random.normal(mu_mean, std_mean, num_bw)
#         std_paras = np.abs(np.random.normal(mu_std, std_std, num_bw))
        
#         for j in range(num_bw):
#             curr_window=np.random.normal(mean_paras[j], std_paras[j], size_bw)
#             single_ts=np.append(single_ts,curr_window)
#         ts.append(single_ts)
#     return np.asarray(ts)

# def corr_stream(s,r,thre_e):     #s and r are 2 arrays
#     inver_list = []
#     if s.shape != r.shape:
#         raise Exception("Error, the time seris for correlation computation are in different shape")
#     corr = np.corrcoef(s[0], r[0])
#     d = math.sqrt(2-2*corr)
#     d_matrix= np.asarray(d)
#     for i in range(d_matrix[0]):
#         if thre_e >= i:
#             return None
#         else:
#             norm = np.fft[i]
#         inver_list.append(norm)
#     return np.asarray(inver_list.append(np.asarray(norm)))

std_mean = 1 # customized parameter
std_std = 1 #customized parameter
size_bw = int(20) #size of basic window
num_bw = 100 #number basic windows in a time series
num_ts = 100 # number of time series
mu_mean = 20 # random
mu_std = 1 # random; could be related to std_std

thre_e = 0.7 #customized threshold
n = 10


def low_list_gen(num_bw, thre_e, mu_mean, std_mean):
    D = math.sqrt(1-thre_e)
    ts_l = []
    val_ini = np.random.normal(mu_mean,std_mean,num_bw)   #initialize a list of number
    print(val_ini)
    for i in val_ini:
        e_dist = math.dist([i],[val_ini[0]])    #Euclidian Distance
        if e_dist < D:
            ts_l.append(i)
    return np.asarray(ts_l)

def dft_matrix(n):
    i,j=np.meshgrid(np.arange(n), np.arange(n))
    cal = np.exp(-2*np.pi*1J/n)
    arr = np.power(cal, i*j)/n
    return arr

ts_low=low_list_gen(num_bw, thre_e, mu_mean, std_mean)   #input data with shape of (x, )
print(ts_low)
print(np.shape(ts_low))

arr = dft_matrix(np.shape(ts_low)[0])
dft_of_list = arr.dot(ts_low).dot(arr)
print(dft_of_list)







