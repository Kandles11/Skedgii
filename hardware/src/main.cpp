#ifndef PUCK_MAIN_CPP
#define PUCK_MAIN_CPP

#include <Arduino.h>
#include "utils/logging.h"
#include "utils/timer.h"
#include "utils/config.h"
#include "utils/status.h"
#include "control/control.h"
#include "wifi/wireless.h"
#include "wifi/connection.h"
#include "../env.h"

#include <mutex>

#include "cJSON.h"

using namespace Puck;

struct periodic_info
{
    int sig;
    sigset_t alarm_sig;
};

sigset_t alarm_sig;
Connection *connection = nullptr;
std::mutex *mtx = nullptr;

static void *background(void *);
static int make_periodic(int unsigned period, struct periodic_info *info);
static void wait_period(struct periodic_info *info);

bool isFresh = false;
bool isSpin = false;

void setup()
{
    mtx = new std::mutex;

    // Serial port for debugging purposes
    if (DO_LOGGING)
        Serial.begin(115200);

    Control::Setup();
    Control::vibrate(10000, 1000, true);
    Control::DrawText("Hello World 1\nHello World 2\nHello World 3");

    // Connect to the WiFi
    connectWiFI();

    // Connect server
    sigemptyset(&alarm_sig);
    for (int i = SIGRTMIN; i <= SIGRTMAX; i++)
        sigaddset(&alarm_sig, i);
    sigprocmask(SIG_BLOCK, &alarm_sig, NULL);
    connection = new Connection(SERVER_IP, SERVER_PORT, "/ratings/puck/", "", 0);
    pthread_t conn_thread;
    pthread_create(&conn_thread, nullptr, background, nullptr);
}

void loop()
{
    {
        std::lock_guard<std::mutex> lk(*mtx);
        if (isFresh)
        {
            setVibrationStatus(isSpin);
        }
    }

    if (Control::isButtonPressed() && getVibrationStatus())
    {
        Control::stopVibrate();
    }
    delay(100);
    timerStep();
}

static void *background(void *)
{
    struct periodic_info info;
    make_periodic(10000, &info);
    size_t data_size = getpagesize();
    while (true)
    {
        char *data = (char *)calloc(1, data_size);
        esp_err_t code = connection->perform(data, data_size, 1000);
        if (code == ESP_OK)
        {
            cJSON *json = cJSON_Parse(data);

            cJSON *subjson = cJSON_GetObjectItem(json, "data");
            cJSON *status_ = cJSON_GetObjectItem(json, "classOpen");

            if (cJSON_IsBool(status_))
            {
                std::unique_lock<std::mutex> lk(*mtx);
                isFresh = true;
                isSpin = cJSON_IsTrue(status_);
            }

            cJSON_Delete(json);
        }

        wait_period(&info);
    }

    return nullptr;
}

static int make_periodic(int unsigned period, struct periodic_info *info)
{
    static int next_sig;
    int ret;
    unsigned int ns;
    unsigned int sec;
    struct sigevent sigev;
    timer_t timer_id;
    struct itimerspec itval;

    /* Initialise next_sig first time through. We can't use static
       initialisation because SIGRTMIN is a function call, not a constant */
    if (next_sig == 0)
        next_sig = SIGRTMIN;
    /* Check that we have not run out of signals */
    if (next_sig > SIGRTMAX)
        return -1;
    info->sig = next_sig;
    next_sig++;
    /* Create the signal mask that will be used in wait_period */
    sigemptyset(&(info->alarm_sig));
    sigaddset(&(info->alarm_sig), info->sig);

    /* Create a timer that will generate the signal we have chosen */
    sigev.sigev_notify = SIGEV_SIGNAL;
    sigev.sigev_signo = info->sig;
    sigev.sigev_value.sival_ptr = (void *)&timer_id;
    ret = timer_create(CLOCK_MONOTONIC, &sigev, &timer_id);
    if (ret == -1)
        return ret;

    /* Make the timer periodic */
    sec = period / 1000000;
    ns = (period - (sec * 1000000)) * 1000;
    itval.it_interval.tv_sec = sec;
    itval.it_interval.tv_nsec = ns;
    itval.it_value.tv_sec = sec;
    itval.it_value.tv_nsec = ns;
    ret = timer_settime(timer_id, 0, &itval, NULL);
    return ret;
}

static void wait_period(struct periodic_info *info)
{
    int sig;
    sigwait(&(info->alarm_sig), &sig);
}

#endif
