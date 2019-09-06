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

#if __name__ is "__main__":
fileLoad()
plotLine(timeData, data1Data, "time [s]", ' ', "Data1")
plotLine(timeData, data2Data, "time [s]", ' ', "Data2")
plotLine(timeData, data3Data, "time [s]", ' ', "Data3")
plotLine(timeData, data4Data, "time [s]", ' ', "Data4")
plotLine(timeData, data5Data, "time [s]", ' ', "Data5")
plotLine(timeData, data6Data, "time [s]", ' ', "Data6")
plotLine(timeData, data7Data, "time [s]", ' ', "Data7")
plotLine(timeData, data8Data, "time [s]", ' ', "Data8")
plotLine(timeData, data9Data, "time [s]", ' ', "Data9")
plotLine(timeData, data10Data, "time [s]", ' ', "Data10")
plotLine(timeData, data11Data, "time [s]", ' ', "Data11")
plotLine(timeData, data12Data, "time [s]", ' ', "Data12")
plotLine(timeData, data13Data, "time [s]", ' ', "Data13")