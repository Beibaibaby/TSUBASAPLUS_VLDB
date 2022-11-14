##import package
import numpy as np
import matplotlib.pyplot as plt
import math



def create_basic_window_matrix(ts_matrix,size_bw):
    num_ts = ts_matrix.shape[0]  # number of time series
    len_ts = ts_matrix.shape[1]  # length of time series
    num_bw = int(len_ts / size_bw)  # number of basic window
    length_pro=num_bw*size_bw
    ts_splited=ts_matrix[:, : length_pro].reshape((num_ts,num_bw,size_bw))
    return ts_splited
    #The return vaule here is a 3-d array: 1. num_ts 2.num_bs 3. size_bw

def sketch_computation_1(ts_splited):#function for computing sigma and delta
    sigma_matrix = np.zeros((ts_splited.shape[0],ts_splited.shape[1]))
    delta_matrix = np.zeros((ts_splited.shape[0], ts_splited.shape[1]))
    for i in range(ts_splited.shape[0]):
        mean=np.mean(ts_splited[i])
        for j in range (ts_splited.shape[1]):
            sigma_matrix[i,j]=np.std(ts_splited[i][j])
            delta_matrix[i,j]=np.mean(ts_splited[i][j])-mean
    return sigma_matrix, delta_matrix

def create_sliding_window_list(size_sliding,num_bs):
    start_s=0
    end_s=size_sliding
    sliding_window_list=[]
    while end_s<=num_bs:
        sliding_window_list.append(np.asarray([start_s,end_s]))
        start_s+=1
        end_s+=1
    return sliding_window_list

def test_validity(ts_matrix, size_bw,size_sliding):
    ts_splited = create_basic_window_matrix(ts_matrix,size_bw)
    num_bs=ts_splited.shape[1]
    mean_list = np.mean(ts_splited,axis=-1)
    list_std_of_mean=[]
    list_of_l2=[]
    sliding_window_list=create_sliding_window_list(size_sliding,num_bs)
    for i in range(mean_list.shape[0]):
        stdlist=[]
        l2=[]
        for sliding_window in sliding_window_list:
            std_of_this_sliding=np.std(mean_list[i][sliding_window[0]:sliding_window[1]])
            l2this=np.max(np.std(mean_list[i][sliding_window[0]:sliding_window[1]]))-np.min(np.std(mean_list[i][sliding_window[0]:sliding_window[1]]))
            l2.append(l2this)
        #range_of_sl = np.max(sliding_window)-np.max(sliding_window)
        #max_mean_range = np.max(abs([a-b for a,b in zip(mean_list[0], [sliding_window[0],sliding_window[1]])]))
            stdlist.append(std_of_this_sliding)
        
        list_std_of_mean.append(np.mean(np.asarray(stdlist)))
        #print(np.mean(np.asarray(stdlist)))
        list_of_l2.append(np.mean(np.asarray(l2)))
        #print(np.mean(np.asarray(l2)))
    return np.asarray(list_std_of_mean), np.asarray(list_of_l2)


def test_validity_check_time(ts_matrix, size_bw, size_sliding):
    ts_splited = create_basic_window_matrix(ts_matrix,size_bw)
    #Create the dataset you will work on
    #print(ts_splited.shape)
    num_bs=ts_splited.shape[1]#how many basic windows in one ts
    mean_list = np.mean(ts_splited,axis=-1)
    crosstimes_std_mean=[]
    sliding_window_list=create_sliding_window_list(size_sliding,num_bs)
    #for i in range(mean_list.shape[0]):
    for i in range(mean_list.shape[0]):
        list_std_of_mean=[]
        for sliding_window in sliding_window_list:
        #print(sliding_window)
            std_of_this_sliding=np.std(mean_list[i][sliding_window[0]:sliding_window[1]])
            #list_of_l2.append(np.max(np.std(mean_list[i][sliding_window[0]:sliding_window[1]]))-np.min(np.std(mean_list[i][sliding_window[0]:sliding_window[1]])))
            list_std_of_mean.append(np.mean(np.asarray(std_of_this_sliding)))
        crosstimes_std_mean.append(np.asarray(list_std_of_mean))
    return np.asarray(list_std_of_mean), np.asarray(crosstimes_std_mean)

