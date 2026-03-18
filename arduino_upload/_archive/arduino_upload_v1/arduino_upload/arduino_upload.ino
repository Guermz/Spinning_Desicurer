#include <Servo.h>

Servo esc;  // ESC control
const int ledPin = 9;  // PWM pin for LED

int motorSpeed = 1000; // Default ESC throttle
bool ledOn = false;

void setup() {
  Serial.begin(9600);
  esc.attach(6); // ESC signal on pin 6
  esc.writeMicroseconds(1000); // Minimum throttle to arm ESC
  pinMode(ledPin, OUTPUT);
  analogWrite(ledPin, 0); // LED off initially

  Serial.println("System ready. Use format: LED ON/OFF MOTOR <1000-2000>");
  delay(2000); // Give ESC time to initialize
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    input.toUpperCase();

    if (input.startsWith("LED ") && input.indexOf("MOTOR") != -1) {
      // Parse LED state
      if (input.indexOf("LED ON") != -1) {
        ledOn = true;
        analogWrite(ledPin, 255); // Full brightness
      } else if (input.indexOf("LED OFF") != -1) {
        ledOn = false;
        analogWrite(ledPin, 0); // LED off
      }

      // Parse motor speed
      int motorIndex = input.indexOf("MOTOR") + 6;
      String speedStr = input.substring(motorIndex);
      int val = speedStr.toInt();
      if (val >= 1000 && val <= 2000) {
        motorSpeed = val;
        esc.writeMicroseconds(motorSpeed);
        Serial.print("LED is ");
        Serial.println(ledOn ? "ON" : "OFF");
        Serial.print("Motor speed set to: ");
        Serial.println(motorSpeed);
      } else {
        Serial.println("Invalid motor speed. Enter between 1000 and 2000.");
      }
    } else {
      Serial.println("Invalid format. Use: LED ON/OFF MOTOR <1000-2000>");
    }
  }
}