#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
manage.py
中型C++ SDL2五子棋项目的辅助管理脚本。
支持一键编译、运行、清理、测试、环境检查等功能。
"""
import os
import sys
import subprocess
import shutil

# 配置区
PROJECT_NAME = "gomoku-sdl2"
BUILD_DIR = "build"
EXECUTABLE = os.path.join(BUILD_DIR, PROJECT_NAME + (".exe" if os.name == "nt" else ""))
CMAKE_GENERATOR = "MinGW Makefiles" if os.name == "nt" else "Unix Makefiles"

# SDL2 检查命令（可根据实际情况调整）
SDL2_INCLUDE_HINT = "SDL.h"
SDL2_LIB_HINT = "SDL2"

# SDL3 检查命令（已更新为SDL3）
SDL3_INCLUDE_HINT = "SDL.h"
SDL3_LIB_HINT = "SDL3"


def check_env():
    """检查 g++、cmake、SDL3、SDL3_ttf、googletest 是否可用"""
    print("[环境检测]")
    # 检查 g++
    try:
        subprocess.check_call(["g++", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("  ✔ g++ 可用")
    except Exception:
        print("  ✘ g++ 不可用，请检查 MinGW-w64 是否安装并配置环境变量！")
        return False
    # 检查 cmake
    try:
        subprocess.check_call(["cmake", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("  ✔ cmake 可用")
    except Exception:
        print("  ✘ cmake 不可用，请安装 cmake 并配置环境变量！")
        return False
    # 检查 third_party/SDL3
    sdl3_h = os.path.join("third_party", "SDL3", "include", "SDL3", "SDL.h")
    sdl3_lib = os.path.join("third_party", "SDL3", "lib", "libSDL3.dll.a")
    sdl3ttf_h = os.path.join("third_party", "SDL3", "include", "SDL3", "SDL_ttf.h")
    sdl3ttf_lib = os.path.join("third_party", "SDL3", "lib", "libSDL3_ttf.dll.a")
    if all(os.path.exists(p) for p in [sdl3_h, sdl3_lib, sdl3ttf_h, sdl3ttf_lib]):
        print("  ✔ SDL3/SDL3_ttf 本地依赖检测通过")
    else:
        print("  ✘ 未检测到 SDL3/SDL3_ttf 本地依赖（third_party/SDL3），请补齐依赖！")
    # 检查 googletest
    gtest_dir = os.path.join("third_party", "googletest-1.14.0")
    if os.path.exists(gtest_dir):
        print("  ✔ googletest 本地依赖检测通过")
    else:
        print("  ✘ 未检测到 googletest 本地依赖（third_party/googletest-1.14.0），请补齐依赖！")
    return True

def build():
    """一键编译项目，支持并行编译和 Release/Debug 切换"""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--jobs', type=int, default=None, help='并行编译线程数')
    parser.add_argument('--release', action='store_true', help='Release 模式编译')
    parser.add_argument('--debug', action='store_true', help='Debug 模式编译（默认）')
    args, unknown = parser.parse_known_args(sys.argv[2:])
    jobs = args.jobs or os.cpu_count() or 2
    build_type = 'Release' if args.release else 'Debug'
    print(f"[编译项目] (并行线程数: {jobs}, 构建类型: {build_type})")
    if not os.path.exists(BUILD_DIR):
        os.mkdir(BUILD_DIR)
    os.chdir(BUILD_DIR)
    # 生成 Makefile
    ret = subprocess.call(["cmake", "-G", CMAKE_GENERATOR, f"-DCMAKE_BUILD_TYPE={build_type}", ".."])
    if ret != 0:
        print("  ✘ cmake 配置失败")
        sys.exit(1)
    # 编译
    ret = subprocess.call(["cmake", "--build", ".", "--", f"-j{jobs}"])
    if ret != 0:
        print("  ✘ 编译失败")
        sys.exit(1)
    print("  ✔ 编译成功")
    os.chdir("..")

def run():
    """运行可执行文件"""
    print("[运行程序]")
    if not os.path.exists(EXECUTABLE):
        print("  ✘ 未找到可执行文件，请先编译！")
        return
    ret = subprocess.call([EXECUTABLE])
    if ret != 0:
        print("  ✘ 程序运行异常")
    else:
        print("  ✔ 程序运行结束")

def clean():
    """清理构建产物"""
    print("[清理构建产物]")
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
        print("  ✔ 已删除 build/ 目录")
    else:
        print("  build/ 目录不存在，无需清理")

def test():
    """运行 build/ 下所有 test_*.exe 测试用例，或指定测试名"""
    print("[运行单元测试]")
    test_names = []
    if len(sys.argv) > 2:
        # 指定测试名
        test_names = [sys.argv[2] + (".exe" if os.name == "nt" and not sys.argv[2].endswith(".exe") else "")]
    else:
        # 自动查找所有 test_*.exe 或 test_*（非.o文件）
        for f in os.listdir(BUILD_DIR):
            if f.startswith("test_") and (f.endswith(".exe") or (os.name != "nt" and not f.endswith(".o"))):
                test_names.append(f)
    if not test_names:
        print("  ✘ 未找到任何测试可执行文件，请先编译测试！")
        return
    all_passed = True
    for name in test_names:
        test_exec = os.path.join(BUILD_DIR, name)
        print(f"  → 运行 {test_exec}")
        ret = subprocess.call([test_exec])
        if ret != 0:
            print(f"  ✘ 测试 {name} 未全部通过")
            all_passed = False
        else:
            print(f"  ✔ 测试 {name} 通过")
    if all_passed:
        print("  ✔ 所有测试通过")
    else:
        print("  ✘ 存在未通过的测试")

def help():
    print("""
用法: python manage.py [命令]

可用命令：
  check     环境检测
  build     编译项目
  run       运行程序
  clean     清理构建产物
  test      运行单元测试
  help      显示本帮助
""")

def main():
    if len(sys.argv) < 2:
        help()
        return
    cmd = sys.argv[1]
    if cmd == "check":
        check_env()
    elif cmd == "build":
        if check_env():
            build()
    elif cmd == "run":
        run()
    elif cmd == "clean":
        clean()
    elif cmd == "test":
        test()
    elif cmd == "help":
        help()
    else:
        print(f"未知命令: {cmd}")
        help()

if __name__ == "__main__":
    main()