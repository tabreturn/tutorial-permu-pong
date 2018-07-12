// 2-button interface
// 2 momentary switches, 1 breadboard, hook-up wires, 2 10kOhm resistor
// Button 1 connected to 5V & pin 2 with jumpers - this button will trigger the paddle to move upwards
// Button 2 connected to 5V & pin 3 with jumpers - this button will trigger the paddle to move downwards
// Button connected to GND with 10kOhm resistor
// For a schematic of the wiring visit https://www.arduino.cc/en/Tutorial/Button 


// constants won't change. They're used here to set pin numbers:
const int upButton = 2;    // the number of the right pushbutton pin - send U
const int downButton = 3;    // the number of the pushbutton pin - send D

// Variables will change:
int upButtonState;             // the current reading from the input pin
int lastUpButtonState = LOW;   // the previous reading from the input pin

int downButtonState;             // the current reading from the input pin
int lastDownButtonState = LOW;   // the previous reading from the input pin

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastUpDebounceTime, lastDownDebounceTime = 0;  // the last time the output pin was toggled
unsigned long upDebounceDelay, downDebounceDelay = 50;    // the debounce time; increase if the output flickers

char moveMe;

void setup() {
  Serial.begin(9600);

  pinMode(upButton, INPUT);
  pinMode(downButton, INPUT);
}

void loop() {
  // read the state of the switch into a local variable:
  int upReading = digitalRead(upButton);
  int downReading = digitalRead(downButton);

  // check to see if you just pressed the button
  // (i.e. the input went from LOW to HIGH), and you've waited long enough
  // since the last press to ignore any noise:

  // If the switch changed, due to noise or pressing:
  if (upReading != lastUpButtonState) {
    // reset the debouncing timer
    lastUpDebounceTime = millis();
  }
  if (downReading != lastDownButtonState) {
    // reset the debouncing timer
    lastUpDebounceTime = millis();
  }

  if ((millis() - lastUpDebounceTime) > upDebounceDelay) {
    // whatever the reading is at, it's been there for longer than the debounce
    // delay, so take it as the actual current state:

    // if the button state has changed:
    if (upReading != upButtonState) {
      upButtonState = upReading;

      // only toggle if the new button state is HIGH
      if (upButtonState == HIGH) {
        moveMe = 'U';
      }
    }
  }

  if ((millis() - lastDownDebounceTime) > downDebounceDelay) {
    if (downReading != downButtonState) {
      downButtonState = downReading;

      // only toggle if the new button state is HIGH
      if (downButtonState == HIGH) {
        moveMe = 'D';
      }
    }
  }

  // send the signal via Serial
  Serial.println(moveMe);

  // save the reading. Next time through the loop, it'll be the lastButtonState:
  lastUpButtonState = upReading;
  lastDownButtonState = downReading;
}
