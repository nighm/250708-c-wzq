#include <gtest/gtest.h>
#include "ai.h"
#include "game.h"
#include <iostream> // Added for std::cout

TEST(AITest, ChooseMoveOnEmptyBoard) {
    Game g;
    auto move = AI::chooseMove(g, Player::Black);
    EXPECT_GE(move.first, 0);
    EXPECT_GE(move.second, 0);
    EXPECT_LT(move.first, 15);
    EXPECT_LT(move.second, 15);
}

TEST(AITest, ChooseMoveNoAvailable) {
    Game g;
    // 填满棋盘，交替落子
    Player p = Player::Black;
    for (int i = 0; i < 15; ++i)
        for (int j = 0; j < 15; ++j) {
            bool ok = g.placePiece(i, j, p);
            ASSERT_TRUE(ok);
            p = (p == Player::Black ? Player::White : Player::Black);
        }
    std::cout << "center cell: " << static_cast<int>(g.getCell(7, 7)) << std::endl;
    EXPECT_NE(g.getCell(7, 7), Player::None);
    for (int i = 0; i < 15; ++i) {
        for (int j = 0; j < 15; ++j) {
            std::cout << static_cast<int>(g.getCell(i, j)) << " ";
        }
        std::cout << std::endl;
    }
    auto move = AI::chooseMove(g, Player::White);
    EXPECT_EQ(move.first, -1);
    EXPECT_EQ(move.second, -1);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
} 