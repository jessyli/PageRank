__author__ = 'jessyli'
import os
import timeit
import sys

import numpy as np
from scipy.sparse import coo_matrix


import GlobalPageRank
import QTSPR


def reading(filename):
    f = open(filename)
    row = []
    col = []
    data = []
    count = float(0)
    length =0
    temp = 1
    rowindex = np.zeros(81434)
    for lines in f.readlines():
        l = lines.split()
        rowindex.put(int(l[0]), 1)
        if(int(l[0])==temp):
            row.append(int(l[0]))
            col.append(int(l[1]))
            count=float(l[2])+count
            length=length+1

        else:
            tempdata = [1.0/count]*length
            data.extend(tempdata)
            row.append(int(l[0]))
            col.append(int(l[1]))
            temp = int(l[0])
            count=float(l[2])
            length=1


    data.append(count)

    rowsize = max(row)
    colsize = max(col)
    matrixsize = max(rowsize, colsize)
    rowindex2 = np.ones(matrixsize+1)
    rowindex3 = rowindex2-rowindex
    row.extend(rowindex3.nonzero()[0])
    col.extend(rowindex3.nonzero()[0])
    tempdata = [1.0]*len(rowindex3.nonzero()[0])
    data.extend(tempdata)
    comatrix = coo_matrix((data, (row, col)), shape=(matrixsize+1, matrixsize+1))



    return comatrix

def reading2(filename):
    f = open(filename)
    TC = dict()
    for lines in f.readlines():
        l = lines.split()
        if(l[1] in TC):
            TC[l[1]].append(l[0])
        else:

            TC[l[1]] = list()
            TC[l[1]].append(l[0])

    return TC

def reading3(filename):
    f = open(filename)
    QTD = dict()

    for lines in f.readlines():
        l = lines.split()
        a = l[0]+l[1]
        QTD[a] = list()
        for i in range(2,14):
            l1 = l[i].split(":")
            QTD[a].append(l1[1])
    return QTD

def reading4(n):
    fn = os.path.join(os.path.dirname(__file__), 'indri-lists/')
    # path = '/Users/jessyli/PycharmProjects/PageRank/indri-lists'
    Rank = dict()
    Score = dict()
    for filename in os.listdir(fn):
        name = str(filename)
        queryname = name.split(".")
        queryname2 = queryname[0].split("-")
        Rank[queryname2[0]+queryname2[1]] = np.zeros(n)
        Score[queryname2[0]+queryname2[1]] = np.zeros(n)
        stringpath = "indri-lists/"+filename
        with open(stringpath) as f:
            for lines in f.readlines():
                l = lines.split()
                np.put(Rank[queryname2[0]+queryname2[1]], int(l[2]), int(l[3]))
                np.put(Score[queryname2[0]+queryname2[1]],int(l[2]), float(l[4]))
    return Rank, Score

def WS_RPG():
    start = timeit.default_timer()
    comatrix = reading("transition.txt")
    n = comatrix.shape[0]
    (Rank, Score) = reading4(n)
    w1 = 0.5
    w2 = 0.5
    GPR = GlobalPageRank.GPR(comatrix)

    Tpagerank = QTSPR.pagerank(comatrix, n)
    QTS = QTSPR.query_topic(Tpagerank, n)
    PTS = QTSPR.query_topic2(Tpagerank, n)
    WS_SCORE = dict()
    WS_QTS = dict()
    WS_PTS = dict()
    CM_SCORE = dict()
    CM_QTS = dict()
    CM_PTS = dict()
    for key in Score:
        WS_SCORE[key]= Score[key]*w1+GPR*w2
        WS_QTS[key] = Score[key]*w1+QTS[key]*w2
        WS_PTS[key] = Score[key]*w1+PTS[key]*w2
        CM_SCORE[key] = Score[key]*GPR
        CM_QTS[key] = Score[key]*QTS[key]
        CM_PTS[key] = Score[key]*PTS[key]
    with open("indri-lists-WS.txt","w") as f:
        for key in Score:
            a = np.argsort(WS_SCORE[key])[::-1]

            que = str(int(key)/10)+"-" + str(int(key)%10)
            for i in range(0,500):
                temp = que + " " + "Q0"+" " + str(a[i]) + " " + str(i+1) + " " + str(WS_SCORE[key][a[i]])+ " "+ "indri"
                f.write("%s\n" % temp)
    stop = timeit.default_timer()
    print stop - start
