import serial
import struct, copy
import time
import pandas as pd
import os
import collections
file_dir = os.path.dirname(os.path.abspath(__file__))
csv_folder = 'csv files'
file_path = os.path.join(file_dir, csv_folder, 'csvData.csv')

# Reads bytes from serial
ser = serial.Serial('COM4', baudrate = 115200, timeout = 10) # open serial
numData = 16 # numper of data points
dataNumBytes = 4 # byte size of each data point
rawData = bytearray(numData * dataNumBytes) # makes array for byte data, size = (numdata points)*(byte size)
dataType = 'f' # data type of data
dataList = []
csvData = []
plotLength = 100
HEADER = ['Time (ms)', 'Latitude','Longitude','Speed (kt)',
          'AccelX (g)','AccelY','AccelZ',
          'GyroX (dps)','GyroY','GyroZ',
          'MagX (uT)','MagY','MagZ',
          'Temp (C)','Pressure (Pa)','Alt (m)']
        

for i in range(numData):   # give an array for each type of data and store them in a list
            dataList.append(collections.deque([0] * plotLength, maxlen=plotLength))
while 1:
    ser.readinto(rawData) # reads serial
    privateData = copy.deepcopy(rawData[:]) # makes copy of rawData
    for i in range(numData):
        data = privateData[(i*dataNumBytes):(dataNumBytes + i*dataNumBytes)] # slices array as there are 'dataNumBytes' bytes per 'numData' points 
        value, = struct.unpack(dataType, data)
        print(value)
        dataList[i].append(value) # makes data array


    csvData.append([dataList[0][-1],dataList[1][-1],dataList[2][-1],
                    dataList[3][-1],dataList[4][-1],dataList[5][-1],
                    dataList[6][-1],dataList[7][-1],dataList[8][-1],
                    dataList[9][-1],dataList[10][-1],dataList[11][-1],
                    dataList[12][-1],dataList[13][-1],dataList[14][-1],
                    dataList[15][-1]])

    df = pd.DataFrame(csvData) # data frame for saving to csv
    df.to_csv(file_path, header=HEADER, index=False)