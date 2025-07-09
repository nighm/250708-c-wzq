cmake_minimum_required(VERSION 3.10)
project(gomoku-sdl2)

# 将SDL3替换为SDL3
find_package(SDL3 REQUIRED)
include_directories(${SDL3_INCLUDE_DIR})

file(GLOB SOURCES src/*.cpp)
add_executable(gomoku ${SOURCES})

target_link_libraries(gomoku ${SDL3_LIBRARY})
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 包含头文件目录
include_directories(include)

# 查找SDL3
# 将SDL3相关配置替换为SDL3
find_package(SDL3 REQUIRED)
include_directories(\${SDL3_INCLUDE_DIR})

# 源文件
file(GLOB SRC_FILES src/*.cpp)

add_executable(gomoku-sdl2 ${SRC_FILES})

target_link_libraries(gomoku-sdl2 \${SDL3_LIBRARY})

# 预留测试目标（可选）
# file(GLOB TEST_SRC tests/*.cpp)
# add_executable(tests ${TEST_SRC})
# target_link_libraries(tests ${SDL3_LIBRARY})