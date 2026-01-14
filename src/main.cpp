#include <Arduino.h>
#include <AccelStepper.h>
#include <ArduinoJson.h>

// pin mappings for ramps 1.6
// axis: label, step, direction, enable (in that order)

AccelStepper base(1, 54, 55); // x-axis
AccelStepper shoulder(1, 60, 61); // y-axis
AccelStepper elbow(1, 46, 48); // z-axis
AccelStepper wrist1(1, 26, 28); // e0-axis
AccelStepper wrist2(1, 36, 34); // e1-axis
// gripper omitted here since ramps 1.6 can only support up to 5 axes.

// group the enable pins (ramps separates these)
const int enablePins[] = {38, 56, 62, 24, 30, 66};

// array to store pointers to each axis
AccelStepper* arm[] = {&base, &shoulder, &elbow, &wrist1, &wrist2};

void setup() {
  // initialize enable pins (low means active for tmc2209)
  for (int pin : enablePins) {
    pinMode(pin, OUTPUT);
    digitalWrite(pin, LOW); // turn on drivers
  }

  // configure the speeds and accelerations of each axis
  for (int i = 0; i < 5; i++) {
    arm[i]->setMaxSpeed(1000); // steps per second
    arm[i]->setAcceleration(500); // steps per second^2
  }
}

void loop() {
  // main code here runs repeatedly
  // check for incoming json commands from python
  if (Serial.available() > 0) {
    JsonDocument doc; // initialize doc
    DeserializationError error = deserializeJson(doc, Serial);
    
    if (!error) {
      // expecting json format: {"t":[x, y, z, e0, e1]}
      JsonArray targets = doc["t"];
      if (targets.size() == 5) { // we can change this to 6 later
        for (int i = 0; i < 5; i++) {
          arm[i]->moveTo(targets[i]); // access the position at the respective axis
        }
      }
    }
  }

  // motor engine - must be called every loop iteration
  // this calculates if a step is needed and pulses the step pin
  for (int i = 0; i < 5; i++) {
    arm[i]->run();
  }
}