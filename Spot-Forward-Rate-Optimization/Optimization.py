from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
n = 21
LL = []
SS = []
SpotRate = [[0 for i in range(n)] for i in range(17)]
ForwardRate = [[0 for i in range(n)] for i in range(17)]
Diff = [[0 for i in range(n)] for i in range(17)] #The difference between spot and forward for each currency
Currency = ['AUD', 'NZD', 'JPY', 'CHF', 'GBP', 'EUR', 'CAD', 'SEK', 'NOK', 'ZAR', 'SGD', 'MXN', 'HKD', 'TRY', 'HUF', 'PLN', 'BRL', 'MYR', 'INR', 'IDR', 'CNY', 'PHP', 'KRW']
def ReadIn():
    with open("/Users/chenpeter/Desktop/Application/Transfer/Research/Book2.txt", "r") as f:
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
        LL.append([])
        SS.append([])
        DiffSort = [0 for i in range(0,n)]
        for i in range(n):
            DiffSort[i] = Diff[Year][i]
        DiffSort.sort()
        SumLong = 0
        for i in range(n):
            for j in range(ThresholdLong):
                if(DiffSort[j]>0):
                    break
                if(DiffSort[j]==Diff[Year][i] and DiffSort[j]<0):
                    SumLong += float(ForwardRate[Year][i])/float(SpotRate[Year+1][i])-1
                    LL[Year].append(i)
        #print(SumLong)
        SumShort = 0
        for i in range(n):
            for j in range(n-1,n-1-ThresholdShort,-1):
                if(DiffSort[j]<0):
                    break
                if(DiffSort[j]==Diff[Year][i] and DiffSort[j]>0):
                    SumShort += float(SpotRate[Year+1][i])/float(ForwardRate[Year][i])-1
                    SS[Year].append(i)
        InvestShort = Investment / 2
        InvestLong = InvestShort
        Investment = InvestShort*(1+SumShort)+InvestLong*(1+SumLong)
        return Ranking(ThresholdLong,ThresholdShort,Investment,Year+1)

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
 
    # show plot
    plt.show()
    
def Optimization():
    A = []
    B = []
    C = []
    Max_Return = 0
    LongT = 0
    ShortT = 0
    for i in range(21):
        for j in range(21):
            Gain = Ranking(i,j,10000,0)
            A.append(i)
            B.append(j)
            C.append(Gain)
            #print(i,j,Gain)
            if(Gain>Max_Return):
                LongT=i
                ShortT=j
                Max_Return = Gain
    print(LongT,ShortT,Max_Return)
    Plot(A,B,C)
ReadIn()
CalcDiff(SpotRate,ForwardRate)
#Optimization()
Ranking(4,6,10000,0)
print(SS)



