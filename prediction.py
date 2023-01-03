##import package
import numpy as np
import matplotlib.pyplot as plt
import math
import tsubasa_plus as tsu

##hyper hyperparameter
size_bw = int(20) #size of basic window
ts=np.load('./datasets/data_noea.npy')#change to your local path
ts=ts[15:100,:]
size_sliding=50


thre=0.5
list=[]
import time



basic_window_matrix=tsu.create_basic_window_matrix(ts,size_bw)


start_time = time.time()
sample_result=tsu.do_sliding_generic(ts,size_bw,size_sliding,thre)
print("--- %s seconds bs---" % (str(time.time() - start_time)))
with open('./logs/time_generic.txt', 'a') as f:
    f.write((str(time.time() - start_time)))
print(sample_result)       
np.save('generic_small',sample_result)


start_time = time.time()
gt_result=tsu.do_sliding_gt(ts,size_bw,size_sliding)
print("--- %s seconds gt---" % (str(time.time() - start_time)))
with open('./logs/time_gt.txt', 'a') as f:
    f.write((str(time.time() - start_time)))

np.save('noea_gt_result_generic_small',gt_result)
print(gt_result)

import numpy as np
import matplotlib.pyplot as plt
import math

gt_result=np.load("noea_gt_result_small.npy")
print(gt_result.shape)
gt_result[gt_result < 0.5]=0
postive = (gt_result >= 0.5).sum()
#print(gt_result)
sample_result=np.load("/u/yxu103/TSUBASAPLUS_VLDB/small_noea_result_sliding_bs_=50_basic=20.npy")
postive_sample=(sample_result >= 0.5).sum()

print('recall='+str(postive_sample/postive))

X=sample_result-gt_result
K=X[X==0]
allsize=X.size
correctsize=K.size
#print(K)

print(correctsize/allsize)

Y=sample_result
Y[Y ==0]=0.5
YY=np.full(Y.shape, 0.5)
Y=Y-YY
K=Y[Y<0]
#print(K)
correctsize=K.size
#print(K)
print(1/(correctsize/allsize))





gt_result=np.load("noea_gt_result_generic_small.npy")
print(gt_result.shape)
gt_result[gt_result < 0.5]=0
#print(gt_result)
sample_result=np.load("generic_small.npy")

postive = (gt_result >= 0.5).sum()

postive_sample=(sample_result >= 0.5).sum()

print('recall='+str(postive_sample/postive))


Y=sample_result
Y[Y ==0]=0.5
YY=np.full(Y.shape, 0.5)
Y=Y-YY
K=Y[Y<0]
#print(K)
allsize=sample_result.size
correctsize=K.size
print(correctsize)
#print(K)
print((correctsize/allsize))




