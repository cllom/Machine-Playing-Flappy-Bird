/*
  modified 17 Apr 2021
  by Marcello tania

  This work may be reproduced, modified, distributed,
  performed, and displayed for any purpose. Copyright is
  retained and must be preserved. The work is provided
  as is; no warranty is provided, and users accept all 
  liability.
*/


#include <Servo.h>

Servo myservo; // create servo object to control a servo
const int ledPin = 13; // the pin that the LED is attached to
int incomingByte;      // a variable to read incoming serial data into
  
void setup() {
  // initialize serial communication:
  Serial.begin(38400);
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);
  myservo.attach(9); // attaches the servo on pin 9 to the servo object
}

void loop() {
  // see if there's incoming serial data:
  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    incomingByte = Serial.read();
    // if it's a capital H (ASCII 72), turn on the LED:
    if (incomingByte == 'H') {
      digitalWrite(ledPin, HIGH);
      myservo.write(8); // sets the servo position according to the scaled value
      delay(20);
    }else if (incomingByte == 'L') {
      digitalWrite(ledPin, LOW);
      myservo.write(30); // sets the servo position according to the scaled value
      delay(20);
    }else if (incomingByte == 'R') {
      digitalWrite(ledPin, LOW);
      myservo.write(30); // sets the servo position according to the scaled value
      delay(200);
    }
    
  }
  Serial.println(Serial.read());
}
