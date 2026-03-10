#include <Servo.h>

Servo esc;

// Change these pins to match your wiring
const int escPin = 5;
const int ledPin = 10;

int motorSpeed = 1000;
bool ledOn = false;

void setMotor(int val) {
  if (val >= 1000 && val <= 2000) {
    motorSpeed = val;
    esc.writeMicroseconds(motorSpeed);

    Serial.print("OK MOTOR ");
    Serial.println(motorSpeed);
  } else {
    Serial.println("ERROR Invalid motor speed. Use 1000-2000.");
  }
}

void setLed(bool onState) {
  ledOn = onState;

  // ON/OFF only
  digitalWrite(ledPin, ledOn ? HIGH : LOW);

  Serial.print("OK LED ");
  Serial.println(ledOn ? "ON" : "OFF");
}

void setup() {
  Serial.begin(9600);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  esc.attach(escPin, 1000, 2000);
  esc.writeMicroseconds(1000);

  Serial.println("ESC arming...");
  delay(5000);
  Serial.println("READY");
  Serial.println("Use: LED ON");
  Serial.println("Use: LED OFF");
  Serial.println("Use: LED ON MOTOR 1200");
  Serial.println("Use: LED OFF MOTOR 1000");
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    input.toUpperCase();

    Serial.print("RX ");
    Serial.println(input);

    if (input == "LED ON") {
      setLed(true);
    }
    else if (input == "LED OFF") {
      setLed(false);
    }
    else if (input.startsWith("LED ON MOTOR ")) {
      setLed(true);
      int val = input.substring(String("LED ON MOTOR ").length()).toInt();
      setMotor(val);
    }
    else if (input.startsWith("LED OFF MOTOR ")) {
      setLed(false);
      int val = input.substring(String("LED OFF MOTOR ").length()).toInt();
      setMotor(val);
    }
    else {
      Serial.println("ERROR Invalid format. Use: LED ON, LED OFF, or LED ON/OFF MOTOR <1000-2000>");
    }
  }
}