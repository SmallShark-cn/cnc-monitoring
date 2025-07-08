import serial
import threading
import time
import logging
from typing import Dict, Any, Optional
from memory_service import memory_service

logger = logging.getLogger(__name__)

class SerialService:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=1):
        """初始化串口服务"""
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.is_running = False
        self.thread = None
        
    def connect(self) -> bool:
        """连接串口"""
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            logger.info(f"串口连接成功: {self.port}")
            return True
        except Exception as e:
            logger.error(f"串口连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开串口连接"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            logger.info("串口连接已断开")
    
    def parse_vibration_data(self, data_str: str) -> Optional[Dict[str, Any]]:
        """解析震动传感器数据"""
        try:
            # 示例数据格式: Ax:0.1 Ay:0.2 Az:0.3 Gx:0.4 Gy:0.5 Gz:0.6 vx:0.7 vy:0.8 vz:0.9 ax:1.0 ay:1.1 az:1.2 t:25.06 sx:0 sy:0 sz:0 fx:0 fy:0 fz:0
            data_dict = {}
            
            # 分割数据
            parts = data_str.strip().split()
            for part in parts:
                if ':' in part:
                    key, value = part.split(':', 1)
                    try:
                        data_dict[key] = float(value)
                    except ValueError:
                        data_dict[key] = 0.0
            
            # 映射到设备数据格式
            device_data = {
                '52': data_dict.get('Ax', 0.0),  # ax
                '53': data_dict.get('Ay', 0.0),  # ay
                '54': data_dict.get('Az', 0.0),  # az
                '55': data_dict.get('Gx', 0.0),  # gx
                '56': data_dict.get('Gy', 0.0),  # gy
                '57': data_dict.get('Gz', 0.0),  # gz
                '58': data_dict.get('vx', 0.0),  # vx
                '59': data_dict.get('vy', 0.0),  # vy
                '60': data_dict.get('vz', 0.0),  # vz
                '61': data_dict.get('ax', 0.0),  # angle_x
                '62': data_dict.get('ay', 0.0),  # angle_y
                '63': data_dict.get('az', 0.0),  # angle_z
                '64': data_dict.get('t', 0.0),   # temperature
                '65': data_dict.get('sx', 0.0),  # sx
                '66': data_dict.get('sy', 0.0),  # sy
                '67': data_dict.get('sz', 0.0),  # sz
                '68': data_dict.get('fx', 0.0),  # fx
                '69': data_dict.get('fy', 0.0),  # fy
                '70': data_dict.get('fz', 0.0)   # fz
            }
            
            return device_data
            
        except Exception as e:
            logger.error(f"解析数据失败: {e}, 原始数据: {data_str}")
            return None
    
    def read_data_loop(self, device_id: int = 80):
        """读取数据的循环"""
        while self.is_running and self.serial_conn and self.serial_conn.is_open:
            try:
                # 读取一行数据
                if self.serial_conn.in_waiting > 0:
                    data_line = self.serial_conn.readline().decode('utf-8').strip()
                    
                    if data_line:
                        logger.debug(f"收到数据: {data_line}")
                        
                                                # 解析数据
                        device_data = self.parse_vibration_data(data_line)
                        if device_data:
                            # 存储到内存
                            success = memory_service.store_vibration_data(device_id, device_data)
                            if success:
                                logger.debug(f"数据存储成功: 设备 {device_id}")
                            else:
                                logger.warning(f"数据存储失败: 设备 {device_id}")
                
                time.sleep(0.1)  # 短暂休眠避免CPU占用过高
                
            except Exception as e:
                logger.error(f"读取数据时发生错误: {e}")
                time.sleep(1)  # 错误时等待更长时间
    
    def start_monitoring(self, device_id: int = 80):
        """开始监控串口数据"""
        if not self.connect():
            logger.error("无法启动监控：串口连接失败")
            return False
        
        self.is_running = True
        self.thread = threading.Thread(
            target=self.read_data_loop,
            args=(device_id,),
            daemon=True
        )
        self.thread.start()
        logger.info(f"开始监控设备 {device_id} 的串口数据")
        return True
    
    def stop_monitoring(self):
        """停止监控"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)
        self.disconnect()
        logger.info("停止串口数据监控")
    
    def send_test_data(self, device_id: int = 80):
        """发送测试数据（用于开发测试）"""
        import random
        
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
        
        success = memory_service.store_vibration_data(device_id, test_data)
        if success:
            logger.info(f"测试数据发送成功: 设备 {device_id}")
        else:
            logger.error(f"测试数据发送失败: 设备 {device_id}")
        
        return success

# 创建全局串口服务实例
serial_service = SerialService() 