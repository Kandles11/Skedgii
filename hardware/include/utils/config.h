#ifndef PUCK_CONFIG_H
#define PUCK_CONFIG_H

#include <Arduino.h>
#include <U8g2lib.h>

namespace Puck
{
    constexpr static gpio_num_t VIBRATION_SIGNAL_PIN = GPIO_NUM_1;

    // TODO: Define DISPLAY_
    using Display = U8G2_SH1106_128X64_NONAME_F_4W_HW_SPI;
    constexpr static auto DISPLAY_ROTATION = U8G2_R0;
    constexpr static gpio_num_t DISPLAY_CS_PIN = GPIO_NUM_2;
    constexpr static gpio_num_t DISPLAY_DC_PIN = GPIO_NUM_3;
    constexpr static gpio_num_t DISPLAY_RST_PIN = GPIO_NUM_4;
};

#endif