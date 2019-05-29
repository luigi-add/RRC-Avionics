# source: https://www.thepoorengineer.com/en/python-gui/#gui

from threading import Thread
import serial
import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import copy
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as Tk
from tkinter.ttk import Frame
import pandas as pd


class serialPlot:
    def __init__(self, serialPort, serialBaud, plotLength, dataNumBytes, numData, IMU_numPlots):
        self.port = serialPort
        self.baud = serialBaud
        self.plotMaxLength = plotLength
        self.dataNumBytes = dataNumBytes
        self.numData = numData
        self.IMU_numPlots = IMU_numPlots
        self.rawData = bytearray(numData * dataNumBytes)
        self.dataType = None
        if dataNumBytes == 2:
            self.dataType = 'h'     # 2 byte integer
        elif dataNumBytes == 4:
            self.dataType = 'f'     # 4 byte float
        self.data = []              # for generic data
        self.dataList = []          # for csv saving
        for i in range(numData):   # give an array for each type of data and store them in a list
            self.data.append(collections.deque([0] * plotLength, maxlen=plotLength))
            self.dataList.append(collections.deque([0] * plotLength, maxlen=plotLength))
        self.isRun = True
        self.isReceiving = False
        self.thread = None
        self.plotTimer = 0
        self.previousTimer = 0
        self.csvMax = 5000000

        # File initialization
        self.file_dir = os.path.dirname(os.path.abspath(__file__))
        self.csv_folder = 'data files'
        self.file_path = os.path.join(self.file_dir, self.csv_folder, 'csvData.csv')
        self.HEADER = ['Time (ms)', 'Latitude','Longitude','Speed (kt)',
                       'AccelX (g)','AccelY','AccelZ',
                       'GyroX (dps)','GyroY','GyroZ',
                       'MagX (uT)','MagY','MagZ',
                       'Temp (C)','Pressure (Pa)','Alt (m)']
        self.csvData = []

        print('Trying to connect to: ' + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')
        try:
            self.serialConnection = serial.Serial(serialPort, serialBaud, timeout=4)
            print('Connected to ' + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')
        except:
            print("Failed to connect with " + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')

    def readSerialStart(self):
        if self.thread == None:
            self.thread = Thread(target=self.backgroundThread)
            self.thread.start()
            # Block till we start receiving values
            while self.isReceiving != True:
                time.sleep(0.1)

    def getIMUData(self, frame, lines, lineValueText, lineLabel, timeText, byteIndex):
        currentTimer = time.process_time()
        self.plotTimer = int((currentTimer - self.previousTimer) * 1000)     # the first reading will be erroneous
        self.previousTimer = currentTimer
        timeText.set_text('Plot Interval = ' + str(self.plotTimer) + 'ms')
        privateData = copy.deepcopy(self.rawData[:])    # so that the 3 values in our plots will be synchronized to the same sample time
        for i in range(self.IMU_numPlots):
            data = privateData[(i*self.dataNumBytes + byteIndex):(self.dataNumBytes + i*self.dataNumBytes + byteIndex)]
            value,  = struct.unpack(self.dataType, data)
            self.data[i].append(value)    # we get the latest data point and append it to our array
            lines[i].set_data(range(self.plotMaxLength), self.data[i])
            lineValueText[i].set_text('[' + lineLabel[i] + '] = ' + str(value))
        self.saveCSV()

    def saveCSV(self):
        privateData = copy.deepcopy(self.rawData[:])
        for i in range(self.numData):
            data = privateData[(i*self.dataNumBytes):(self.dataNumBytes + i*self.dataNumBytes)]
            value,  = struct.unpack(self.dataType, data)
            self.dataList[i].append(value)
        self.csvData.append([self.dataList[0][-1],self.dataList[1][-1],self.dataList[2][-1],
                             self.dataList[3][-1],self.dataList[4][-1],self.dataList[5][-1],
                             self.dataList[6][-1],self.dataList[7][-1],self.dataList[8][-1],
                             self.dataList[9][-1],self.dataList[10][-1],self.dataList[11][-1],
                             self.dataList[12][-1],self.dataList[13][-1],self.dataList[14][-1],
                             self.dataList[15][-1]])
        df = pd.DataFrame(self.csvData)
        df.to_csv(self.file_path, header=self.HEADER, index=False)
        print(len(self.csvData))
        if (len(self.csvData) > self.csvMax): # only saves the last x amount of data
            self.csvData = []

    def backgroundThread(self):    # retrieve data
        time.sleep(1.0)  # give some buffer time for retrieving data
        self.serialConnection.reset_input_buffer()
        while (self.isRun):
            self.serialConnection.readinto(self.rawData)
            self.isReceiving = True
            #print(self.rawData)

    def close(self):
        self.isRun = False
        self.thread.join()
        self.serialConnection.close()
        print('Disconnected...')



class Window(Frame):
    def __init__(self, figure, master, SerialReference):
        Frame.__init__(self, master)
        self.entry = None
        self.setPoint = None
        self.master = master        # a reference to the master window
        self.serialReference = SerialReference      # keep a reference to our serial connection so that we can use it for bi-directional communicate from this class
        self.initWindow(figure)     # initialize the window with our settings

    def initWindow(self, figure):
        self.master.title("Real Time Plot")
        canvas = FigureCanvasTkAgg(figure, master=self.master)
        toolbar = NavigationToolbar2Tk(canvas, self.master)
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        lbl1 = Tk.Label(self.master, text="Scaling Factor")
        lbl1.pack(padx=5, pady=5)
        self.entry = Tk.Entry(self.master)
        self.entry.insert(0, '1.0')     # (index, string)
        self.entry.pack(padx=5)
        SendButton = Tk.Button(self.master, text='Send', command=self.sendFactorToMCU)
        SendButton.pack(padx=5)



def main():
    portName = 'COM4'
    # portName = '/dev/ttyUSB0'
    baudRate = 115200
    maxPlotLength = 100     # number of points in x-axis of real time plot
    dataNumBytes = 4        # number of bytes of 1 data point
    numData = 16            # number of data points
    IMU_numPlots = 3            # number of plots in 1 graph
    s = serialPlot(portName, baudRate, maxPlotLength, dataNumBytes, numData, IMU_numPlots)   # initializes all required variables
    s.readSerialStart()                                               # starts background thread

    # plotting starts below
    pltInterval = 50    # Period at which the plot animation updates [ms]
    xmin = 0
    xmax = maxPlotLength
    ymin = -(16)
    ymax = 16
    fig = plt.figure(figsize=(10, 8))
    ax = plt.axes(xlim=(xmin, xmax), ylim=(float(ymin - (ymax - ymin) / 10), float(ymax + (ymax - ymin) / 10)))
    ax.set_title('Arduino Accelerometer')
    ax.set_xlabel("Time")
    ax.set_ylabel("Accelerometer Output")

    # put our plot onto Tkinter's GUI
    root = Tk.Tk()
    app = Window(fig, root, s)

    lineLabel = ['X', 'Y', 'Z']
    style = ['r-', 'c-', 'b-']  # linestyles for the different plots
    timeText = ax.text(0.70, 0.95, '', transform=ax.transAxes)
    lines = []
    lineValueText = []
    byteIndex = 16
    for i in range(IMU_numPlots):
        lines.append(ax.plot([], [], style[i], label=lineLabel[i])[0])
        lineValueText.append(ax.text(0.70, 0.90-i*0.05, '', transform=ax.transAxes))
    anim = animation.FuncAnimation(fig, s.getIMUData, fargs=(lines, lineValueText, lineLabel, timeText, byteIndex), interval=pltInterval)    # fargs has to be a tuple
    
    plt.legend(loc="upper left")



    root.mainloop()   # use this instead of plt.show() since we are encapsulating everything in Tkinter

    s.close()


if __name__ == '__main__':
    main()
