##import package
import numpy as np
import matplotlib.pyplot as plt
import math
import tsubasa_plus as tsu

##hyper hyperparameter
size_bw = int(20) #size of basic window
ts=np.load('./datasets/generated_ts.npy')#change to your local path
size_sliding=50
#ts=ts[50:80,:]

thre=0.5
list=[]
import time


basic_window_matrix=tsu.create_basic_window_matrix(ts,size_bw)

start_time = time.time()
sample_result=tsu.do_sliding_two_phrase(ts,size_bw,size_sliding,thre)

print("--- %s seconds bs---" % (str(time.time() - start_time)))
with open('./logs/time_generic.txt', 'a') as f:
    f.write((str(time.time() - start_time))) #Record time

np.save('g_2p_corr_matrix',sample_result)

start_time = time.time()
sample_result=tsu.do_sliding_gt(ts,size_bw,size_sliding)

print("--- %s seconds bs---" % (str(time.time() - start_time)))
with open('./logs/time_generic.txt', 'a') as f:
    f.write((str(time.time() - start_time))) #Record time

np.save('g_gt_corr_matrix',sample_result)

import numpy as np
import matplotlib.pyplot as plt
import math

gt_result=np.load("g_gt_corr_matrix.npy")
print(gt_result.shape)
gt_result[gt_result < 0.5]=0
postive = (gt_result >= 0.5).sum()
#print(gt_result)
sample_result=np.load("g_2p_corr_matrix.npy")
postive_sample=(sample_result >= 0.5).sum()

print(str(postive_sample))
print(str(postive))
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





gt_result=np.load("g_gt_corr_matrix.npy")
print(gt_result.shape)
gt_result[gt_result < 0.5]=0
#print(gt_result)
sample_result=np.load("g_2p_corr_matrix.npy")

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
