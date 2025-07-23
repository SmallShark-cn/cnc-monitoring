from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
import threading
import time
import json
import redis
import random
import datetime
import asyncio
from vibration_api import router as vibration_router
from serial_service import serial_service
from memory_service import memory_service
import os
from Login import router as login_router
import websockets

REMOTE_WS_BASE = "ws://192.168.1.101:8000"

app = FastAPI(title="CNC监控系统", description="震动传感器数据监控系统")

RWKV_SETTINGS_FILE = '../rwkv_setting.json'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

r = redis.Redis(host='localhost', port=6379, db=0)

# WebSocket连接管理
vibration_clients = set()
acoustic_clients = set()
tool_wear_clients = set()
vibration_time_domain_clients = set()
vibration_frequency_domain_clients = set()
vibration_time_frequency_clients = set()
vibration_statistics_clients = set()
acoustic_time_domain_clients = set()
acoustic_frequency_domain_clients = set()
acoustic_time_frequency_clients = set()
acoustic_statistics_clients = set()


def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def save_to_redis(key, value, max_length=30):
    """保存数据到Redis列表，限制长度"""
    r.lpush(key, json.dumps(value))
    r.ltrim(key, 0, max_length - 1)

def get_from_redis(key):
    """从Redis获取数据"""
    data = r.lrange(key, 0, -1)
    return [json.loads(item) for item in data]

# 注册震动传感器API路由
app.include_router(vibration_router)
app.include_router(login_router)

# 注释掉性能数据接口中的假数据生成
@app.get("/api/performance")
async def get_performance():
    """获取性能数据"""
    performance_data = get_from_redis('performance_history')
    # if not performance_data:
    #     # 生成模拟数据
    #     performance_data = [random.randint(75, 95) for _ in range(12)]
    #     for value in performance_data:
    #         save_to_redis('performance_history', value)
    return {"data": performance_data}

# 注释掉统计数据接口中的假数据生成
@app.get("/api/stats")
async def get_stats():
    """获取统计数据"""
    stats_data = get_from_redis('stats_history')
    # if not stats_data:
    #     # 生成模拟数据
    #     stats_data = {
    #         "total": random.randint(780000, 790000),
    #         "efficiency": random.randint(57000, 59000),
    #         "quality": random.randint(91000, 93000)
    #     }
    #     save_to_redis('stats_history', stats_data)
    # else:
    #     stats_data = stats_data[0]  # 取最新数据
    return stats_data

@app.get("/api/vibration/rms-history")
async def get_rms_history():
    """获取RMS历史数据"""
    rms_data = get_from_redis('rms_history')
    return {"history": [item['rms'] if isinstance(item, dict) else item for item in rms_data]}

@app.get("/api/acoustic/history")
async def get_acoustic_history():
    """获取声学历史数据"""
    acoustic_data = get_from_redis('acoustic_history')
    return {"history": acoustic_data}

@app.get("/api/tool-wear/history")
async def get_tool_wear_history():
    """获取刀具磨损历史数据"""
    tool_wear_data = get_from_redis('tool_wear_history')
    return {"history": tool_wear_data}

# WebSocket端点
# 注释掉所有WebSocket端点中的假数据生成和推送
@app.websocket("/ws/vibration/time-domain")
async def ws_vibration_time_domain(websocket: WebSocket):
    await websocket.accept()
    remote_url = f"{REMOTE_WS_BASE}/ws/vibration/time-domain"
    try:
        async with websockets.connect(remote_url) as remote_ws:
            while True:
                data = await remote_ws.recv()
                await websocket.send_text(data)
    except Exception as e:
        print(f"转发远程WebSocket数据出错: {e}")
    finally:
        await websocket.close()

@app.websocket("/ws/vibration/frequency-domain")
async def ws_vibration_frequency_domain(websocket: WebSocket):
    await websocket.accept()
    remote_url = f"{REMOTE_WS_BASE}/ws/vibration/frequency-domain"
    try:
        async with websockets.connect(remote_url) as remote_ws:
            while True:
                data = await remote_ws.recv()
                await websocket.send_text(data)
    except Exception as e:
        print(f"转发远程WebSocket数据出错: {e}")
    finally:
        await websocket.close()

