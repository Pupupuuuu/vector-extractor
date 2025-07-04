#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图像特征向量提取工具打包脚本
该脚本将安装必要的依赖并打包应用为可执行文件
"""

import os
import sys
import subprocess
import platform

def print_step(message):
    """打印步骤信息"""
    print("\n" + "=" * 60)
    print(f"  {message}")
    print("=" * 60)

def run_command(command):
    """运行命令并返回结果"""
    print(f"执行命令: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"命令执行失败: {result.stderr}")
        return False
    return True

def install_dependencies():
    """安装必要的依赖"""
    print_step("安装依赖")
    
    # 安装requirements.txt中的依赖
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt"):
        print("安装项目依赖失败！")
        return False
    
    # 安装PyInstaller
    if not run_command(f"{sys.executable} -m pip install pyinstaller"):
        print("安装PyInstaller失败！")
        return False
    
    print("依赖安装完成!")
    return True

def build_executable(debug_mode=False):
    """打包应用为可执行文件"""
    print_step("打包可执行文件")
    script = "vector_extractor.py"
    output_name = "vector_extractor"
    
    # 检查目标文件是否存在
    if not os.path.exists(script):
        print(f"错误: 找不到源文件 {script}")
        return False
    
    # 构建PyInstaller命令
    cmd = f"{sys.executable} -m PyInstaller --onefile --name {output_name} {script}"
    
    # 添加必要的隐藏导入
    cmd += " --hidden-import torch --hidden-import torchvision --hidden-import PIL --hidden-import PIL.Image"
    
    # 如果是调试模式，保留终端窗口
    if not debug_mode:
        if platform.system() == "Windows":
            cmd += " --windowed"  # Windows上使用--windowed选项，但命令行程序可能需要保留终端
    
    # 执行打包命令
    if not run_command(cmd):
        print("打包失败!")
        return False
    
    # 检查dist文件夹是否创建
    if not os.path.exists("dist"):
        print("错误: 打包完成但没有生成dist文件夹")
        return False
    
    # 检查可执行文件是否生成
    exe_ext = ".exe" if platform.system() == "Windows" else ""
    exe_path = os.path.join("dist", f"{output_name}{exe_ext}")
    
    if not os.path.exists(exe_path):
        print(f"错误: 可执行文件未生成: {exe_path}")
        return False
    
    print(f"打包成功! 可执行文件位于: {exe_path}")
    return True

def main():
    """主函数"""
    print("图像特征向量提取工具打包程序")
    print("该程序将安装依赖并打包应用为可执行文件")
    
    # 询问用户是否需要安装依赖
    install_deps = input("是否需要安装依赖? (y/n) [默认: y]: ").strip().lower()
    if install_deps != "n":
        if not install_dependencies():
            print("依赖安装失败，停止打包流程")
            return
    
    # 询问用户是否保留控制台窗口（调试模式）
    debug_mode = input("\n是否保留控制台窗口(调试模式)? (y/n) [默认: n]: ").strip().lower()
    debug_mode = debug_mode.startswith("y")
    
    # 打包可执行文件
    if not build_executable(debug_mode):
        print("打包失败")
        return
    
    print("\n打包过程完成!")
    
    # 询问用户是否立即打开dist文件夹
    if platform.system() == "Windows":
        open_folder = input("\n是否打开dist文件夹? (y/n) [默认: y]: ").strip().lower()
        if open_folder != "n":
            os.startfile("dist")
    
    input("按回车键继续...")

if __name__ == "__main__":
    main()
