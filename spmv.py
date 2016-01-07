import os, sys
from scipy.io.mmio import mminfo, mmread, mmwrite, MMFile
import scipy.io as sio
import numpy as np
from os import listdir
import glob
from scipy.sparse.base import *
from scipy.sparse.csr import *
from scipy.sparse.csc import *
from scipy.sparse.lil import *
from scipy.sparse.dok import *
from scipy.sparse.coo import *
from scipy.sparse.dia import *
from scipy.sparse.bsr import *
from scipy.sparse.construct import *
from scipy.sparse.extract import *

import csv
import math

from os.path import isfile, join
import timeit


def output(csv_writer, fname, r,c,nnz, time1, time2, time3, time4, time5, time6):
    timings = [[fname],[r],[c],[nnz],[time1],[time2],[time3],[time4],[time5],[time6]]
    length2 = len(timings[0])
    for y in range(length2):
        csv_writer.writerow([x[y] for x in timings])


#SpMV
def multiply(fname):
    mat = mmread(fname)
    rows, cols, nnzs = mminfo(fname)[0:3]
    vec = np.ones((rows,1), dtype=np.int)
    
    matcoo = mat.tocoo()
    start1 = timeit.default_timer()
    matcoo.dot(vec)
    stop1 = timeit.default_timer()
    t1 = (stop1 - start1)*math.pow(10,6)

    matcsr = mat.tocsr()
    start2 = timeit.default_timer()
    matcsr.dot(vec)
    stop2 = timeit.default_timer()
    t2 = (stop2 - start2)*math.pow(10,6)

    matcsc = mat.tocsc()
    start3 = timeit.default_timer()
    matcsc.dot(vec)
    stop3 = timeit.default_timer()
    t3 = (stop3-start3)*math.pow(10,6)
    

    matlil = mat.tolil()
    start4 = timeit.default_timer()
    matlil.dot(vec)
    stop4 = timeit.default_timer()
    t4 = (stop4 - start4)*math.pow(10,6)
    
    matdia = mat.todia()
    start5 = timeit.default_timer()
    matdia.dot(vec)
    stop5 = timeit.default_timer()
    t5 = (stop5-start5)*math.pow(10,6)
    
    
    matdok = mat.todok()
    start6 = timeit.default_timer()
    matdok.dot(vec)
    stop6 = timeit.default_timer()
    t6 = (stop6 - start6)*math.pow(10,6)
    
    return rows,cols,nnzs,t1,t2,t3,t4,t5,t6



testfile = open('SpMV.csv', 'wb')
csv_writer = csv.writer(testfile)
format = [['Matrix'],['No. of rows'],['No. of columns'],['No. of non-zeros'],['COO'],['CSR'],['CSC'],['LIL'],['DIA'],['DOK']]
length1 = len(format[0])
for y in range(length1):
    csv_writer.writerow([x[y] for x in format])

mypath = '/Users/nehapulipati/Documents/forpython/Matrices'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


for i in range(1,len(onlyfiles)):
    if onlyfiles[i] != 'spmv.py':
        name = onlyfiles[i]
        row, col, nnz, res1, res2, res3, res4, res5, res6 = multiply(name)
        
        output(csv_writer, name, row, col, nnz, res1,res2,res3,res4,res5,res6)





