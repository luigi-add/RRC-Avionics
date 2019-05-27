/*
   This program sends raw float (4 bytes) to serial, much for efficient than strings
*/
#include <SPI.h>
#include <SparkFunMPU9250-DMP.h>
MPU9250_DMP imu;
#include <Adafruit_BMP280.h>
Adafruit_BMP280 bmp;
#include <Adafruit_GPS.h>
Adafruit_GPS GPS(&Serial1);
#include <SD.h>
Sd2Card card;
SdVolume volume;
SdFile root;
int CSpin = 53;
File dataFile;
unsigned long timer = millis(); // uses millis function for timing
long interval = 1000; // sets interval time in milliseconds
int LC = 0; // loop counter

void setup() {
  Serial.begin(115200);

  /*======================================== SD Setup ========================================*/
  // Pins for Mega2560
  // CS 53
  // DI 51
  // DO 50
  // CLK 52
  pinMode(CSpin, OUTPUT);
  delay(1000); // give sd card some time

  if (!SD.begin(CSpin)) {
    Serial.println("Card failed, or not present");
    while (1);
  }
  SD.remove("datalog.txt"); // clears old file
  dataFile = SD.open("datalog.txt", FILE_WRITE);
  if (!dataFile) {
    Serial.println("error opening datalog.txt");
    while (1) ;
  }
  
  dataFile.println("Time (ms),Latitude,Longitude,Speed (kt),"
                   "AccelX (g),AccelY,AccelZ,"
                   "GyroX (dps),GyroY,GyroZ,"
                   "MagX (uT),MagY,MagZ,"
                   "Temp (C),Pressure (Pa),Alt (m)"); // header for txt file
  /*======================================== IMU Setup ========================================*/
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
  imu.setGyroFSR(2000); // Set gyro to 2000 dps
  imu.setAccelFSR(16); // Set accel to +/-16g
  imu.setLPF(5); // Set LPF corner frequency to 5Hz
  imu.setSampleRate(10); // Set sample rate to 10Hz
  imu.setCompassSampleRate(10); // Set mag rate to 10Hz
  /*======================================== BMP Setup ========================================*/
  if (!bmp.begin()) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
    while (1);
  }
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
  /*======================================== GPS Setup ========================================*/
  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA); // recommended min data collection
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate
}


void loop() {

  char c = GPS.read();
  if (GPS.newNMEAreceived()) {
    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another
  }
  float t = imu.time;
  float lat = GPS.latitudeDegrees; // accurate within 1 meter
  float lon = GPS.longitudeDegrees;
  float spd = GPS.speed; // knots

  float acx = imu.calcAccel(imu.ax); // g
  float acy = imu.calcAccel(imu.ay);
  float acz = imu.calcAccel(imu.az);
  float gyx = imu.calcGyro(imu.gx); // dps
  float gyy = imu.calcGyro(imu.gy);
  float gyz = imu.calcGyro(imu.gz);
  float mgx = imu.calcMag(imu.mx); // uT
  float mgy = imu.calcMag(imu.my);
  float mgz = imu.calcMag(imu.mz);

  static float relP = bmp.readPressure() / 100; // sets relative pressure point from initial pressure reading
  float tmp = bmp.readTemperature(); // C
  float prs = bmp.readPressure(); // Pa
  float alt = bmp.readAltitude(relP); // m

  /*======================================== Write to Serial & Save to SD ========================================*/
  if (timer > millis())
    timer = millis();
  // approximately every interval or so, print out the current data set
  if (millis() - timer > interval) {
    timer = millis(); // reset the timer
    if (imu.dataReady())
    {
      serialFloatPrint(t);
      serialFloatPrint(lat);
      serialFloatPrint(lon);
      serialFloatPrint(spd);

      imu.update(UPDATE_ACCEL | UPDATE_GYRO | UPDATE_COMPASS);
      serialFloatPrint(acx);
      serialFloatPrint(acy);
      serialFloatPrint(acz);
      serialFloatPrint(gyx);
      serialFloatPrint(gyy);
      serialFloatPrint(gyz);
      serialFloatPrint(mgx);
      serialFloatPrint(mgy);
      serialFloatPrint(mgz);

      serialFloatPrint(tmp);
      serialFloatPrint(prs);
      serialFloatPrint(alt);

      dataFile.println();
      
      LC = LC + 1; // Increment loop count
      if (LC > 50) { // every 50 loops, buzzer plays
        tone(8, 1047, 150); // plays a C6 on pin 8 for 150 ms
        LC = 0;
      }
    }
  }
  dataFile.flush();
}

void serialFloatPrint(float f) {
  byte * b = (byte *) &f;
  //  Serial.print("f:"); // data type
  Serial.write(b[0]);
  Serial.write(b[1]);
  Serial.write(b[2]);
  Serial.write(b[3]);

  // save to file
  dataFile.print(f);
  dataFile.print(",");
  /* DEBUG */
  //  Serial.println();
  //  Serial.print(b[0], BIN);
  //  Serial.print(b[1], BIN);
  //  Serial.print(b[2], BIN);
  //  Serial.println(b[3], BIN);
}
