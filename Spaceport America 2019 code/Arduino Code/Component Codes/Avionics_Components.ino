// Current Implemented Components:
// IMU, Pressure & Temp Sensor, SD Card Reader
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>
#include <Adafruit_BMP280.h>
Adafruit_BMP280 bmp; // I2C

#include <SparkFunMPU9250-DMP.h>
#define SerialPort Serial
MPU9250_DMP imu;

SoftwareSerial mySerial(11, 10); // For gps serial
Adafruit_GPS GPS(&mySerial);

#include <SD.h>
File dataFile;

// CS 50
// DI 51
// DO 52
// CLK 53

void setup() {
  Serial.begin(115200);
  GPS.begin(115200);

  /* ---------------------------- SD Log ----------------------------- */
  // Pins for Mega2560
  // CS 50
  // DI 51
  // DO 52
  // CLK 53
  // black = scl, white = sca
//  pinMode(50,OUTPUT);
//  digitalWrite(50, HIGH);
  Serial.print("Initializing SD card...");
  delay(1000);
  // make sure that the default chip select pin is set to
  // output, even if you don't use it:
  pinMode(SS, OUTPUT);

  // see if the card is present and can be initialized:
  if (!SD.begin(50, 51, 52, 53)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    while (1) {
      if (SD.begin(50, 51, 52, 53)) {
        break;
      }
    }
  }
  Serial.println("card initialized.");

  // Open up the file we're going to log to!
  dataFile = SD.open("datalog.txt", FILE_WRITE);
  if (! dataFile) {
    Serial.println("error opening datalog.txt");
    // Wait forever since we cant write data
    while (1) ;
  }

  /* ----------------------------- Sensor --------------------------- */

  Serial.println(F("Avionics Sensor and IMU"));

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
      SerialPort.println("Unable to communicate with MPU-9250");
      SerialPort.println("Check connections, and try again.");
      SerialPort.println();
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
  imu.setAccelFSR(2); // Set accel to +/-2g
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

void loop() {
  printSensorData(); // Sensor Data output

  if ( imu.dataReady() )
  {
    imu.update(UPDATE_ACCEL | UPDATE_GYRO | UPDATE_COMPASS);
    printIMUData(); // IMU Data output
  }

  char c = GPS.read();

  if (GPS.newNMEAreceived()) {
    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another
  }

  if (GPS.fix) {

    Serial.print(GPS.latitudeDegrees, 4);
    Serial.print(", ");
    Serial.println(GPS.longitudeDegrees, 4);
    Serial.print("Altitude: "); Serial.println(GPS.altitude);
    Serial.println(" ");

  }
  else {
    Serial.print("No GPS Fix");
    Serial.println(" ");
    Serial.println(" ");
  }

  dataFile.flush();
  delay(5000);
}

void printSensorData(void) {
  // Write to Serial
  Serial.print(F("Temperature = "));
  Serial.print(bmp.readTemperature());
  Serial.println(" *C");

  Serial.print(F("Pressure = "));
  Serial.print(bmp.readPressure());
  Serial.println(" Pa");

  Serial.print(F("Approx altitude = "));
  Serial.print(bmp.readAltitude(1013.25)); /* Adjusted to local forecast! */
  Serial.println(" m");

  Serial.println();

  // Write to file
  dataFile.println(bmp.readTemperature());
  dataFile.println(bmp.readPressure());
  dataFile.println(bmp.readAltitude(1013.25));
}

void printIMUData(void)
{
  // After calling update() the ax, ay, az, gx, gy, gz, mx,
  // my, mz, time, and/or temerature class variables are all
  // updated. Access them by placing the object. in front:

  // Use the calcAccel, calcGyro, and calcMag functions to
  // convert the raw sensor readings (signed 16-bit values)
  // to their respective units.
  float accelX = imu.calcAccel(imu.ax);
  float accelY = imu.calcAccel(imu.ay);
  float accelZ = imu.calcAccel(imu.az);
  float gyroX = imu.calcGyro(imu.gx);
  float gyroY = imu.calcGyro(imu.gy);
  float gyroZ = imu.calcGyro(imu.gz);
  float magX = imu.calcMag(imu.mx);
  float magY = imu.calcMag(imu.my);
  float magZ = imu.calcMag(imu.mz);

  SerialPort.println("Accel: " + String(accelX) + ", " +
                     String(accelY) + ", " + String(accelZ) + " g");
  SerialPort.println("Gyro: " + String(gyroX) + ", " +
                     String(gyroY) + ", " + String(gyroZ) + " dps");
  SerialPort.println("Mag: " + String(magX) + ", " +
                     String(magY) + ", " + String(magZ) + " uT");
  SerialPort.println("Time: " + String(imu.time) + " ms");
  SerialPort.println();

  // Write to file
  dataFile.println(accelX);
  dataFile.println(accelY);
  dataFile.println(accelZ);
  dataFile.println(gyroX);
  dataFile.println(gyroY);
  dataFile.println(gyroZ);
  dataFile.println(magX);
  dataFile.println(magY);
  dataFile.println(magZ);
  dataFile.println(imu.time);
}
