import prediction
import numpy as np
import matplotlib.pyplot as plt
import math

##hyper hyperparameter
size_bw = int(10) #size of basic window
ts=np.load('D:/UR/tsubasa/data.npy')#change to your local path
#print(ts.shape)

corr_list = []

#if __name__ == '__main__':
def pair_corr():
    ts = np.load('D:/UR/tsubasa/data.npy')
    basic_window_matrix=prediction.create_basic_window_matrix(ts,size_bw)
    for i in range(basic_window_matrix.shape[0]):
        for j in range(basic_window_matrix.shape[0]):
            corr_list.append(prediction.corr_pair(basic_window_matrix[i],basic_window_matrix[j]))
            corr_array = np.asarray(corr_list)
    corr_matrix = corr_array.reshape(10,10)
    return corr_matrix.shape