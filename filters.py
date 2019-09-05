import os
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import butter, lfilter, filtfilt, freqz

cwd = os.getcwd()
dataFolderName = "coilV-201908"
dataFolder = os.path.join(cwd, dataFolderName)

timeData = []
voltageData = []
timeIdata = []
currentData = []

def meanFix(Ydata, cutIdx):
    mean = 0
    for idx in range(cutIdx):
        mean = mean + Ydata[idx]
    mean = mean / cutIdx
    print("\n\n%f\n\n" %(mean))
    for idx in range(len(Ydata)):
        Ydata[idx] = Ydata[idx] - mean

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
                        timeIdata.append(float(dataLine[0]))
                        currentData.append(float(dataLine[1]))
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
                        timeData.append(float(dataLine[0]))
                        voltageData.append(float(dataLine[1]))
                    except:
                        pass
            print("voltage time data size : ", end=" ")
            print(np.shape(timeData))
            print("voltage data size : ", end=" ")
            print(np.shape(voltageData))
            print("current time data size : ", end=" ")
            print(np.shape(timeIdata))
            print("current data size : ", end=" ")
            print(np.shape(currentData))
            f.close()
            break
        else:
            print('\n' + "!!!!Input Error!!!!" + '\n')
            pass 
    return file_name
        
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
    
def subplots2(X1Data, X2Data, Y1Data, Y2Data, Xlabel, Y1label, Y2label, title1, title2, xM_tick=1500, xm_tick=500):
    Xdata = X1Data
    X2data = X2Data
    YData = Y1Data
    filtered = Y2Data
    major_ticks = []
    minor_ticks = []
    for idx in range(len(Xdata)):
        if idx % xM_tick == 0:
            major_ticks.append(Xdata[idx])
        if idx % xm_tick == 0:
            minor_ticks.append(Xdata[idx])
    
    plt.subplot(2,1,1)
    #ax1.set_xticks(major_ticks)
    #ax1.set_xticks(minor_ticks, minor=True)
    
    plt.plot(Xdata, YData)
    plt.title(title1)
    plt.xlabel(Xlabel)
    plt.ylabel(Y1label)
    plt.grid()

    plt.subplot(2,1,2)
    #ax2.set_xticks(major_ticks)
    #ax2.set_xticks(minor_ticks, minor=True)
    
    plt.plot(X2data, filtered)
    plt.title(title2)
    plt.xlabel(Xlabel)
    plt.ylabel(Y2label)
    plt.grid()
    
    plt.subplots_adjust(hspace=0.5)
    plt.show()   

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    #y = lfilter(b, a, data)
    y = filtfilt(b, a, data)
    return y

def run_lowpass_filter(order, fs, cutoff, Xdata, Ydata, xM_tick, xm_tick):
    filtered = butter_lowpass_filter(Ydata, cutoff, fs, order)
    subplots2(Xdata, Xdata, Ydata, filtered, "Time [sec]", "Voltage [V]", "Voltage [V]", "Raw Data", \
        "LP Filtered Data", xM_tick, xm_tick)
    return filtered

def induced_voltage(Xdata, Ydata, inductance):
    indV = [0]
    for idx in range(len(Xdata)-1):
        deltaX = abs(Xdata[idx+1] - Xdata[idx])
        deltaY = Ydata[idx+1] - Ydata[idx] 
        voltage = inductance * deltaY / deltaX
        indV.append(voltage)
    return indV
    
class KalmanFilter():
    # REF
    # https://core.ac.uk/download/pdf/20641186.pdf
    def __init__(self, process_noise, sensor_noise, estimated_error, initial_value):
        self.q = process_noise # process noise covariance
        self.r = sensor_noise # measurement noise covariance
        self.x = estimated_error # value
        self.p = initial_value # estimation error covariance
        self.k = 0 # kalman gain

    def getFiltered(self, measurement):
        self.p = self.p + self.q
        self.k = self.p / (self.p + self.r)
        self.x = self.x + self.k * (measurement - self.x)
        self.p = (1-self.k)* self.p
        #print("P : %f K : %f X : %f " %(self.p, self.k, self.x))

        return self.x

    def setParameters(self, process_noise, sensor_noise, estimated_error):
        self.q = process_noise
        self.r = sensor_noise
        self.p = estimated_error

    def meanFix(self, filteredList):
        minData = 0
        #FIXME
        biasIdx = 23 # idx of the data list to move mean of the data
        for i in range(biasIdx):
            minData = minData + filteredList[i]
        minData = minData / biasIdx

        for idx, data in enumerate(filteredList):
            temp = data - minData
            filteredList[idx] = temp 

def run_kalman_filter(Xdata, Ydata, xM_tick, xm_tick, p_noise=0.125, s_noise=32, e_error=0, init_value=1023):
    kalman = KalmanFilter(p_noise, s_noise, e_error, init_value)
    filtered = []
    for data in voltageData:
        filteredMeasurement = kalman.getFiltered(data)
        filtered.append(filteredMeasurement) 
    #kalman.meanFix(filtered)    
    subplots2(Xdata, Xdata, Ydata, filtered, "Time [sec]", "Voltage [V]", "Voltage [V]", "Raw Data", \
        "Kalman Filtered Data", xM_tick, xm_tick)
    return filtered
    
if __name__ == "__main__":
    # Load data
    print("="*75+"\n\t\tINPUT VOLTAGE DATA\n"+"="*75)
    filename = fileLoad()
    print("="*75+"\n\t\tINPUT CURRENT DATA\n"+"="*75)
    filename2 = fileLoad()
    fs = 500
    if filename.count("currents") or filename.count("current"):
        meanFix(voltageData, 900)
    else:
        meanFix(voltageData, 9000)
        fs = 5000
    plotLine(xArr=timeData, yArr=voltageData, xLabel="Time [sec]", yLabel='Voltage [V]', title="Raw Data")
    
    # Low pass filter
    order = 5
    cutoff = 100
    lpFiltered = run_lowpass_filter(order=order, fs=fs, cutoff=cutoff, Xdata=timeData, Ydata=voltageData,\
        xM_tick=fs*5, xm_tick=fs)
    
    # Kalman filter
    p_noise = 0.000125 # 0.0125 for low ramping, 0.125 for 1A/sec 2A/sec
    s_noise = 64
    e_error = 0
    init_value = 1023
    kFiltered = run_kalman_filter(Xdata=timeData, Ydata=voltageData, xM_tick=fs*5, xm_tick=fs\
        ,p_noise=p_noise, s_noise=s_noise, e_error=e_error, init_value=init_value)
    
    # compare with induced voltage calculations
    inductance = 1.1668e-3
    inducedV = induced_voltage(Xdata=timeIdata, Ydata=currentData, inductance=inductance)
    subplots2(X1Data=timeData, X2Data=timeIdata, Y1Data=lpFiltered, Y2Data=inducedV, \
        Xlabel="Time [sec]", Y1label="Voltage [V]", Y2label="Voltage [V]", title1="Low-Pass Filter", title2="Induced Voltage")
    
    # show the difference btw RAW voltage and Induced Voltage Calculations
    diff = []
    for idx in range(len(timeData)):
        if idx == 10:
            pass
        elif idx % 10 == 0:
            iidx = int(idx/10)-1
            diff.append(voltageData[idx]-inducedV[iidx])
    print(np.shape(diff))
    plotLine(xArr=timeIdata, yArr=diff, xLabel="Time [sec]", yLabel='Voltage [V]', title="Difference btw RAW and Induced Calc.")    