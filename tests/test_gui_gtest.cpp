#include <gtest/gtest.h>
#include "gui.h"

TEST(GuiTest, ConstructDestruct) {
    // 只测试能否正常构造和析构，不弹窗
    Gui* gui = nullptr;
    EXPECT_NO_THROW({ gui = new Gui(800, 800); });
    EXPECT_NE(gui, nullptr);
    EXPECT_NO_THROW({ delete gui; });
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
} 