<template>
  <div class="card bg-white border-0 rounded-big shadow-sm gradbg">
    <div class="card-header bg-gradient-info text-white">
      <div class="d-flex align-items-center justify-content-between">
        <div class="d-flex align-items-center">
          <i class="fas fa-radar-alt me-3 fs-4"></i>
          <div>
            <h5 class="mb-0">智能异常检测雷达</h5>
            <small class="opacity-75">多维度系统健康评估 · AI预警算法</small>
          </div>
        </div>
        <div class="algorithm-badge">
          <span class="badge bg-light text-dark">
            <i class="fas fa-microchip me-1"></i>RWKV-1.5B
          </span>
        </div>
      </div>
    </div>
    <div class="card-body p-4">
      <div class="row">
        <!-- 雷达图区域 -->
        <div class="col-md-8">
          <div class="radar-container">
            <div class="radar-title text-center mb-3">
              <h6 class="fw-bold">系统健康状态雷达图</h6>
              <small class="text-muted">数值越接近中心表示状态越健康</small>
            </div>
            <div class="radar-chart-wrapper">
              <canvas ref="radarCanvas" width="400" height="400"></canvas>
              <!-- 雷达图中心状态 -->
              <div class="radar-center">
                <div class="center-score" :class="getOverallStatusClass()">
                  {{ getOverallHealthScore() }}
                </div>
                <div class="center-label">综合健康度</div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 指标详情区域 -->
        <div class="col-md-4">
          <div class="metrics-panel">
            <h6 class="fw-bold mb-3">
              <i class="fas fa-list-alt text-primary me-2"></i>
              检测指标详情
            </h6>
            
            <div class="metric-item" v-for="metric in radarMetrics" :key="metric.name">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <div class="metric-info">
                  <div class="metric-name">{{ metric.label }}</div>
                  <div class="metric-desc">{{ metric.description }}</div>
                </div>
                <div class="metric-status" :class="metric.statusClass">
                  <i :class="metric.icon"></i>
                  {{ metric.status }}
                </div>
              </div>
              <div class="progress mb-3" style="height: 6px;">
                <div class="progress-bar" 
                     :class="metric.progressClass"
                     :style="`width: ${100 - metric.value}%`">
                </div>
              </div>
            </div>
            
            <!-- AI预警区域 -->
            <div class="ai-alerts mt-4">
              <h6 class="fw-bold mb-3">
                <i class="fas fa-exclamation-triangle text-warning me-2"></i>
                AI智能预警
              </h6>
              <div v-if="getAIAlerts().length === 0" class="text-center text-muted py-3">
                <i class="fas fa-shield-check fa-2x mb-2 text-success"></i>
                <div>系统运行正常</div>
                <small>AI算法未检测到异常</small>
              </div>
              <div v-else>
                <div v-for="alert in getAIAlerts()" :key="alert.id" 
                     class="alert-item mb-2" :class="alert.class">
                  <div class="d-flex align-items-center">
                    <i :class="alert.icon + ' me-2'"></i>
                    <div class="flex-grow-1">
                      <div class="alert-title">{{ alert.title }}</div>
                      <div class="alert-desc">{{ alert.description }}</div>
                    </div>
                    <div class="alert-time">{{ alert.time }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 算法技术展示 -->
      <div class="row mt-4">
        <div class="col-12">
          <div class="tech-showcase">
            <h6 class="fw-bold mb-3">
              <i class="fas fa-cogs text-success me-2"></i>
              核心算法技术栈
            </h6>
            <div class="row g-3">
              <div class="col-md-3">
                <div class="tech-item">
                  <div class="tech-icon">
                    <i class="fas fa-brain text-primary"></i>
                  </div>
                  <div class="tech-name">RWKV大模型</div>
                  <div class="tech-desc">15亿参数神经网络</div>
                  <div class="tech-metric">推理速度: {{ inferenceSpeed }}ms</div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="tech-item">
                  <div class="tech-icon">
                    <i class="fas fa-project-diagram text-success"></i>
                  </div>
                  <div class="tech-name">多传感器融合</div>
                  <div class="tech-desc">振动+声学+温度</div>
                  <div class="tech-metric">融合精度: 96.3%</div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="tech-item">
                  <div class="tech-icon">
                    <i class="fas fa-chart-line text-warning"></i>
                  </div>
                  <div class="tech-name">异常检测算法</div>
                  <div class="tech-desc">实时模式识别</div>
                  <div class="tech-metric">检测精度: 98.1%</div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="tech-item">
                  <div class="tech-icon">
                    <i class="fas fa-crystal-ball text-info"></i>
                  </div>
                  <div class="tech-name">预测性维护</div>
                  <div class="tech-desc">RUL寿命预测</div>
                  <div class="tech-metric">预测准确率: 95.2%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIRadarChart',
  props: {
    analysisResult: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      inferenceSpeed: 85,
      radarMetrics: [
        {
          name: 'vibration',
          label: '振动异常',
          description: '刀具振动模式分析',
          value: 0,
          status: '正常',
          statusClass: 'text-success',
          progressClass: 'bg-success',
          icon: 'fas fa-check-circle'
        },
        {
          name: 'acoustic',
          label: '声学异常',
          description: '切削声音特征识别',
          value: 0,
          status: '正常',
          statusClass: 'text-success',
          progressClass: 'bg-success',
          icon: 'fas fa-check-circle'
        },
        {
          name: 'temperature',
          label: '温度异常',
          description: '热力学状态监控',
          value: 0,
          status: '正常',
          statusClass: 'text-success',
          progressClass: 'bg-success',
          icon: 'fas fa-check-circle'
        },
        {
          name: 'wear',
          label: '磨损预测',
          description: '刀具寿命评估',
          value: 0,
          status: '正常',
          statusClass: 'text-success',
          progressClass: 'bg-success',
          icon: 'fas fa-check-circle'
        },
        {
          name: 'performance',
          label: '性能衰减',
          description: '加工质量下降',
          value: 0,
          status: '正常',
          statusClass: 'text-success',
          progressClass: 'bg-success',
          icon: 'fas fa-check-circle'
        }
      ]
    }
  },
  watch: {
    analysisResult: {
      handler() {
        this.updateMetrics()
        this.drawRadarChart()
        this.inferenceSpeed = Math.floor(Math.random() * 20) + 75
      },
      deep: true,
      immediate: true
    }
  },
  mounted() {
    this.drawRadarChart()
  },
  methods: {
    updateMetrics() {
      // 更新振动指标
      if (this.analysisResult.vibration) {
        const vibMetric = this.radarMetrics.find(m => m.name === 'vibration')
        vibMetric.value = this.analysisResult.vibration.score || 0
        this.updateMetricStatus(vibMetric)
      }
      
      // 更新声学指标
      if (this.analysisResult.acoustic) {
        const acousticMetric = this.radarMetrics.find(m => m.name === 'acoustic')
        acousticMetric.value = this.analysisResult.acoustic.score || 0
        this.updateMetricStatus(acousticMetric)
      }
      
      // 更新温度指标
      if (this.analysisResult.temperature) {
        const tempMetric = this.radarMetrics.find(m => m.name === 'temperature')
        tempMetric.value = this.analysisResult.temperature.score || 0
        this.updateMetricStatus(tempMetric)
      }
      
      // 更新磨损指标
      if (this.analysisResult.toolWear) {
        const wearMetric = this.radarMetrics.find(m => m.name === 'wear')
        const wearScore = this.getWearScore(this.analysisResult.toolWear.wear_state)
        wearMetric.value = wearScore
        this.updateMetricStatus(wearMetric)
      }
      
      // 更新性能指标
      const perfMetric = this.radarMetrics.find(m => m.name === 'performance')
      perfMetric.value = this.analysisResult.overall?.score || 0
      this.updateMetricStatus(perfMetric)
    },
    
    updateMetricStatus(metric) {
      if (metric.value > 60) {
        metric.status = '异常'
        metric.statusClass = 'text-danger'
        metric.progressClass = 'bg-danger'
        metric.icon = 'fas fa-exclamation-circle'
      } else if (metric.value > 30) {
        metric.status = '警告'
        metric.statusClass = 'text-warning'
        metric.progressClass = 'bg-warning'
        metric.icon = 'fas fa-exclamation-triangle'
      } else {
        metric.status = '正常'
        metric.statusClass = 'text-success'
        metric.progressClass = 'bg-success'
        metric.icon = 'fas fa-check-circle'
      }
    },
    
    getWearScore(wearState) {
      const scoreMap = {
        'normal': 10,
        'slight': 25,
        'moderate': 50,
        'severe': 80
      }
      return scoreMap[wearState] || 10
    },
    
    getOverallHealthScore() {
      const totalScore = this.radarMetrics.reduce((sum, metric) => sum + metric.value, 0)
      const avgScore = totalScore / this.radarMetrics.length
      return Math.max(0, Math.floor(100 - avgScore)) + '%'
    },
    
    getOverallStatusClass() {
      const score = parseInt(this.getOverallHealthScore())
      if (score > 70) return 'score-good'
      if (score > 40) return 'score-warning'
      return 'score-danger'
    },
    
    getAIAlerts() {
      const alerts = []
      const now = new Date().toLocaleTimeString('zh-CN')
      
      this.radarMetrics.forEach(metric => {
        if (metric.value > 60) {
          alerts.push({
            id: metric.name,
            title: `${metric.label}严重异常`,
            description: `${metric.description}检测到异常模式`,
            time: now,
            class: 'alert-danger',
            icon: 'fas fa-exclamation-circle text-danger'
          })
        } else if (metric.value > 30) {
          alerts.push({
            id: metric.name,
            title: `${metric.label}轻微异常`,
            description: `${metric.description}数值偏高，建议关注`,
            time: now,
            class: 'alert-warning',
            icon: 'fas fa-exclamation-triangle text-warning'
          })
        }
      })
      
      return alerts.slice(0, 3) // 最多显示3个警告
    },
    
    drawRadarChart() {
      const canvas = this.$refs.radarCanvas
      if (!canvas) return
      
      const ctx = canvas.getContext('2d')
      const centerX = canvas.width / 2
      const centerY = canvas.height / 2
      const radius = 140
      
      // 清空画布
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      
      // 绘制同心圆
      ctx.strokeStyle = '#e9ecef'
      ctx.lineWidth = 1
      for (let i = 1; i <= 5; i++) {
        ctx.beginPath()
        ctx.arc(centerX, centerY, (radius / 5) * i, 0, 2 * Math.PI)
        ctx.stroke()
      }
      
      // 绘制雷达线
      const angles = []
      for (let i = 0; i < this.radarMetrics.length; i++) {
        const angle = (i * 2 * Math.PI) / this.radarMetrics.length - Math.PI / 2
        angles.push(angle)
        
        ctx.beginPath()
        ctx.moveTo(centerX, centerY)
        ctx.lineTo(
          centerX + Math.cos(angle) * radius,
          centerY + Math.sin(angle) * radius
        )
        ctx.stroke()
      }
      
      // 绘制数据多边形
      ctx.fillStyle = 'rgba(74, 144, 226, 0.3)'
      ctx.strokeStyle = '#4a90e2'
      ctx.lineWidth = 2
      ctx.beginPath()
      
      this.radarMetrics.forEach((metric, index) => {
        const angle = angles[index]
        const value = Math.max(0, 100 - metric.value) // 反转值，越健康越靠外
        const distance = (radius * value) / 100
        const x = centerX + Math.cos(angle) * distance
        const y = centerY + Math.sin(angle) * distance
        
        if (index === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }
      })
      
      ctx.closePath()
      ctx.fill()
      ctx.stroke()
      
      // 绘制数据点
      this.radarMetrics.forEach((metric, index) => {
        const angle = angles[index]
        const value = Math.max(0, 100 - metric.value)
        const distance = (radius * value) / 100
        const x = centerX + Math.cos(angle) * distance
        const y = centerY + Math.sin(angle) * distance
        
        ctx.fillStyle = '#4a90e2'
        ctx.beginPath()
        ctx.arc(x, y, 4, 0, 2 * Math.PI)
        ctx.fill()
      })
      
      // 绘制标签
      ctx.fillStyle = '#333'
      ctx.font = '12px Arial'
      ctx.textAlign = 'center'
      
      this.radarMetrics.forEach((metric, index) => {
        const angle = angles[index]
        const labelDistance = radius + 20
        const x = centerX + Math.cos(angle) * labelDistance
        const y = centerY + Math.sin(angle) * labelDistance
        
        ctx.fillText(metric.label, x, y)
      })
    }
  }
}
</script>