@app.websocket("/ws/vibration/time-frequency")
async def ws_vibration_time_frequency(websocket: WebSocket):
    await websocket.accept()
    remote_url = f"{REMOTE_WS_BASE}/ws/vibration/time-frequency"
    try:
        async with websockets.connect(remote_url) as remote_ws:
            while True:
                data = await remote_ws.recv()
                await websocket.send_text(data)
    except Exception as e:
        print(f"转发远程WebSocket数据出错: {e}")
    finally:
        await websocket.close()

@app.websocket("/ws/vibration/statistics")
async def ws_vibration_statistics(websocket: WebSocket):
    await websocket.accept()
    remote_url = f"{REMOTE_WS_BASE}/ws/vibration/statistics"
    try:
        async with websockets.connect(remote_url) as remote_ws:
            while True:
                data = await remote_ws.recv()
                await websocket.send_text(data)
    except Exception as e:
        print(f"转发远程WebSocket数据出错: {e}")
    finally:
        await websocket.close()

# 数据监控WebSocket端点 - 声学传感器
@app.websocket("/ws/acoustic/time-domain")
async def ws_acoustic_time_domain(websocket: WebSocket):
    await websocket.accept()
    remote_url = f"{REMOTE_WS_BASE}/ws/acoustic/time-domain"
    try:
        async with websockets.connect(remote_url) as remote_ws:
            while True:
                data = await remote_ws.recv()
                await websocket.send_text(data)
    except Exception as e:
        print(f"转发远程WebSocket数据出错: {e}")
    finally:
        await websocket.close()

@app.websocket("/ws/acoustic/frequency-domain")
async def ws_acoustic_frequency_domain(websocket: WebSocket):
    await websocket.accept()
    remote_url = f"{REMOTE_WS_BASE}/ws/acoustic/frequency-domain"
    try:
        async with websockets.connect(remote_url) as remote_ws:
            while True:
                data = await remote_ws.recv()
                await websocket.send_text(data)
    except Exception as e:
        print(f"转发远程WebSocket数据出错: {e}")
    finally:
        await websocket.close()

@app.websocket("/ws/acoustic/time-frequency")
async def ws_acoustic_time_frequency(websocket: WebSocket):
    await websocket.accept()
    remote_url = f"{REMOTE_WS_BASE}/ws/acoustic/time-frequency"
    try:
        async with websockets.connect(remote_url) as remote_ws:
            while True:
                data = await remote_ws.recv()
                await websocket.send_text(data)
    except Exception as e:
        print(f"转发远程WebSocket数据出错: {e}")
    finally:
        await websocket.close()

@app.websocket("/ws/acoustic/statistics")
async def ws_acoustic_statistics(websocket: WebSocket):
    await websocket.accept()
    remote_url = f"{REMOTE_WS_BASE}/ws/acoustic/statistics"
    try:
        async with websockets.connect(remote_url) as remote_ws:
            while True:
                data = await remote_ws.recv()
                await websocket.send_text(data)
    except Exception as e:
        print(f"转发远程WebSocket数据出错: {e}")
    finally:
        await websocket.close()

@app.websocket("/ws/tool-wear")
async def ws_tool_wear(websocket: WebSocket):
    await websocket.accept()
    remote_url = f"{REMOTE_WS_BASE}/ws/tool-wear"
    try:
        async with websockets.connect(remote_url) as remote_ws:
            while True:
                data = await remote_ws.recv()
                await websocket.send_text(data)
    except Exception as e:
        print(f"转发远程WebSocket数据出错: {e}")
    finally:
        await websocket.close()

