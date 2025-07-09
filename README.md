# gomoku-sdl2

基于 SDL2 的中型 C++ 五子棋项目

## 项目简介
- 采用 C++17 标准，SDL2 实现窗口化图形界面
- 支持人机对战（AI），悔棋、重新开始、胜负判断等基本功能
- 结构清晰，便于维护和扩展

## 目录结构
```
├── CMakeLists.txt         # CMake 构建脚本
├── README.md              # 项目说明
├── manage.py              # 一键管理脚本
├── include/               # 头文件
├── src/                   # 源文件
├── assets/                # 资源文件（图片/字体等）
├── tests/                 # 单元测试
└── docs/                  # 设计文档
```

## 依赖环境
- g++ (推荐 MinGW-w64)
- CMake 3.10+
- SDL2 开发包
- Python 3.x（仅用于 manage.py 辅助脚本）

## 编译与运行
1. 安装 SDL2 开发包，并配置好环境变量（INCLUDE、LIB）
2. 一键编译/运行（推荐）：
   ```bash
   python manage.py build
   python manage.py run
   ```
3. 手动编译：
   ```bash
   mkdir build
   cd build
   cmake -G "MinGW Makefiles" ..
   cmake --build .
   ./gomoku-sdl2.exe
   ```

## 常见问题
- SDL2 未找到：请确认 SDL2 开发包已安装，并配置 INCLUDE/LIB 路径
- 编译报错：请检查 g++、cmake、SDL2 是否安装齐全

## 扩展说明
- AI 算法可在 ai.h/ai.cpp 中扩展
- 测试用例可放在 tests/ 目录
- 资源文件（如字体、图片）放在 assets/ 目录
- 设计文档可放在 docs/ 目录

---
如有问题请联系开发者或提交 issue。 