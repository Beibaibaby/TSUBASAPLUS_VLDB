##import package
import numpy as np
import matplotlib.pyplot as plt
import math
import tsubasa_plus as tsu
import numpy as np
import matplotlib.pyplot as plt
import math

size_bw = int(20) 
ts=np.load('./data_noea.npy')#change to your local path
#ts=ts[5:10,:]
size_sliding=50
ts_50 = ts[50:100]

thre=0.5
# sliding_step = tsu.do_sliding_two_phrase(ts[10:120],size_bw,size_sliding,thre)
# print(sliding_step)

# # #mean_list=mean_list[ (mean_list >= 50) & (mean_list <= -100) ]
# # print(crosstime_stdmean)
# # #max_min_list=max_min_list[(max_min_list >= 50) & (max_min_list <= -100)]
# # #p#rint(mean_list)
# np.save('NOEA_result_sliding_two_phrase='+str(size_sliding)+'_basic='+str(size_bw),sliding_step)

sliding_step_gt = tsu.do_sliding_gt(ts_50,size_bw,size_sliding)
print(sliding_step_gt)
np.save('NOEA_gt_sliding_50',sliding_step_gt)

sliding_step_2p = tsu.do_sliding_two_phrase(ts_50,size_bw,size_sliding,thre)
print(sliding_step_2p)
np.save('NOEA_2p_sliding_50', sliding_step_2p)



# plt.plot(np.arange(0, crosstime_stdmean.shape[1]), crosstime_stdmean.mean(axis=0))
# plt.title("Cross-time-series of Mean of Std-FIN")
# plt.xlabel("time")
# plt.ylabel("Mean of std of cross time series")
# plt.savefig('Mean of std of cross time series_FIN')
# plt.show()

# print(np.mean(ts))

# ts=np.load('./origindata.csv')#change to your local path
# size_sliding=50
# print(ts.shape)

# thre=0.5
# mean_list, crosstime_stdmean =tsu.test_validity(ts,size_bw,size_sliding)
# #p#rint(mean_list)
# plt.hist(mean_list,bins=100)
# plt.title("Hist of Mean of Std coeff of (each time series)-FIN")
# plt.xlabel("Mean of Std coeff of (each time series)")
# plt.ylabel("Count")
# plt.savefig('plot_Hist of Mean of Std coeff of (each time series)_FIN')
# plt.show()

# plt.plot(np.arange(0, crosstime_stdmean.shape[1]), crosstime_stdmean.mean(axis=0))
# plt.title("Cross-time-series of Mean of Std-NOEA")
# plt.xlabel("time")
# plt.ylabel("Mean of std of cross time series")
# plt.savefig('Mean of std of cross time series_Fin')
# plt.show()

# print(np.mean(ts))


