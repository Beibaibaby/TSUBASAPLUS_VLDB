import numpy as np
import matplotlib.pyplot as plt
import math

gt_result=np.load("NOEA_gt_sliding_50.npy")
print(gt_result.shape)
gt_result[gt_result < 0.5]=0
postive = (gt_result >= 0.5).sum()
#print(gt_result)
sample_result=np.load("NOEA_2p_sliding_50.npy")
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





gt_result=np.load("NOEA_gt_sliding_50.npy")
print(gt_result.shape)
gt_result[gt_result < 0.5]=0
#print(gt_result)
sample_result=np.load("NOEA_2p_sliding_50.npy")

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




