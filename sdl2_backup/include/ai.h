#pragma once
#include "game.h"
#include <utility>

class AI {
public:
    // 传入当前棋盘和玩家，返回AI选择的落子点(row, col)
    static std::pair<int, int> chooseMove(const Game& game, Player aiPlayer);
}; 