import os
import sys
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import butter, lfilter, filtfilt, freqz

cwd = os.getcwd()
dataFolderName = "20190830"
dataFolder = os.path.join(cwd, dataFolderName)

timeData = []
data1Data = [] # current input (by command?)
data2Data = [] # shunt
data3Data = [] # coil voltage (maybe)
data4Data = [] # hall? u2
data5Data = [] # hall? u4
data6Data = [] # hall? u5
data7Data = [] # hall? u6
data8Data = [] # hall? u1
data9Data = []  # temp (deprecated)
data10Data = [] # temp (deprecated)
data11Data = [] # temp (deprecated)
data12Data = [] # temp (deprecated)
data13Data = [] # temp (deprecated)
hallData = []

coeff_matrix = [
    [4.9139e3,   -1.3941e3,   -0.2682e3,   -0.1720e3,   -0.0949e3,   -0.1485e3],
   [-3.4375e3,    5.6612e3,   -0.9794e3,   -0.1594e3,  -0.0763e3,   -0.0875e3],
    [1.2155e3,   -3.5242e3,    5.6534e3,   -1.1425e3,   -0.2120e3,   -0.1898e3],
   [-0.8416e3,    1.6780e3,  -4.2991e3,    5.6978e3,  -0.8802e3,   -0.2511e3],
    [0.3409e3,   -1.0833e3,    2.0590e3,   -3.9891e3,    5.5089e3,   -1.1651e3],
   [-0.2400e3,   0.3329e3,   -1.0053e3,    1.4199e3,   -3.2652e3,    4.7195e3],
]

def plotLine(xArr, yArr, xLabel, yLabel, title, *args):
    argsList = []
    for arg in args:
        argsList.append(arg)
    
    _fig, ax = plt.subplots()
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.plot(xArr, yArr)
    plt.title(title)
    plt.grid()
    plt.show()
    
def plotMultiLine(xArr, *args):
    strList = []
    dataList = []
    for arg in args:
        if type(arg) == str:
            strList.append(arg)
        elif type(arg) == list:
            dataList.append(arg)
    _fig, ax = plt.subplots()
    try:
        ax.set_xlabel(strList[0])
        ax.set_ylabel(strList[1])
        plt.title(strList[2])
    except IndexError:
        pass
    for yArr in dataList:
        ax.plot(xArr, yArr)
    plt.grid()
    plt.show()    

def fileLoad():
    relPath = "./"+dataFolderName
    while(True):
        print('\n\n' + "="*75)
        file_name = input("\n\n\t\tChoose Raw Data\n\tex]test_0.1 (*NO .txt!)\n\n")
        file_name = file_name + ".txt"
        filePath = os.path.join(dataFolder, file_name)
        relFilePath =  os.path.join(relPath, file_name)
        print(filePath)
        if os.path.isfile(filePath) is True:
            print("File : %s LOADED" %(file_name))
            f = open(relFilePath, "r")
            _lineTrash = f.readline()
            if file_name.count("currents"):
                while True:
                    line = f.readline()
                    if not line:
                        break
                    try:
                        line = line.strip()
                        dataLine = line.split()
                        timeData.append(float(dataLine[1])/1000)
                        data1Data.append(float(dataLine[2]))
                        data2Data.append(float(dataLine[3])*-1e4)
                        data3Data.append(float(dataLine[4]))
                        data4Data.append(float(dataLine[5]))
                        data5Data.append(float(dataLine[6]))
                        data6Data.append(float(dataLine[7]))
                        data7Data.append(float(dataLine[8]))
                        data8Data.append(float(dataLine[9]))
                        data9Data.append(float(dataLine[10]))
                        data10Data.append(float(dataLine[11]))
                        data11Data.append(float(dataLine[12]))
                        data12Data.append(float(dataLine[13]))
                        data13Data.append(float(dataLine[14]))
                    except:
                        pass        
            else:        
                while True:
                    line = f.readline()
                    if not line:
                        break
                    try:
                        line = line.strip()
                        dataLine = line.split()
                        timeData.append(float(dataLine[1])/1000)
                        data1Data.append(float(dataLine[2]))
                        data2Data.append(float(dataLine[3])*-1e4)
                        data3Data.append(float(dataLine[4]))
                        data4Data.append(float(dataLine[5]))
                        data5Data.append(float(dataLine[6]))
                        data6Data.append(float(dataLine[7]))
                        data7Data.append(float(dataLine[8]))
                        data8Data.append(float(dataLine[9]))
                        data9Data.append(float(dataLine[10]))
                        data10Data.append(float(dataLine[11]))
                        data11Data.append(float(dataLine[12]))
                        data12Data.append(float(dataLine[13]))
                        data13Data.append(float(dataLine[14]))
                    except:
                        pass
            print("voltage time data size : ", end=" ")
            print(np.shape(timeData))
            print("voltage data size : ", end=" ")
            print(np.shape(data4Data))
            f.close()
            break
        else:
            print('\n' + "!!!!Input Error!!!!" + '\n')
            pass 
    return file_name

def hall_rearange():
    for idx  in range(len(data8Data)):
        temp = []
        temp.append(data8Data[idx]) # hall? u1
        temp.append(data4Data[idx]) # hall? u2
        temp.append(data5Data[idx]) # hall? u4
        temp.append(data6Data[idx]) # hall? u5
        temp.append(data7Data[idx]) # hall? u6
        hallData.append(temp)

if __name__ == "__main__":
    fileLoad()
    hall_rearange()
    #plotLine(timeData, data1Data, "time [s]", ' ', "Data1")
    plotLine(timeData, data2Data, "time [s]", ' ', "Data2")
    #plotLine(timeData, data3Data, "time [s]", ' ', "Data3")
    plotLine(timeData, data4Data, "time [s]", ' ', "Data4")
    plotLine(timeData, data5Data, "time [s]", ' ', "Data5")
    plotLine(timeData, data6Data, "time [s]", ' ', "Data6")
    plotLine(timeData, data7Data, "time [s]", ' ', "Data7")
    plotLine(timeData, data8Data, "time [s]", ' ', "Data8")
    
    plotMultiLine(timeData, data4Data, data5Data, data6Data, data7Data, data8Data)