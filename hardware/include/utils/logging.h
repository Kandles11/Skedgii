#ifndef PUCK_LOGGING_H
#define PUCK_LOGGING_H

#include <string>

namespace Puck
{
    void log(char message[]);
    void log(int value);

    void logln(char message[]);
    void logln(int value);
    void logln(std::string value);

    void logError(char message[], int error);
};

#endif