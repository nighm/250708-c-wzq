#include <SDL3/SDL.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
    if (SDL_InitVideo() < 0) {
        printf("SDL3初始化失败: %s\n", SDL_GetError());
        return 1;
    }
    printf("SDL3版本: %d.%d.%d\n", SDL_MAJOR_VERSION, SDL_MINOR_VERSION, SDL_PATCHLEVEL);
    SDL_Quit();
    return 0;
}