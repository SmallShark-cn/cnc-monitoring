<template>
  <div class="row g-3">
    <!-- 声学传感器卡片 -->
    <div class="col-md-4">
      <div class="card border-0 h-100 gradbg rounded-big shadow-sm">
        <div class="card-body p-4">
          <!-- 头部信息 -->
          <div class="d-flex justify-content-between align-items-start mb-4">
            <div class="flex-grow-1">
              <div class="d-flex align-items-center mb-2">
                <i class="fas fa-microphone text-success me-2"></i>
                <h6 class="text-muted mb-0">声学传感器</h6>
              </div>
              <h3 class="text-dark mb-1">{{ formatNumber(acousticData.spl, 1) }} <span class="fs-6 text-muted">dB</span></h3>
              <div class="row g-2 mt-2">
                <div class="col-6">
                  <small class="text-muted d-block">RMS</small>
                  <span class="fw-semibold text-dark">{{ formatNumber(acousticData.rms, 3) }}</span>
                </div>
                <div class="col-6">
                  <small class="text-muted d-block">峰值</small>
                  <span class="fw-semibold text-dark">{{ formatNumber(acousticData.peak, 3) }}</span>
                </div>
              </div>
            </div>
            <div class="bg-success bg-opacity-10 p-3 rounded-circle">
              <i class="fas fa-microphone text-success fs-5"></i>
            </div>
          </div>
          
          <!-- 详细数据 -->
          <div class="row g-2 mb-3">
            <div class="col-4">
              <small class="text-muted d-block">峰度</small>
              <span class="fw-semibold text-dark">{{ formatNumber(acousticData.kurtosis, 2) }}</span>
            </div>
            <div class="col-4">
              <small class="text-muted d-block">偏度</small>
              <span class="fw-semibold text-dark">{{ formatNumber(acousticData.skewness, 2) }}</span>
            </div>
            <div class="col-4">
              <small class="text-muted d-block">标准差</small>
              <span class="fw-semibold text-dark">{{ formatNumber(acousticData.std, 3) }}</span>
            </div>
          </div>
          
          <!-- 图表 -->
          <div style="height: 100px;">
            <Line
              :data="acousticChartData"
              :options="miniChartOptions"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- 振动传感器卡片 -->
    <div class="col-md-4">
      <div class="card gradbg border-0 h-100 rounded-big shadow-sm">
        <div class="card-body p-4">
          <!-- 头部信息 -->
          <div class="d-flex justify-content-between align-items-start mb-4">
            <div class="flex-grow-1">
              <div class="d-flex align-items-center mb-2">
                <i class="fas fa-wave-square text-primary me-2"></i>
                <h6 class="text-muted mb-0">振动传感器</h6>
              </div>
              <h3 class="text-dark mb-1">{{ formatNumber(vibrationData.rms, 3) }} <span class="fs-6 text-muted">m/s²</span></h3>
              <div class="row g-2 mt-2">
                <div class="col-6">
                  <small class="text-muted d-block">峰值</small>
                  <span class="fw-semibold text-dark">{{ formatNumber(vibrationData.peak, 3) }}</span>
                </div>
                <div class="col-6">
                  <small class="text-muted d-block">标准差</small>
                  <span class="fw-semibold text-dark">{{ formatNumber(vibrationData.std, 3) }}</span>
                </div>
              </div>
            </div>
            <div class="bg-primary bg-opacity-10 p-3 rounded-circle">
              <i class="fas fa-wave-square text-primary fs-5"></i>
            </div>
          </div>
          
          <!-- 详细数据 -->
          <div class="row g-2 mb-3">
            <div class="col-4">
              <small class="text-muted d-block">峰度</small>
              <span class="fw-semibold text-dark">{{ formatNumber(vibrationData.kurtosis, 2) }}</span>
            </div>
            <div class="col-4">
              <small class="text-muted d-block">偏度</small>
              <span class="fw-semibold text-dark">{{ formatNumber(vibrationData.skewness, 2) }}</span>
            </div>
            <div class="col-4">
              <small class="text-muted d-block">RMS</small>
              <span class="fw-semibold text-dark">{{ formatNumber(vibrationData.rms, 3) }}</span>
            </div>
          </div>
          
          <!-- 图表 -->
          <div style="height: 100px;">
            <Bar
              :data="vibrationChartData"
              :options="miniBarOptions"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- 刀具磨损状态卡片 -->
    <div class="col-md-4">
      <div class="card gradbg border-0 h-100 rounded-big shadow-sm">
        <div class="card-body p-4">
          <!-- 头部信息 -->
          <div class="d-flex justify-content-between align-items-start mb-4">
            <div class="flex-grow-1">
              <div class="d-flex align-items-center mb-2">
                <i class="fas fa-tools text-warning me-2"></i>
                <h6 class="text-muted mb-0">刀具磨损状态</h6>
              </div>
              <h3 class="text-dark mb-1">{{ getWearStateText(toolWearData.wear_state) }}</h3>
              <div class="row g-2 mt-2">
                <div class="col-6">
                  <small class="text-muted d-block">置信度</small>
                  <span class="fw-semibold text-dark">{{ formatNumber(toolWearData.confidence * 100, 1) }}%</span>
                </div>
                <div class="col-6">
                  <small class="text-muted d-block">剩余寿命</small>
                  <span class="fw-semibold text-dark">{{ toolWearData.rul }}h</span>
                </div>
              </div>
            </div>
            <div class="bg-warning bg-opacity-10 p-3 rounded-circle">
              <i class="fas fa-tools text-warning fs-5"></i>
            </div>
          </div>
          
          <!-- 贡献度分析 -->
          <div class="row g-2 mb-3">
            <div class="col-6">
              <small class="text-muted d-block">振动贡献</small>
              <div class="progress" style="height: 6px;">
                <div class="progress-bar bg-primary" :style="{ width: toolWearData.contributions.vibration * 100 + '%' }"></div>
              </div>
              <small class="text-muted">{{ formatNumber(toolWearData.contributions.vibration * 100, 1) }}%</small>
            </div>
            <div class="col-6">
              <small class="text-muted d-block">声学贡献</small>
              <div class="progress" style="height: 6px;">
                <div class="progress-bar bg-success" :style="{ width: toolWearData.contributions.acoustic * 100 + '%' }"></div>
              </div>
              <small class="text-muted">{{ formatNumber(toolWearData.contributions.acoustic * 100, 1) }}%</small>
            </div>
          </div>
          
          <!-- 图表 -->
          <div style="height: 100px;">
            <Doughnut
              :data="toolWearChartData"
              :options="doughnutOptions"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script>
  import { Line, Bar, Doughnut } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
  } from 'chart.js'
  
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
  )
  
  export default {
    name: 'StatsCards',
    components: {
      Line,
      Bar,
      Doughnut
    },
    data() {
      return {
        // WebSocket连接
        acousticWs: null,
        vibrationWs: null,
        toolWearWs: null,
        
        // 实时数据
        acousticData: {
          timestamp: '',
          rms: 0,
          peak: 0,
          kurtosis: 0,
          skewness: 0,
          std: 0,
          spl: 0
        },
        vibrationData: {
          timestamp: '',
          rms: 0,
          peak: 0,
          kurtosis: 0,
          skewness: 0,
          std: 0
        },
        toolWearData: {
          timestamp: '',
          wear_state: 'normal',
          confidence: 0,
          rul: 0,
          contributions: { vibration: 0, acoustic: 0 }
        },
        
        // 图表数据历史记录（用于实时更新）
        acousticHistory: [],
        vibrationHistory: [],
        toolWearHistory: [],
        
        // 图表配置
        miniChartOptions: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: { 
              enabled: true,
              mode: 'index',
              intersect: false,
              backgroundColor: 'rgba(0,0,0,0.8)',
              titleColor: '#fff',
              bodyColor: '#fff',
              borderColor: '#ddd',
              borderWidth: 1
            }
          },
          scales: {
            x: { 
              display: false,
              grid: { display: false }
            },
            y: { 
              display: false,
              grid: { display: false }
            },
            y1: {
              display: false,
              grid: { display: false },
              position: 'right'
            }
          },
          elements: {
            point: { radius: 0 },
            line: { tension: 0.4 }
          },
          interaction: {
            mode: 'index',
            intersect: false
          },
          animation: {
            duration: 300
          }
        },
        miniBarOptions: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: { 
              enabled: true,
              mode: 'index',
              intersect: false,
              backgroundColor: 'rgba(0,0,0,0.8)',
              titleColor: '#fff',
              bodyColor: '#fff',
              borderColor: '#ddd',
              borderWidth: 1
            }
          },
          scales: {
            x: { 
              display: false,
              grid: { display: false }
            },
            y: { 
              display: false,
              grid: { display: false }
            }
          },
          animation: {
            duration: 300
          }
        },
        doughnutOptions: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: { 
              enabled: true,
              backgroundColor: 'rgba(0,0,0,0.8)',
              titleColor: '#fff',
              bodyColor: '#fff',
              borderColor: '#ddd',
              borderWidth: 1,
              callbacks: {
                label: function(context) {
                  return context.label + ': ' + context.parsed + '%'
                }
              }
            }
          },
          animation: {
            duration: 300
          }
        }
      }
    },
    computed: {
      // 声学传感器图表数据 - 多指标展示
      acousticChartData() {
        return {
          labels: this.acousticHistory.map((_, index) => index + 1),
          datasets: [
            {
              label: 'SPL',
              data: this.acousticHistory.map(item => item.spl),
              borderColor: '#10B981',
              backgroundColor: 'rgba(16, 185, 129, 0.1)',
              borderWidth: 2,
              fill: true,
              tension: 0.4,
              yAxisID: 'y'
            },
            {
              label: 'RMS',
              data: this.acousticHistory.map(item => item.rms * 1000), // 放大显示
              borderColor: '#F59E0B',
              backgroundColor: 'rgba(245, 158, 11, 0.1)',
              borderWidth: 1,
              fill: false,
              tension: 0.4,
              yAxisID: 'y1'
            }
          ]
        }
      },
      
      // 振动传感器图表数据 - 多指标对比
      vibrationChartData() {
        return {
          labels: this.vibrationHistory.map((_, index) => index + 1),
          datasets: [
            {
              label: 'RMS',
              data: this.vibrationHistory.map(item => item.rms * 1000),
              backgroundColor: '#3B82F6',
              borderRadius: 2
            },
            {
              label: '峰值',
              data: this.vibrationHistory.map(item => item.peak * 1000),
              backgroundColor: '#8B5CF6',
              borderRadius: 2
            }
          ]
        }
      },
      
      // 刀具磨损图表数据 - 置信度展示
      toolWearChartData() {
        const wearColor = this.getWearStateColor(this.toolWearData.wear_state)
        return {
          labels: ['磨损置信度', '剩余'],
          datasets: [{
            data: [this.toolWearData.confidence * 100, (1 - this.toolWearData.confidence) * 100],
            backgroundColor: [wearColor, '#E5E7EB'],
            borderWidth: 0,
            cutout: '60%'
          }]
        }
      }
    },
    async mounted() {
      this.initWebSocketConnections()
    },
    beforeUnmount() {
      this.closeWebSocketConnections()
    },
    methods: {
      formatNumber(num, decimals = 0) {
        if (typeof num !== 'number') return '0'
        return num.toLocaleString('zh-CN', {
          minimumFractionDigits: decimals,
          maximumFractionDigits: decimals
        })
      },
      
      // 初始化WebSocket连接
      initWebSocketConnections() {
        // 声学传感器WebSocket
        this.acousticWs = new WebSocket('ws://localhost:8000/ws/acoustic/statistics')
        this.acousticWs.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            this.updateAcousticData(data)
          } catch (error) {
            console.error('声学数据解析错误:', error)
          }
        }
        this.acousticWs.onerror = (error) => {
          console.error('声学WebSocket连接错误:', error)
        }
        
        // 振动传感器WebSocket
        this.vibrationWs = new WebSocket('ws://localhost:8000/ws/vibration/statistics')
        this.vibrationWs.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            this.updateVibrationData(data)
          } catch (error) {
            console.error('振动数据解析错误:', error)
          }
        }
        this.vibrationWs.onerror = (error) => {
          console.error('振动WebSocket连接错误:', error)
        }
        
        // 刀具磨损WebSocket
        this.toolWearWs = new WebSocket('ws://localhost:8000/ws/tool-wear')
        this.toolWearWs.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            this.updateToolWearData(data)
          } catch (error) {
            console.error('刀具磨损数据解析错误:', error)
          }
        }
        this.toolWearWs.onerror = (error) => {
          console.error('刀具磨损WebSocket连接错误:', error)
        }
      },
      
      // 关闭WebSocket连接
      closeWebSocketConnections() {
        if (this.acousticWs) {
          this.acousticWs.close()
        }
        if (this.vibrationWs) {
          this.vibrationWs.close()
        }
        if (this.toolWearWs) {
          this.toolWearWs.close()
        }
      },
      
      // 更新声学数据
      updateAcousticData(data) {
        this.acousticData = { ...data }
        this.acousticHistory.push(data)
        
        // 保持最近20个数据点，避免内存泄漏
        if (this.acousticHistory.length > 20) {
          this.acousticHistory.shift()
        }
      },
      
      // 更新振动数据
      updateVibrationData(data) {
        this.vibrationData = { ...data }
        this.vibrationHistory.push(data)
        
        // 保持最近20个数据点
        if (this.vibrationHistory.length > 20) {
          this.vibrationHistory.shift()
        }
      },
      
      // 更新刀具磨损数据
      updateToolWearData(data) {
        this.toolWearData = { ...data }
        this.toolWearHistory.push(data)
        
        // 保持最近10个数据点
        if (this.toolWearHistory.length > 10) {
          this.toolWearHistory.shift()
        }
      },
      
      // 获取磨损状态文本
      getWearStateText(wearState) {
        const stateMap = {
          'normal': '正常',
          'mild_wear': '轻微磨损',
          'moderate_wear': '中度磨损',
          'severe_wear': '严重磨损'
        }
        return stateMap[wearState] || '未知'
      },
      
      // 获取磨损状态颜色
      getWearStateColor(wearState) {
        const colorMap = {
          'normal': '#10B981', // 绿色
          'mild_wear': '#F59E0B', // 黄色
          'moderate_wear': '#F97316', // 橙色
          'severe_wear': '#EF4444' // 红色
        }
        return colorMap[wearState] || '#6B7280'
      }
    }
  }
  </script>

  <style>
.card.gradbg {
  background: linear-gradient(180deg, #ffffff, #ffffff);
  transition: all 0.3s ease;
  border: 1px solid rgba(0,0,0,0.05);
}

.card.gradbg:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1) !important;
}

.card-body {
  position: relative;
}

.progress {
  background-color: rgba(0,0,0,0.05);
  border-radius: 10px;
}

.progress-bar {
  border-radius: 10px;
  transition: width 0.6s ease;
}

.fw-semibold {
  font-weight: 600;
}

.text-dark {
  color: #1f2937 !important;
}

.text-muted {
  color: #6b7280 !important;
}

.rounded-circle {
  transition: all 0.3s ease;
}

.rounded-circle:hover {
  transform: scale(1.05);
}

/* 实时数据更新动画 */
@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

.fw-semibold {
  animation: pulse 2s infinite;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .card-body {
    padding: 1rem !important;
  }
  
  h3 {
    font-size: 1.5rem !important;
  }
  
  .row.g-2 {
    margin: 0 -0.25rem;
  }
  
  .col-4, .col-6 {
    padding: 0 0.25rem;
  }
}
</style>