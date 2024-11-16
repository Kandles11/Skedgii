#ifndef PUCK_WIRELESS_H
#define PUCK_WIRELESS_H

namespace Puck
{
    char* getWifiStatus(int status);
    void checkConnection();
    void connectWiFI();
    void createWiFi();
};

#endif