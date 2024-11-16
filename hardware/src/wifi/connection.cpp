#include <wifi/connection.h>
#include <esp_log.h>

namespace Puck
{
    Connection::Connection(int write_max_size)
    {
        const esp_http_client_config_t ESP_HTTP_CONFIG{
            .host = "127.0.0.1",
            .port = 1111,
            .path = "/",
            .query = "esp",
        };

        handle.init(&ESP_HTTP_CONFIG);
        handle.open(write_max_size);
    }

    Connection::~Connection()
    {
        handle.close();
        handle.cleanup();
    }

    Connection::Connection(Connection &&other)
    {
        handle = other.handle;
        other.handle.handle = nullptr;
    }

    Connection &Connection::operator=(Connection &&other)
    {
        if (&other == this)
        {
            return *this;
        }
        handle = other.handle;
        other.handle.handle = nullptr;
        return *this;
    }

    namespace impl
    {
        void http_client::init(esp_http_client_config_t const *config)
        {
            handle = esp_http_client_init(config);
        }
        esp_err_t http_client::open(int write_len)
        {
            return esp_http_client_open(handle, write_len);
        }
        esp_err_t http_client::close()
        {
            return esp_http_client_close(handle);
        }
        esp_err_t http_client::cleanup()
        {
            return esp_http_client_cleanup(handle);
        }
        esp_err_t http_client::perform()
        {
            return esp_http_client_perform(handle);
        }
        esp_err_t http_client::set_method(esp_http_client_method_t method)
        {
            return esp_http_client_set_method(handle, method);
        }
        int http_client::get_status_code()
        {
            return esp_http_client_get_status_code(handle);
        }
        int http_client::get_content_length()
        {
            return esp_http_client_get_content_length(handle);
        }
        int http_client::read_response(char *buffer, int len)
        {
            return esp_http_client_read_response(handle, buffer, len);
        }
    }
}
