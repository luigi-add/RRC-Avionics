import serial
import numpy
import matplotlib as plt
from drawnow import * # function for live graphs

# Definitions
com = 'COM4'
baud = 115200 # baudrate
to = 60 # timeout, s
nData = 3 # number of data points
ser = serial.Serial(com, baudrate = baud, timeout = to)
data = [0]*nData # initialize array of zeros for number of data points
plt.ion() # allows live data plots
maxP = 50; # max number of data points shown on graph
i = 0
j = 0

# Initilize Data Arrays
Lat1 = []; Lng1 = []; Spd1 = []; Sat1 = [];
Tmp1 = []; Prs1 = []; Alt1 = []; 
Acx1 = []; Acy1 = []; Acz1 = []; 
Gyx1 = []; Gyy1 = []; Gyz1 = [];
Mgx1 = []; Mgy1 = []; Mgz1 = []; t1 = [];

def makeFig(): # draws figures
    #plt.figure(1) # temp data
    #plt.ylim(20,30)
    #plt.title('Temp Data')
    #plt.grid(True)
    #plt.ylabel('Temp (C)')
    #plt.plot(Tmp1, 'r-')

    plt.figure(1) # accel data
    plt.ylim(-1.5,1.5)
    plt.title('Accel Data')
    plt.grid(True)
    plt.ylabel('Accel (g)')
    plt.plot(Acx1, 'b-', label='Accel_x')
    plt.plot(Acy1, 'r-', label='Accel_y')
    plt.plot(Acz1, 'g-', label='Accel_z')
    plt.legend(loc='upper right')

while 1: # main loop
    # [Lat, Long, Speed (knots), numSatellites, 
    # Temp (C), Pressure (Pa), Alt (m), AccelX (g), AccelY, AccelZ
    # GyroX (dps), GyroY, GyroZ, MagX (uT), MagY, MagZ, Time (ms)]
    
    while (ser.inWaiting() == 0): # waits for available data
        pass # do nothing
    for j in range(0,nData):
        Rdata = ser.readline().decode().strip('\r\n') # decodes data and removes \r\n delimiters
        Rdata = float(Rdata) # converts string readings to float
        data[j] = Rdata
        print(data)

    # Data separation into arrays

    Acx = data[0]; Acy = data[1]; Acz = data[2]; 
 

    # Appends arrays per loop

    Acx1.append(Acx); Acy1.append(Acy); Acz1.append(Acz); 
    

    drawnow(makeFig)
    plt.pause(0.00001) # required for drawnow
    i = i+1
    if (i > maxP): # deletes the first data points, shifting newer data over, results in moving graph

        Acx1.pop(0); Acy1.pop(0); Acz1.pop(0); 
  
