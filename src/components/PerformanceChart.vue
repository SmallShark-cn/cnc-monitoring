<template>
  <div class="card vibration-card border-0 mb-4 rounded-big shadow-sm gradbg" style="min-height: 30px; max-width: 1200px;">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h5 class="text-dark mb-0">震动传感器数据监控</h5>
        <div class="d-flex gap-2">
          <button @click="startMonitoring" class="btn btn-success btn-sm" :disabled="isMonitoring">
            <i class="fas fa-play me-1"></i>启动监控
          </button>
          <button @click="stopMonitoring" class="btn btn-danger btn-sm" :disabled="!isMonitoring">
            <i class="fas fa-stop me-1"></i>停止监控
          </button>
          <button @click="sendTestData" class="btn btn-warning btn-sm">
            <i class="fas fa-database me-1"></i>发送测试数据
          </button>
          <button @click="refreshData" class="btn btn-primary btn-sm">
            <i class="fas fa-sync-alt me-1"></i>刷新数据
          </button>
        </div>
      </div>
      
      <!-- 设备状态卡片 -->
      <div class="row mb-4">
        <div class="col-md-3">
          <div class="status-card status-online">
            <div class="card-body text-center">
              <h6>设备状态</h6>
              <span class="badge" :class="deviceStatus.is_online ? 'status-badge-online' : 'status-badge-offline'">
                {{ deviceStatus.is_online ? '在线' : '离线' }}
              </span>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="status-card status-data">
            <div class="card-body text-center">
              <h6>数据总数</h6>
              <h4>{{ deviceStatus.data_count || 0 }}</h4>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="status-card status-temp">
            <div class="card-body text-center">
              <h6>平均温度</h6>
              <h4>{{ statistics.avg_temperature ? statistics.avg_temperature.toFixed(1) + '°C' : 'N/A' }}</h4>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="status-card status-vibration">
            <div class="card-body text-center">
              <h6>最大振动</h6>
              <h4>{{ statistics.max_vibration ? statistics.max_vibration.toFixed(2) : 'N/A' }}</h4>
            </div>
          </div>
        </div>
      </div>

      <!-- 数据表格 -->
      <div class="table-responsive">
        <table class="table vibration-table">
          <thead>
            <tr>
              <th>时间</th>
              <th>温度 (°C)</th>
              <th>振动速度 (mm/s)</th>
              <th>振动位移 (mm)</th>
              <th>振动频率 (Hz)</th>
              <th>加速度 (g)</th>
              <th>陀螺仪 (°/s)</th>
              <th>角度 (°)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in vibrationData" :key="item.timestamp">
              <td>{{ formatTime(item.timestamp) }}</td>
              <td>{{ item.temperature.toFixed(2) }}</td>
              <td>
                <span class="data-badge badge-velocity me-1">X:{{ item.vx.toFixed(2) }}</span>
                <span class="data-badge badge-velocity me-1">Y:{{ item.vy.toFixed(2) }}</span>
                <span class="data-badge badge-velocity">Z:{{ item.vz.toFixed(2) }}</span>
              </td>
              <td>
                <span class="data-badge badge-displacement me-1">X:{{ item.sx.toFixed(2) }}</span>
                <span class="data-badge badge-displacement me-1">Y:{{ item.sy.toFixed(2) }}</span>
                <span class="data-badge badge-displacement">Z:{{ item.sz.toFixed(2) }}</span>
              </td>
              <td>
                <span class="data-badge badge-frequency me-1">X:{{ item.fx.toFixed(1) }}</span>
                <span class="data-badge badge-frequency me-1">Y:{{ item.fy.toFixed(1) }}</span>
                <span class="data-badge badge-frequency">Z:{{ item.fz.toFixed(1) }}</span>
              </td>
              <td>
                <span class="data-badge badge-acceleration me-1">X:{{ item.ax.toFixed(3) }}</span>
                <span class="data-badge badge-acceleration me-1">Y:{{ item.ay.toFixed(3) }}</span>
                <span class="data-badge badge-acceleration">Z:{{ item.az.toFixed(3) }}</span>
              </td>
              <td>
                <span class="data-badge badge-gyroscope me-1">X:{{ item.gx.toFixed(1) }}</span>
                <span class="data-badge badge-gyroscope me-1">Y:{{ item.gy.toFixed(1) }}</span>
                <span class="data-badge badge-gyroscope">Z:{{ item.gz.toFixed(1) }}</span>
              </td>
              <td>
                <span class="data-badge badge-angle me-1">X:{{ item.angle_x.toFixed(1) }}</span>
                <span class="data-badge badge-angle me-1">Y:{{ item.angle_y.toFixed(1) }}</span>
                <span class="data-badge badge-angle">Z:{{ item.angle_z.toFixed(1) }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- 分页 -->
      <div class="d-flex justify-content-between align-items-center mt-3">
        <div>
          <span class="text-muted">显示 {{ vibrationData.length }} 条记录</span>
        </div>
        <div class="d-flex gap-2">
          <select v-model="selectedDevice" @change="onDeviceChange" class="form-select form-select-sm" style="width: auto;">
            <option value="80">设备 80</option>
            <option value="81">设备 81</option>
          </select>
          <select v-model="dataLimit" @change="refreshData" class="form-select form-select-sm" style="width: auto;">
            <option value="10">10条</option>
            <option value="20">20条</option>
            <option value="50">50条</option>
            <option value="100">100条</option>
          </select>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VibrationDataTable',
  data() {
    return {
      vibrationData: [],
      ws: null,
      deviceStatus: {
        is_online: false,
        data_count: 0,
        last_update: null
      },
      statistics: {
        avg_temperature: 0,
        max_vibration: 0,
        avg_vibration: 0
      },
      isMonitoring: false,
      selectedDevice: 80,
      dataLimit: 20
    }
  },
  mounted() {
    this.initWebSocket()
  },
  beforeUnmount() {
    if (this.ws) this.ws.close()
  },
  methods: {
    initWebSocket() {
      if (this.ws) this.ws.close()
      this.vibrationData = []
      this.ws = new WebSocket('ws://localhost:8000/ws/vibration/time-domain')
      this.ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data)
          if (msg.data && Array.isArray(msg.data)) {
            msg.data.forEach(item => {
              // 可根据selectedDevice过滤设备（如有device_id字段）
              this.vibrationData.push(item)
              if (this.vibrationData.length > this.dataLimit) {
                this.vibrationData.shift()
              }
            })
          }
        } catch (e) {
          console.error('WebSocket数据解析失败', e)
        }
      }
      this.ws.onerror = (e) => {
        console.error('WebSocket连接错误', e)
      }
    },
    onDeviceChange() {
      // 如有多设备可在此切换ws地址或过滤数据
      this.vibrationData = []
      // this.initWebSocket() // 如需切换ws可取消注释
    },
    refreshData() {
      this.vibrationData = []
    },
    formatTime(timestamp) {
      const date = new Date(timestamp)
      return date.toLocaleString('zh-CN')
    },
    async startMonitoring() {
      try {
        const response = await fetch('http://localhost:8000/api/serial/start', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ device_id: parseInt(this.selectedDevice) })
        })
        const result = await response.json()
        
        if (result.success) {
          this.isMonitoring = true
          alert('串口监控已启动')
        } else {
          alert('启动失败: ' + result.message)
        }
      } catch (error) {
        console.error('启动监控失败:', error)
        alert('启动监控失败')
      }
    },
    
    async stopMonitoring() {
      try {
        const response = await fetch('http://localhost:8000/api/serial/stop', {
          method: 'POST'
        })
        const result = await response.json()
        
        if (result.success) {
          this.isMonitoring = false
          alert('串口监控已停止')
        } else {
          alert('停止失败: ' + result.message)
        }
      } catch (error) {
        console.error('停止监控失败:', error)
        alert('停止监控失败')
      }
    },
    
    async sendTestData() {
      try {
        const response = await fetch('http://localhost:8000/api/test/send-data', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ device_id: parseInt(this.selectedDevice) })
        })
        const result = await response.json()
        
        if (result.success) {
          alert('测试数据发送成功')
          await this.refreshData()
        } else {
          alert('发送失败: ' + result.message)
        }
      } catch (error) {
        console.error('发送测试数据失败:', error)
        alert('发送测试数据失败')
      }
    },
  }
}
</script>


