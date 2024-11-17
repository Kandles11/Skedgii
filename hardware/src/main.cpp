#ifndef PUCK_MAIN_CPP
#define PUCK_MAIN_CPP

#include <Arduino.h>
#include "utils/logging.h"
#include "utils/timer.h"
#include "utils/config.h"
#include "utils/status.h"
#include "control/control.h"
#include "wifi/wireless.h"
#include "wifi/connection.h"
#include "../env.h"

using namespace Puck;
void setup()
{
    // Serial port for debugging purposes
    if (DO_LOGGING)
        Serial.begin(115200);

    Control::Setup();
    Control::vibrate(10000, 1000, true);
    Control::DrawText("Hello World 1\nHello World 2\nHello World 3");

    // Connect to the WiFi
    connectWiFI();
}

void loop()
{
    if (Control::isButtonPressed() && getVibrationStatus()) {
        Control::stopVibrate();
    }
    delay(100);
    timerStep();
}

#endif
