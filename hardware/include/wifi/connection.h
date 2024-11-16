#ifndef PUCK_CONNECTION_H
#define PUCK_CONNECTION_H

#include "Arduino.h"
#include <esp_http_client.h>

namespace Puck
{
    namespace impl
    {
        struct http_client
        {
            esp_http_client_handle_t handle;

            void init(esp_http_client_config_t const *config);
            esp_err_t open(int write_len);
            esp_err_t close();
            esp_err_t cleanup();
            esp_err_t perform();
            esp_err_t set_method(esp_http_client_method_t method);
            int get_status_code();
            int get_content_length();
            int read_response(char *buffer, int len);
        };
    }
    class Connection
    {
    public:
        Connection(int write_max_size = 0);
        ~Connection();

        Connection(Connection&& other);
        Connection& operator=(Connection&& other);

        esp_err_t set_method(esp_http_client_method_t method)
        {
            return handle.set_method(method);
        }
        esp_err_t perform(void *data, int length)
        {

            const esp_err_t code = handle.perform();
            if (code == ESP_OK)
                handle.read_response(static_cast<char *>(data), length);
            return code;
        }

    private:
        impl::http_client handle;
    };
};

#endif