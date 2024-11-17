#include <utils/config.h>
#include <control/display.h>

namespace Puck::Control
{
    Puck::Display display(Puck::DISPLAY_ROTATION, Puck::DISPLAY_CS_PIN, Puck::DISPLAY_DC_PIN, Puck::DISPLAY_RST_PIN);

    void setupDisplay()
    {
        display.begin();
    }
} // namespace Puck::Display
