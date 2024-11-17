#ifndef PUCK_CONTROL_H
#define PUCK_CONTROL_H

namespace Puck::Control
{
    void Setup();
    void Vibrate(int milliOn, int milliOff, bool loop);
    void DrawText(const char *message);
};

#endif