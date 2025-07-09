#include "gui.h"
#include <SDL.h>
#include <SDL_ttf.h>
#include <string>
#include <iostream>

struct Gui::Impl {
    SDL_Window* window = nullptr;
    SDL_Renderer* renderer = nullptr;
    int width, height;
    bool running = true;
    bool vsAI = false;
};

Gui::Gui(int width, int height) : impl(new Impl) {
    impl->width = width;
    impl->height = height;
    SDL_InitVideo();
    TTF_Init();
    impl->window = SDL_CreateWindow("五子棋 Gomoku", width, height, 0);
    impl->renderer = SDL_CreateRenderer(impl->window, SDL_RENDERER_ACCELERATED);
}

Gui::~Gui() {
    SDL_DestroyRenderer(impl->renderer);
    SDL_DestroyWindow(impl->window);
    TTF_Quit();
    SDL_Quit();
    delete impl;
}

void Gui::run(Game& game, bool vsAI) {
    impl->vsAI = vsAI;
    int cellSize = std::min(impl->width, impl->height) / BOARD_SIZE;
    while (impl->running) {
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT) impl->running = false;
            if (e.type == SDL_EVENT_MOUSE_BUTTON_DOWN && game.status() == GameStatus::Playing) {
                int x = e.button.x / cellSize;
                int y = e.button.y / cellSize;
                if (game.currentPlayer() == Player::Black || !vsAI) {
                    game.placePiece(y, x, game.currentPlayer());
                }
            }
        }
        // AI 回合
        if (vsAI && game.status() == GameStatus::Playing && game.currentPlayer() == Player::White) {
            auto move = AI::chooseMove(game, Player::White);
            if (move.first != -1)
                game.placePiece(move.first, move.second, Player::White);
        }
        // 绘制
        SDL_SetRenderDrawColor(impl->renderer, 240, 217, 181, 255);
        SDL_RenderClear(impl->renderer);
        // 画棋盘
        SDL_SetRenderDrawColor(impl->renderer, 0, 0, 0, 255);
        for (int i = 0; i <= BOARD_SIZE; ++i) {
            SDL_RenderDrawLine(impl->renderer, cellSize*i, 0, cellSize*i, cellSize*BOARD_SIZE);
            SDL_RenderDrawLine(impl->renderer, 0, cellSize*i, cellSize*BOARD_SIZE, cellSize*i);
        }
        // 画棋子
        for (int i = 0; i < BOARD_SIZE; ++i) {
            for (int j = 0; j < BOARD_SIZE; ++j) {
                Player p = game.getCell(i, j);
                if (p == Player::None) continue;
                SDL_SetRenderDrawColor(impl->renderer, p == Player::Black ? 0 : 255, p == Player::Black ? 0 : 255, p == Player::Black ? 0 : 255, 255);
                SDL_Rect rect = {j*cellSize+cellSize/8, i*cellSize+cellSize/8, cellSize*3/4, cellSize*3/4};
                SDL_RenderFillRect(impl->renderer, &rect);
            }
        }
        SDL_RenderPresent(impl->renderer);
        SDL_Delay(16);
    }
} 