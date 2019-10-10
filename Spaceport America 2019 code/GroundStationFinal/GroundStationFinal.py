from tkinter import *
from PIL import Image, ImageTk
import time, sys, struct, copy, os
import pandas as pd
import collections
import serial
import random

'''
smallmap_corners = {topleft: [32.955651, -106.930123], topright: [32.955651, -106.892924],
                    botleft: [32.937436, -106.930123], botright: [32.937436, -106.892924]}
largemap_corners = {topleft: [32.979024, -106.967445], topright: [32.979024, -106.858726],
                    botleft: [32.925260, -106.930123], botright: [32.925260, -106.858726]}
change'''

#   ************ Initializations ***************
#File Init
file_dir = os.path.dirname(os.path.abspath(__file__))
imgFolder = 'appImages'
csv_folder = 'dataFiles'
csvFile = os.path.join(file_dir, csv_folder, 'csvData.csv')

HEADER = ['Time (ms)', 'Latitude','Longitude','Speed (kt)',
          'AccelX (g)','AccelY','AccelZ',
          'GyroX (dps)','GyroY','GyroZ',
          'MagX (uT)','MagY','MagZ',
          'Temp (C)','Pressure (Pa)','Alt (m)']

smallmap_side = {'top': 32.955651, 'bot': 32.937436, 'left': -106.930123, 'right': -106.892924}
largemap_side = {'top': 32.979024, 'bot': 32.925260, 'left': -106.967445, 'right': -106.858726}

#Serial Init
comPort = 'COM5'
#comPort = '/dev/ttyUSB0'
ser = serial.Serial(comPort, baudrate = 115200,
                    bytesize = serial.EIGHTBITS, 
                    parity = serial.PARITY_NONE, 
                    stopbits = serial.STOPBITS_ONE, 
                    timeout = 10) # open serial
numData = 16 # numper of data points
dataNumBytes = 4 # byte size of each data point
rawData = bytearray(numData * dataNumBytes) # makes array for byte data, size = (numdata points)*(byte size)
dataType = 'f' # data type of data
dataList = []
dataString = []
csvData = []
plotLength = 100
csvMax = 5000000

for i in range(numData):   # give an array for each type of data and store them in a list
            dataList.append(collections.deque([0] * plotLength, maxlen=plotLength))
            dataString.append(collections.deque([0] * plotLength, maxlen=plotLength))

#   ************ Initializations ***************


#   ************ Functions ***************

# RRC logo
def showLogo():
    LogoFrame = Frame(window)
    LogoFrame.grid(row=1, column=1, columnspan=2)
    size = 110,110

    loadlogo = Image.open(os.path.join(file_dir, imgFolder, 'rocketry.png'))
    loadlogo.thumbnail(size, Image.ANTIALIAS)
    render = ImageTk.PhotoImage(loadlogo)

    img = Button(LogoFrame, image=render, command=lambda:exit())
    img.image = render
    img.grid(row=0, column=0, sticky=E)

def exit():
    window.destroy()

# clock
def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)

# updates number data on GUI
def GUIdata():
    
    global nData
    global csvData
    #Right Output Box
    acx.delete(1.0,END)
    acy.delete(1.0,END)
    acz.delete(1.0,END)
    t.delete(1.0,END)   

    acx.insert(END,nData[4])
    acy.insert(END,nData[5])
    acz.insert(END,nData[6])
    t.insert(END,nData[0]/1000)

    #Bottom Output Box
    lat.delete(1.0,END)
    tmp.delete(1.0,END)
    spd.delete(1.0,END)
    lon.delete(1.0,END)   
    prs.delete(1.0,END) 
    alt.delete(1.0,END) 

    lat.insert(END,nData[1])
    tmp.insert(END,nData[13])
    spd.insert(END,nData[3])
    lon.insert(END,nData[2])
    prs.insert(END,nData[14])
    alt.insert(END,nData[15])

