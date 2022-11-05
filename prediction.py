##import package
import numpy as np
import matplotlib.pyplot as plt
import math
import tsubasa_plus as tsu

##hyper hyperparameter
size_bw = int(20) #size of basic window
ts=np.load('/localdisk2/draco/tsubasa/fin_dataset.npy')#change to your local path

size_sliding=50


thre=0.5
list=[]
basic_window_matrix=tsu.create_basic_window_matrix(ts,size_bw)
sample_result=tsu.do_sliding_hl(ts,size_bw,size_sliding,thre)
np.save('fin_result_sliding_hl_='+str(size_sliding)+'_basic='+str(size_bw),sample_result)
print(sample_result)

gt_result=tsu.do_sliding_gt(ts,size_bw,size_sliding)
np.save('fin_gt_result',gt_result)
print(gt_result)

