import numpy as np

std_mean = 100 # customized parameter
std_std = 100 #customized parameter
size_bw = int(20) #size of basic window
num_bw = 100 #number basic windows in a time series
num_ts = 10 # number of time series
mu_mean = 20 # random
mu_std = 10 # random; could be related to std_std

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

ts=np.asarray(ts)
print(ts.shape)
np.save('./datasets/generated_ts',ts)
        