#ifndef PUCK_STATUS_H
#define PUCK_STATUS_H

namespace Puck
{
    bool getConnectionStatus();
    void setConnectionStatus(bool value);

    bool getVibrationStatus();
    void setVibrationStatus(bool value);
};

#endif