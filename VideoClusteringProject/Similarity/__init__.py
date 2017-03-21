from sklearn import *
import numpy as np
from scipy.cluster.hierarchy import complete, fcluster
f = open("DAudioM_V1.out","r")
i=0
D = np.zeros((198,198))
for line in f:
    s = line[:-1].split("\t")
    #print s
    for j in range(0,len(s)):
        D[i][j] = float(s[j])
    i = i + 1

X = complete(D)

Result= fcluster(X,3)
print Result

