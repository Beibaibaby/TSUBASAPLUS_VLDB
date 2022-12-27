import numpy as np
import math

std_mean = 1 # customized parameter
std_std = 1 #customized parameter
size_bw = int(20) #size of basic window
num_bw = 100 #number basic windows in a time series
num_ts = 100 # number of time series
mu_mean = 20 # random
mu_std = 1 # random; could be related to std_std

thre_e = 0.5 #customized threshold



def draft_ts(mu_mean, std_mean, mu_std, std_std, num_bw):
    ts=[]
    for i in range(num_ts):
        single_ts=[]
        single_ts=np.asarray(single_ts)
        mean_paras = np.random.normal(mu_mean, std_mean, num_bw)
        std_paras = np.abs(np.random.normal(mu_std, std_std, num_bw))
        
        for j in range(num_bw):
            curr_window=np.random.normal(mean_paras[j], std_paras[j], size_bw)
            single_ts=np.append(single_ts,curr_window)
        ts.append(single_ts)
    return np.asarray(ts)

def corr_stream(s,r):     #s and r are 2 arrays
    if s.shape != r.shape:
        raise Exception("Error, the time seris for correlation computation are in different shape")
    return np.corrcoef(s[0], r[0])

def d_value_of_ts(s,r):
    d = math.sqrt(2-2*corr_stream(s,r))
    return np.asarray(d)

def norm_DFT(s,r, thre_e):  #inverse DFT into new lists if larger than threshold
    inver_list = []
    d = d_value_of_ts(s,r)
    for i in range(d[0]):
        if thre_e >= d:
            return 0
        else: 
            norm = np.fft(d)    #inverse
        inver_list.append(norm)
    return np.asarray(inver_list.append(np.asarray(norm)))
