#include "control/control.h"

#include "Arduino.h"
#include "utils/timer.h"
#include "utils/config.h"
#include "utils/status.h"
#include "utils/logging.h"
#include "control/display.h"
#include "control/vibration.h"

namespace Puck::Control
{
    void Setup()
    {
        setupDisplay();
        setupVibration();
        pinMode(BUTTON_PIN, INPUT_PULLUP);
    }

    void DrawText(const char *message)
    {
        display.clearBuffer();
        display.setFont(u8g2_font_samim_16_t_all);
        char *message_ = strdup(message);
        char *token = strtok(message_, "\n");

        int line_y = 20;
        while (token != NULL)
        {
            display.drawStr(0, line_y, token);
            token = strtok(NULL, "\n");
            line_y += 20;
        }
        free(message_);

        display.sendBuffer();
    }

    // TODO: Impliment usage milliOff
    void vibrate(int milliOn, int milliOff, bool loop)
    {
        if (!getVibrationStatus()) {
            enableVibration();
            timerDelay(milliOn, &disableVibration);
        }
    }

    void stopVibrate() {
        disableVibration();
    }

    bool isButtonPressed() {
        logln(digitalRead(BUTTON_PIN));
        if (digitalRead(BUTTON_PIN) == HIGH) {
            return false;
        } else {
            return true;
        }
    }
};
