#include "game.h"
#include "gui.h"
#include <iostream>

int main(int argc, char* argv[]) {
    std::cout << "五子棋 Gomoku (SDL2版)\n";
    std::cout << "1. 人机对战\n2. 双人对战\n请选择模式(1/2): ";
    int mode = 1;
    std::cin >> mode;
    Game game;
    Gui gui(800, 800);
    gui.run(game, mode == 1);
    return 0;
} 