def corr_pair(x,y):
    if x.shape != y.shape:
        raise Exception("Error, the time seris for correlation computation are in different shape")
    list=[]
    sigma_list_x = np.zeros(x.shape[0])
    delta_list_x=np.zeros(x.shape[0])
    sigma_list_y = np.zeros(x.shape[0])
    delta_list_y=np.zeros(x.shape[0])
    mean_x=np.mean(x)

    for i in range(x.shape[0]):
        sigma_list_x[i]=np.std(x[i])
        delta_list_x[i]=np.mean(x[i])-mean_x

    mean_y=np.mean(y)
    for i in range(y.shape[0]):
        sigma_list_y[i]=np.std(y[i])
        delta_list_y[i]=np.mean(y[i])-mean_y

    for i in range(x.shape[0]):
        corr=np.corrcoef(x[i],y[i])
        list.append(corr[0,1])

    cor_list=np.asarray(list)
    numerator=0
    denumerator_1=0
    denumerator_2=0
    for i in range(x.shape[0]):
        #print(sigma_list_x[i])
        numerator += (x[i].size *(sigma_list_x[i]*sigma_list_y[i]*cor_list[0] + delta_list_x[i]*delta_list_y[i]))
        denumerator_1 += x[i].size * (sigma_list_x[i]**2 + delta_list_x[i]**2)
        denumerator_2 += y[i].size * (sigma_list_y[i]**2 + delta_list_y[i]**2)

    denumerator_1=math.sqrt(denumerator_1)
    denumerator_2 =math.sqrt(denumerator_2)

    return np.asarray(numerator/(denumerator_1*denumerator_2))


def corr_pair_complete(x,y):
    if x.shape != y.shape:
        raise Exception("Error, the time seris for correlation computation are in different shape")
    list=[]
    sigma_list_x = np.zeros(x.shape[0])
    delta_list_x=np.zeros(x.shape[0])
    sigma_list_y = np.zeros(x.shape[0])
    delta_list_y=np.zeros(x.shape[0])
    mean_x=np.mean(x)
    for i in range(x.shape[0]):
        sigma_list_x[i]=np.std(x[i])
        delta_list_x[i]=np.mean(x[i])-mean_x

    mean_y=np.mean(y)
    for i in range(y.shape[0]):
        sigma_list_y[i]=np.std(y[i])
        delta_list_y[i]=np.mean(y[i])-mean_y

    for i in range(x.shape[0]):
        #print(x[i])
        corr=np.corrcoef(x[i],y[i])
        #print(corr)
        list.append(corr[0,1])

    cor_list=np.asarray(list)
    numerator=0
    denumerator_1=0
    denumerator_2=0
    for i in range(x.shape[0]):
        #print(sigma_list_x[i])
        numerator += (x[i].size *(sigma_list_x[i]*sigma_list_y[i]*cor_list[0] + delta_list_x[i]*delta_list_y[i]))
        denumerator_1 += x[i].size * (sigma_list_x[i]**2 + delta_list_x[i]**2)
        denumerator_2 += y[i].size * (sigma_list_y[i]**2 + delta_list_y[i]**2)

    denumerator_1=math.sqrt(denumerator_1)
    denumerator_2 =math.sqrt(denumerator_2)

    return np.asarray(numerator/(denumerator_1*denumerator_2)), cor_list



def corr_pair_query(x,y,starting,len_sliding):
    return corr_pair(x[starting:starting+len_sliding], y[starting:starting+len_sliding])



def jumping(x,y,t,size_sliding,thre):
    corr_ini=corr_pair_query(x,y,t,size_sliding)
    a,c = corr_pair_complete(x[t:t+size_sliding], y[t:t+size_sliding])
    if a>thre:
        print('jumped step', str(0))
        #print(a)
        #print(t)
        return 0

    for i in range(size_sliding):
        corr_ini+= (1 - c[i])/size_sliding
        if corr_ini>thre:
             print('jumped step',str(i))
             return i
    print('jumped step',str(size_sliding))
    return size_sliding


def jumping_high_low(x, y, t, size_sliding,thre):
    corr_ini = corr_pair_query(x, y, t, size_sliding)
    a, c = corr_pair_complete(x[t:t + size_sliding], y[t:t + size_sliding])
    if a < thre:
        for i in range(size_sliding):
            corr_ini += (1 - c[i]) / size_sliding
            if corr_ini > thre:
                print('jumped step', str(i))
                return i
        print('jumped step', str(size_sliding))
        return size_sliding
    elif a==thre:
        print('jumped step', str(0))
        return 0
    else:
        for i in range(size_sliding):
            corr_ini -= (1 + c[i]) / size_sliding
            if corr_ini < thre:
                print('jumped step', str(i))
                return i
        print('jumped step', str(size_sliding))
        return size_sliding

def binarySearch( low, high,c,corr_ini,thre,size_sliding):
    if low > high:
        print('jumped step',str(size_sliding))
        return size_sliding
    else:
        mid = int((low + high) / 2)
        corr=(mid-np.sum(c[:mid]))/size_sliding+corr_ini
        if corr > thre:
            print('jumped step',str(mid))
            return mid
        else:                          
            return binarySearch( low, mid-1,c,corr_ini,thre,size_sliding)

def jumping_bs_upper(x, y, t, size_sliding,thre):
    corr_ini=corr_pair_query(x,y,t,size_sliding)
    a,c = corr_pair_complete(x[t:t+size_sliding], y[t:t+size_sliding])
    if a>thre:
        print('jumped step', str(0))
        return 0
    k=binarySearch(0,size_sliding,c,corr_ini,thre,size_sliding)
    return k




