#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <MPU6050_tockn.h>

Adafruit_BMP280 bmp;
MPU6050 mpu(Wire);

void setup() {
  Serial.begin(9600);
  while(!Serial);
  
  if (!bmp.begin(0x76)) {
    Serial.println("Could not find a valid BMP280 sensor, check wiring!");
    while (1);
  }
  
  mpu.begin();
  mpu.calcGyroOffsets(true);
}

void loop() {
  sensors_event_t event;
  bmp.getEvent(&event);
  float pressure = event.pressure;
  
  Vector rawAccel = mpu.readRawAccel();
  Vector normAccel = mpu.readNormalizeAccel();

  Serial.print("Pressure: ");
  Serial.print(pressure);
  Serial.print(" Pa\t");

  Serial.print("Accel X: ");
  Serial.print(normAccel.XAxis);
  Serial.print("\tY: ");
  Serial.print(normAccel.YAxis);
  Serial.print("\tZ: ");
  Serial.print(normAccel.ZAxis);
  Serial.println();

  delay(500);
}
