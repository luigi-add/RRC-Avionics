//=============== Arctic Thunder Avionics Code ================//
// Revision number: 6.0                                        //
// Revised by, date: Zakary Harrison, June 9 2018              //
// Verification Status: Functioning                            //
// Major changes: Data reformatting for G.S.                   //
//=============================================================//


// Libraries
#include <avr/wdt.h>
#include <I2Cdev.h>
#include <TinyGPS.h>
#include "Adafruit_MCP9808.h"
#include <SPI.h>
#include <SD.h>
#include <Wire.h>
#include <MPU6050.h>
//#include <Adafruit_Sensor.h>
//#include <Adafruit_BMP280.h>
#include <SoftwareSerial.h>

// IR Sensor setup
int IR_pin = 3;
int IR_sensor;
int pay_dist; // measured in cm

// Pressure/Temperature/Altitude Setup (BMP 280)
//Adafruit_BMP280 bmp(BMP_CS); // hardware SPI
//Adafruit_BMP280 bmp(BMP_CS, BMP_MOSI, BMP_MISO,  BMP_SCK);
// @ Ryerson : 90m above sea level |-> according to BMP -> 163.4
//Adafruit_BMP280 bmp; // I2C
//float exp_o; // Used in Baro Pressure calcs (later)
//int Ph = 1013; // Barometric pressure at your ground level (calculated later)
//int rtemp, rpress, ralt , rtemp_conv, rpress_conv, ralt_conv, 
int battemp;
//String rock_T = "";
//String rock_P = "";
//String rock_A = "";

// GPS Setup
TinyGPS gps;
SoftwareSerial ss(4, 3);
long lat, lon;
unsigned long fix_age, speed;//time, date, 
// Don't need these unless we want GPS signal stats:
//unsigned long chars;
//unsigned short sentences, failed_checksum;

// MPU Setup
MPU6050 avAG(0x68);
MPU6050 payAG(0x69);
const int avMPU = 1;
const int payMPU = 2;
int16_t AcZ; //AcX, AcY, Tmp;
int accelSet;

// MCP 9808 setup
Adafruit_MCP9808 rocket_temp = Adafruit_MCP9808();


// SD Setup
File IRData;
File enviroData;
File GPSData;
File avMPUData;
File payMPUData; //file for acceleration data
const int chipSelect = 8;




//============== SETUP ==============//
void setup() {
  //wdt_disable();
  //I2C start
  Wire.begin();
  //Serial start
  Serial.begin(57600);
  ss.begin(57600);
  //Serial.println("Start");

  //Initialize SD Card
  if (!SD.begin(chipSelect)) {
    //Serial.println(F("SD card not initialized."));
  }

  // IR Sensor Setup
  pinMode(IR_pin, INPUT);
  //Serial.println(F("IR Sensor Initialized"));

  //Initialize BMP
  //if (bmp.begin()) {
    //Serial.println(F("BMP initialized."));
  //}
  // Set initial pressure
  //Ph = bmp.readPressure() / 100;

  //Initialize Avionics MPU
  avAG.initialize();
  Wire.beginTransmission(0x68);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);  
  avAG.setFullScaleAccelRange(MPU6050_ACCEL_FS_16);
  //Serial.println(F("Av MPU initialized."));
  Wire.endTransmission(true);

  //Initalize Payload MPU
  payAG.initialize();
  Wire.beginTransmission(0x69);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);  
  payAG.setFullScaleAccelRange(MPU6050_ACCEL_FS_16);
  //Serial.println(F("Pay MPU initialized."));
  Wire.endTransmission(true);

  // Initialize MCP
  if (rocket_temp.begin()) {
    //Serial.println(F("MCP initialized"));
  }

  //wdt_enable(WDTO_1S);
}

