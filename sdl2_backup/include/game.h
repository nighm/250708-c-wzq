#pragma once
#include <vector>
#include <utility>

// 棋盘尺寸
constexpr int BOARD_SIZE = 15;

// 玩家枚举
enum class Player { None, Black, White };

// 游戏状态
enum class GameStatus { Playing, BlackWin, WhiteWin, Draw };

class Game {
public:
    Game();
    void reset();
    bool placePiece(int row, int col, Player player);
    bool undo();
    Player getCell(int row, int col) const;
    Player currentPlayer() const;
    GameStatus status() const;
    const std::vector<std::pair<int, int>>& moveHistory() const;
private:
    std::vector<std::vector<Player>> board;
    std::vector<std::pair<int, int>> history;
    Player curPlayer;
    GameStatus gameStatus;
    bool checkWin(int row, int col, Player player) const;
    bool checkDraw() const;
}; 