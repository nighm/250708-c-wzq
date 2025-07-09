cmake_minimum_required(VERSION 3.10)
project(gomoku-sdl2)

# SDL3
set(SDL3_ROOT "${CMAKE_SOURCE_DIR}/third_party/SDL3")
include_directories("${SDL3_ROOT}/include")
link_directories("${SDL3_ROOT}/lib")

file(GLOB SOURCES src/*.cpp)

add_subdirectory(third_party/googletest-1.14.0)
enable_testing()

add_executable(gomoku ${SOURCES})
target_link_libraries(gomoku
    "${SDL3_ROOT}/lib/libSDL3.dll.a"
    "${SDL3_ROOT}/lib/libSDL3_ttf.dll.a"
)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 包含头文件目录
include_directories(include)

# 只保留主程序和测试目标的最小可用构建配置，无任何 PCH、target_precompile_headers、CheckCXXCompilerFlag 相关内容

# 预留测试目标（可选）
# file(GLOB TEST_SRC tests/*.cpp)
# add_executable(tests ${TEST_SRC})
# target_link_libraries(tests ${SDL3_LIBRARY})

add_executable(test_game_gtest tests/test_game_gtest.cpp src/game.cpp)
target_link_libraries(test_game_gtest gtest_main "${SDL3_ROOT}/lib/libSDL3.dll.a")
add_test(NAME test_game_gtest COMMAND test_game_gtest)

add_executable(test_ai_gtest tests/test_ai_gtest.cpp src/ai.cpp src/game.cpp)
target_link_libraries(test_ai_gtest gtest_main "${SDL3_ROOT}/lib/libSDL3.dll.a")
add_test(NAME test_ai_gtest COMMAND test_ai_gtest)

add_executable(test_gui_gtest tests/test_gui_gtest.cpp src/gui.cpp src/game.cpp src/ai.cpp)
target_link_libraries(test_gui_gtest gtest_main "${SDL3_ROOT}/lib/libSDL3.dll.a" "${SDL3_ROOT}/lib/libSDL3_ttf.dll.a")
add_test(NAME test_gui_gtest COMMAND test_gui_gtest)

# 必须在所有 add_executable 之后再添加 googletest 子目录

# 已删除的test_game.cpp相关目标移除

# 编译缓存（ccache/sccache）
find_program(CCACHE_PROGRAM ccache)
find_program(SCCACHE_PROGRAM sccache)
if(CCACHE_PROGRAM)
    message(STATUS "ccache detected, enabling...")
    set(CMAKE_C_COMPILER_LAUNCHER "${CCACHE_PROGRAM}")
    set(CMAKE_CXX_COMPILER_LAUNCHER "${CCACHE_PROGRAM}")
elseif(SCCACHE_PROGRAM)
    message(STATUS "sccache detected, enabling...")
    set(CMAKE_C_COMPILER_LAUNCHER "${SCCACHE_PROGRAM}")
    set(CMAKE_CXX_COMPILER_LAUNCHER "${SCCACHE_PROGRAM}")
endif()