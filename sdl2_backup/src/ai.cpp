#include "ai.h"
#include <vector>
#include <cstdlib>
#include <ctime>

std::pair<int, int> AI::chooseMove(const Game& game, Player aiPlayer) {
    // 简单AI：优先中心、否则随机可落点
    int bestRow = -1, bestCol = -1;
    int center = BOARD_SIZE / 2;
    if (game.getCell(center, center) == Player::None)
        return {center, center};
    std::vector<std::pair<int, int>> candidates;
    for (int i = 0; i < BOARD_SIZE; ++i) {
        for (int j = 0; j < BOARD_SIZE; ++j) {
            if (game.getCell(i, j) == Player::None)
                candidates.emplace_back(i, j);
        }
    }
    if (candidates.empty()) return {-1, -1};
    std::srand((unsigned)std::time(nullptr));
    int idx = std::rand() % candidates.size();
    return candidates[idx];
}

// AI决策逻辑实现
// TODO: 优化 minimax 算法的剪枝策略以提升性能 <-- 添加此行
void AI::makeDecision() {
    // ... 现有代码 ...
}