# 注释掉测试数据接口
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
    # try:
    #     success = memory_service.generate_test_data(device_id)
    #     if success:
    #         return {"success": True, "message": f"测试数据发送成功，设备ID: {device_id}"}
    #     else:
    #         return {"success": False, "message": "测试数据发送失败"}
    # except Exception as e:
    #     return {"success": False, "message": f"发送失败: {str(e)}"}
    return {"success": False, "message": "已禁用假数据功能"}

# 注释掉后台假数据生成线程
def background_data_generator():
    import time
    while True:
        # 振动统计特征数据
        vibration_statistics = {
            "timestamp": now_iso(),
            "rms": round(random.uniform(0, 1), 3),
            "peak": round(random.uniform(0, 2), 3),
            "kurtosis": round(random.uniform(2, 6), 3),
            "skewness": round(random.uniform(-1, 1), 3),
            "std": round(random.uniform(0, 0.2), 3)
        }
        save_to_redis('vibration_statistics', vibration_statistics)

        # 振动时域数据
        vibration_time_domain = {
            "timestamp": now_iso(),
            "acceleration": {
                "x": round(random.uniform(-2, 2), 3),
                "y": round(random.uniform(-2, 2), 3),
                "z": round(random.uniform(-2, 2), 3)
            },
            "velocity": {
                "x": round(random.uniform(-0.1, 0.1), 3),
                "y": round(random.uniform(-0.1, 0.1), 3),
                "z": round(random.uniform(-0.1, 0.1), 3)
            },
            "displacement": {
                "x": round(random.uniform(-0.01, 0.01), 3),
                "y": round(random.uniform(-0.01, 0.01), 3),
                "z": round(random.uniform(-0.01, 0.01), 3)
            },
            "temperature": round(random.uniform(20, 22), 1)
        }
        save_to_redis('vibration_time_domain', vibration_time_domain)

        # 振动频域数据
        frequencies = [0, 0.5, 500]
        amplitudes = [round(random.uniform(0.001, 0.1), 3) for _ in range(3)]
        psd = [round(amp * amp, 6) for amp in amplitudes]
        vibration_frequency_domain = {
            "frequencies": frequencies,
            "amplitudes": amplitudes,
            "psd": psd,
            "timestamp": now_iso()
        }
        save_to_redis('vibration_frequency_domain', vibration_frequency_domain)

        # 振动时频数据
        time_points = [now_iso()]
        freq_points = [0, 0.5, 500]
        spectrogram = [[round(random.uniform(0.001, 0.1), 3) for _ in range(3)]]
        vibration_time_frequency = {
            "time": time_points,
            "frequencies": freq_points,
            "spectrogram": spectrogram,
            "timestamp": now_iso()
        }
        save_to_redis('vibration_time_frequency', vibration_time_frequency)

        # 声学统计特征数据（新格式）
        acoustic_statistics = {
            "timestamp": now_iso(),
            "rms": round(random.uniform(0, 1), 3),
            "peak": round(random.uniform(0, 2), 3),
            "kurtosis": round(random.uniform(2, 6), 3),
            "skewness": round(random.uniform(-1, 1), 3),
            "std": round(random.uniform(0, 0.2), 3),
            "spl": round(random.uniform(60, 120), 1)
        }
        save_to_redis('acoustic_statistics', acoustic_statistics)

        # 声学时域音频波形（新格式）
        acoustic_time_domain = {
            "data": [{
                "timestamp": now_iso(),
                "amplitude": round(random.uniform(-1, 1), 3)
            }]
        }
        save_to_redis('acoustic_time_domain', acoustic_time_domain)

        # 声学频域谱数据（新格式）
        afrequencies = [0, 21.5, 22050]
        aamplitudes = [round(random.uniform(0.001, 0.2), 3) for _ in range(3)]
        apsd = [round(amp * amp, 6) for amp in aamplitudes]
        acoustic_frequency_domain = {
            "frequencies": afrequencies,
            "amplitudes": aamplitudes,
            "psd": apsd,
            "timestamp": now_iso()
        }
        save_to_redis('acoustic_frequency_domain', acoustic_frequency_domain)

        # 声学时频分析数据（新格式）
        atime_points = [now_iso()]
        afreq_points = [0, 21.5, 10000]
        aspectrogram = [[round(random.uniform(0.001, 0.2), 3) for _ in range(3)]]
        acoustic_time_frequency = {
            "time": atime_points,
            "frequencies": afreq_points,
            "spectrogram": aspectrogram,
            "timestamp": now_iso()
        }
        save_to_redis('acoustic_time_frequency', acoustic_time_frequency)

        # 融合分析：刀具磨损状态
        tool_wear_fusion = {
            "timestamp": now_iso(),
            "wear_state": random.choice(["normal"]),
            "confidence": round(random.uniform(0.7, 1.0), 2),
            "rul": random.randint(800, 1000),
            "contributions": {"vibration": round(random.uniform(0.3, 0.7), 2), "acoustic": round(random.uniform(0.3, 0.7), 2)}
        }
        save_to_redis('fusion_tool_wear', tool_wear_fusion)

        # 融合分析：相关性分析
        correlation_matrix = {
            "correlation_matrix": {
                "vibration_x_rms_acoustic_rms": round(random.uniform(0.5, 1.0), 2),
                "vibration_y_rms_acoustic_spl": round(random.uniform(0.5, 1.0), 2)
            }
        }
        save_to_redis('fusion_correlation', correlation_matrix)

        # 旧有数据
        vibration_data = {
            "timestamp": now_iso(),
            "rms": round(random.uniform(0, 1), 3),
            "peak": round(random.uniform(0, 2), 3),
            "kurtosis": round(random.uniform(2, 6), 3),
            "skewness": round(random.uniform(-1, 1), 3),
            "std": round(random.uniform(0, 0.2), 3)
        }
        save_to_redis('rms_history', vibration_data)

        acoustic_data = {
            "timestamp": now_iso(),
            "rms": round(random.uniform(0, 1), 3),
            "peak": round(random.uniform(0, 2), 3),
            "kurtosis": round(random.uniform(2, 6), 3),
            "skewness": round(random.uniform(-1, 1), 3),
            "std": round(random.uniform(0, 0.2), 3),
            "spl": round(random.uniform(60, 120), 1)
        }
        save_to_redis('acoustic_history', acoustic_data)

        tool_wear_data = {
            "timestamp": now_iso(),
            "wear_state": random.choice(['normal']),
            "confidence": round(random.uniform(0.7, 1.0), 2),
            "rul": random.randint(90, 100),
            "contributions": {
                "vibration": round(random.uniform(0.3, 0.7), 2),
                "acoustic": round(random.uniform(0.3, 0.7), 2)
            }
        }
        save_to_redis('tool_wear_history', tool_wear_data)

        time.sleep(1)

