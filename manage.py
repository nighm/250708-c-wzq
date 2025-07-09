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
    """检查 g++、cmake、SDL3 是否可用"""
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
    # 检查 SDL2
    found = False
    for path in os.environ.get("INCLUDE", "").split(os.pathsep):
        if os.path.exists(os.path.join(path, SDL2_INCLUDE_HINT)):
            found = True
            break
    if found:
        print("  ✔ SDL2 头文件检测通过")
    else:
        print("  ✘ 未检测到 SDL2 头文件（请确保 SDL2 开发包已安装并配置 INCLUDE 路径）")
        # 仅警告，不强制退出
    # 检查 SDL3
    found = False
    for path in os.environ.get("INCLUDE", "").split(os.pathsep):
        if os.path.exists(os.path.join(path, SDL3_INCLUDE_HINT)):
            found = True
            break
    if found:
        print("  ✔ SDL3 头文件检测通过")
    else:
        print("  ✘ 未检测到 SDL3 头文件（请确保 SDL3 开发包已安装并配置 INCLUDE 路径）")
        # 仅警告，不强制退出
    return True

def build():
    """一键编译项目"""
    print("[编译项目]")
    if not os.path.exists(BUILD_DIR):
        os.mkdir(BUILD_DIR)
    os.chdir(BUILD_DIR)
    # 生成 Makefile
    ret = subprocess.call(["cmake", "-G", CMAKE_GENERATOR, ".."])
    if ret != 0:
        print("  ✘ cmake 配置失败")
        sys.exit(1)
    # 编译
    ret = subprocess.call(["cmake", "--build", "."])
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
    """运行 tests/ 下的所有测试用例（需后续补充测试代码）"""
    print("[运行单元测试]")
    # 假设测试可执行文件为 build/tests.exe 或 build/tests
    test_exec = os.path.join(BUILD_DIR, "tests" + (".exe" if os.name == "nt" else ""))
    if not os.path.exists(test_exec):
        print("  ✘ 未找到测试可执行文件，请先编译测试！")
        return
    ret = subprocess.call([test_exec])
    if ret != 0:
        print("  ✘ 测试未全部通过")
    else:
        print("  ✔ 所有测试通过")

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