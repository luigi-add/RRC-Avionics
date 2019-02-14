import sys,os,time,math




class DataSave:
    def __init__(self):
        #Start time
        self.__notTime = time.time()
        self.__telemetry = open(os.path.dirname(os.path.realpath(__file__)) + "/../DataFiles/telemetry.txt", "w")
        self.__csv = open(os.path.dirname(os.path.realpath(__file__))+"/../DataFiles/telemetry.csv","w")
        self.__altitude = open(os.path.dirname(os.path.realpath(__file__))+"/../DataFiles/altitude.csv","w")
        self.__pressure = open(os.path.dirname(os.path.realpath(__file__)) + "/../DataFiles/pressure.csv","w")
        self.__distance = open(os.path.dirname(os.path.realpath(__file__)) + "/../DataFiles/IRdistance.csv","w")
        self.__temperature = open(os.path.dirname(os.path.realpath(__file__)) + "/../DataFiles/temperature.csv", "w")
        self.__acceleration = open(os.path.dirname(os.path.realpath(__file__)) + "/../DataFiles/acceleration.csv", "w")
        self.__acceleration = open(os.path.dirname(os.path.realpath(__file__)) + "/../DataFiles/accelerationEx.csv", "w")
        self.__acceleration = open(os.path.dirname(os.path.realpath(__file__)) + "/../DataFiles/accelerationIn.csv", "w")
        self.__acceleration = open(os.path.dirname(os.path.realpath(__file__)) + "/../DataFiles/accelerationBoth.csv", "w")
        self.__acceleration = open(os.path.dirname(os.path.realpath(__file__)) + "/../DataFiles/batTemperature.csv", "w")
        


    def addToTelemetry(self,string):
        self.__telemetry = open(os.path.dirname(os.path.realpath(__file__)) + "/../DataFiles/telemetry.txt", "a")
        self.__telemetry.write(" "+string)
        self.__telemetry.close()

    def addToCSV(self,dataObj):
        self.__csv = open(os.path.dirname(os.path.realpath(__file__))+"/../DataFiles/telemetry.csv","a")
        self.__csv.write("%.2f" % (time.time()-self.__notTime))
        for i in range(0,15):
            self.__csv.write(","+str(dataObj.getOnIndex(i)))
        self.__csv.write("\n")
        self.__csv.close()

    def addToAltitude(self,dataObj):
        self.__altitude = open(os.path.dirname(os.path.realpath(__file__))+"/../DataFiles/altitude.csv","a")
        self.__altitude.write("%.2f" % (time.time()-self.__notTime))
        self.__altitude.write(","+str(dataObj.getOnIndex(3)))
        self.__altitude.write("\n")
        self.__altitude.close()

    def addToPressure(self,dataObj):
        self.__pressure = open(os.path.dirname(os.path.realpath(__file__)) + "/../DataFiles/pressure.csv","a")
        self.__pressure.write("%.2f" % (time.time()-self.__notTime))
        self.__pressure.write(","+str(dataObj.getOnIndex(2)))
        self.__pressure.write("\n")
        self.__pressure.close()

    def addToDistance(self,dataObj):
        self.__distance = open(os.path.dirname(os.path.realpath(__file__)) + "/../DataFiles/IRdistance.csv","a")
        self.__distance.write("%.2f" % (time.time()-self.__notTime))
        self.__distance.write(","+str(dataObj.getOnIndex(0)))
        self.__distance.write("\n")
        self.__distance.close()

    def addToTemperature(self, dataObj):
        self.__temperature = open(os.path.dirname(os.path.realpath(__file__)) + "/../DataFiles/temperature.csv", "a")
        self.__temperature.write("%.2f" % (time.time()-self.__notTime))
        self.__temperature.write("," + str(dataObj.getOnIndex(1)))
        self.__temperature.write("\n")
        self.__temperature.close()

    def addToBatTemperature(self, dataObj):
        self.__temperature = open(os.path.dirname(os.path.realpath(__file__)) + "/../DataFiles/batTemperature.csv", "a")
        self.__temperature.write("%.2f" % (time.time()-self.__notTime))
        self.__temperature.write("," + str(dataObj.getOnIndex(4)))
        self.__temperature.write("\n")
        self.__temperature.close()

    def addToAccelerationEx(self, dataObj):
        self.__acceleration = open(os.path.dirname(os.path.realpath(__file__)) + "/../DataFiles/accelerationEx.csv", "a")
        self.__acceleration.write("%.2f" % (time.time()-self.__notTime))
        self.__acceleration.write("," + str(dataObj.getOnIndex(12)))
        self.__acceleration.write("\n")
        self.__acceleration.close()

    def addToAccelerationIn(self, dataObj):
        self.__acceleration = open(os.path.dirname(os.path.realpath(__file__)) + "/../DataFiles/accelerationIn.csv", "a")
        self.__acceleration.write("%.2f" % (time.time()-self.__notTime))
        self.__acceleration.write("," + str(dataObj.getOnIndex(15)))
        self.__acceleration.write("\n")
        self.__acceleration.close()

    def addToAccelerationBoth(self, dataObj):
        self.__acceleration = open(os.path.dirname(os.path.realpath(__file__)) + "/../DataFiles/accelerationBoth.csv",
                                   "a")
        self.__acceleration.write("%.2f" % (time.time()-self.__notTime))
        self.__acceleration.write("," + str(dataObj.getOnIndex(15)))
        self.__acceleration.write("," + str(dataObj.getOnIndex(12)))
        self.__acceleration.write("\n")
        self.__acceleration.close()


if __name__ == '__main__':
    save = DataSave()
    #serialCOM = serialCOM.Data()
    #serialCOM.setOnIndex(12,54)
    #save.addToTemperature(serialCOM)
    time.sleep(10)
    #serialCOM.setOnIndex(12,42)
    #save.addToTemperature(serialCOM)
    save.addToTelemetry("Hello world!")