//================= END SETUP ===============//
//===========================================//
//============== MAIN LOOP BEGINS ===========//
void loop() {

  //============================================//
  //================= IR SENSOR ================//
  // Reference : https://www.dfrobot.com/wiki/index.php/SHARP_GP2Y0A41SK0F_IR_ranger_sensor_(4-30cm)_SKU:SEN0143

  //Serial.println(F("===IR SENSOR==="));

  // Read analog voltage and calculate distance
  IR_sensor = analogRead(IR_pin);
  if (IR_sensor < 16)  IR_sensor = 16;
  pay_dist = 2076 / (IR_sensor - 11); // this is for 4-30cm

  // Store distance data to SD
  IRData = SD.open("IR.txt", FILE_WRITE);
  if (IRData) {
    // Serial.println("Writing IR Sensor data to SD");
    IRData.println(pay_dist);
    IRData.close();
  }
  //else Serial.println(F("Could not save IR data"));

  // Transmit or print distance data
  //Serial.print(F("Payload bay distance reading:"));
  Serial.print(F("a"));
  Serial.println(pay_dist);
  //Serial.print(",");

  //==================================================//
  //=================== BMP + MCU ====================//

  // Read values from BMP
  //rtemp = bmp.readTemperature();
  //rpress = bmp.readPressure();
  //ralt = bmp.readAltitude(Ph);
  battemp = rocket_temp.readTempC();

  // Store enviro data to SD
  //enviroData = SD.open("envir.txt", FILE_WRITE);
  //if (enviroData) {
    //Serial.println(F("Writing Atmospheric data to SD"));
    //enviroData.print(rtemp);
    //enviroData.print(",");
//    enviroData.print(rpress);
//    enviroData.print(",");
//    enviroData.print(ralt);
//    enviroData.print(",");
//    enviroData.print(battemp);
//    enviroData.println();
//    delay(5);
//    enviroData.close();
//  }
  //else Serial.println(F("Could not save BMP data"));

  //Transmit or print atmospheric data
  //Serial.print(F("Temperature:"));
  //Serial.print("b");
  //Serial.println(rtemp);
  //Serial.print(F(","));

  //Serial.print(F("Pressure: "));
  //Serial.print("c");
  //Serial.println(rpress);
  //Serial.print(F(","));

  //Serial.print(F("Altitude: "));
  //Serial.print("d");
  //Serial.println(ralt);
  //Serial.print(F(","));

  //Serial.print(F("Battery Temp: "));
  Serial.print(F("e"));
  Serial.println(battemp);
  //Serial.print(F(","));

  //=============================================//
  //==================== GPS ====================//

  //Serial.println(F("===GPS==="));

  bool newData = false;
  //unsigned long chars;
  //unsigned short sentences, failed;

  // For one/twenty second we parse GPS data and report some key values
  for (unsigned long start = millis(); millis() - start < 50;)
  {
    while (ss.available())
    {
      char c = ss.read();
      //Serial.print(c); // uncomment this line if you want to see the GPS data flowing
      if (gps.encode(c)) // Did a new valid sentence come in?
        newData = true;          
    }
  }

  if (newData)
  {
  // Retrieve latitude and longitude to the millionth of a degree
  gps.get_position(&lat, &lon, &fix_age);

  // Time in hhmmsscc, date in ddmmyy
  //gps.get_datetime(&date, &time, &fix_age);

  // Returns speed in 100ths of a knot
  //speed = gps.speed();

  // Store GPS data
  GPSData = SD.open(F("gpsdata.txt"), FILE_WRITE);
  if (GPSData) {
    //Serial.println(F("Writing GPS data to SD"));
    GPSData.print(lat);
    GPSData.print(F(","));
    GPSData.print(lon);
    //GPSData.print(F(","));
    //GPSData.print(time);
    //GPSData.print(F(","));
    //GPSData.print(date);
    GPSData.print(F(","));
    GPSData.println(speed);
    delay(5);
    GPSData.close();
  }
  //else Serial.println(F("Could not save GPS data"));

  // Transmit or print GPS data
  //Serial.print(F("Lat Lon:"));
  Serial.print(F("f"));
  Serial.println(lat);
  //Serial.print(",");
  Serial.print(F("g"));
  Serial.println(lon);
  //Serial.print(F(","));
  //Serial.print("h");
  //Serial.println(time);
  //Serial.print(F(","));
  //Serial.println("i");
  //Serial.println(date);
  //Serial.print(F(","));
  Serial.println(F("j"));
  Serial.println(speed);
  //Serial.print(F(","));
  }
  //else (Serial.print("No GPS Data Found on Pin 4")
  
  //======================== MPUs =====================//
  //Serial.println(F("===AvBay MPU==="));

  // Collect Avionics MPU Data
  AGEval(avMPU);

  // Store Avionics MPU data
  avMPUData = SD.open("avMPU.txt", FILE_WRITE);
  if (avMPUData) {
    //Serial.println(F("Writing avMPU data to SD"));
    //avMPUData.print(AcX/2610.0);
    //avMPUData.print(F(","));
    //avMPUData.print(AcY/2610.0);
    //avMPUData.print(F(","));
    avMPUData.println(AcZ/2610.0);
    delay(5);
    avMPUData.close();
  }
  //else Serial.println(F("Could not save AvMPU data"));

  //Transmit or print AvAccel data
  //Serial.print("X: ");
  //Serial.print(F("k"));
  //Serial.println(AcX/2610.0);
  //Serial.print(F(","));
  //Serial.print(F("l"));
  //Serial.println(AcY/2610.0);
  //Serial.print(F(","));
  Serial.print(F("m"));
  Serial.println(AcZ/2610.0);
  //Serial.print(F(","));

  //Serial.println(F("===Payload MPU==="));

  // Collect Payload MPU data
  AGEval(payMPU);

  // Store Payload MPU Data
  payMPUData = SD.open("payMPU.txt", FILE_WRITE);
  if (payMPUData) {
    //Serial.println(F("Writing payMPU data to SD"));
    //payMPUData.print(AcX/2335.0);
    //payMPUData.print(F(","));
    //payMPUData.print(AcY/2335.0);
    //payMPUData.print(F(","));
    payMPUData.println(AcZ/2335.0);
    delay(5);
    payMPUData.close();
  }
  //else Serial.println(F("Could not save payMPU data"));

  //Transmit or print payAccel data
  //Serial.print("X: ");
  //Serial.print(F("n"));
  //Serial.println(AcX/2335.0);
  //Serial.print(F(","));
  //Serial.print(F("o"));
  //Serial.println(AcY/2335.0);
  //Serial.print(F(","));
  Serial.print(F("p"));
  Serial.println(AcZ/2335.0);
  //Serial.print(F(","));
}

