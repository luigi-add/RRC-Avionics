import serial
import csv
from DataRead import * # imports function for data readings

# Definitions
com = 'COM5'
baud = 115200 # baudrate
to = 60 # timeout, s
nData = 17 # number of data points
Header = ['Lat', 'Long', 'Spd (knots)', 'nSat',
          'Temp (C)','Pressure (Pa)','Alt (m)',
          'AccelX (g)','AccelY','AccelZ',
          'GyroX (dps)', 'GyroY', 'GyroZ',
          'MagX (uT)', 'MagY', 'MagZ', 'Time (ms)']


with open('dataList.csv', 'w') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(Header)
    while 1:
     
        data = DataRead(com, baud, to, nData)
        print(data)
        csv_writer.writerow(data)
        csvfile.flush()