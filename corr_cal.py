import numpy as np
import matplotlib.pyplot as plt

basic_winsize = 100
basic_winsize=int(basic_winsize)
ts=np.load('D:/UR/tsubasa/data.npy')
print(ts.shape)

def corr_pair(x,y):
    x_win = int(np.size(x)/basic_winsize)
    y_win = int(np.size(y)/ basic_winsize)
    x_cor = np.reshape(x[: basic_winsize * x_win], (x_win, basic_winsize))
    y_cor = np.reshape(y[: basic_winsize * y_win], (y_win, basic_winsize)) 
    list=[] 
    for i in range(x_cor.shape[0]):
        corr=np.corrcoef(x_cor[i],y_cor[i])
        list.append(corr)
    print(list)
    print(corr)

corr_pair(ts[0], ts[1])