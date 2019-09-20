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
meshI1 = []
meshI2 = []
meshI3 = []
meshI4 = []
meshI5 = []
coeff_matrix = [
[0.000270214471229482,0.0000807586376188975,0.0000439701000562218,0.0000303100748452958,0.0000231034113176958],
[0.000226660339850649,0.000267610484317059,0.0000714627156302221,0.0000410934140857493,0.0000288892983682616],
[0.0000469766856825697,0.0000923085238440956,0.000265139039369246,0.000129042608281353,0.0000544388573082632],
[0.0000333463398814744,.0000507815416448289,0.000108927613438887,0.000263359903011763,0.000106018215255542],
[0.0000258660273892805,0.0000352359162939813,0.0000552482075045511,0.000133483147049729,0.000265696001265904]
]
inv_coeff = np.linalg.inv(coeff_matrix)
print(inv_coeff)

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
def mean_fix(strIdx, mIdx, endIdx, dataList):
    mean = 0
    for idx in range(strIdx, mIdx, 1):
        mean = mean + dataList[idx] 
    mean = mean / (mIdx-strIdx)
    for idx in range(strIdx, endIdx, 1):
        dataList[idx] = dataList[idx] - mean
        
def hall_rearange():
    for idx  in range(len(data8Data)):
        if idx < 2300:
            data4Data[idx] = 0# hall? u2
            data5Data[idx] = 0# hall? u4
            data6Data[idx] = 0# hall? u5
            data7Data[idx] = 0# hall? u6
            data8Data[idx] = 0# hall? u1
        elif idx > 5740:
            data4Data[idx] = 0# hall? u2
            data5Data[idx] = 0# hall? u4
            data6Data[idx] = 0# hall? u5
            data7Data[idx] = 0# hall? u6
            data8Data[idx] = 0# hall? u1
        else:
            pass
    mean_fix(2300, 2347, 3617, data8Data)
    mean_fix(3617, 3626, 4361, data8Data)
    mean_fix(4361, 5286, 5740, data8Data)
    
    mean_fix(2300, 2330, 3617, data4Data)
    mean_fix(3617, 3626, 4361, data4Data)
    mean_fix(4361, 5286, 5740, data4Data)
    
    mean_fix(2300, 2330, 3617, data5Data)
    mean_fix(3617, 3626, 4361, data5Data)
    mean_fix(4361, 5286, 5740, data5Data)
    
    mean_fix(2300, 2330, 3617, data6Data)
    mean_fix(3617, 3626, 4361, data6Data)
    mean_fix(4361, 5286, 5740, data6Data)

    mean_fix(2300, 2330, 3617, data7Data)
    mean_fix(3617, 3626, 4361, data7Data)
    mean_fix(4361, 5286, 5740, data7Data)
    '''
    mean_fix(strIdx, mIdx, endIdx, data5Data)
    mean_fix(strIdx, mIdx, endIdx, data5Data)
    mean_fix(strIdx, mIdx, endIdx, data5Data)
    
    mean_fix(strIdx, mIdx, endIdx, data6Data)
    mean_fix(strIdx, mIdx, endIdx, data6Data)
    mean_fix(strIdx, mIdx, endIdx, data6Data)
    
    mean_fix(strIdx, mIdx, endIdx, data7Data)
    mean_fix(strIdx, mIdx, endIdx, data7Data)
    mean_fix(strIdx, mIdx, endIdx, data7Data)
    '''

def inverse_calc():

    for idx in range(len(data8Data)):
        hall = [data8Data[idx],data4Data[idx],data5Data[idx],data6Data[idx],data7Data[idx]] 
        temp = np.matmul(inv_coeff, hall)
        meshI1.append(temp[0])
        meshI2.append(temp[1])
        meshI3.append(temp[2])
        meshI4.append(temp[3])
        meshI5.append(temp[4])
if __name__ == "__main__":
    fileLoad()
    
    #plotLine(timeData, data1Data, "time [s]", ' ', "Command Ampere")
    
    plotLine(timeData, data2Data, "time [s]", ' ', "Shunt Voltage")
    plotLine(timeData, data3Data, "time [s]", ' ', "Raw Coil Voltage")
    #plotLine(timeData, data8Data, "time [s]", ' ', "Raw Hall1")
    #plotLine(timeData, data4Data, "time [s]", ' ', "Raw Hall2")
    #plotLine(timeData, data5Data, "time [s]", ' ', "Raw Hall4")
    #plotLine(timeData, data6Data, "time [s]", ' ', "Raw Hall5")
    #plotLine(timeData, data7Data, "time [s]", ' ', "Raw Hall6")
    
    hall_rearange()

    #plotLine(timeData, data8Data, "time [s]", ' ', "Hall1")
    #plotLine(timeData, data4Data, "time [s]", ' ', "Hall2")
    #plotLine(timeData, data5Data, "time [s]", ' ', "Hall4")
    #plotLine(timeData, data6Data, "time [s]", ' ', "Hall5")
    #plotLine(timeData, data7Data, "time [s]", ' ', "Hall6")
    #plotMultiLine(timeData, data4Data, data5Data, data6Data, data7Data, data8Data)
    inverse_calc()
    plotMultiLine(timeData, meshI1, meshI2, meshI3, meshI4, meshI5)