<style scoped>
.card.rounded-big{
  border-radius: 1rem ;
}

/* 震动卡片主题 */
.vibration-card {
  background: #fff;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(173, 216, 230, 0.3);
}

/* 状态卡片样式 */
.status-card {
  border-radius: 12px;
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.status-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(173, 216, 230, 0.3);
}

.status-online {
  background: linear-gradient(135deg, rgba(100, 149, 237, 0.8), rgba(70, 130, 180, 0.6));
  color: white;
}

.status-data {
  background: linear-gradient(135deg, rgba(64, 224, 208, 0.8), rgba(72, 209, 204, 0.6));
  color: white;
}

.status-temp {
  background: linear-gradient(135deg, rgba(255, 182, 193, 0.8), rgba(255, 160, 122, 0.6));
  color: white;
}

.status-vibration {
  background: linear-gradient(135deg, rgba(144, 238, 144, 0.8), rgba(50, 205, 50, 0.6));
  color: white;
}

/* 状态徽章 */
.status-badge-online {
  background-color: rgba(40, 167, 69, 0.9) !important;
  color: white;
}

.status-badge-offline {
  background-color: rgba(220, 53, 69, 0.9) !important;
  color: white;
}

/* 表格样式 */
.vibration-table {
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  overflow: hidden;
  backdrop-filter: blur(5px);
}