//========================== FUNCTIONS ============================//

//void bmp_rocket() {
//  rtemp = bmp.readTemperature();
//  rpres = bmp.readPressure();
//  // ALT correction
//  // Barometric pressure varying with altitude is represented using the formula: P=Po*e^(-(Mg/RT)*h)
//  // Where Po=Sea level Bar. Pressure (use hPa)// M=molar mass of Earth's air//R=Universal Gas constant
//  //       T=Standard temperature// g=gravitational constant
//  //  exp_o = exp((-((M * g) / (R * T)) * h));
//  //  Ph = Po * exp_o;
//  ralt = bmp.readAltitude(Ph);
//}


// Evaluate acceleration data from MPU set to corresponding address (1 or 2 for Av, Pay respectively)
void AGEval(const int addr) {

  if (addr == 1) {

    Wire.beginTransmission(0x68);
    Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(0x68, 14, true); // request a total of 14 registers
  }
  
  else if (addr == 2) {

    Wire.beginTransmission(0x69);
    Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(0x69, 14, true); // request a total of 14 registers
  }

  //AcX = Wire.read() << 8 | Wire.read(); // 0x3F (ACCEL_XOUT_H) & 0x40 (ACCEL_ZOUT_L)
  //AcY = Wire.read() << 8 | Wire.read(); // 0x3F (ACCEL_YOUT_H) & 0x40 (ACCEL_ZOUT_L)
  AcZ = Wire.read() << 8 | Wire.read(); // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  //Tmp = Wire.read() << 8 | Wire.read(); // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)

}

void softReset(){
  asm volatile ("  jmp 0");
}

