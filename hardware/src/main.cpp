#ifndef PUCK_MAIN_CPP
#define PUCK_MAIN_CPP

#include <Arduino.h>
#include "utils/logging.h"
#include "utils/timer.h"
#include "utils/config.h"
#include "control/control.h"
#include "wifi/wireless.h"
#include "wifi/connection.h"
#include "../env.h"

using namespace Puck;

void setup() {
    // Serial port for debugging purposes
    if (DO_LOGGING) Serial.begin(115200);

    setupPuck();
    vibrate(1000, 1000, true);

    // Connect to the WiFi
    connectWiFI();
}

void loop() {
    delay(100);
  	timerStep();
}

#endif

