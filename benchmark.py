import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt

time_seires = input(int("Number of time series: "))
length = input(int("Length of ts: "))
bs_size = input(int("Length of ts: "))
# x_data = 
# y_data = 

ts_list = []
def generator():
    for i in range(time_seires):
        ts_list.append(i)

def func(x, a, mean, std):
    return a*np.exp(-(x-mean)**2/(2*std**2))