#pragma once

#include <stdexcept>
#include <string>

namespace tinyhuman {

class TinyHumanError : public std::runtime_error {
public:
    TinyHumanError(const std::string& message, int status, const std::string& body = "")
        : std::runtime_error(message), status_(status), body_(body) {}

    int status() const noexcept { return status_; }
    const std::string& body() const noexcept { return body_; }

private:
    int status_;
    std::string body_;
};

} // namespace tinyhuman
