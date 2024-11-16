#ifndef PUCK_STATUS_CPP
#define PUCK_STATUS_CPP

#include "utils/status.h"

namespace Puck
{
    bool connected = false;

    bool getConnectionStatus() {
        return connected;
    }

    void setConnectionStatus(bool value) {
        connected = value;
    }
};

#endif