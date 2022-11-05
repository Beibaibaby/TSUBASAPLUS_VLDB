import numpy as np
tt=np.load('/u/yxu103/TSUBASAPLUS/output/fin_dataset.npy')
print(np.count_nonzero(~np.isnan(tt)))
print(tt.shape)
tt[np.isnan(tt)] = 0
np.save('/localdisk2/draco/tsubasa/fin_dataset',tt[:,:2000])



