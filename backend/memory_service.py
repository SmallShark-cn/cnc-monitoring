import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from vibration_models import VibrationData
import logging
import threading
import time
import random

logger = logging.getLogger(__name__)

class MemoryService:
    def __init__(self):
        """初始化内存存储服务"""
        self.data_store = {}
        self.device_status = {}
        self.lock = threading.Lock()
        
    def store_vibration_data(self, device_id: int, data: Dict[str, Any]) -> bool:
        """存储震动传感器数据"""
        try:
            with self.lock:
                # 创建时间戳
                timestamp = datetime.now()
                
                # 构建数据键
                data_key = f"vibration:device:{device_id}:{timestamp.strftime('%Y%m%d%H%M%S')}"
                
                # 存储原始数据
                data_dict = {
                    'device_id': device_id,
                    'timestamp': timestamp.isoformat(),
                    'ax': float(data.get('52', 0)),
                    'ay': float(data.get('53', 0)),
                    'az': float(data.get('54', 0)),
                    'gx': float(data.get('55', 0)),
                    'gy': float(data.get('56', 0)),
                    'gz': float(data.get('57', 0)),
                    'vx': float(data.get('58', 0)),
                    'vy': float(data.get('59', 0)),
                    'vz': float(data.get('60', 0)),
                    'angle_x': float(data.get('61', 0)),
                    'angle_y': float(data.get('62', 0)),
                    'angle_z': float(data.get('63', 0)),
                    'temperature': float(data.get('64', 0)),
                    'sx': float(data.get('65', 0)),
                    'sy': float(data.get('66', 0)),
                    'sz': float(data.get('67', 0)),
                    'fx': float(data.get('68', 0)),
                    'fy': float(data.get('69', 0)),
                    'fz': float(data.get('70', 0))
                }
                
                # 存储数据
                self.data_store[data_key] = data_dict
                
                # 添加到设备的最新数据列表
                latest_key = f"vibration:latest:device:{device_id}"
                if latest_key not in self.data_store:
                    self.data_store[latest_key] = []
                
                self.data_store[latest_key].insert(0, data_key)
                # 只保留最近100条记录
                self.data_store[latest_key] = self.data_store[latest_key][:100]
                
                # 更新设备状态
                status_key = f"vibration:status:device:{device_id}"
                status_data = {
                    'last_update': timestamp.isoformat(),
                    'is_online': True,
                    'data_count': len(self.data_store[latest_key])
                }
                self.device_status[status_key] = status_data
                
                logger.info(f"数据存储成功: {data_key}")
                return True
                
        except Exception as e:
            logger.error(f"存储数据失败: {e}")
            return False
    
    def get_latest_data(self, device_id: int, limit: int = 50) -> List[VibrationData]:
        try:
            with self.lock:
                latest_key = f"vibration:latest:device:{device_id}"
                if latest_key not in self.data_store:
                    return []
                
                data_keys = self.data_store[latest_key][:limit]
                
                vibration_data_list = []
                for key in data_keys:
                    if key in self.data_store:
                        data_dict = self.data_store[key]
                        vibration_data = VibrationData(**data_dict)
                        vibration_data_list.append(vibration_data)
                
                # 按时间戳排序
                vibration_data_list.sort(key=lambda x: x.timestamp, reverse=True)
                return vibration_data_list
                
        except Exception as e:
            logger.error(f"获取数据失败: {e}")
            return []
    
    def get_device_status(self, device_id: int) -> Optional[Dict[str, Any]]:
        try:
            with self.lock:
                status_key = f"vibration:status:device:{device_id}"
                return self.device_status.get(status_key)
                
        except Exception as e:
            logger.error(f"获取设备状态失败: {e}")
            return None
    
    def get_statistics(self, device_id: int, hours: int = 24) -> Dict[str, Any]:
        try:
            with self.lock:
                # 获取指定时间范围内的数据
                end_time = datetime.now()
                start_time = end_time - timedelta(hours=hours)
                
                latest_key = f"vibration:latest:device:{device_id}"
                if latest_key not in self.data_store:
                    return {}
                
                data_list = []
                for key in self.data_store[latest_key]:
                    if key in self.data_store:
                        data_dict = self.data_store[key]
                        data_timestamp = datetime.fromisoformat(data_dict['timestamp'])
                        if start_time <= data_timestamp <= end_time:
                            data_list.append(data_dict)
                
                if not data_list:
                    return {}
                
                # 计算统计数据
                stats = {
                    'total_records': len(data_list),
                    'avg_temperature': sum(d['temperature'] for d in data_list) / len(data_list),
                    'max_vibration': max(max(d['vx'], d['vy'], d['vz']) for d in data_list),
                    'avg_vibration': sum((d['vx'] + d['vy'] + d['vz']) / 3 for d in data_list) / len(data_list),
                    'time_range': {
                        'start': start_time.isoformat(),
                        'end': end_time.isoformat()
                    }
                }
                
                return stats
                
        except Exception as e:
            logger.error(f"获取统计数据失败: {e}")
            return {}
    
    def cleanup_old_data(self, days: int = 7):
        """清理旧数据"""
        try:
            with self.lock:
                cutoff_time = datetime.now() - timedelta(days=days)
                keys_to_delete = []
                
                for key in self.data_store:
                    if key.startswith("vibration:device:"):
                        try:
                            data_dict = self.data_store[key]
                            data_timestamp = datetime.fromisoformat(data_dict['timestamp'])
                            if data_timestamp < cutoff_time:
                                keys_to_delete.append(key)
                        except:
                            continue
                
                for key in keys_to_delete:
                    del self.data_store[key]
                    logger.info(f"删除旧数据: {key}")
                    
        except Exception as e:
            logger.error(f"清理旧数据失败: {e}")
    
    def generate_test_data(self, device_id: int = 80):
        """生成测试数据"""
        test_data = {
            '52': random.uniform(-2.0, 2.0),  # ax
            '53': random.uniform(-2.0, 2.0),  # ay
            '54': random.uniform(-2.0, 2.0),  # az
            '55': random.uniform(-180.0, 180.0),  # gx
            '56': random.uniform(-180.0, 180.0),  # gy
            '57': random.uniform(-180.0, 180.0),  # gz
            '58': random.uniform(0.0, 10.0),  # vx
            '59': random.uniform(0.0, 10.0),  # vy
            '60': random.uniform(0.0, 10.0),  # vz
            '61': random.uniform(-90.0, 90.0),  # angle_x
            '62': random.uniform(-90.0, 90.0),  # angle_y
            '63': random.uniform(-90.0, 90.0),  # angle_z
            '64': random.uniform(20.0, 30.0),  # temperature
            '65': random.uniform(0.0, 5.0),  # sx
            '66': random.uniform(0.0, 5.0),  # sy
            '67': random.uniform(0.0, 5.0),  # sz
            '68': random.uniform(0.0, 100.0),  # fx
            '69': random.uniform(0.0, 100.0),  # fy
            '70': random.uniform(0.0, 100.0)   # fz
        }
        
        success = self.store_vibration_data(device_id, test_data)
        if success:
            logger.info(f"测试数据生成成功: 设备 {device_id}")
        else:
            logger.error(f"测试数据生成失败: 设备 {device_id}")
        
        return success

# 创建全局内存服务实例
memory_service = MemoryService() 