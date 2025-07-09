#include <gtest/gtest.h>
#include "game.h"

TEST(GameTest, PlacePieceAndUndo) {
    Game g;
    EXPECT_EQ(g.getCell(7, 7), Player::None);
    EXPECT_TRUE(g.placePiece(7, 7, Player::Black));
    EXPECT_EQ(g.getCell(7, 7), Player::Black);
    EXPECT_TRUE(g.undo());
    EXPECT_EQ(g.getCell(7, 7), Player::None);
}

TEST(GameTest, WinCondition) {
    Game g;
    for (int i = 0; i < 5; ++i) g.placePiece(0, i, Player::Black);
    EXPECT_EQ(g.status(), GameStatus::BlackWin);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
} 