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
            esp_err_t set_timeout_ms(int timeout_ms);
            int get_status_code();
            int get_content_length();
            int read_response(char *buffer, int len);
        };
    }
    class Connection
    {
    public:
        Connection(esp_http_client_config_t const &config, int write_max_size = 0);
        Connection(const char *host, int port, const char *path, const char *query, int write_max_size = 0);
        ~Connection();

        Connection(Connection &&other);
        Connection &operator=(Connection &&other);

        esp_err_t set_method(esp_http_client_method_t method)
        {
            return handle.set_method(method);
        }
        esp_err_t perform(void *data, int length, int timeout_ms = 0)
        {

            if (timeout_ms > 0)
            {
                handle.set_timeout_ms(timeout_ms);
            }
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