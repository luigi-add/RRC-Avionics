#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(11, 10);
Adafruit_GPS GPS(&mySerial);

void setup() {
  // put your setup code here, to run once:
Serial.begin(115200); 
GPS.begin(9600);
// Setup recommended minimum data collection 
GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA); 
 // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate

}

void loop() {

char c = GPS.read(); 

if (GPS.newNMEAreceived()) {
    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another
  }

  if (GPS.fix) {

    Serial.print(GPS.latitudeDegrees, 4);
    Serial.print(", ");
    Serial.println(GPS.longitudeDegrees, 4);


  }



}
