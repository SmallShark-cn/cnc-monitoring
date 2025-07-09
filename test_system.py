#!/usr/bin/env python3
"""
CNC监控系统测试脚本
测试Redis连接、后端API和前端服务
"""

import requests
import json
import time
import subprocess
import sys
from pathlib import Path

class SystemTester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:5173"
        
    def test_redis_connection(self):
        """测试Redis连接"""
        print("🔴 测试Redis连接...")
        try:
            result = subprocess.run(['redis-cli', 'ping'], capture_output=True, text=True)
            if result.returncode == 0 and 'PONG' in result.stdout:
                print("✅ Redis连接正常")
                return True
            else:
                print("❌ Redis连接失败")
                return False
        except FileNotFoundError:
            print("❌ Redis未安装或未启动")
            return False
    
    def test_backend_api(self):
        """测试后端API"""
        print("🔵 测试后端API...")
        try:
            # 测试健康检查
            response = requests.get(f"{self.base_url}/docs", timeout=5)
            if response.status_code == 200:
                print("✅ 后端API服务正常")
                return True
            else:
                print(f"❌ 后端API响应异常: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ 无法连接到后端API")
            return False
        except Exception as e:
            print(f"❌ 后端API测试失败: {e}")
            return False
    
    def test_api_endpoints(self):
        """测试API端点"""
        print("🔧 测试API端点...")
        endpoints = [
            "/api/performance",
            "/api/stats",
            "/api/vibration/rms-history",
            "/api/acoustic/history",
            "/api/tool-wear/history"
        ]
        
        success_count = 0
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    print(f"✅ {endpoint} - 正常")
                    success_count += 1
                else:
                    print(f"❌ {endpoint} - 异常 ({response.status_code})")
            except Exception as e:
                print(f"❌ {endpoint} - 失败: {e}")
        
        print(f"📊 API端点测试结果: {success_count}/{len(endpoints)} 成功")
        return success_count == len(endpoints)
    
    def test_frontend(self):
        """测试前端服务"""
        print("🟢 测试前端服务...")
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                print("✅ 前端服务正常")
                return True
            else:
                print(f"❌ 前端服务响应异常: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ 无法连接到前端服务")
            return False
        except Exception as e:
            print(f"❌ 前端服务测试失败: {e}")
            return False
    
    def test_data_generation(self):
        """测试数据生成"""
        print("📊 测试数据生成...")
        try:
            # 等待一段时间让数据生成
            time.sleep(3)
            
            # 检查是否有数据
            response = requests.get(f"{self.base_url}/api/vibration/rms-history", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'history' in data and len(data['history']) > 0:
                    print(f"✅ 数据生成正常，当前有 {len(data['history'])} 条记录")
                    return True
                else:
                    print("❌ 没有生成数据")
                    return False
            else:
                print("❌ 无法获取数据")
                return False
        except Exception as e:
            print(f"❌ 数据生成测试失败: {e}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🧪 开始系统测试...")
        print("=" * 50)
        
        tests = [
            ("Redis连接", self.test_redis_connection),
            ("后端API", self.test_backend_api),
            ("API端点", self.test_api_endpoints),
            ("前端服务", self.test_frontend),
            ("数据生成", self.test_data_generation)
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n📋 测试: {test_name}")
            result = test_func()
            results.append((test_name, result))
        
        print("\n" + "=" * 50)
        print("📊 测试结果汇总:")
        
        passed = 0
        for test_name, result in results:
            status = "✅ 通过" if result else "❌ 失败"
            print(f"  {test_name}: {status}")
            if result:
                passed += 1
        
        print(f"\n🎯 总体结果: {passed}/{len(results)} 项测试通过")
        
        if passed == len(results):
            print("🎉 所有测试通过！系统运行正常。")
            return True
        else:
            print("⚠️  部分测试失败，请检查系统配置。")
            return False

def main():
    tester = SystemTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 系统已准备就绪！")
        print("📊 前端地址: http://localhost:5173")
        print("🔧 后端API: http://localhost:8000")
        print("📖 API文档: http://localhost:8000/docs")
    else:
        print("\n🔧 请检查系统配置并重新启动。")
        sys.exit(1)

if __name__ == "__main__":
    main() 