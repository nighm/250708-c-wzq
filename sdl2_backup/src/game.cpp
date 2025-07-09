#include "game.h"
#include <algorithm>

Game::Game() {
    reset();
}

void Game::reset() {
    board.assign(BOARD_SIZE, std::vector<Player>(BOARD_SIZE, Player::None));
    history.clear();
    curPlayer = Player::Black;
    gameStatus = GameStatus::Playing;
}

bool Game::placePiece(int row, int col, Player player) {
    if (row < 0 || row >= BOARD_SIZE || col < 0 || col >= BOARD_SIZE) return false;
    if (board[row][col] != Player::None) return false;
    if (gameStatus != GameStatus::Playing) return false;
    board[row][col] = player;
    history.emplace_back(row, col);
    if (checkWin(row, col, player)) {
        gameStatus = (player == Player::Black) ? GameStatus::BlackWin : GameStatus::WhiteWin;
    } else if (checkDraw()) {
        gameStatus = GameStatus::Draw;
    } else {
        curPlayer = (player == Player::Black) ? Player::White : Player::Black;
    }
    return true;
}

bool Game::undo() {
    if (history.empty() || gameStatus != GameStatus::Playing) return false;
    auto last = history.back();
    board[last.first][last.second] = Player::None;
    history.pop_back();
    curPlayer = (curPlayer == Player::Black) ? Player::White : Player::Black;
    return true;
}

Player Game::getCell(int row, int col) const {
    if (row < 0 || row >= BOARD_SIZE || col < 0 || col >= BOARD_SIZE) return Player::None;
    return board[row][col];
}

Player Game::currentPlayer() const {
    return curPlayer;
}

GameStatus Game::status() const {
    return gameStatus;
}

const std::vector<std::pair<int, int>>& Game::moveHistory() const {
    return history;
}

bool Game::checkWin(int row, int col, Player player) const {
    static const int dirs[4][2] = { {0,1},{1,0},{1,1},{1,-1} };
    for (auto& d : dirs) {
        int cnt = 1;
        for (int k = 1; k <= 4; ++k) {
            int r = row + d[0]*k, c = col + d[1]*k;
            if (r<0||r>=BOARD_SIZE||c<0||c>=BOARD_SIZE||board[r][c]!=player) break;
            ++cnt;
        }
        for (int k = 1; k <= 4; ++k) {
            int r = row - d[0]*k, c = col - d[1]*k;
            if (r<0||r>=BOARD_SIZE||c<0||c>=BOARD_SIZE||board[r][c]!=player) break;
            ++cnt;
        }
        if (cnt >= 5) return true;
    }
    return false;
}

bool Game::checkDraw() const {
    for (const auto& row : board)
        for (auto cell : row)
            if (cell == Player::None) return false;
    return true;
} 