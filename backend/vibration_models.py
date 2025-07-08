from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class VibrationData(BaseModel):
    device_id: int
    timestamp: datetime
    
    # 加速度数据 (Ax, Ay, Az)
    ax: float = 0.0
    ay: float = 0.0
    az: float = 0.0
    
    # 陀螺仪数据 (Gx, Gy, Gz)
    gx: float = 0.0
    gy: float = 0.0
    gz: float = 0.0
    
    # 振动速度 (vx, vy, vz)
    vx: float = 0.0
    vy: float = 0.0
    vz: float = 0.0
    
    # 振动角度 (ax, ay, az) - 注意这里与加速度重名，实际使用时需要区分
    angle_x: float = 0.0
    angle_y: float = 0.0
    angle_z: float = 0.0
    
    # 温度 (t)
    temperature: float = 0.0
    
    # 振动位移 (sx, sy, sz)
    sx: float = 0.0
    sy: float = 0.0
    sz: float = 0.0
    
    # 振动频率 (fx, fy, fz)
    fx: float = 0.0
    fy: float = 0.0
    fz: float = 0.0

class VibrationDataResponse(BaseModel):
    success: bool
    data: list[VibrationData]
    message: str = ""
    total_count: int = 0

class RealTimeData(BaseModel):
    """实时数据流结构"""
    device_id: int
    data: Dict[str, Any]
    timestamp: datetime 