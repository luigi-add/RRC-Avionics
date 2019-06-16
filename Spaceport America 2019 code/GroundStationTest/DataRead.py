import serial
import struct, copy
import time
import pandas as pd
import os
import collections
file_dir = os.path.dirname(os.path.abspath(__file__))
csv_folder = 'dataFiles'
file_path = os.path.join(file_dir, csv_folder, 'csvData.csv')

# Reads bytes from serial
<<<<<<< HEAD
ser = serial.Serial('COM3', baudrate = 115200, timeout = 10) # open serial
=======
ser = serial.Serial('COM5', baudrate = 115200, timeout = 10) # open serial
>>>>>>> c7767873ddf91663d0fb58bd1cae97044935f15c
numData = 16 # numper of data points
dataNumBytes = 4 # byte size of each data point
rawData = bytearray(numData * dataNumBytes) # makes array for byte data, size = (numdata points)*(byte size)
dataType = 'f' # data type of data
dataList = []
dataString = []
csvData = []
plotLength = 100
#HEADER = ['Time (ms)', 'Latitude','Longitude','Speed (kt)',
#          'AccelX (g)','AccelY','AccelZ',
#          'GyroX (dps)','GyroY','GyroZ',
#          'MagX (uT)','MagY','MagZ',
#          'Temp (C)','Pressure (Pa)','Alt (m)']
        

for i in range(numData):   # give an array for each type of data and store them in a list
            dataList.append(collections.deque([0] * plotLength, maxlen=plotLength))
            dataString.append(collections.deque([0] * plotLength, maxlen=plotLength))
while 1:
    ser.readinto(rawData) # reads serial
    privateData = copy.deepcopy(rawData[:]) # makes copy of rawData
    for i in range(numData):
        data = privateData[(i*dataNumBytes):(dataNumBytes + i*dataNumBytes)] # slices array as there are 'dataNumBytes' bytes per 'numData' points 
        value, = struct.unpack(dataType, data)
        dataString[i].append(round(value,3))
        dataList[i].append(value) # makes data array
    x=[dataString[0][-1],dataString[1][-1],dataString[2][-1],
                   dataString[3][-1],dataString[4][-1],dataString[5][-1],
                   dataString[6][-1],dataString[7][-1],dataString[8][-1],
                   dataString[9][-1],dataString[10][-1],dataString[11][-1],
                   dataString[12][-1],dataString[13][-1],dataString[14][-1],
                   dataString[15][-1]]
    
    print(x)


    #csvData.append([dataList[0][-1],dataList[1][-1],dataList[2][-1],
    #                dataList[3][-1],dataList[4][-1],dataList[5][-1],
    #                dataList[6][-1],dataList[7][-1],dataList[8][-1],
    #                dataList[9][-1],dataList[10][-1],dataList[11][-1],
    #                dataList[12][-1],dataList[13][-1],dataList[14][-1],
    #                dataList[15][-1]])

    #df = pd.DataFrame(csvData) # data frame for saving to csv
    #df.to_csv(file_path, header=HEADER, index=False)