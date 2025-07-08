from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from vibration_models import VibrationData, VibrationDataResponse
from memory_service import memory_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/vibration", tags=["震动传感器"])

@router.get("/data/{device_id}", response_model=VibrationDataResponse)
async def get_vibration_data(
    device_id: int,
    limit: int = Query(default=50, ge=1, le=100, description="返回数据条数限制")
):
    """获取指定设备的震动数据"""
    try:
        data = memory_service.get_latest_data(device_id, limit)
        return VibrationDataResponse(
            success=True,
            data=data,
            total_count=len(data),
            message=f"成功获取设备 {device_id} 的震动数据"
        )
    except Exception as e:
        logger.error(f"获取震动数据失败: {e}")
        raise HTTPException(status_code=500, detail="获取数据失败")

@router.get("/status/{device_id}")
async def get_device_status(device_id: int):
    """获取设备状态"""
    try:
        status = memory_service.get_device_status(device_id)
        if status:
            return {
                "success": True,
                "data": status,
                "message": f"设备 {device_id} 状态正常"
            }
        else:
            return {
                "success": False,
                "data": None,
                "message": f"设备 {device_id} 离线或未找到状态信息"
            }
    except Exception as e:
        logger.error(f"获取设备状态失败: {e}")
        raise HTTPException(status_code=500, detail="获取设备状态失败")

@router.get("/statistics/{device_id}")
async def get_vibration_statistics(
    device_id: int,
    hours: int = Query(default=24, ge=1, le=168, description="统计时间范围（小时）")
):
    """获取震动数据统计信息"""
    try:
        stats = memory_service.get_statistics(device_id, hours)
        if stats:
            return {
                "success": True,
                "data": stats,
                "message": f"成功获取设备 {device_id} 的统计数据"
            }
        else:
            return {
                "success": False,
                "data": {},
                "message": f"设备 {device_id} 在指定时间范围内无数据"
            }
    except Exception as e:
        logger.error(f"获取统计数据失败: {e}")
        raise HTTPException(status_code=500, detail="获取统计数据失败")

@router.get("/devices")
async def get_all_devices():
    """获取所有设备列表"""
    try:
        # 这里可以根据实际需求从Redis中获取所有设备信息
        # 暂时返回示例数据
        devices = [
            {
                "device_id": 80,
                "name": "震动传感器-01",
                "location": "车间A",
                "status": "online"
            },
            {
                "device_id": 81,
                "name": "震动传感器-02", 
                "location": "车间B",
                "status": "offline"
            }
        ]
        
        return {
            "success": True,
            "data": devices,
            "message": "成功获取设备列表"
        }
    except Exception as e:
        logger.error(f"获取设备列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取设备列表失败")

@router.post("/data/{device_id}")
async def store_vibration_data(device_id: int, data: dict):
    """存储震动数据（用于测试或外部数据源）"""
    try:
        success = memory_service.store_vibration_data(device_id, data)
        if success:
            return {
                "success": True,
                "message": f"成功存储设备 {device_id} 的震动数据"
            }
        else:
            raise HTTPException(status_code=500, detail="数据存储失败")
    except Exception as e:
        logger.error(f"存储震动数据失败: {e}")
        raise HTTPException(status_code=500, detail="数据存储失败")

@router.get("/realtime/{device_id}")
async def get_realtime_data(device_id: int):
    """获取实时数据（用于WebSocket或轮询）"""
    try:
        # 获取最新的几条数据作为实时数据
        latest_data = memory_service.get_latest_data(device_id, 1)
        if latest_data:
            return {
                "success": True,
                "data": latest_data[0],
                "message": "获取实时数据成功"
            }
        else:
            return {
                "success": False,
                "data": None,
                "message": "暂无实时数据"
            }
    except Exception as e:
        logger.error(f"获取实时数据失败: {e}")
        raise HTTPException(status_code=500, detail="获取实时数据失败") 