#!/usr/bin/env python3
"""
CNC监控系统启动脚本
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import fastapi
        import uvicorn
        print("✓ Python依赖检查通过")
        return True
    except ImportError as e:
        print(f"✗ 缺少Python依赖: {e}")
        return False

def install_dependencies():
    """安装Python依赖"""
    print("正在安装Python依赖...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], check=True)
        print("✓ Python依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Python依赖安装失败: {e}")
        return False

def start_backend():
    """启动后端服务"""
    print("正在启动后端服务...")
    try:
        # 切换到backend目录
        os.chdir("backend")
        
        # 启动FastAPI服务
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
        
        print("✓ 后端服务启动成功 (http://localhost:8000)")
        return process
    except Exception as e:
        print(f"✗ 后端服务启动失败: {e}")
        return None

def start_frontend():
    """启动前端服务"""
    print("正在启动前端服务...")
    try:
        # 切换到项目根目录
        os.chdir("..")
        
        # 检查是否安装了npm依赖
        if not Path("node_modules").exists():
            print("正在安装npm依赖...")
            subprocess.run(["npm", "install"], check=True)
        
        # 启动Vue开发服务器
        process = subprocess.Popen(["npm", "run", "dev"])
        
        print("✓ 前端服务启动成功 (http://localhost:5173)")
        return process
    except Exception as e:
        print(f"✗ 前端服务启动失败: {e}")
        return None

def main():
    """主函数"""
    print("=" * 50)
    print("CNC监控系统启动器")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 安装依赖
    if not install_dependencies():
        return
    
    # 启动后端
    backend_process = start_backend()
    if not backend_process:
        return
    
    # 等待后端启动
    time.sleep(3)
    
    # 启动前端
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        return
    
    print("\n" + "=" * 50)
    print("系统启动完成！")
    print("前端地址: http://localhost:5173")
    print("后端API: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    print("按 Ctrl+C 停止所有服务")
    print("=" * 50)
    
    try:
        # 等待用户中断
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在停止服务...")
        
        # 停止前端
        if frontend_process:
            frontend_process.terminate()
            print("✓ 前端服务已停止")
        
        # 停止后端
        if backend_process:
            backend_process.terminate()
            print("✓ 后端服务已停止")
        
        print("所有服务已停止")

if __name__ == "__main__":
    main() 