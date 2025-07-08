# CNC震动传感器监控系统

这是一个基于FastAPI + Vue.js + Redis的震动传感器数据监控系统，用于实时监控和分析CNC设备的震动数据。

## 系统架构

```
震动传感器 → 串口 → FastAPI后端 → Redis缓存 → Vue前端
```

### 数据流程
1. 震动传感器通过串口发送数据
2. FastAPI后端接收并解析数据
3. 数据存储到Redis进行缓存
4. Vue前端从API获取数据并展示

## 功能特性

### 后端功能
- ✅ 串口数据接收和解析
- ✅ Redis数据缓存和存储
- ✅ RESTful API接口
- ✅ 实时数据监控
- ✅ 数据统计分析
- ✅ 设备状态管理

### 前端功能
- ✅ 实时数据表格展示
- ✅ 设备状态监控
- ✅ 数据统计卡片
- ✅ 串口监控控制
- ✅ 测试数据发送
- ✅ 自动数据刷新

## 安装和配置

### 1. 环境要求
- Python 3.8+
- Node.js 16+
- Redis 6.0+
- 串口设备（震动传感器）

### 2. 安装Redis

**macOS:**
```bash
brew install redis
brew services start redis
```

**Ubuntu:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

**Windows:**
下载并安装Redis for Windows

### 3. 安装Python依赖
```bash
cd backend
pip install -r requirements.txt
```

### 4. 安装前端依赖
```bash
npm install
```

## 快速启动

### 方法1: 使用启动脚本（推荐）
```bash
python start_system.py
```

### 方法2: 手动启动

**启动后端:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**启动前端:**
```bash
npm run dev
```

## 使用说明

### 1. 访问系统
- 前端界面: http://localhost:5173
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

### 2. 震动监控页面
访问 `http://localhost:5173/vibration` 进入震动监控页面

### 3. 功能操作

#### 串口监控控制
- **启动监控**: 点击"启动监控"按钮开始接收串口数据
- **停止监控**: 点击"停止监控"按钮停止接收数据
- **发送测试数据**: 点击"发送测试数据"按钮生成模拟数据

#### 数据查看
- **设备选择**: 选择要监控的设备ID（80或81）
- **数据条数**: 选择要显示的数据条数（10-100条）
- **自动刷新**: 系统每5秒自动刷新数据

#### 数据统计
- **设备状态**: 显示设备在线状态
- **数据总数**: 显示已接收的数据条数
- **平均温度**: 显示24小时内的平均温度
- **最大振动**: 显示24小时内的最大振动值

## API接口说明

### 震动数据接口

#### 获取震动数据
```
GET /api/vibration/data/{device_id}?limit=50
```

#### 获取设备状态
```
GET /api/vibration/status/{device_id}
```

#### 获取统计数据
```
GET /api/vibration/statistics/{device_id}?hours=24
```

#### 启动串口监控
```
POST /api/serial/start
Body: {"device_id": 80}
```

#### 停止串口监控
```
POST /api/serial/stop
```

#### 发送测试数据
```
POST /api/test/send-data
Body: {"device_id": 80}
```

## 数据格式

### 震动传感器数据格式
```
Ax:0.1 Ay:0.2 Az:0.3 Gx:0.4 Gy:0.5 Gz:0.6 vx:0.7 vy:0.8 vz:0.9 ax:1.0 ay:1.1 az:1.2 t:25.06 sx:0 sy:0 sz:0 fx:0 fy:0 fz:0
```

### 数据字段说明
- **Ax, Ay, Az**: 加速度数据 (g)
- **Gx, Gy, Gz**: 陀螺仪数据 (°/s)
- **vx, vy, vz**: 振动速度 (mm/s)
- **ax, ay, az**: 振动角度 (°)
- **t**: 温度 (°C)
- **sx, sy, sz**: 振动位移 (mm)
- **fx, fy, fz**: 振动频率 (Hz)

## 配置说明

### 串口配置
在 `backend/serial_service.py` 中修改串口配置：
```python
class SerialService:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=1):
```

### Redis配置
在 `backend/redis_service.py` 中修改Redis配置：
```python
class RedisService:
    def __init__(self, host='localhost', port=6379, db=0):
```

## 故障排除

### 1. Redis连接失败
- 检查Redis服务是否启动
- 检查Redis端口是否正确
- 检查防火墙设置

### 2. 串口连接失败
- 检查串口设备是否正确连接
- 检查串口权限设置
- 检查串口配置参数

### 3. 前端无法连接后端
- 检查后端服务是否启动
- 检查CORS配置
- 检查网络连接

### 4. 数据不显示
- 检查Redis中是否有数据
- 检查API接口是否正常
- 检查前端网络请求

## 开发说明

### 添加新的传感器类型
1. 在 `vibration_models.py` 中添加新的数据模型
2. 在 `serial_service.py` 中添加数据解析逻辑
3. 在 `redis_service.py` 中添加数据存储逻辑
4. 在前端组件中添加数据展示

### 扩展API功能
1. 在 `vibration_api.py` 中添加新的API接口
2. 在 `main.py` 中注册新的路由
3. 在前端添加对应的功能

### 自定义数据展示
1. 修改 `PerformanceChart.vue` 组件
2. 添加新的图表类型
3. 自定义数据格式和样式

## 许可证

MIT License

## 联系方式

如有问题或建议，请联系开发团队。 