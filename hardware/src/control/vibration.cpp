#include "control/vibration.h"

#include "Arduino.h"
#include "utils/config.h"

namespace Puck::Control
{
    void setupVibration() {
        pinMode(VIBRATION_SIGNAL_PIN, OUTPUT);
    }

    void enableVibration() {
        digitalWrite(VIBRATION_SIGNAL_PIN, HIGH);
    }

    void disableVibration() {
        digitalWrite(VIBRATION_SIGNAL_PIN, LOW);
    }
};
