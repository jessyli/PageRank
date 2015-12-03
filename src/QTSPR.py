__author__ = 'jessyli'
import numpy as np
from scipy.spatial import distance

import ReadingFile


def pagerank(comatrix, n):
    TC = ReadingFile.reading2("doc-topics.txt")

    comatrixtrans = comatrix.transpose()

    alpha = 0.2
    beta = 0.6
    gama = 0.2
    mindistance = 1e-5
    Tele = dict()
    for key in TC:
        Tele[key] = np.zeros(n)
        for value in TC.get(key):
            Tele[key][int(value)]=1.0/float(len(TC.get(key)))
    TPageRank = dict()
    Rvector = np.ones(n)*(1.0/n)
    P0 = Rvector
    for key in TC:
        TPageRank[key] = Rvector
        tempvector = TPageRank[key]
        TPageRank[key] = alpha*comatrixtrans*TPageRank[key]+beta*Tele[key]+gama*P0
        while(distance.euclidean(TPageRank[key], tempvector)>mindistance):
            tempvector = TPageRank[key]
            TPageRank[key] = alpha*comatrixtrans*TPageRank[key]+beta*Tele[key]+gama*P0
        # print(TPageRank[key].sum())
    return TPageRank

def query_topic(TPageRank, n):
    QTD = ReadingFile.reading3("query-topic-distro.txt")
    TSPR = dict()

    for key in QTD:
        TSPR[key] = np.zeros(n)
        for topic in range(0, len(QTD[key])-1):
            t = str(topic+1)
            TSPR[key] = float(QTD[key][topic])*TPageRank[t]+TSPR[key]
        # print("$$$$$$$$$$$$$$")
        # print(TSPR[key].sum())
    return TSPR

def query_topic2(TPageRank, n):
    QTD = ReadingFile.reading3("user-topic-distro.txt")
    TSPR = dict()

    for key in QTD:
        TSPR[key] = np.zeros(n)
        for topic in range(0, len(QTD[key])-1):
            t = str(topic+1)
            TSPR[key] = float(QTD[key][topic])*TPageRank[t]+TSPR[key]
        # print("$$$$$$$$$$$$$$")
        # print(TSPR[key].sum())
    return TSPR




def main():
    comatrix = ReadingFile.reading("transition.txt")
    n = comatrix.shape[0]
    TpageRank = pagerank(comatrix, n)
    TSPR = query_topic(TpageRank, n)
    UTSPR = query_topic2(TpageRank, n)
    with open("QTSPR-U2Q2-10.txt","w") as f:
        count = 1
        for item in TSPR['22']:
            temp = str(count) + " " + str(item)
            f.write("%s\n" % temp)
            count=count+1
    with open("PTSPR-U2Q2-10.txt","w") as f:
        count = 1
        for item in UTSPR['22']:
            temp = str(count) + " " + str(item)
            f.write("%s\n" % temp)
            count=count+1
if __name__ == "__main__": main()