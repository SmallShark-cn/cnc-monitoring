from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import threading
import time
from vibration_api import router as vibration_router
from serial_service import serial_service
from memory_service import memory_service

app = FastAPI(title="CNC监控系统", description="震动传感器数据监控系统")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册震动传感器API路由
app.include_router(vibration_router)

@app.get("/api/performance")
async def get_performance():
    return {"data": [80, 75, 85, 78, 90, 88, 92, 95, 89, 93, 96, 94]}

@app.get("/api/stats")
async def get_stats():
    return {"total": 785200, "efficiency": 58000, "quality": 92000}

@app.post("/api/serial/start")
async def start_serial_monitoring(background_tasks: BackgroundTasks, device_id: int = 80):
    """启动串口监控"""
    try:
        success = serial_service.start_monitoring(device_id)
        if success:
            return {"success": True, "message": f"串口监控已启动，设备ID: {device_id}"}
        else:
            return {"success": False, "message": "串口监控启动失败"}
    except Exception as e:
        return {"success": False, "message": f"启动失败: {str(e)}"}

@app.post("/api/serial/stop")
async def stop_serial_monitoring():
    """停止串口监控"""
    try:
        serial_service.stop_monitoring()
        return {"success": True, "message": "串口监控已停止"}
    except Exception as e:
        return {"success": False, "message": f"停止失败: {str(e)}"}

@app.post("/api/test/send-data")
async def send_test_data(device_id: int = 80):
    """发送测试数据"""
    try:
        success = memory_service.generate_test_data(device_id)
        if success:
            return {"success": True, "message": f"测试数据发送成功，设备ID: {device_id}"}
        else:
            return {"success": False, "message": "测试数据发送失败"}
    except Exception as e:
        return {"success": False, "message": f"发送失败: {str(e)}"}

@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化"""
    print("CNC监控系统启动中...")
    # 可以在这里启动串口监控
    # serial_service.start_monitoring(80)

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的清理"""
    print("CNC监控系统关闭中...")
    serial_service.stop_monitoring()