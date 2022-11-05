# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import prediction
import numpy as np
import matplotlib.pyplot as plt
import math

##hyper hyperparameter
size_bw = int(10) #size of basic window
#change to your local path
#print(ts.shape)


if __name__ == '__main__':
    ts = np.load('./data_prepared.npy')
    basic_window_matrix=prediction.create_basic_window_matrix(ts,size_bw)
    print(prediction.corr_pair(basic_window_matrix[4],basic_window_matrix[1]))