# 新增API：数据监控相关
@app.get("/api/vibration/time-domain")
async def get_vibration_time_domain():
    data = get_from_redis('vibration_time_domain')
    return {"data": data[0] if data else {}}

@app.get("/api/vibration/frequency-domain")
async def get_vibration_frequency_domain():
    data = get_from_redis('vibration_frequency_domain')
    return data[0] if data else {}

@app.get("/api/vibration/time-frequency")
async def get_vibration_time_frequency():
    data = get_from_redis('vibration_time_frequency')
    return data[0] if data else {}

@app.get("/api/vibration/statistics")
async def get_vibration_statistics():
    data = get_from_redis('vibration_statistics')
    return data[0] if data else {}

@app.get("/api/acoustic/time-domain")
async def get_acoustic_time_domain():
    data = get_from_redis('acoustic_time_domain')
    return {"data": data[0] if data else {}}

@app.get("/api/acoustic/frequency-domain")
async def get_acoustic_frequency_domain():
    data = get_from_redis('acoustic_frequency_domain')
    return data[0] if data else {}

@app.get("/api/acoustic/time-frequency")
async def get_acoustic_time_frequency():
    data = get_from_redis('acoustic_time_frequency')
    return data[0] if data else {}

@app.get("/api/acoustic/statistics")
async def get_acoustic_statistics():
    data = get_from_redis('acoustic_statistics')
    return data[0] if data else {}