# updates map on GUI
def updateMap():
    # ************ RANDOM NUMBERS TEST - REPLACE WITH REAL COORDINATES *************
    #coordx = (-106.930123 - (-106.892934))/2+(-106.892934) # center x
    #coordy = (32.955651-32.937436)/2+32.937436 # center y
    
    #coordx = round(random.uniform(largemap_side['left'],largemap_side['right']),6)
    #coordy = round(random.uniform(largemap_side['bot'],largemap_side['top']),6)
    #coordx = round(random.uniform(smallmap_side['left'],smallmap_side['right']),6)
    #coordy = round(random.uniform(smallmap_side['bot'],smallmap_side['top']),6)
    
    # ************ RANDOM NUMBERS TEST - REPLACE WITH REAL COORDINATES *************
    global nData
    coordx = nData[2]
    coordy = nData[1]

    #print(coordx,coordy)


    if (coordx < smallmap_side['left'] or coordx > smallmap_side['right']) or (coordy > smallmap_side['top'] or coordy < smallmap_side['bot']):
        latitude_length = largemap_side['top'] - largemap_side['bot'] 
        longitude_length = abs(largemap_side['left'] - largemap_side['right'])
        yScale = height/latitude_length
        xScale = width/longitude_length            
        x = int((largemap_side['left'] - coordx) * xScale * (-1)) - int(csize[0]/2)
        y = int((largemap_side['top'] - coordy) * yScale) - int(csize[1]/2)
        loadlargemap.paste(loadcircle, (x,y), mask=loadcircle)
        loadlargemap.save(os.path.join(file_dir, imgFolder, "Large_Map1.png"))
        map = ImageTk.PhotoImage(loadlargemap)

    elif (coordx >= smallmap_side['left'] or coordx <= smallmap_side['right']) or (coordy <= smallmap_side['top'] or coordy >= smallmap_side['bot']):
        latitude_length = smallmap_side['top'] - smallmap_side['bot'] 
        longitude_length = abs(smallmap_side['left'] - smallmap_side['right'])
        yScale = height/latitude_length
        xScale = width/longitude_length
        x = int((smallmap_side['left'] - coordx) * xScale * (-1)) - int(csize[0]/2)
        y = int((smallmap_side['top'] - coordy) * yScale) - int(csize[1]/2)
        loadsmallmap.paste(loadcircle, (x,y), mask=loadcircle)
        loadsmallmap.save(os.path.join(file_dir, imgFolder, "Small_Map1.png"))
        map = ImageTk.PhotoImage(loadsmallmap)

        # For large map coordinate paste
        latitude_length = largemap_side['top'] - largemap_side['bot'] 
        longitude_length = abs(largemap_side['left'] - largemap_side['right'])
        yScale = height/latitude_length
        xScale = width/longitude_length            
        x = int((largemap_side['left'] - coordx) * xScale * (-1)) - int(csize[0]/2)
        y = int((largemap_side['top'] - coordy) * yScale) - int(csize[1]/2)
        loadlargemap.paste(loadcircle, (x,y), mask=loadcircle)
        loadlargemap.save(os.path.join(file_dir, imgFolder, "Large_Map1.png"))
    else:
        pass

    
    img = Label(MapFrame, image=map)
    img.image = map
    img.grid(row=0, column=0)



def getSerial():
    ser.readinto(rawData) # reads serial
    privateData = copy.deepcopy(rawData[:]) # makes copy of rawData
    for i in range(numData):
        data = privateData[(i*dataNumBytes):(dataNumBytes + i*dataNumBytes)] # slices array as there are 'dataNumBytes' bytes per 'numData' points 
        value, = struct.unpack(dataType, data)
        dataString[i].append(round(value,5))
        dataList[i].append(value) # makes data array
    global nData
    nData = [dataString[0][-1],dataString[1][-1],dataString[2][-1], # newest data value
                   dataString[3][-1],dataString[4][-1],dataString[5][-1],
                   dataString[6][-1],dataString[7][-1],dataString[8][-1],
                   dataString[9][-1],dataString[10][-1],dataString[11][-1],
                   dataString[12][-1],dataString[13][-1],dataString[14][-1],
                   dataString[15][-1]]
    #print(rawData)
    print(nData)
    global csvData
    csvData.append([dataList[0][-1],dataList[1][-1],dataList[2][-1],
                    dataList[3][-1],dataList[4][-1],dataList[5][-1],
                    dataList[6][-1],dataList[7][-1],dataList[8][-1],
                    dataList[9][-1],dataList[10][-1],dataList[11][-1],
                    dataList[12][-1],dataList[13][-1],dataList[14][-1],
                    dataList[15][-1]])
    df = pd.DataFrame(csvData)
    df.to_csv(csvFile, header=HEADER, index=False)
    #print(len(csvData))
    if (len(csvData) > csvMax): # only saves the last x amount of data
        csvData = []
    
