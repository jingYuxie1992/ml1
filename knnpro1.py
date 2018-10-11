# -*- coding: utf-8 -*-
"""
1.计算距离
2.排序
3.选点
4.计算频率
5.判断类别
"""
import numpy
import operator
import matplotlib 
import matplotlib.pyplot as plt
import os
from os import listdir

def classify0(inX,DataSet,labels,K):
    
    dataSetSize=DataSet.shape[0]
    
    diffmat=numpy.tile(inX,(dataSetSize,1))-DataSet
    
    sqdiffmat=diffmat**2
    
    sqDistance=sqdiffmat.sum(axis=1)
    
    sorteddistance=sqDistance.argsort()
    
    classcount={}
    
    for i in range(K):
    
        votellabel=labels[sorteddistance[i]]
        
        classcount[votellabel]=classcount.get(votellabel,0)+1
    
    sortclasscount=sorted(classcount.items(),key=operator.itemgetter(1),reverse=True)
    return sortclasscount[0][0] 

'''
读取文件
建立数据文件
1.读取打开
2.得到行数（矩阵维度）
3.创建numpy矩阵
4.解析文件
'''
def file2matrix(filename):

    fr = open(filename)

    array0lines=fr.readlines()

    
    number0flines=len(array0lines)
    
    returnmax=numpy.zeros((number0flines,3))
    
    classlabelsvector=[]

    index=0
    
    for line in array0lines:
        
        line= line.strip()
        
        listfromline=line.split('\t')

        returnmax[index,:]=listfromline[0:3]
        
        classlabelsvector.append((listfromline[-1]))
        
        index +=1
    
        
    return classlabelsvector ,returnmax 
    
    
'''
均值函数
'''
def autnorm(dataset):
    
    m=dataset.shape[0]
    
    minvals=dataset.min(0)
    
    maxvals=dataset.max(0)
    
    ranges=maxvals-minvals
    
    minvalsmatrix=numpy.tile(minvals,(m,1))
    
    normdata=(dataset-minvalsmatrix)/numpy.tile(ranges,(m,1))
    
    return normdata,ranges,minvals

'''
测试函数

'''

def datingClasstest():
    
    hoRatio=0.1
    
    datingdatelabels,datingdateMat=file2matrix('datingTestSet.txt')
    
    normdata,ranges,minvals=autnorm(datingdateMat)
    
    m=normdata.shape[0]
    
    numtestvec=int(hoRatio*m)
    
    errornum=0.0
    
    for i in range(numtestvec):
        classifierResult=classify0(normdata[i,:],normdata[numtestvec:m,:],datingdatelabels[numtestvec:m],3)
        
        print("the classifyfier came back with: " ,classifierResult)
        print("the real anwer ist: " ,datingdatelabels[i])
        
        if classifierResult !=datingdatelabels[i]:
            
            errornum +=1.0
            
    print("the total error rate is %f" % (errornum/float(numtestvec)))
    
def classifyperson():
    
    resultlist=['not at all','in small doses','in large doses']
    
    percenTats=float(input("Percentage of time spent playing video ganme?"))
    
    flymiles=float(input("flier miler?"))
    
    icecream=float(input("icecream?"))
    
    Inx=numpy.array([[flymiles,icecream,percenTats]])
    
    datingDatalabels,datingdataMat=file2matrix("datingTestSet2.txt")    
    
    normdata,Rangm,minvalllll=autnorm(datingdataMat)
    
    Inx=(Inx-minvalllll)/Rangm
    
    result=classify0(Inx,normdata,datingDatalabels,3)
    
    if  result =="1":
    
        print("the result ist",resultlist[0])

    if  result =="2":
    
        print("the result ist",resultlist[1])
   
    if  result =="3":
    
        print("the result ist",resultlist[2])
    
    return Inx,result

'''
手写字母识别
'''
def img2vector(filename):
    returnVect=numpy.zeros((1,1024))
    fr=open(filename)
    linestr=fr.readlines()
    for i in range(32):
        line=linestr[i]
        for j in range(32):
            returnVect[0,32*i+j]=line[j]
    return returnVect
    
    
    
    
def handwritingclasstest():
    
    hwlabels=[]
    
    trainingsfilelist=listdir('/Users/grid/trainingDigits')
    
    m=len(trainingsfilelist)
    
    traningsmat=numpy.zeros((m,1024))
    
    for i in range(m-1):
        os.chdir('/Users/grid/trainingDigits')
        filenamestr=trainingsfilelist[i+1]
        
        filestr=filenamestr.split('.')[0]
        
        classnumstr=filestr.split('_')[0]
        
        hwlabels.append(classnumstr)
        
        traningsmat[i,:]=img2vector(filenamestr)
    
    testfilelist=listdir('/Users/grid/testDigits')
    
    errorcount=0.0
    
    mTest=len(testfilelist)
    
    
    for i in range(mTest):
        filetestnamestr=testfilelist[i]
        
        fileteststr=filetestnamestr.split('.')[0]
        
        testclassnumerstr=fileteststr.split('_')[0]
        
        os.chdir('/Users/grid//testDigits')
        
        testvector=img2vector(filetestnamestr)
        
        classiferResult=classify0(testvector,traningsmat,hwlabels,10)
        
        print("Result is",classiferResult)
        print("the real answer is",testclassnumerstr)
        if  classiferResult != testclassnumerstr:
            errorcount +=1
            
    print("the total errorcount is ",errorcount)  
    print("the total error rate is : %f" %(errorcount/float(mTest)))
    
handwritingclasstest()
        

       