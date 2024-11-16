#ifndef PUCK_CONTROL_CPP
#define PUCK_CONTROL_CPP

#include "control/control.h"

#include "Arduino.h"
#include "utils/timer.h"
#include "control/vibration.h"

namespace Puck
{
    void setupPuck() {
        setupVibration();
    }

    void vibrate(int milliOn, int milliOff, bool loop) {
        enableVibration();
        timerDelay(milliOn, &disableVibration);
    }
};

#endif