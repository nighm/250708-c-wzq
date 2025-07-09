# gomoku-sdl3

基于 SDL3 的中型 C++ 五子棋项目，支持一键自动化构建、测试与运行，依赖全部本地化，便于跨平台移植和复现。

## 项目简介
- 采用 C++17 标准，SDL3 实现窗口化图形界面
- 支持人机对战（AI）、悔棋、重新开始、胜负判断等基本功能
- 结构清晰，便于维护和扩展
- 单元测试体系完善，集成 GoogleTest
- 所有依赖均优先本地 third_party 目录自动查找，无需全局安装 SDL3/SDL3_ttf

## 目录结构
```
├── CMakeLists.txt         # CMake 构建脚本
├── README.md              # 项目说明
├── manage.py              # 一键管理脚本
├── include/               # 头文件
├── src/                   # 源文件
├── assets/                # 资源文件（图片/字体等）
├── tests/                 # 单元测试
├── third_party/           # 本地依赖（SDL3、SDL3_ttf、googletest等）
└── docs/                  # 设计文档
```

## 依赖环境
- g++ (推荐 MinGW-w64，需加入 PATH)
- CMake 3.10+（需加入 PATH）
- Python 3.x（需加入 PATH，仅用于 manage.py 辅助脚本）
- SDL3/SDL3_ttf（已包含于 third_party/SDL3，无需额外下载）
- GoogleTest（已包含于 third_party/googletest-1.14.0，无需额外下载）

### Windows 环境快速配置
1. 安装 MinGW-w64 并将 bin 目录加入系统 PATH
2. 安装 CMake 并将 bin 目录加入系统 PATH
3. 安装 Python 3.x 并将 python.exe 加入系统 PATH

## 编译与运行
### 一键编译/运行（推荐）
```bash
python manage.py build         # 编译所有目标
python manage.py run           # 运行主程序
```

### 支持并行编译（加速构建）
可在 manage.py 中配置并行参数，或手动执行：
```bash
cmake --build build -- -j8      # 8线程并行编译
```

### 手动编译
```bash
mkdir build
cd build
cmake -G "MinGW Makefiles" ..
cmake --build .
./gomoku.exe
```

## 单元测试体系
- 所有测试用例位于 tests/ 目录，基于 GoogleTest
- 一键运行所有测试：
  ```bash
  python manage.py test
  ```
- 可扩展测试用例，自动发现所有 test_*.exe 测试目标

## 编译加速与缓存
- 本项目自动检测并优先启用 ccache 或 sccache 编译缓存（如已安装）。
- 推荐安装 ccache（Linux/macOS/WSL）或 sccache（Windows/Linux），可大幅提升二次编译速度。
- 安装方法：
  - ccache: https://ccache.dev/ （可用包管理器安装）
  - sccache: https://github.com/mozilla/sccache （Windows 推荐，支持 Rust/C++）
- 启用方式：只需将 ccache/sccache 加入 PATH，CMake 会自动检测并启用。
- 效果：首次全量编译正常，后续仅变动文件会极快完成。

## 脚本与自动化
- `manage.py`