# 新增API：融合分析相关
@app.get("/api/fusion/tool-wear")
async def get_fusion_tool_wear():
    data = get_from_redis('fusion_tool_wear')
    return data[0] if data else {}

@app.get("/api/fusion/correlation")
async def get_fusion_correlation():
    data = get_from_redis('fusion_correlation')
    return data[0] if data else {}

@app.post('/api/rwkv-settings')
async def save_rwkv_settings(request: Request):
    data = await request.json()
    try:
        with open(RWKV_SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return {"message": "参数保存成功"}
    except Exception as e:
        return {"message": f"保存失败: {e}"}, 500

@app.get('/api/rwkv-settings')
async def get_rwkv_settings():
    if not os.path.exists(RWKV_SETTINGS_FILE):
        # 默认参数
        return {
            "modelSize": "1.5B",
            "tokenShift": 0.5,
            "layers": 2,
            "contextLength": 1024,
            "samplingRate": 51200,
            "alertThreshold": 7.0
        }
    try:
        with open(RWKV_SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {"message": f"读取失败: {e}"}, 500

# 注释掉后台假数据生成线程
@app.on_event("startup")
async def startup_event():
    print("CNC监控系统启动中...")
    # 自动生成RWKV参数文件（如不存在）
    default_rwkv = {
        "modelSize": "1.5B",
        "tokenShift": 0.5,
        "layers": 2,
        "contextLength": 1024,
        "samplingRate": 51200,
        "alertThreshold": 7.0
    }
    if not os.path.exists('rwkv_settings.json'):
        with open('rwkv_settings.json', 'w', encoding='utf-8') as f:
            json.dump(default_rwkv, f, ensure_ascii=False, indent=2)
    # threading.Thread(target=background_data_generator, daemon=True).start()
    # 初始化Redis数据
    # if not r.exists('performance_history'):
    #     performance_data = [random.randint(75, 95) for _ in range(12)]
    #     for value in performance_data:
    #         save_to_redis('performance_history', value)
    # if not r.exists('stats_history'):
    #     stats_data = {
    #         "total": random.randint(780000, 790000),
    #         "efficiency": random.randint(57000, 59000),
    #         "quality": random.randint(91000, 93000)
    #     }
    #     save_to_redis('stats_history', stats_data)

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的清理"""
    print("CNC监控系统关闭中...")
    serial_service.stop_monitoring()
    
    # 清空Redis数据
    try:
        keys_to_clear = [
            'rms_history', 'acoustic_history', 'tool_wear_history',
            'performance_history', 'stats_history'
        ]
        for key in keys_to_clear:
            r.delete(key)
        print("Redis数据已清空")
    except Exception as e:
        print(f"清空Redis数据时出错: {e}")
    
    # 清理WebSocket连接
    for client in vibration_clients:
        try:
            await client.close()
        except:
            pass
    for client in acoustic_clients:
        try:
            await client.close()
        except:
            pass
    for client in tool_wear_clients:
        try:
            await client.close()
        except:
            pass
    for client in vibration_time_domain_clients:
        try:
            await client.close()
        except:
            pass
    for client in vibration_frequency_domain_clients:
        try:
            await client.close()
        except:
            pass
    for client in vibration_time_frequency_clients:
        try:
            await client.close()
        except:
            pass
    for client in vibration_statistics_clients:
        try:
            await client.close()
        except:
            pass
    for client in acoustic_time_domain_clients:
        try:
            await client.close()
        except:
            pass
    for client in acoustic_frequency_domain_clients:
        try:
            await client.close()
        except:
            pass
    for client in acoustic_time_frequency_clients:
        try:
            await client.close()
        except:
            pass
    for client in acoustic_statistics_clients:
        try:
            await client.close()
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)