def WS_QTS():
    start = timeit.default_timer()
    comatrix = reading("transition.txt")
    n = comatrix.shape[0]
    (Rank, Score) = reading4(n)
    w1 = 0.5
    w2 = 0.5
    GPR = GlobalPageRank.GPR(comatrix)

    Tpagerank = QTSPR.pagerank(comatrix, n)
    QTS = QTSPR.query_topic(Tpagerank, n)
    PTS = QTSPR.query_topic2(Tpagerank, n)
    WS_SCORE = dict()
    WS_QTS = dict()
    WS_PTS = dict()
    CM_SCORE = dict()
    CM_QTS = dict()
    CM_PTS = dict()
    for key in Score:
        WS_SCORE[key]= Score[key]*w1+GPR*w2
        WS_QTS[key] = Score[key]*w1+QTS[key]*w2
        WS_PTS[key] = Score[key]*w1+PTS[key]*w2
        CM_SCORE[key] = Score[key]*GPR
        CM_QTS[key] = Score[key]*QTS[key]
        CM_PTS[key] = Score[key]*PTS[key]
    with open("indri-lists-WS_QTS.txt","w") as f:
        for key in Score:
            a = np.argsort(WS_QTS[key])[::-1]

            que = str(int(key)/10)+"-" + str(int(key)%10)
            for i in range(0,500):
                temp = que + " " + "Q0"+" " + str(a[i]) + " " + str(i+1) + " " + str(WS_QTS[key][a[i]])+ " "+ "indri"
                f.write("%s\n" % temp)
    stop = timeit.default_timer()
    print stop - start
def WS_PTS():
    start = timeit.default_timer()
    comatrix = reading("transition.txt")
    n = comatrix.shape[0]
    (Rank, Score) = reading4(n)
    w1 = 0.5
    w2 = 0.5
    GPR = GlobalPageRank.GPR(comatrix)

    Tpagerank = QTSPR.pagerank(comatrix, n)
    QTS = QTSPR.query_topic(Tpagerank, n)
    PTS = QTSPR.query_topic2(Tpagerank, n)
    WS_SCORE = dict()
    WS_QTS = dict()
    WS_PTS = dict()
    CM_SCORE = dict()
    CM_QTS = dict()
    CM_PTS = dict()
    for key in Score:
        WS_SCORE[key]= Score[key]*w1+GPR*w2
        WS_QTS[key] = Score[key]*w1+QTS[key]*w2
        WS_PTS[key] = Score[key]*w1+PTS[key]*w2
        CM_SCORE[key] = Score[key]*GPR
        CM_QTS[key] = Score[key]*QTS[key]
        CM_PTS[key] = Score[key]*PTS[key]
    with open("indri-lists-WS_PTS.txt","w") as f:
        for key in Score:
            a = np.argsort(WS_PTS[key])[::-1]

            que = str(int(key)/10)+"-" + str(int(key)%10)
            for i in range(0,500):
                temp = que + " " + "Q0"+" " + str(a[i]) + " " + str(i+1) + " " + str(WS_PTS[key][a[i]])+ " "+ "indri"
                f.write("%s\n" % temp)
    stop = timeit.default_timer()
    print stop - start
def NS_RPG():
    start = timeit.default_timer()
    comatrix = reading("transition.txt")
    n = comatrix.shape[0]
    (Rank, Score) = reading4(n)
    w1 = 0.5
    w2 = 0.5
    GPR = GlobalPageRank.GPR(comatrix)
    Tpagerank = QTSPR.pagerank(comatrix, n)
    QTS = QTSPR.query_topic(Tpagerank, n)
    PTS = QTSPR.query_topic2(Tpagerank, n)
    WS_SCORE = dict()
    WS_QTS = dict()
    WS_PTS = dict()
    CM_SCORE = dict()
    CM_QTS = dict()
    CM_PTS = dict()
    for key in Score:
        WS_SCORE[key]= Score[key]*w1+GPR*w2
        WS_QTS[key] = Score[key]*w1+QTS[key]*w2
        WS_PTS[key] = Score[key]*w1+PTS[key]*w2
        CM_SCORE[key] = Score[key]*GPR
        CM_QTS[key] = Score[key]*QTS[key]
        CM_PTS[key] = Score[key]*PTS[key]
    with open("indri-lists-NS.txt","w") as f:
        for key in Score:
            a = np.argsort(GPR)[::-1]

            que = str(int(key)/10)+"-" + str(int(key)%10)
            for i in range(0,500):
                temp = que + " " + "Q0"+" " + str(a[i]) + " " + str(i+1) + " " + str(GPR[a[i]])+ " "+ "indri"
                # temp =  "Q0"+" " + str(a[i]) + " " + str(i+1) + " " + str(GPR[a[i]])+ " "+ "indri"
                f.write("%s\n" % temp)
    stop = timeit.default_timer()
    print stop - start
