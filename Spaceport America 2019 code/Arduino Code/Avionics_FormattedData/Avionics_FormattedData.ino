// Current Implemented Components:
// IMU, Pressure & Temp Sensor, SD Card Reader, RFD, GPS, Buzzer
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>
#include <Adafruit_BMP280.h>
Adafruit_BMP280 bmp; // I2C

#include <SparkFunMPU9250-DMP.h>
MPU9250_DMP imu;

// below = software serial
//SoftwareSerial mySerial(10, 11); //  GPS TX, RX --> Controller RX, TX
//Adafruit_GPS GPS(&mySerial);

// below = hardware serial
Adafruit_GPS GPS(&Serial1);

#include <SD.h>
Sd2Card card;
SdVolume volume;
SdFile root;
int CSpin = 53;
File dataFile;

void setup() {
  Serial.begin(115200);

  /* ---------------------------- SD Log ----------------------------- */
  // Pins for Mega2560
  // CS 53
  // DI 51
  // DO 50
  // CLK 52
  // black = scl, white = sca

  // make sure that the default chip select pin is set to
  // output, even if you don't use it:
  pinMode(CSpin, OUTPUT);
  delay(2000);
  // see if the card is present and can be initialized:
  if (!SD.begin(CSpin)) {
    Serial.println("Card failed, or not present");
    while (1);
  }


  // Open up the file we're going to log to!
  dataFile = SD.open("datalog.txt", FILE_WRITE);
  if (! dataFile) {
    Serial.println("error opening datalog.txt");
    // Wait forever since we cant write data
    while (1) ;
  }

  /* ----------------------------- Sensor --------------------------- */


  if (!bmp.begin()) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
    while (1);
  }
  /* Default settings from datasheet. */
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */

  /* ----------------------------- IMU --------------------------- */
  if (imu.begin() != INV_SUCCESS)
  {
    while (1)
    {
      Serial.println("Unable to communicate with MPU-9250");
      Serial.println("Check connections, and try again.");
      Serial.println();
      delay(5000);
    }
  }
  // Enable all sensors:
  imu.setSensors(INV_XYZ_GYRO | INV_XYZ_ACCEL | INV_XYZ_COMPASS);
  // Use setGyroFSR() and setAccelFSR() to configure the
  // gyroscope and accelerometer full scale ranges.
  // Gyro options are +/- 250, 500, 1000, or 2000 dps
  imu.setGyroFSR(2000); // Set gyro to 2000 dps
  // Accel options are +/- 2, 4, 8, or 16 g
  imu.setAccelFSR(16); // Set accel to +/-16g
  // Note: the MPU-9250's magnetometer FSR is set at
  // +/- 4912 uT (micro-tesla's)

  // setLPF() can be used to set the digital low-pass filter
  // of the accelerometer and gyroscope.
  // Can be any of the following: 188, 98, 42, 20, 10, 5
  // (values are in Hz).
  imu.setLPF(5); // Set LPF corner frequency to 5Hz

  // The sample rate of the accel/gyro can be set using
  // setSampleRate. Acceptable values range from 4Hz to 1kHz
  imu.setSampleRate(10); // Set sample rate to 10Hz

  // Likewise, the compass (magnetometer) sample rate can be
  // set using the setCompassSampleRate() function.
  // This value can range between: 1-100Hz
  imu.setCompassSampleRate(10); // Set mag rate to 10Hz

  /* ----------------------------- GPS ------------------------------- */
  GPS.begin(9600);
  // Setup recommended minimum data collection
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate

}

unsigned long timer = millis(); // uses millis function for timing
long interval = 500; // sets interval time in milliseconds

void loop() {

  char c = GPS.read();
  if (GPS.newNMEAreceived()) {
    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another
  }

  // if millis() resets, just reset timer
  if (timer > millis())
    timer = millis();
  // approximately every interval or so, print out the current data set
  if (millis() - timer > interval) {
    timer = millis(); // reset the timer

    if (imu.dataReady())
    {
      imu.update(UPDATE_ACCEL | UPDATE_GYRO | UPDATE_COMPASS);
      printGPSData(); // GPS Data output
      printSensorData(); // Sensor Data output
      printIMUData(); // IMU Data output
    }
    tone(8, 1047, 150); // plays a C6 for 200 ms
  }

  dataFile.flush();
}
void printGPSData(void) {
  // Write to Serial
  Serial.println(GPS.latitudeDegrees, 4);
  Serial.println(GPS.longitudeDegrees, 4);
  Serial.println(GPS.speed); // knots
  Serial.println((int)GPS.satellites);
  
  // Write to File
  dataFile.println(GPS.latitudeDegrees, 4);
  dataFile.println(GPS.longitudeDegrees, 4);
  dataFile.println(GPS.speed);
  dataFile.println((int)GPS.satellites);
}
void printSensorData(void) {
  // Write to Serial
  static float relP = bmp.readPressure() / 100; // sets relative pressure point from initial pressure reading
  Serial.println(bmp.readTemperature()); // C
  Serial.println(bmp.readPressure()); // Pa
  // Toronto = 997 hPa, Albaquerque = 1009 hPa
  Serial.println(bmp.readAltitude(relP)); // Relative altitude, m

  // Write to file
  dataFile.println(bmp.readTemperature());
  dataFile.println(bmp.readPressure());
  dataFile.println(bmp.readAltitude(relP));
}

void printIMUData(void)
{
  // After calling update() the ax, ay, az, gx, gy, gz, mx,
  // my, mz, time, and/or temerature class variables are all
  // updated. Access them by placing the object. in front:

  // Use the calcAccel, calcGyro, and calcMag functions to
  // convert the raw sensor readings (signed 16-bit values)
  // to their respective units.

  // Write to Serial
  SerialPort.println(imu.calcAccel(imu.ax)); // g
  SerialPort.println(imu.calcAccel(imu.ay));
  SerialPort.println(imu.calcAccel(imu.az));
  SerialPort.println(imu.calcGyro(imu.gx)); // dps
  SerialPort.println(imu.calcGyro(imu.gy));
  SerialPort.println(imu.calcGyro(imu.gz));
  SerialPort.println(imu.calcMag(imu.mx)); // uT
  SerialPort.println(imu.calcMag(imu.my));
  SerialPort.println(imu.calcMag(imu.mz));
  SerialPort.println(imu.time); // ms

  // Write to file
  dataFile.println(imu.calcAccel(imu.ax)); // g
  dataFile.println(imu.calcAccel(imu.ay));
  dataFile.println(imu.calcAccel(imu.az));
  dataFile.println(imu.calcGyro(imu.gx)); // dps
  dataFile.println(imu.calcGyro(imu.gy));
  dataFile.println(imu.calcGyro(imu.gz));
  dataFile.println(imu.calcMag(imu.mx)); // uT
  dataFile.println(imu.calcMag(imu.my));
  dataFile.println(imu.calcMag(imu.mz));
  dataFile.println(imu.time); // ms
}