def do_sliding(ts,size_bw,size_sliding,thre):
    basic_window_matrix = create_basic_window_matrix(ts, size_bw)
    time_len=basic_window_matrix.shape[1]-size_sliding+1
    correlation_matrix=np.zeros((basic_window_matrix.shape[1]-size_sliding+1,basic_window_matrix.shape[0],basic_window_matrix.shape[0]))
    for i in range(basic_window_matrix.shape[0]):
        for j in range(basic_window_matrix.shape[0]):
              if i!=j:
                  t = 0
                  x = basic_window_matrix[i]
                  y = basic_window_matrix[j]
                  while t <= time_len - 1:
                      jumped_step = jumping(x, y, t, size_sliding,thre)
                      if jumped_step == 0:
                          corr = corr_pair_query(x, y, t, size_sliding)
                          correlation_matrix[t, i, j] = corr
                          t = t + 1
                      else:
                          t = t + jumped_step
                          if t <= time_len - 1:
                              corr = corr_pair_query(x, y, t, size_sliding)
                              correlation_matrix[t, i, j] = corr
                          else:
                              break
              else:
                  correlation_matrix[:, i, j]=1


    return correlation_matrix


def do_sliding_hl(ts,size_bw,size_sliding,thre):
    basic_window_matrix = create_basic_window_matrix(ts, size_bw)
    time_len=basic_window_matrix.shape[1]-size_sliding+1
    correlation_matrix=np.zeros((basic_window_matrix.shape[1]-size_sliding+1,basic_window_matrix.shape[0],basic_window_matrix.shape[0]))
    for i in range(basic_window_matrix.shape[0]):
        with open('/u/yxu103/TSUBASAPLUS/logs/compute_hl_fin.txt', 'w') as f:
             f.write(str(i/basic_window_matrix.shape[0]))
        for j in range(basic_window_matrix.shape[0]):
            if i!=j:
                  t = 0
                  x = basic_window_matrix[i]
                  y = basic_window_matrix[j]
                  while t <= time_len - 1:
                      jumped_step = jumping_high_low(x, y, t, size_sliding,thre)
                      if jumped_step == 0:
                          corr = corr_pair_query(x, y, t, size_sliding)
                          correlation_matrix[t, i, j] = corr
                          t = t + 1
                      else:
                          t = t + jumped_step
                          if t <= time_len - 1:
                              corr = corr_pair_query(x, y, t, size_sliding)
                              correlation_matrix[t, i, j] = corr
                          else:
                              break
            else:
                  correlation_matrix[:, i, j]=1


    return correlation_matrix


def do_sliding_bs_upper(ts,size_bw,size_sliding,thre):
    basic_window_matrix = create_basic_window_matrix(ts, size_bw)
    time_len=basic_window_matrix.shape[1]-size_sliding+1
    correlation_matrix=np.zeros((basic_window_matrix.shape[1]-size_sliding+1,basic_window_matrix.shape[0],basic_window_matrix.shape[0]))
    for i in range(basic_window_matrix.shape[0]):
        for j in range(basic_window_matrix.shape[0]):
              if i!=j:
                  t = 0
                  x = basic_window_matrix[i]
                  y = basic_window_matrix[j]
                  while t <= time_len - 1:
                      jumped_step = jumping_bs_upper(x, y, t, size_sliding,thre)
                      if jumped_step == 0:
                          corr = corr_pair_query(x, y, t, size_sliding)
                          correlation_matrix[t, i, j] = corr
                          t = t + 1
                      else:
                          t = t + jumped_step
                          if t <= time_len - 1:
                              corr = corr_pair_query(x, y, t, size_sliding)
                              correlation_matrix[t, i, j] = corr
                          else:
                              break
              else:
                  correlation_matrix[:, i, j]=1


    return correlation_matrix





def do_sliding_gt(ts,size_bw,size_sliding):
    basic_window_matrix = create_basic_window_matrix(ts, size_bw)
    time_len=basic_window_matrix.shape[1]-size_sliding+1
    correlation_matrix=np.zeros((basic_window_matrix.shape[1]-size_sliding+1,basic_window_matrix.shape[0],basic_window_matrix.shape[0]))
    for i in range(basic_window_matrix.shape[0]):
        for j in range(basic_window_matrix.shape[0]):
              if i!=j:
                  t = 0
                  x = basic_window_matrix[i]
                  y = basic_window_matrix[j]
                  while t <= time_len - 1:
                              corr = corr_pair_query(x, y, t, size_sliding)
                              correlation_matrix[t, i, j] = corr
                              t=t+1

              else:
                  correlation_matrix[:, i, j]=1
    return correlation_matrix

