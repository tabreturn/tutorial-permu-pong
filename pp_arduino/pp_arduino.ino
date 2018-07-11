// input types
// 1: 1-button
// 2: 2-button
// 3: analog

int input_mode = 1;

void setup() {
  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);
  Serial.begin(9600);
}

int ledState = HIGH;
int buttonState;
int lastButtonState = LOW;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;


void loop() {
  if (input_mode == 1) {
    Serial.println(!digitalRead(2));
  }
  
  if (input_mode == 2) {
    if (!digitalRead(2)) {
      Serial.println('L');
    }
    else if (!digitalRead(3)) {
      Serial.println('R');
    }
  }
  if (input_mode == 3) {
    Serial.println( analogRead(A0) );
  }
}
