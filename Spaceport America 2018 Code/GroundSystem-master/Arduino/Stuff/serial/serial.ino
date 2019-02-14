char a;


void setup() {
  delay(500);
  Serial.begin(57600);              //Starting serial communication
  pinMode(LED_BUILTIN, OUTPUT);
}
  
void loop() {
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on
  Serial.write("\a25\r"); //14 IRdistance
  Serial.write("\b34.87\r"); //12 pressTemp
  Serial.write("\f4573\r"); //15 pressure
  Serial.write("\n347\r"); //11 pressAlt
  Serial.write("\t64.65\r"); //13 tempBattery
  Serial.write("\v43.780724\r"); //0 gpsLat
  Serial.write("\\-79.418214\r"); //1 gpsLong
  Serial.write("^2345\r"); //3 gpsTime
  Serial.write("\'234534.42\r"); //3 gpsDate
  Serial.write("\"123.52\r"); //2 gpsSpeed
  Serial.write("~45.73\r"); //5 accelX rocket
  Serial.write("@23.753\r"); //6 accelY rocket
  Serial.write("#72.6523\r"); //7 accelZ rocket
  Serial.write("$54.12\r"); //8 accelX1 payload
  Serial.write("&65.643\r"); //9 accelY1 payload
  Serial.write("%-34.653\r"); //10 accelZ1 payload
  
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);   // turn the LED on
  delay(500);
}
