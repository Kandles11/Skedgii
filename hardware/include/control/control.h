#ifndef PUCK_CONTROL_H
#define PUCK_CONTROL_H

namespace Puck::Control
{
    void Setup();
    void vibrate(int milliOn, int milliOff, bool loop);
    void stopVibrate();
    void DrawText(const char *message);
    bool isButtonPressed();
};

#endif