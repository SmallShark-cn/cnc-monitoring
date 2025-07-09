# CNC监控系统

一个基于Vue.js + FastAPI + Redis的实时CNC机床监控系统，支持振动、声学和刀具磨损数据的实时监控和可视化。

## 系统架构

- **前端**: Vue.js 3 + Chart.js + Bootstrap
- **后端**: FastAPI + WebSocket + Redis
- **数据存储**: Redis (实时数据) + 内存缓存
- **实时通信**: WebSocket + HTTP API

## 功能特性

### 🎯 核心功能
- **实时数据监控**: 振动、声学、刀具磨损数据实时采集
- **数据可视化**: 多种图表展示数据趋势
- **告警系统**: 异常状态实时告警
- **历史数据**: Redis存储最近30条历史数据
- **多设备支持**: 支持多台CNC设备同时监控

### 📊 数据展示
- **统计卡片**: 实时显示各传感器关键指标
- **性能趋势图**: Windows资源管理器风格的实时曲线图
- **告警计数器**: 实时告警信息展示
- **数据表格**: 详细的传感器数据列表

## 快速开始

### 1. 环境要求

- Python 3.8+
- Node.js 16+
- Redis 6.0+

### 2. 安装依赖

```bash
# 安装Python依赖
cd backend
pip install -r requirements.txt

# 安装Node.js依赖
npm install
```

### 3. 启动系统

#### 方式一：使用启动脚本（推荐）
```bash
python start_system.py
```

#### 方式二：手动启动
```bash
# 1. 启动Redis
redis-server

# 2. 启动后端API服务
cd backend
python main.py

# 3. 启动前端开发服务器
npm run dev
```

### 4. 访问系统

- **前端界面**: http://localhost:5173
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

## 数据流架构

### 后端数据流
```
WebSocket推送 → Redis存储 → HTTP API → 前端展示
```

1. **WebSocket服务**: 实时推送模拟数据
2. **Redis存储**: 保存最近30条历史数据
3. **HTTP API**: 提供历史数据查询接口

### 前端数据流
```
Dashboard.vue (数据中心) → 子组件 (展示层)
```

1. **Dashboard.vue**: 定时拉取所有历史数据
2. **子组件**: 通过props接收数据并渲染

## API接口

### WebSocket接口
- `ws://localhost:8000/ws/vibration/statistics` - 振动统计数据
- `ws://localhost:8000/ws/acoustic/statistics` - 声学统计数据
- `ws://localhost:8000/ws/tool-wear` - 刀具磨损数据

### HTTP接口
- `GET /api/vibration/rms-history` - 获取RMS历史数据
- `GET /api/acoustic/history` - 获取声学历史数据
- `GET /api/tool-wear/history` - 获取刀具磨损历史数据
- `GET /api/performance` - 获取性能数据
- `GET /api/stats` - 获取统计数据

## 组件说明

### 前端组件
- **Dashboard.vue**: 主页面，数据中心
- **StatsCards.vue**: 统计卡片组件
- **VibrationTrendChart.vue**: 振动趋势图表
- **PerformanceChart.vue**: 性能监控表格
- **WarningCounter.vue**: 告警计数器

### 后端模块
- **main.py**: 主应用入口，WebSocket和HTTP API
- **mock_realtime_data.py**: 模拟实时数据生成
- **redis_service.py**: Redis数据管理
- **vibration_api.py**: 振动数据API
- **serial_service.py**: 串口通信服务

## 配置说明

### Redis配置
- 默认连接: `localhost:6379`
- 数据库: `db=0`
- 数据保留: 最近30条记录

### 前端配置
- 开发服务器: `localhost:5173`
- API基础URL: `http://localhost:8000`

### 后端配置
- 服务端口: `8000`
- WebSocket支持: 多客户端连接
- CORS配置: 允许前端跨域访问

## 开发指南

### 添加新的数据类型
1. 在后端`main.py`中添加新的WebSocket端点
2. 在Redis中存储新数据
3. 添加对应的HTTP API接口
4. 在前端Dashboard.vue中拉取新数据
5. 创建新的展示组件

### 自定义图表样式
- 修改`VibrationTrendChart.vue`中的`chartOptions`
- 调整颜色、线条样式、动画效果
- 支持Windows资源管理器风格

## 故障排除

### 常见问题
1. **Redis连接失败**: 确保Redis服务已启动
2. **WebSocket连接错误**: 检查后端服务是否正常运行
3. **前端数据不更新**: 检查API接口是否正常响应
4. **图表不显示**: 确认Chart.js依赖已正确安装

### 日志查看
- 后端日志: 控制台输出
- 前端日志: 浏览器开发者工具
- Redis日志: `redis-cli monitor`

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
