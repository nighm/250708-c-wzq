import os
import re
import shutil
import subprocess
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent
# 需要处理的文件类型
SOURCE_EXTENSIONS = ('.h', '.cpp', '.c')
# SDL2到SDL3的API替换规则
API_REPLACEMENTS = {
    # 初始化函数
    r'SDL_Init\((SDL_INIT_VIDEO.*?)\)': r'SDL_InitVideo()',
    r'SDL_Init\((SDL_INIT_AUDIO.*?)\)': r'SDL_InitAudio()',
    # 窗口创建
    r'SDL_CreateWindow\((.*?), (.*?), (.*?), (.*?), (.*?), (.*?)\)': 
        r'SDL_CreateWindow(\1, \4, \5, \6)',
    # 事件类型
    r'SDL_QUIT': r'SDL_EVENT_QUIT',
    r'SDL_KEYDOWN': r'SDL_EVENT_KEY_DOWN',
    r'SDL_MOUSEBUTTONDOWN': r'SDL_EVENT_MOUSE_BUTTON_DOWN',
    # 渲染器创建
    r'SDL_CreateRenderer\((.*?), (.*?), (.*?)\)': r'SDL_CreateRenderer(\1, \3)'
}

def modify_cmakelists():
    "修改CMakeLists.txt文件"
    cmake_path = PROJECT_ROOT / 'CMakeLists.txt'
    if not cmake_path.exists():
        print(f"❌ 未找到CMakeLists.txt: {cmake_path}")
        return False

    # 读取文件内容
    with open(cmake_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换SDL2为SDL3
    new_content = content.replace('SDL2', 'SDL3')
    # 修复可能的变量名变化
    new_content = re.sub(r'SDL3_INCLUDE_DIRS', 'SDL3_INCLUDE_DIR', new_content)
    new_content = re.sub(r'SDL3_LIBRARIES', 'SDL3_LIBRARY', new_content)

    # 写入修改
    with open(cmake_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"✅ 修改完成: {cmake_path}")
    return True

def process_source_files():
    "处理所有源代码文件"
    # 创建备份目录
    backup_dir = PROJECT_ROOT / 'sdl2_backup'
    backup_dir.mkdir(exist_ok=True)

    # 遍历所有源代码文件
    for root, _, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(SOURCE_EXTENSIONS):
                file_path = Path(root) / file
                # 跳过备份目录
                if backup_dir in file_path.parents:
                    continue

                # 备份文件
                rel_path = file_path.relative_to(PROJECT_ROOT)
                backup_path = backup_dir / rel_path
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, backup_path)

                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # 替换头文件
                new_content = content.replace('#include <SDL2/SDL.h>', '#include <SDL3/SDL.h>')

                # 应用API替换规则
                for pattern, replacement in API_REPLACEMENTS.items():
                    new_content = re.sub(pattern, replacement, new_content)

                # 写入修改
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"🔄 更新文件: {file_path}")

    print(f"📋 所有文件已处理，原始文件备份至: {backup_dir}")
    return True

def clean_and_rebuild():
    "清理并重新构建项目"
    build_dir = PROJECT_ROOT / 'build'
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(exist_ok=True)

    # 运行CMake和Make
    try:
        # Windows使用MinGW Makefiles生成器
        subprocess.run(
            ['cmake', '..', '-G', 'MinGW Makefiles'],
            cwd=build_dir,
            check=True,
            capture_output=True,
            text=True
        )
        subprocess.run(
            ['mingw32-make'],
            cwd=build_dir,
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ 项目构建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e.stderr}")
        return False

def main():
    print("===== SDL2 to SDL3 迁移工具 ======")
    print(f"项目目录: {PROJECT_ROOT}")

    # 确认操作
    confirm = input("此操作将修改项目文件，是否继续? (y/N): ")
    if confirm.lower() != 'y':
        print("操作已取消")
        return

    # 执行迁移步骤
    success = True
    success &= modify_cmakelists()
    success &= process_source_files()
    success &= clean_and_rebuild()

    if success:
        print("\n🎉 迁移完成! 请测试应用是否正常运行")
        print("注意: 部分API可能需要手动调整，请查看编译错误信息")
    else:
        print("\n⚠️ 迁移过程中出现错误，请检查日志")

if __name__ == '__main__':
    main()