def NS_QTS():
    start = timeit.default_timer()
    comatrix = reading("transition.txt")
    n = comatrix.shape[0]
    (Rank, Score) = reading4(n)
    w1 = 0.5
    w2 = 0.5
    GPR = GlobalPageRank.GPR(comatrix)

    Tpagerank = QTSPR.pagerank(comatrix, n)
    QTS = QTSPR.query_topic(Tpagerank, n)
    PTS = QTSPR.query_topic2(Tpagerank, n)
    WS_SCORE = dict()
    WS_QTS = dict()
    WS_PTS = dict()
    CM_SCORE = dict()
    CM_QTS = dict()
    CM_PTS = dict()
    for key in Score:
        WS_SCORE[key]= Score[key]*w1+GPR*w2
        WS_QTS[key] = Score[key]*w1+QTS[key]*w2
        WS_PTS[key] = Score[key]*w1+PTS[key]*w2
        CM_SCORE[key] = Score[key]*GPR
        CM_QTS[key] = Score[key]*QTS[key]
        CM_PTS[key] = Score[key]*PTS[key]
    with open("indri-lists-NS_QTS.txt","w") as f:
        for key in Score:
            a = np.argsort(QTS[key])[::-1]

            que = str(int(key)/10)+"-" + str(int(key)%10)
            for i in range(0,500):
                temp = que + " " + "Q0"+" " + str(a[i]) + " " + str(i+1) + " " + str(QTS[key][a[i]])+ " "+ "indri"
                f.write("%s\n" % temp)
    stop = timeit.default_timer()
    print stop - start
def NS_PTS():
    start = timeit.default_timer()
    comatrix = reading("transition.txt")
    n = comatrix.shape[0]
    (Rank, Score) = reading4(n)
    w1 = 0.5
    w2 = 0.5
    GPR = GlobalPageRank.GPR(comatrix)

    Tpagerank = QTSPR.pagerank(comatrix, n)
    QTS = QTSPR.query_topic(Tpagerank, n)
    PTS = QTSPR.query_topic2(Tpagerank, n)
    WS_SCORE = dict()
    WS_QTS = dict()
    WS_PTS = dict()
    CM_SCORE = dict()
    CM_QTS = dict()
    CM_PTS = dict()
    for key in Score:
        WS_SCORE[key]= Score[key]*w1+GPR*w2
        WS_QTS[key] = Score[key]*w1+QTS[key]*w2
        WS_PTS[key] = Score[key]*w1+PTS[key]*w2
        CM_SCORE[key] = Score[key]*GPR
        CM_QTS[key] = Score[key]*QTS[key]
        CM_PTS[key] = Score[key]*PTS[key]
    with open("indri-lists-NS_PTS.txt","w") as f:
        for key in Score:
            a = np.argsort(PTS[key])[::-1]

            que = str(int(key)/10)+"-" + str(int(key)%10)
            for i in range(0,500):
                temp = que + " " + "Q0"+" " + str(a[i]) + " " + str(i+1) + " " + str(PTS[key][a[i]])+ " "+ "indri"
                f.write("%s\n" % temp)
    stop = timeit.default_timer()
    print stop - start
