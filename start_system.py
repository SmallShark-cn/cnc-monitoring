#!/usr/bin/env python3
"""
CNC监控系统启动脚本
启动Redis、后端API服务和前端开发服务器
"""

import subprocess
import time
import sys
import os
import signal
import threading
from pathlib import Path

class SystemStarter:
    def __init__(self):
        self.processes = []
        self.running = True
        
    def start_redis(self):
        """启动Redis服务"""
        print("🔴 启动Redis服务...")
        try:
            # 检查Redis是否已运行
            result = subprocess.run(['redis-cli', 'ping'], capture_output=True, text=True)
            if result.returncode == 0 and 'PONG' in result.stdout:
                print("✅ Redis服务已在运行")
                return None
            
            # 启动Redis
            redis_process = subprocess.Popen(
                ['redis-server'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(2)  # 等待Redis启动
            
            # 验证Redis是否启动成功
            result = subprocess.run(['redis-cli', 'ping'], capture_output=True, text=True)
            if result.returncode == 0 and 'PONG' in result.stdout:
                print("✅ Redis服务启动成功")
                return redis_process
            else:
                print("❌ Redis服务启动失败")
                return None
        except FileNotFoundError:
            print("❌ Redis未安装，请先安装Redis")
            return None
        except Exception as e:
            print(f"❌ Redis启动错误: {e}")
            return None
    
    def start_backend(self):
        """启动后端API服务"""
        print("🔵 启动后端API服务...")
        try:
            backend_dir = Path(__file__).parent / "backend"
            backend_process = subprocess.Popen(
                [sys.executable, "main.py"],
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(3)  # 等待后端启动
            print("✅ 后端API服务启动成功 (http://localhost:8000)")
            return backend_process
        except Exception as e:
            print(f"❌ 后端启动错误: {e}")
            return None
    
    def start_frontend(self):
        """启动前端开发服务器"""
        print("🟢 启动前端开发服务器...")
        try:
            frontend_process = subprocess.Popen(
                ["npm", "run", "dev"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(5)  # 等待前端启动
            print("✅ 前端开发服务器启动成功 (http://localhost:5173)")
            return frontend_process
        except FileNotFoundError:
            print("❌ npm未安装，请先安装Node.js")
            return None
        except Exception as e:
            print(f"❌ 前端启动错误: {e}")
            return None
    
    def monitor_processes(self):
        """监控进程状态"""
        while self.running:
            for i, process in enumerate(self.processes):
                if process and process.poll() is not None:
                    print(f"⚠️  进程 {i} 已退出，返回码: {process.returncode}")
            time.sleep(5)
    
    def signal_handler(self, signum, frame):
        """信号处理器"""
        print("\n🛑 收到停止信号，正在关闭服务...")
        self.running = False
        self.stop_all()
        sys.exit(0)
    
    def stop_all(self):
        """停止所有服务"""
        print("🛑 正在停止所有服务...")
        for process in self.processes:
            if process:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                except Exception as e:
                    print(f"停止进程时出错: {e}")
        print("✅ 所有服务已停止")
    
    def start(self):
        """启动整个系统"""
        print("🚀 启动CNC监控系统...")
        print("=" * 50)
        
        # 注册信号处理器
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # 启动Redis
        redis_process = self.start_redis()
        if redis_process:
            self.processes.append(redis_process)
        
        # 启动后端
        backend_process = self.start_backend()
        if backend_process:
            self.processes.append(backend_process)
        
        # 启动前端
        frontend_process = self.start_frontend()
        if frontend_process:
            self.processes.append(frontend_process)
        
        print("=" * 50)
        print("🎉 CNC监控系统启动完成！")
        print("📊 前端地址: http://localhost:5173")
        print("🔧 后端API: http://localhost:8000")
        print("📖 API文档: http://localhost:8000/docs")
        print("=" * 50)
        print("按 Ctrl+C 停止所有服务")
        
        # 启动监控线程
        monitor_thread = threading.Thread(target=self.monitor_processes, daemon=True)
        monitor_thread.start()
        
        try:
            # 保持主线程运行
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    starter = SystemStarter()
    starter.start() 