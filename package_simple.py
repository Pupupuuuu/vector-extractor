#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图像特征向量提取工具打包脚本（简化版）
该脚本将直接安装必要的依赖并打包应用为可执行文件，无需用户交互
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
    """运行命令并打印输出"""
    print(f"执行命令: {command}")
    process = subprocess.Popen(
        command, 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    # 实时打印输出
    for line in process.stdout:
        print(line.strip())
    
    process.wait()
    return process.returncode == 0

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

def build_executable():
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

if __name__ == "__main__":
    print("图像特征向量提取工具打包程序（简化版）")
    print("该程序将直接安装依赖并打包应用为可执行文件")
    
    # 安装依赖
    if not install_dependencies():
        print("依赖安装失败，停止打包流程")
        sys.exit(1)
    
    # 打包可执行文件
    if not build_executable():
        print("打包失败")
        sys.exit(1)
    
    print("\n打包过程完成!")
    print("可执行文件位于dist目录中")
    
    # 在Windows上，打开dist文件夹
    if platform.system() == "Windows":
        os.startfile("dist")
    
    input("按回车键退出...") 