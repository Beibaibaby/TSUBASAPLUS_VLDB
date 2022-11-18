import numpy as np
import matplotlib.pyplot as plt
import math

gt_result=np.load("noea_gt_result_small.npy")
print(gt_result.shape)
gt_result[gt_result < 0.5]=0
#print(gt_result)
sample_result=np.load("/u/yxu103/TSUBASAPLUS_VLDB/small_noea_result_sliding_bs_=50_basic=20.npy")

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

gt_result=np.load("noea_gt_result_small.npy")
print(gt_result.shape)
gt_result[gt_result < 0.5]=0
#print(gt_result)
sample_result=np.load("noea_loop_upper_result_small.npy")

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