def CM_RPG():
    start = timeit.default_timer()
    comatrix = reading("transition.txt")
    n = comatrix.shape[0]
    (Rank, Score) = reading4(n)
    w1 = 0.5
    w2 = 0.5
    GPR = GlobalPageRank.GPR(comatrix)

    Tpagerank = QTSPR.pagerank(comatrix, n)
    QTS = QTSPR.query_topic(Tpagerank, n)
    PTS = QTSPR.query_topic2(Tpagerank, n)
    WS_SCORE = dict()
    WS_QTS = dict()
    WS_PTS = dict()
    CM_SCORE = dict()
    CM_QTS = dict()
    CM_PTS = dict()
    for key in Score:
        WS_SCORE[key]= Score[key]*w1+GPR*w2
        WS_QTS[key] = Score[key]*w1+QTS[key]*w2
        WS_PTS[key] = Score[key]*w1+PTS[key]*w2
        CM_SCORE[key] = Score[key]*GPR
        CM_QTS[key] = Score[key]*QTS[key]
        CM_PTS[key] = Score[key]*PTS[key]
    with open("indri-lists-NS.txt","w") as f:
        for key in Score:
            a = np.argsort(GPR)[::-1]

            que = str(int(key)/10)+"-" + str(int(key)%10)
            for i in range(0,500):
                temp = que + " " + "Q0"+" " + str(a[i]) + " " + str(i+1) + " " + str(GPR[a[i]])+ " "+ "indri"
                f.write("%s\n" % temp)
    stop = timeit.default_timer()
    print stop - start
def CM_QTS():
    start = timeit.default_timer()
    comatrix = reading("transition.txt")
    n = comatrix.shape[0]
    (Rank, Score) = reading4(n)
    w1 = 0.5
    w2 = 0.5
    GPR = GlobalPageRank.GPR(comatrix)

    Tpagerank = QTSPR.pagerank(comatrix, n)
    QTS = QTSPR.query_topic(Tpagerank, n)
    PTS = QTSPR.query_topic2(Tpagerank, n)
    WS_SCORE = dict()
    WS_QTS = dict()
    WS_PTS = dict()
    CM_SCORE = dict()
    CM_QTS = dict()
    CM_PTS = dict()
    for key in Score:
        WS_SCORE[key]= Score[key]*w1+GPR*w2
        WS_QTS[key] = Score[key]*w1+QTS[key]*w2
        WS_PTS[key] = Score[key]*w1+PTS[key]*w2
        CM_SCORE[key] = Score[key]*GPR
        CM_QTS[key] = Score[key]*QTS[key]
        CM_PTS[key] = Score[key]*PTS[key]
    with open("indri-lists-CM_QTS.txt","w") as f:
        for key in Score:
            a = np.argsort(WS_QTS[key])[::-1]

            que = str(int(key)/10)+"-" + str(int(key)%10)
            for i in range(0,500):
                temp = que + " " + "Q0"+" " + str(a[i]) + " " + str(i+1) + " " + str(CM_QTS[key][a[i]])+ " "+ "indri"
                f.write("%s\n" % temp)
    stop = timeit.default_timer()
    print stop - start
def CM_PTS():
    start = timeit.default_timer()
    comatrix = reading("transition.txt")
    n = comatrix.shape[0]
    (Rank, Score) = reading4(n)
    w1 = 0.5
    w2 = 0.5
    GPR = GlobalPageRank.GPR(comatrix)

    Tpagerank = QTSPR.pagerank(comatrix, n)
    QTS = QTSPR.query_topic(Tpagerank, n)
    PTS = QTSPR.query_topic2(Tpagerank, n)
    WS_SCORE = dict()
    WS_QTS = dict()
    WS_PTS = dict()
    CM_SCORE = dict()
    CM_QTS = dict()
    CM_PTS = dict()
    for key in Score:
        WS_SCORE[key]= Score[key]*w1+GPR*w2
        WS_QTS[key] = Score[key]*w1+QTS[key]*w2
        WS_PTS[key] = Score[key]*w1+PTS[key]*w2
        CM_SCORE[key] = Score[key]*GPR
        CM_QTS[key] = Score[key]*QTS[key]
        CM_PTS[key] = Score[key]*PTS[key]
    with open("indri-lists-CM_PTS.txt","w") as f:
        for key in Score:
            a = np.argsort(WS_PTS[key])[::-1]

            que = str(int(key)/10)+"-" + str(int(key)%10)
            for i in range(0,500):
                temp = que + " " + "Q0"+" " + str(a[i]) + " " + str(i+1) + " " + str(CM_PTS[key][a[i]])+ " "+ "indri"
                f.write("%s\n" % temp)
    stop = timeit.default_timer()
    print stop - start
if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname('/src/'), '..'))
    globals()[sys.argv[1]]()