#   ************ Functions ***************

# Window init
window = Tk()
window.geometry("480x320")
window.attributes("-fullscreen",True)
window.resizable(0, 0) # this prevents from resizing the window
window.title("Northern Lightning")

#Rightside Frame
rFrame = Frame(window)
rFrame.grid(row=0, column=1, sticky=E)

#Right Labels
rL1 = Label(rFrame, text="acX(g)", font=30).grid(row=1, column=0, sticky=E)
rL2 = Label(rFrame, text="acY(g)", font=30).grid(row=2, column=0, sticky=E)
rL3 = Label(rFrame, text="acZ(g)", font=30).grid(row=3, column=0, sticky=E)
rL4 = Label(rFrame, text="time(s)", font=30).grid(row=4, column=0, sticky=E)

#Bottom Frame
bFrame = Frame(window)
bFrame.grid(row=1, column=0, sticky=W)

#Bottom Labels
bL1 = Label(bFrame, text="Lat", font=30).grid(row=0, column=0, sticky=E)
bL2 = Label(bFrame, text="Tmp(C)", font=30).grid(row=0, column=2, sticky=E)
bL3 = Label(bFrame, text="Spd(kt)", font=30).grid(row=0, column=4, sticky=E)
bL4 = Label(bFrame, text="Lon", font=30).grid(row=1, column=0, sticky=E)
bL5 = Label(bFrame, text="Prs(Pa)", font=30).grid(row=1, column=2, sticky=E)
bL6 = Label(bFrame, text="Alt(m)", font=30).grid(row=1, column=4, sticky=E)

#Right Output Box
acx = Text(rFrame, width=6, height=2, bg="light grey")
acx.grid(row=1, column=1, sticky=E)
acy = Text(rFrame, width=6, height=2, bg="light grey")
acy.grid(row=2, column=1, sticky=E)
acz = Text(rFrame, width=6, height=2, bg="light grey")
acz.grid(row=3, column=1, sticky=E)
t = Text(rFrame, width=6, height=2, bg="light grey")
t.grid(row=4, column=1, sticky=E)

#Bottom Output Box
lat = Text(bFrame, width=14, height=2, bg="light grey")
lat.grid(row=0, column=1, sticky=E)
tmp = Text(bFrame, width=5, height=2, bg="light grey")
tmp.grid(row=0, column=3, sticky=E)
spd = Text(bFrame, width=6, height=2, bg="light grey")
spd.grid(row=0, column=5, sticky=E)
lon = Text(bFrame, width=14, height=2, bg="light grey")
lon.grid(row=1, column=1, sticky=E)
prs = Text(bFrame, width=5, height=2, bg="light grey")
prs.grid(row=1, column=3, sticky=E)
alt = Text(bFrame, width=6, height=2, bg="light grey")
alt.grid(row=1, column=5, sticky=E)
 
#Clock
clock=Label(rFrame, relief=SUNKEN, bg="white")
clock.grid(row=0, column=0, columnspan=2, pady=20, ipadx=30)

#Map
MapFrame = Frame(window)
MapFrame.grid(row=0, column=0, sticky=W+E+N+S)

height = 220
width = 360
msize = width,height # map resolution
loadsmallmap =  Image.open(os.path.join(file_dir, imgFolder, 'Small_Map.png')) # loads small map, default
loadsmallmap.thumbnail(msize, Image.ANTIALIAS)
loadlargemap =  Image.open(os.path.join(file_dir, imgFolder, 'Large_Map.png')) # loads large map
loadlargemap.thumbnail(msize, Image.ANTIALIAS)
csize = 5,5 # circle resolution
loadcircle = Image.open(os.path.join(file_dir, imgFolder, 'circle.png')) # loads circle
loadcircle.thumbnail(csize)

showLogo()
tick()

while 1:
    window.update()
    getSerial()
    GUIdata()
    updateMap()