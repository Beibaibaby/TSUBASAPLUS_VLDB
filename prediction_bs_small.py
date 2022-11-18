##import package
import numpy as np
import matplotlib.pyplot as plt
import math
import tsubasa_plus as tsu

##hyper hyperparameter
size_bw = int(20) #size of basic window
ts=np.load('./datasets/data_noea.npy')#change to your local path
ts=ts[5:20,:]
size_sliding=50


thre=0.5
list=[]
import time



basic_window_matrix=tsu.create_basic_window_matrix(ts,size_bw)

start_time = time.time()
sample_result=tsu.do_sliding_bs_upper(ts,size_bw,size_sliding,thre)
print("--- %s seconds bs---" % (str(time.time() - start_time)))
with open('./logs/time_bs_small.txt', 'a') as f:
    f.write((str(time.time() - start_time)))
print(sample_result)          

np.save('small_noea_result_sliding_bs_='+str(size_sliding)+'_basic='+str(size_bw),sample_result)


start_time = time.time()
loop_result=tsu.do_sliding(ts,size_bw,size_sliding,thre)
print("--- %s seconds loop---" % (str(time.time() - start_time)))
with open('./logs/time_loop_small.txt', 'a') as f:
    f.write((str(time.time() - start_time)))

np.save('noea_loop_upper_result_small',loop_result)
print(loop_result)


start_time = time.time()
gt_result=tsu.do_sliding_gt(ts,size_bw,size_sliding)
print("--- %s seconds gt---" % (str(time.time() - start_time)))
with open('./logs/time_gt_small.txt', 'a') as f:
    f.write((str(time.time() - start_time)))

np.save('noea_gt_result_small',gt_result)
print(gt_result)


