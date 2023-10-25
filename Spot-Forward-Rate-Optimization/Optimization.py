"""
This module includes a program that reads data from 'Spot_Forward_Raw_Data.txt' 
and go over through different investment strategies to find the optimized
strategy 

Functions
---------
Data_Path_Set:
    Retrieves the path of 'Spot_Forward_Raw_Data.txt'
ReadIn:
    Reads data from the txt file and stores it in arrays
StoreData:
    Fix the index issue of the ReadIn data
CalcDiff:
    Calculate the difference between spot rate and forward rate for certain currency
Ranking:
    Recursive function, using the ranking-based algorithm to return the result of
    different investment strategy
Plot:
    Plot the result of different investment strategies
Optimization:
    Traverse all investment strategies to return the optimized one
"""

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import os

#Initiate the array to store the data 
n = 21
SpotRate = [[0 for i in range(n)] for i in range(17)]
ForwardRate = [[0 for i in range(n)] for i in range(17)]
Diff = [[0 for i in range(n)] for i in range(17)]
Currency = ['AUD', 'NZD', 'JPY', 'CHF', 'GBP', 'EUR', 'CAD', 'SEK', 'NOK', 'ZAR', 'SGD', 'MXN', 'HKD', 'TRY', 'HUF', 'PLN', 'BRL', 'MYR', 'INR', 'IDR', 'CNY', 'PHP', 'KRW']

def Data_Path_Set():
    current_directory = os.path.dirname(__file__)
    return os.path.join(current_directory, 'Spot_Forward_Raw_Data.txt')

def ReadIn():
    file_path = Data_Path_Set()
    with open(file_path, "r") as f:
        cnt = 1
        
        for line in f.readlines():
            line = line.strip('\n') 
            ListData = line.split("\t")
            
            if(cnt<=17):
                StoreData(ListData,SpotRate,cnt%17)
                cnt += 1
            else:
                StoreData(ListData,ForwardRate,cnt%17)
                cnt += 1 

def StoreData(List,Data,Cnt):
    Data[Cnt-1] = List

def CalcDiff(Spot,Forward):
    for i in range(17):
        for j in range(n):
            if(ForwardRate[i][j]!=''):
                Diff[i][j] = (float(SpotRate[i][j])/float(ForwardRate[i][j])) - 1
        
def Ranking(ThresholdLong,ThresholdShort,Investment,Year):
    if(Year==16):
        return Investment
    else:
        DiffSort = [0 for i in range(0,n)]
        
        for i in range(n):
            DiffSort[i] = Diff[Year][i]
            
        DiffSort.sort()
        SumLong = 0
        InvestShort = Investment / 2
        InvestLong = InvestShort
        cntLong = 0
        
        for i in range(n):
            for j in range(ThresholdLong):
                if(DiffSort[j]>0):
                    break
                
                if(DiffSort[j]==Diff[Year][i] and DiffSort[j]<0):
                    cntLong += 1
                    
        if(cntLong==0):
            cntLong=1
            
        InvPerLong = InvestLong / cntLong
        
        for i in range(n):
            for j in range(ThresholdLong):
                if(DiffSort[j]>0):
                    break
                
                if(DiffSort[j]==Diff[Year][i] and DiffSort[j]<0):
                    SumLong += InvPerLong*(1+float(ForwardRate[Year][i])/float(SpotRate[Year+1][i])-1)

        SumShort = 0
        cntShort = 0
        
        for i in range(n):
            for j in range(n-1,n-1-ThresholdShort,-1):
                if(DiffSort[j]<0):
                    break
                
                if(DiffSort[j]==Diff[Year][i] and DiffSort[j]>0):
                    cntShort += 1
                    
        if(cntShort==0):
            cntShort=1
        
        InvPerShort = InvestShort / cntShort
        for i in range(n):
            for j in range(n-1,n-1-ThresholdShort,-1):
                if(DiffSort[j]<0):
                    break
                
                if(DiffSort[j]==Diff[Year][i] and DiffSort[j]>0):
                    SumShort += InvPerShort*(1+float(SpotRate[Year+1][i])/float(ForwardRate[Year][i])-1)    

        return Ranking(ThresholdLong,ThresholdShort,SumShort+SumLong,Year+1)

def Plot(A,B,C):
    # Creating dataset
    x = A
    y = B
    z = C
 
    # Creating figure
    fig = plt.figure(figsize = (10, 7))
    ax = plt.axes(projection ="3d")
 
    # Creating plot
    ax.scatter3D(x, y, z, color = "green")
    plt.title("simple 3D scatter plot")
    plt.show()
    
def Optimization():
    A = []
    B = []
    C = []
    
    Max_Return = 0
    LongT = 0
    ShortT = 0
    
    for i in range(1,21):
        for j in range(1,21):
            Gain = Ranking(i,j,10000,0)
            A.append(i)
            B.append(j)
            C.append(Gain)

            if(Gain>Max_Return):
                LongT=i
                ShortT=j
                Max_Return = Gain
                
    print(LongT,ShortT,Max_Return)
    
    Plot(A,B,C)

ReadIn()
CalcDiff(SpotRate,ForwardRate)
Optimization()






