#include <gtest/gtest.h>
#include "tinyhuman/error.hpp"

using namespace tinyhuman;

TEST(TinyHumanErrorTest, ConstructorSetsFields) {
    TinyHumanError err("test error", 404, "body text");
    EXPECT_EQ(err.status(), 404);
    EXPECT_EQ(std::string(err.what()), "test error");
    EXPECT_EQ(err.body(), "body text");
}

TEST(TinyHumanErrorTest, DefaultEmptyBody) {
    TinyHumanError err("msg", 500);
    EXPECT_EQ(err.status(), 500);
    EXPECT_EQ(err.body(), "");
}

TEST(TinyHumanErrorTest, IsRuntimeError) {
    TinyHumanError err("msg", 500);
    const std::runtime_error* base = &err;
    EXPECT_NE(base, nullptr);
    EXPECT_EQ(std::string(base->what()), "msg");
}