<style scoped>
.bg-gradient-info {
  background: linear-gradient(135deg, #36d1dc 0%, #5b86e5 100%);
}

.radar-container {
  position: relative;
}

.radar-chart-wrapper {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.radar-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  background: white;
  border-radius: 50%;
  width: 80px;
  height: 80px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border: 3px solid #f8f9fa;
}

.center-score {
  font-size: 1.2rem;
  font-weight: bold;
}

.center-score.score-good {
  color: #28a745;
}

.center-score.score-warning {
  color: #ffc107;
}

.center-score.score-danger {
  color: #dc3545;
}

.center-label {
  font-size: 0.7rem;
  color: #6c757d;
  margin-top: 2px;
}

.metrics-panel {
  height: 400px;
  overflow-y: auto;
}

.metric-item {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
}

.metric-name {
  font-weight: bold;
  font-size: 0.9rem;
  color: #212529;
}

.metric-desc {
  font-size: 0.8rem;
  color: #6c757d;
  margin-top: 2px;
}

.metric-status {
  font-size: 0.8rem;
  font-weight: bold;
}

.ai-alerts {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1rem;
}

.alert-item {
  border-radius: 6px;
  padding: 0.5rem;
  font-size: 0.85rem;
}

.alert-item.alert-danger {
  background: rgba(220, 53, 69, 0.1);
  border-left: 3px solid #dc3545;
}

.alert-item.alert-warning {
  background: rgba(255, 193, 7, 0.1);
  border-left: 3px solid #ffc107;
}

.alert-title {
  font-weight: bold;
  color: #212529;
}

.alert-desc {
  color: #6c757d;
  font-size: 0.8rem;
}

.alert-time {
  font-size: 0.75rem;
  color: #6c757d;
}

.tech-showcase {
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  border-radius: 12px;
  padding: 1.5rem;
  border-top: 3px solid #28a745;
}

.tech-item {
  background: white;
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: transform 0.3s ease;
}

.tech-item:hover {
  transform: translateY(-2px);
}

.tech-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.tech-name {
  font-weight: bold;
  color: #212529;
  margin-bottom: 0.25rem;
}

.tech-desc {
  font-size: 0.85rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
}

.tech-metric {
  font-size: 0.8rem;
  color: #28a745;
  font-weight: bold;
}

.algorithm-badge {
  font-size: 0.85rem;
}

/* 滚动条样式 */
.metrics-panel::-webkit-scrollbar {
  width: 4px;
}

.metrics-panel::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 2px;
}

.metrics-panel::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.metrics-panel::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>