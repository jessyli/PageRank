__author__ = 'jessyli'
import numpy as np
from scipy.spatial import distance

import ReadingFile


def GPR(comatrix):

    comatrixtrans = comatrix.transpose()
    Rvector = np.ones(comatrixtrans.shape[0])*(1.0/comatrixtrans.shape[0])
    P0 = Rvector
    alpha = 0.1
    mindistance = 1e-5
    tempvector = Rvector
    Rvector = (1-alpha)*comatrixtrans*Rvector+alpha*P0
    count = 1
    while(distance.euclidean(Rvector, tempvector)>mindistance):
        tempvector = Rvector
        Rvector = (1-alpha)*comatrixtrans*Rvector+alpha*P0
        count=count+1
    return Rvector


def main():
    import sys
    print(sys.path)
    comatrix = ReadingFile.reading("transition.txt")
    Rvector = GPR(comatrix)
    with open("GPR-10.txt","w") as f:
        count = 1
        for item in Rvector:
            temp = str(count) + " " + str(item)
            f.write("%s\n" % temp)
            count=count+1


if __name__ == "__main__": main()
