#ifndef PUCK_STATUS_H
#define PUCK_STATUS_H

namespace Puck
{
    bool getConnectionStatus();
    void setConnectionStatus(bool value);

    bool getLoggingStatus();
    void setLoggingStatus(bool value);
};

#endif