from tkinter import *
import tkinter.messagebox
import tkinter.font as tkfont
from time import sleep
import os, sys, random, socket

sys.path.append("..")
from PIL import ImageTk, Image, ImageDraw
import time
import src.GPSMap as GPSMap, src.Status as Status, src.System_Plots as System_Plots, src.serialCOM as serialCOM, src.LEDfunc as LEDfunc, src.DataSave as DataSave
import threading
from queue import Queue

'''

    This class is used to display the main window

'''
# resolution of the screen
height = 480
width = 320
statusBackGround = 'cyan'

# Threading options
threadLock = threading.Lock()
queue = Queue()

# Serial options
baudRate = 57600


class Display:
    
    
    # ***************** Instantiate *****************
    def __init__(self, master):
        self.__master = master
        # Set window parameters
        self.__master.resizable(width=False, height=False)
        self.__master.geometry('{}x{}'.format(height, width))
        #self.__master.update_idletasks()
        # To make window borderless
        self.__master.overrideredirect(True)

        #Set up data saving to files
        self.__dataList = serialCOM.Data()

        #File saver to save data
        self.__filesaver=DataSave.DataSave()

        #Craete setup gpio pins for LEDs
        LEDfunc.setupLED()

        LEDfunc.redLED(1)

        # Make serial object
        self.__serialData = serialCOM.SerialCom(baudRate, 'ttyS0',self.__dataList,self.__filesaver)

        #Place main frame where items are to be displayed on
        self.__placeMainFrame()

        #Start LED flash cycle
        self.__cycleCounter = 0
        self.__flashCycle()
    
        # Load compass image and render image
        load = Image.open(os.path.dirname(os.path.realpath(__file__)) + "/../appImages/rocketry.png")
        load.thumbnail(size=(220, 435))
        render = ImageTk.PhotoImage(load)

        self.__img = Label(self.__mainFrame, image=render, bg=statusBackGround)
        self.__img.image = render
        self.__img.pack()

        self.__printLabel()
        self.__statusBar()
        self.__startDataThread()
        self.__keepThreadAlive()

    def __flashCycle(self):        
        if self.__cycleCounter == 4:
            self.__cycleCounter = 0

        switch = [1,1,1,1]

        switch[self.__cycleCounter] = 0

        LEDfunc.rgbLED(switch)

        self.__cycleCounter += 1
        time = 5000/(1+(2.5)**(self.__cycleCounter - 2)) + 300
        #print("Time LED:  "+str(time))
        self.__master.after(int(time),self.__flashCycle)

    def __startDataThread(self):
        self.__thread = self.__serialData.startThread(self.__dataList)

    def __keepThreadAlive(self):
        print("Restarting data receive thread")
        self.__serialData = serialCOM.SerialCom(baudRate, 'ttyS0',self.__dataList,self.__filesaver)
        if not self.__thread.is_alive():
            self.__thread = self.__serialData.startThread(self.__dataList)
        self.__master.after(100,self.__keepThreadAlive)

    def __placeMainFrame(self):
        self.__mainFrame = Frame(self.__master, height=220, width=475, bg=statusBackGround)
        self.__mainFrame.pack_propagate(False)
        self.__mainFrame.place(x=4, y=22)

    # ***************** Print the time label *****************

    def __printLabel(self):
        # Print label of time and time of last received message
        self.__timeFrame = Frame(self.__master)
        self.__timeFrame.pack(side=TOP)
        self.__time = Label(self.__timeFrame)
        self.__time.config(bd=1, relief=SUNKEN, width=54)
        self.__time.bind("<ButtonPress-1>", lambda ev: self.__homeReturn())
        self.__time.pack_propagate(False)
        self.__time.pack(side=RIGHT, anchor=NE, padx=3)

        def LEDexit(ev):
            LEDfunc.cleanUp()
            os._exit(0)

        self.__exit = Label(self.__timeFrame,text="X",bg="red",relief=RAISED,width=4)
        self.__exit.bind("<ButtonPress-1>", lambda ev: self.__exit.config(relief=SUNKEN))
        self.__exit.bind("<ButtonRelease-1>", lambda ev: LEDexit(ev))
        self.__exit.pack_propagate(False)
        self.__exit.pack(anchor=NW)
        self.__getTime()
        
    def __homeReturn(self):
        self.__mainFrame.destroy()
        self.__placeMainFrame()
        # Load compass image and render image
        load = Image.open(os.path.dirname(os.path.realpath(__file__)) + "/../appImages/rocketry.png")
        load.thumbnail(size=(220, 435))
        render = ImageTk.PhotoImage(load)

        self.__img = Label(self.__mainFrame, image=render, bg=statusBackGround)
        self.__img.image = render
        self.__img.pack()

    def __getTime(self):
        ## 12 hour format ##
        currentTime = time.strftime("%I:%M:%S")  # Current time to display
        lastMesgTime = self.__dataList.lastTimeDataReceived  # Time of last message
        self.__time.config(text="Time:  " + currentTime + "\t\t" + "Time of Last Message:  " + lastMesgTime)
        self.__master.after(10, self.__getTime)

    # ***************** All descriptive status data *****************

    def __statusBar(self):
        # Main frame
        status = Frame(self.__master)
        status.pack(side=BOTTOM, fill="x")

        # Frame with map information
        self.__mapCoordinates = Frame(status, bg=statusBackGround, height=70, width=height / 3 - 4)
        self.__mapCoordinates.pack(side=LEFT, pady=2, padx=2)
        self.__mapCoordinates.pack_propagate(False)
        self.__mapCoordinates.bind("<ButtonPress-1>", self.__changeFrameMap)

        # Frame containing timer information and separation status
        self.__statusStopWatch = Frame(status, bg=statusBackGround, height=70, width=height / 3 - 4)
        self.__statusStopWatch.pack(side=LEFT, pady=2, padx=2)
        self.__statusStopWatch.pack_propagate(False)
        self.__statusStopWatch.bind("<ButtonPress-1>", self.__changeFrameStatus)

        # Frame containing altitude and pressure information
        self.__altitudePressure = Frame(status, bg=statusBackGround, height=70, width=height / 3 - 4)
        self.__altitudePressure.pack(side=LEFT, pady=2, padx=2)
        self.__altitudePressure.pack_propagate(False)
        self.__altitudePressure.bind("<ButtonPress-1>", self.__changeFrameAltimeter)

        # Load compass image and render image
        load = Image.open(os.path.dirname(os.path.realpath(__file__)) + "/../appImages/compass.png")
        load.thumbnail(size=(50, 50))
        render = ImageTk.PhotoImage(load)

        # Paint compass image in label with parent being frame with map information
        self.__img = Label(self.__mapCoordinates, image=render, bg=statusBackGround)
        self.__img.image = render
        self.__img.pack(side=LEFT, anchor=W, pady=2, padx=8)
        self.__img.bind("<ButtonPress-1>", self.__changeFrameMap)

        # Set text label with coordinates with parent being frame with map information
        self.__latitude_longitude = Label(self.__mapCoordinates, text="%.5f" % self.getgpsLat() + " ,\n" + "%.5f" % self.getgpsLong() + "",
                                          bg=statusBackGround, fg="black")
        self.__latitude_longitude.pack(side=LEFT, anchor=W, padx=8)
        self.__latitude_longitude.bind("<ButtonPress-1>", self.__changeFrameMap)

        # Paint stopwatch timer
        self.__stopWatch = Label(self.__statusStopWatch, text= "%.5f" % (float(time.time())-float(self.__dataList.lastTimeDataRecivedNumber)) + " s", bg=statusBackGround,
                                 fg="black")
        self.__stopWatch.config(font=("times", 20))
        self.__stopWatch.pack(side=TOP, anchor=N)
        self.__stopWatch.bind("<ButtonPress-1>", self.__changeFrameStatus)

        # Paint status indication for separation
        self.__statusFlag = Label(self.__statusStopWatch, text="Live Data", bg=statusBackGround)
        self.__statusFlag.config(font=("times", 15))
        self.__statusFlag.pack(side=TOP, anchor=S)
        self.__statusFlag.bind("<ButtonPress-1>", self.__changeFrameStatus)

        # Paint label of altitude or pressure value
        self.__altitude_pressure = Label(self.__altitudePressure, text=str(self.getpressAlt()) + "m",
                                         bg=statusBackGround)
        self.__altitude_pressure.config(font=("times"))
        self.__altitude_pressure.pack(side=TOP, anchor=N)
        self.__altitude_pressure.bind("<ButtonPress-1>", self.__changeFrameAltimeter)

        # Paint descriptive label of data
        self.__title_of_data = Label(self.__altitudePressure, text="Plots", bg=statusBackGround)
        self.__title_of_data.config(font=("times", 18))
        self.__title_of_data.pack(side=TOP)
        self.__title_of_data.bind("<ButtonPress-1>", self.__changeFrameAltimeter)
        
        self.__updateStatus()
        
    def __updateStatus(self):
        self.__latitude_longitude.config(text="%.5f" % self.getgpsLat() + " ,\n" + "%.5f" % self.getgpsLong() + "")
        
        self.__stopWatch.config(text= "%.5f" % (float(time.time())-float(self.__dataList.lastTimeDataRecivedNumber)) + " s")
        #print(str(float(time.time())-float(self.__dataList.lastTimeDataRecivedNumber)))        
        self.__altitude_pressure.config(text=str(self.getpressAlt()) + " m")
        
        self.__master.after(10,self.__updateStatus)

    # ******************Event handlers*************************

    def __changeFrameMap(self, ev):
        # Switch frame to map
        self.__mainFrame.destroy()
        self.__placeMainFrame()
        self.__runMap = GPSMap.Map(self.__mainFrame)
        self.__mapBackgroundUpdate()
        self.__runMap.firstImage = 5



        # Unbind when pushed
        self.__mapCoordinates.unbind("<ButtonPress-1>")
        self.__img.unbind("<ButtonPress-1>")
        self.__latitude_longitude.unbind("<ButtonPress-1>")

        # Bind all other buttons
        self.__statusStopWatch.bind("<ButtonPress-1>", self.__changeFrameStatus)
        self.__stopWatch.bind("<ButtonPress-1>", self.__changeFrameStatus)
        self.__statusFlag.bind("<ButtonPress-1>", self.__changeFrameStatus)
        self.__altitudePressure.bind("<ButtonPress-1>", self.__changeFrameAltimeter)
        self.__altitude_pressure.bind("<ButtonPress-1>", self.__changeFrameAltimeter)

    def __mapBackgroundUpdate(self):
        self.__runMap.setCoordinate([self.getgpsLong,self.getgpsLat])
        self.__runMap.update()
        self.__master.after(10, self.__mapBackgroundUpdate)

    def __changeFrameStatus(self, ev):
        # Switch frame to map
        self.__mainFrame.destroy()
        self.__placeMainFrame()
        self.__statusFrame = Status.Display(self.__mainFrame)
        self.__statusBackgroundUpdate()

        # Unbind when pushed
        self.__statusStopWatch.unbind("<ButtonPress-1>")
        self.__stopWatch.unbind("<ButtonPress-1>")
        self.__statusFlag.unbind("<ButtonPress-1>")

        # Bind all other buttons
        self.__mapCoordinates.bind("<ButtonPress-1>", self.__changeFrameMap)
        self.__img.bind("<ButtonPress-1>", self.__changeFrameMap)
        self.__latitude_longitude.bind("<ButtonPress-1>", self.__changeFrameMap)
        self.__altitudePressure.bind("<ButtonPress-1>", self.__changeFrameAltimeter)
        self.__altitude_pressure.bind("<ButtonPress-1>", self.__changeFrameAltimeter)

    def __statusBackgroundUpdate(self):
        self.__statusFrame.setSpeed(self.getgpsSpeed())
        self.__statusFrame.setAltitude(self.getpressAlt())
        self.__statusFrame.setaccel([self.getaccelX(), self.getaccelY(), self.getaccelZ()])
        self.__statusFrame.setaccel1([self.getaccelX1(), self.getaccelY1(), self.getaccelZ1()])
        self.__statusFrame.setPressure(self.getpressure())
        self.__statusFrame.setTemperature(self.getpressTemp())
        self.__statusFrame.setBatteryTemperature(self.gettempBattery())
        self.__statusFrame.setIRDistance(self.getIRdistance())
        self.__statusFrame.update()
        self.__master.after(10, self.__statusBackgroundUpdate)

    def __changeFrameAltimeter(self, ev):
        # Switch frame to map
        self.__mainFrame.destroy()
        self.__placeMainFrame()
        self.__statusAltimeter = System_Plots.Plot(self.__mainFrame)
        #self.__altimeterBagroundUpdate()
        
        # Unbind when pushed
        self.__altitudePressure.unbind("<ButtonPress-1>")
        self.__altitude_pressure.unbind("<ButtonPress-1>")

        # Bind all other buttons
        self.__mapCoordinates.bind("<ButtonPress-1>", self.__changeFrameMap)
        self.__img.bind("<ButtonPress-1>", self.__changeFrameMap)
        self.__latitude_longitude.bind("<ButtonPress-1>", self.__changeFrameMap)
        self.__statusStopWatch.bind("<ButtonPress-1>", self.__changeFrameStatus)
        self.__stopWatch.bind("<ButtonPress-1>", self.__changeFrameStatus)
        self.__statusFlag.bind("<ButtonPress-1>", self.__changeFrameStatus)

    def __altimeterBagroundUpdate(self):
        self.__statusAltimeter.update()
        self.__master.after(1000,self.__altimeterBagroundUpdate)

    # ****************** Methods used to get data **************

    def getgpsLat(self):
        with self.__serialData.lock:
            return self.__dataList.gpsLat

    def getgpsLong(self):
        with self.__serialData.lock:
            return self.__dataList.gpsLong

    def getgpsSpeed(self):
        with self.__serialData.lock:
            return self.__dataList.gpsSpeed

    def getgpsTime(self):
        with self.__serialData.lock:
            return self.__dataList.gpsTime

    def gpsAlt(self):
        with self.__serialData.lock:
            return self.__dataList.gpsAlt

    def getaccelX(self):
        with self.__serialData.lock:
            return self.__dataList.accelX

    def getaccelY(self):
        with self.__serialData.lock:
            return self.__dataList.accelY

    def getaccelZ(self):
        with self.__serialData.lock:
            return self.__dataList.accelZ

    def getaccelX1(self):
        with self.__serialData.lock:
            return self.__dataList.accelX1

    def getaccelY1(self):
        with self.__serialData.lock:
            return self.__dataList.accelY1

    def getaccelZ1(self):
        with self.__serialData.lock:
            return self.__dataList.accelZ1

    def getpressAlt(self):
        with self.__serialData.lock:
            return self.__dataList.pressAlt

    def getpressTemp(self):
        with self.__serialData.lock:
            return self.__dataList.pressTemp

    def gettempBattery(self):
        with self.__serialData.lock:
            return self.__dataList.tempBattery

    def getstrainGauge(self):
        with self.__serialData.lock:
            return self.__dataList.strainGauge

    def getIRdistance(self):
        with self.__serialData.lock:
            return self.__dataList.IRdistance

    def getpressure(self):
        with self.__serialData.lock:
            return self.__dataList.pressure


if __name__ == '__main__':
    root = Tk()
    display = Display(root)
    root.mainloop()
