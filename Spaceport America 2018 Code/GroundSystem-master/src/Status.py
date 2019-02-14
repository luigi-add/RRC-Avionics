from tkinter import *

# resolution of the screen
height = 422
width = 250
statusBackGround = 'light cyan'
BackGround = 'red'


class Display:
    # ***************** Instantiate *****************
    def __init__(self, master):
        self.__master = master

        # Set window parameters
        if __name__ == '__main__':
            self.__master.resizable(width=False, height=False)
            self.__master.geometry('{}x{}'.format(height, width))

        self.__speed = 0
        self.__altitude = 0
        self.__accel = [0, 0, 0]
        self.__accel1 = [0, 0, 0]
        self.__pressure = 0
        self.__temperature = 0
        self.__batteryTemperature = 0
        self.__IRdistance = 0

        self.__labels()

    # Main Frame For labels
    def __labels(self):
        # Main frame
        self.__labelFrame = Frame(self.__master, bg='cyan')
        self.__labelFrame.pack(fill=BOTH)

        # Paint label of Speed
        self.__accelSpeed = Label(self.__labelFrame, text="Speed:\t\t\t" + str(self.__speed), bg=statusBackGround,anchor=W)
        self.__accelSpeed.pack_propagate(False)
        self.__accelSpeed.config(font=("arial", "12", "italic", "bold"), fg="black",relief=RIDGE)
        self.__accelSpeed.pack(side=TOP, anchor=W, fill=X, pady =1)

        # Paint label of Altitude
        self.__accelAltitude = Label(self.__labelFrame, text="Altitude:\t\t\t" + str(self.__altitude), bg=statusBackGround,anchor=W)
        self.__accelAltitude.config(font=("arial", "12", "italic", "bold"), fg="black",relief=RIDGE)
        self.__accelAltitude.pack(side=TOP, anchor=W, fill=X, pady =1)

        # Paint label of all axis of acceleration of rocket
        self.__accelerationOfRocket = Label(self.__labelFrame,
                                            text="Rocket Acc.\tX:  " + str(self.__accel[0]) + "\tY:  " + str(
                                                self.__accel[1]) + "\tZ:  " + str(self.__accel[2]), bg=statusBackGround,anchor=W)
        self.__accelerationOfRocket.config(font=("arial", "12", "italic", "bold"), fg="black",relief=RIDGE)
        self.__accelerationOfRocket.pack(side=TOP, anchor=W, fill=X, pady =1)

        # Paint label of all axis of acceleration of payload
        self.__accelerationOfPayload = Label(self.__labelFrame,
                                             text="Payload Acc.\tX:  " + str(self.__accel1[0]) + "\tY:  " + str(
                                                 self.__accel1[1]) + "\tZ:  " + str(self.__accel1[2]), bg=statusBackGround,anchor=W)
        self.__accelerationOfPayload.config(font=("arial", "12", "italic", "bold"), fg="black",relief=RIDGE)
        self.__accelerationOfPayload.pack(side=TOP, anchor=W, fill=X, pady =1)

        # Paint label of pressure
        self.__pressureDisplay = Label(self.__labelFrame, text="Pressure:\t\t" + str(self.__pressure),
                                       bg=statusBackGround,anchor=W)
        self.__pressureDisplay.config(font=("arial", "12", "italic", "bold"), fg="black",relief=RIDGE)
        self.__pressureDisplay.pack(side=TOP, anchor=W, fill=X, pady =1)

        # Paint label of temperature
        self.__temperatureDisplay = Label(self.__labelFrame, text="Temperature:\t\t" + str(self.__temperature),
                                          bg=statusBackGround,anchor=W)
        self.__temperatureDisplay.config(font=("arial", "12", "italic", "bold"), fg="black",relief=RIDGE)
        self.__temperatureDisplay.pack(side=TOP, anchor=W, fill=X, pady =1)

        # Paint label of temperature
        self.__batteryTemperatureDisplay = Label(self.__labelFrame, text="Battery Temperature:\t\t" + str(self.__batteryTemperature),
                                          bg=statusBackGround,anchor=W)
        self.__batteryTemperatureDisplay.config(font=("arial", "12", "italic", "bold"), fg="black",relief=RIDGE)
        self.__batteryTemperatureDisplay.pack(side=TOP, anchor=W, fill=X, pady =1)

        # Paint label of IR distance of payload
        self.__IRDisplay = Label(self.__labelFrame, text="IR Distance:\t\t" + str(self.__IRdistance), bg=statusBackGround,anchor=W)
        self.__IRDisplay.config(font=("arial", "12", "italic", "bold"), fg="black",relief=RIDGE)
        self.__IRDisplay.pack(side=TOP, anchor=W, fill=X, pady =1)

    def update(self):
        self.__accelSpeed.config(text="Speed:\t\t\t\t" + str(self.__speed))
        self.__accelAltitude.config(text="Altitude:\t\t\t\t" + str(self.__altitude))
        self.__accelerationOfRocket.config(
            text="Rocket Acc.\t\tX:  " + str(self.__accel[0]) + "\tY:  " + str(self.__accel[1]) + "\tZ:  " + str(
                self.__accel[2]))
        self.__accelerationOfPayload.config(
            text="Payload Acc.\t\tX:  " + str(self.__accel1[0]) + "\tY:  " + str(self.__accel1[1]) + "\tZ:  " + str(
                self.__accel1[2]))
        self.__pressureDisplay.config(text="Pressure:\t\t\t" + str(self.__pressure))
        self.__batteryTemperatureDisplay.config(text="Battery Temperature:\t\t" + str(self.__batteryTemperature))
        self.__temperatureDisplay.config(text="Temperature:\t\t\t" + str(self.__temperature))
        self.__IRDisplay.config(text="IR Distance:\t\t\t" + str(self.__IRdistance))

    # ****************************************Setters******************************************
    def setSpeed(self, speed):
        self.__speed = speed

    def setAltitude(self, altitude):
        self.__altitude = altitude

    # must input an array [x,y,z]
    def setaccel(self, accel):
        self.__accel = accel

    # must input an array [x,y,z]
    def setaccel1(self, accel1):
        self.__accel1 = accel1

    def setPressure(self, pressure):
        self.__pressure = pressure

    def setTemperature(self, temperature):
        self.__temperature = temperature

    def setBatteryTemperature(self, batteryTemp):
        self.__batteryTemperature = batteryTemp

    def setIRDistance(self, IRDistance):
        self.__IRdistance = IRDistance


if __name__ == '__main__':
    root = Tk()
    root.wm_title("Status/Signal")
    display = Display(root)
    display.setSpeed(456)
    display.setAltitude(534)
    display.setaccel([5, 3, 1])
    display.setaccel1([5, 7, 4])
    display.setPressure(543)
    display.setTemperature(57)
    display.setBatteryTemperature(69)
    display.setIRDistance(12)
    display.update()
    root.mainloop()