.vibration-table thead {
  background: linear-gradient(135deg, rgba(173, 216, 230, 0.9), rgba(135, 206, 250, 0.8));
}

.vibration-table thead th {
  color: #2c3e50;
  font-weight: 600;
  border: none;
  padding: 15px 10px;
}

.vibration-table tbody tr {
  transition: all 0.2s ease;
}

.vibration-table tbody tr:hover {
  background: rgba(173, 216, 230, 0.2);
}

.vibration-table tbody td {
  border: none;
  padding: 12px 10px;
  color: #2c3e50;
}

/* 数据徽章样式 */
.data-badge {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  border: 1px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(5px);
}

.badge-velocity {
  background: rgba(100, 149, 237, 0.7);
  color: white;
}

.badge-displacement {
  background: rgba(255, 182, 193, 0.7);
  color: white;
}

.badge-frequency {
  background: rgba(144, 238, 144, 0.7);
  color: white;
}

.badge-acceleration {
  background: rgba(255, 160, 122, 0.7);
  color: white;
}

.badge-gyroscope {
  background: rgba(64, 224, 208, 0.7);
  color: white;
}

.badge-angle {
  background: rgba(147, 112, 219, 0.7);
  color: white;
}

/* 按钮样式调整 */
.btn {
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(173, 216, 230, 0.4);
}

/* 选择框样式 */
.form-select {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(173, 216, 230, 0.5);
  backdrop-filter: blur(5px);
}

.form-select:focus {
  border-color: rgba(173, 216, 230, 0.8);
  box-shadow: 0 0 0 0.2rem rgba(173, 216, 230, 0.25);
}
/* 鼠标悬停效果 */
.card.gradbg {
  background: linear-gradient(180deg, #ffffff, #ffffff);
  transition: all 0.3s ease;
  border: 1px solid rgba(0,0,0,0.05);
}

.card.gradbg:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1) !important;
}
</style>