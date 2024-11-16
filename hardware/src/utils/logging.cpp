#ifndef PUCK_LOGGING_CPP
#define PUCK_LOGGING_CPP

#include "utils/logging.h"
#include "../env.h"

#include <Arduino.h>
#include <iostream>

#include "utils/status.h"

namespace Puck
{
    void log(char message[]) {
        if (DO_LOGGING) Serial.print(message);
    }

    void log(int value) {
        if (DO_LOGGING) Serial.print(value);
    }

    void log(float value) {
        if (DO_LOGGING) Serial.print(value);
    }

    void logln(char message[]) {
        if (DO_LOGGING) Serial.println(message);
    }

    void logln(int value) {
        if (DO_LOGGING) Serial.println(value);
    }

    void logln(float value) {
        if (DO_LOGGING) Serial.println(value);
    }

    void logln(std::string value) {
        if (DO_LOGGING) Serial.println(value.c_str());
    }

    void logError(char message[], int error) {
        if (DO_LOGGING) Serial.printf(message, error);
    }
};

#endif