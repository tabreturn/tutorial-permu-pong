// analog Input : Force Resistive Sensor Interface
// 1 FRS, 1 breadboard, hook-up wires, 1 10kOhm resistor
// For a schematic visit https://learn.adafruit.com/force-sensitive-resistor-fsr/using-an-fsr


int reading; // reading from analog pin
int lowest = 512;
int highest = 512; // highest value assumed 512
int output; //

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  reading = analogRead(A0);
  lowest = min(reading, lowest);
  highest = max(reading, highest);
  output = map(reading, lowest, highest, 0, 1024);
  Serial.println(output);
}
