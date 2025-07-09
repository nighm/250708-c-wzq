#pragma once
#include "game.h"

class Gui {
public:
    Gui(int width, int height);
    ~Gui();
    void run(Game& game, bool vsAI = false);
private:
    struct Impl;
    Impl* impl;
}; 