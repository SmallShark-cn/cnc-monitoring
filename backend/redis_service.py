import redis
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from vibration_models import VibrationData, RealTimeData
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisService:
    def __init__(self, host='localhost', port=6379, db=0):
        """初始化Redis连接"""
        try:
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            self.redis_client.ping()
            logger.info("Redis连接成功")
        except Exception as e:
            logger.error(f"Redis连接失败: {e}")
            self.redis_client = None
    
    def store_vibration_data(self, device_id: int, data: Dict[str, Any]) -> bool:
        """存储震动传感器数据"""
        if not self.redis_client:
            return False
        
        try:
            timestamp = datetime.now()
            
            data_key = f"vibration:device:{device_id}:{timestamp.strftime('%Y%m%d%H%M%S')}"
            
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
            
            self.redis_client.setex(
                data_key,
                86400,
                json.dumps(data_dict)
            )
            
            # 添加到设备的最新数据列表
            latest_key = f"vibration:latest:device:{device_id}"
            self.redis_client.lpush(latest_key, data_key)
            self.redis_client.ltrim(latest_key, 0, 99)
            
            status_key = f"vibration:status:device:{device_id}"
            status_data = {
                'last_update': timestamp.isoformat(),
                'is_online': True,
                'data_count': self.redis_client.llen(latest_key)
            }
            self.redis_client.setex(status_key, 300, json.dumps(status_data))  # 5分钟过期
            
            logger.info(f"数据存储成功: {data_key}")
            return True
            
        except Exception as e:
            logger.error(f"存储数据失败: {e}")
            return False
    
    def get_latest_data(self, device_id: int, limit: int = 50) -> List[VibrationData]:
        """获取最新的震动数据"""
        if not self.redis_client:
            return []
        
        try:
            latest_key = f"vibration:latest:device:{device_id}"
            data_keys = self.redis_client.lrange(latest_key, 0, limit - 1)
            
            vibration_data_list = []
            for key in data_keys:
                data_json = self.redis_client.get(key)
                if data_json:
                    data_dict = json.loads(data_json)
                    vibration_data = VibrationData(**data_dict)
                    vibration_data_list.append(vibration_data)
            
            # 按时间戳排序
            vibration_data_list.sort(key=lambda x: x.timestamp, reverse=True)
            return vibration_data_list
            
        except Exception as e:
            logger.error(f"获取数据失败: {e}")
            return []
    
    def get_device_status(self, device_id: int) -> Optional[Dict[str, Any]]:
        """获取设备状态"""
        if not self.redis_client:
            return None
        
        try:
            status_key = f"vibration:status:device:{device_id}"
            status_json = self.redis_client.get(status_key)
            
            if status_json:
                return json.loads(status_json)
            return None
            
        except Exception as e:
            logger.error(f"获取设备状态失败: {e}")
            return None
    
    def get_statistics(self, device_id: int, hours: int = 24) -> Dict[str, Any]:
        """获取统计数据"""
        if not self.redis_client:
            return {}
        
        try:
            # 获取指定时间范围内的数据
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=hours)
            
            latest_key = f"vibration:latest:device:{device_id}"
            data_keys = self.redis_client.lrange(latest_key, 0, -1)
            
            data_list = []
            for key in data_keys:
                data_json = self.redis_client.get(key)
                if data_json:
                    data_dict = json.loads(data_json)
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
        if not self.redis_client:
            return
        
        try:
            cutoff_time = datetime.now() - timedelta(days=days)
            pattern = "vibration:device:*"
            
            for key in self.redis_client.scan_iter(match=pattern):
                data_json = self.redis_client.get(key)
                if data_json:
                    data_dict = json.loads(data_json)
                    data_timestamp = datetime.fromisoformat(data_dict['timestamp'])
                    if data_timestamp < cutoff_time:
                        self.redis_client.delete(key)
                        logger.info(f"删除旧数据: {key}")
            
        except Exception as e:
            logger.error(f"清理旧数据失败: {e}")

# 创建全局Redis服务实例
redis_service = RedisService() 