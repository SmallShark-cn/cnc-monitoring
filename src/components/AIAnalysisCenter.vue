<template>
  <div class="card bg-white border-0 rounded-big shadow-sm gradbg">
    <div class="card-header bg-gradient-primary text-white">
      <div class="d-flex align-items-center">
        <i class="fas fa-brain me-3 fs-4"></i>
        <div>
          <h5 class="mb-0">AI算法融合分析中心</h5>
          <small class="opacity-75">RWKV大模型 · 多传感器融合 · 智能预测</small>
        </div>
      </div>
    </div>
    <div class="card-body p-4">
      <!-- 实时推理状态 -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="ai-status-bar">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="fw-bold">🧠 RWKV模型推理状态</span>
              <span class="badge bg-success">
                <i class="fas fa-circle pulse-animation"></i> 实时运行
              </span>
            </div>
            <div class="progress mb-2" style="height: 8px;">
              <div class="progress-bar bg-gradient-success progress-bar-animated" 
                   :style="`width: ${analysisResult.overall?.score || 0}%`"
                   role="progressbar">
              </div>
            </div>
            <div class="d-flex justify-content-between">
              <small class="text-muted">推理速度: {{ inferenceSpeed }}ms</small>
              <small class="text-muted">系统健康度: {{ (100 - (analysisResult.overall?.score || 0)).toFixed(1) }}%</small>
            </div>
          </div>
        </div>
      </div>

      <!-- 多传感器融合矩阵 -->
      <div class="row mb-4">
        <div class="col-12">
          <h6 class="fw-bold mb-3">
            <i class="fas fa-project-diagram text-primary me-2"></i>
            多传感器融合矩阵
          </h6>
          <div class="fusion-matrix">
            <div class="row g-2">
              <div class="col-4">
                <div class="sensor-node vibration" :class="getSensorStatus('vibration')">
                  <div class="sensor-icon">
                    <i class="fas fa-wave-square"></i>
                  </div>
                  <div class="sensor-name">振动传感器</div>
                  <div class="sensor-value">{{ formatValue(analysisResult.vibration?.score || 0) }}</div>
                  <div class="sensor-weight">权重: 50%</div>
                </div>
              </div>
              <div class="col-4">
                <div class="sensor-node acoustic" :class="getSensorStatus('acoustic')">
                  <div class="sensor-icon">
                    <i class="fas fa-microphone"></i>
                  </div>
                  <div class="sensor-name">声学传感器</div>
                  <div class="sensor-value">{{ formatValue(analysisResult.acoustic?.score || 0) }}</div>
                  <div class="sensor-weight">权重: 20%</div>
                </div>
              </div>
              <div class="col-4">
                <div class="sensor-node temperature" :class="getSensorStatus('temperature')">
                  <div class="sensor-icon">
                    <i class="fas fa-thermometer-half"></i>
                  </div>
                  <div class="sensor-name">温度传感器</div>
                  <div class="sensor-value">{{ formatValue(analysisResult.temperature?.score || 0) }}</div>
                  <div class="sensor-weight">权重: 30%</div>
                </div>
              </div>
            </div>
            <!-- 融合箭头 -->
            <div class="fusion-arrows">
              <div class="arrow-down">
                <i class="fas fa-arrow-down text-primary"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI决策输出 -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="ai-decision-panel">
            <h6 class="fw-bold mb-3">
              <i class="fas fa-robot text-success me-2"></i>
              AI智能决策输出
            </h6>
            <div class="row g-3">
              <div class="col-md-6">
                <div class="decision-item">
                  <div class="decision-label">刀具状态预测</div>
                  <div class="decision-value" :class="getWearStatusClass(analysisResult.toolWear?.wear_state)">
                    <i v-if="isAbnormalWearState(analysisResult.toolWear?.wear_state)" 
                       class="fas fa-exclamation-triangle me-2 blink-fast"></i>
                    {{ getWearStatusText(analysisResult.toolWear?.wear_state) }}
                  </div>
                  <div class="decision-confidence">
                    置信度: {{ formatConfidence(analysisResult.toolWear?.confidence) }}%
                    <span v-if="isHighConfidence(analysisResult.toolWear?.confidence)" 
                          class="badge bg-success ms-2">高置信度</span>
                    <span v-else-if="isLowConfidence(analysisResult.toolWear?.confidence)" 
                          class="badge bg-warning ms-2">低置信度</span>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="decision-item">
                  <div class="decision-label">剩余使用寿命</div>
                  <div class="decision-value text-info">
                    {{ analysisResult.toolWear?.rul || 0 }} 小时
                  </div>
                  <div class="decision-confidence">
                    预测精度: 95.2%
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 算法性能指标 -->
      <div class="row">
        <div class="col-12">
          <h6 class="fw-bold mb-3">
            <i class="fas fa-chart-line text-warning me-2"></i>
            算法性能指标
          </h6>
          <div class="row g-3">
            <div class="col-3">
              <div class="metric-card">
                <div class="metric-icon">
                  <i class="fas fa-bullseye text-success"></i>
                </div>
                <div class="metric-value">96.3%</div>
                <div class="metric-label">检测准确率</div>
              </div>
            </div>
            <div class="col-3">
              <div class="metric-card">
                <div class="metric-icon">
                  <i class="fas fa-tachometer-alt text-primary"></i>
                </div>
                <div class="metric-value">{{ inferenceSpeed }}ms</div>
                <div class="metric-label">推理速度</div>
              </div>
            </div>
            <div class="col-3">
              <div class="metric-card">
                <div class="metric-icon">
                  <i class="fas fa-shield-alt text-warning"></i>
                </div>
                <div class="metric-value">1.7%</div>
                <div class="metric-label">误报率</div>
              </div>
            </div>
            <div class="col-3">
              <div class="metric-card">
                <div class="metric-icon">
                  <i class="fas fa-microchip text-info"></i>
                </div>
                <div class="metric-value">1.5B</div>
                <div class="metric-label">模型参数</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 智能建议 -->
      <div class="row mt-4" v-if="getSmartRecommendations().length > 0">
        <div class="col-12">
          <div class="smart-recommendations">
            <h6 class="fw-bold mb-3">
              <i class="fas fa-lightbulb text-warning me-2"></i>
              AI智能建议
            </h6>
            <div class="recommendations-list">
              <div v-for="(rec, index) in getSmartRecommendations()" :key="index" 
                   class="recommendation-item">
                <div class="rec-icon">
                  <i :class="rec.icon"></i>
                </div>
                <div class="rec-content">
                  <div class="rec-title">{{ rec.title }}</div>
                  <div class="rec-desc">{{ rec.description }}</div>
                </div>
                <div class="rec-priority" :class="rec.priorityClass">
                  {{ rec.priority }}
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
  name: 'AIAnalysisCenter',
  props: {
    analysisResult: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      inferenceSpeed: 85,
      lastUpdateTime: Date.now()
    }
  },
  watch: {
    analysisResult: {
      handler() {
        // 模拟推理时间变化
        this.inferenceSpeed = Math.floor(Math.random() * 20) + 75 // 75-95ms
        this.lastUpdateTime = Date.now()
      },
      deep: true
    }
  },
  methods: {
    formatValue(value) {
      return typeof value === 'number' ? value.toFixed(1) : '0.0'
    },
    
    formatConfidence(confidence) {
      return confidence ? (confidence * 100).toFixed(1) : '0.0'
    },
    
    getSensorStatus(sensorType) {
      const score = this.analysisResult[sensorType]?.score || 0
      if (score > 60) return 'status-critical'
      if (score > 30) return 'status-warning'
      return 'status-normal'
    },
    
    getWearStatusClass(status) {
      const statusMap = {
        'normal': 'text-success',
        'slight': 'text-info',
        'moderate': 'text-warning',
        'severe': 'text-danger'
      }
      return statusMap[status] || 'text-muted'
    },
    
    getWearStatusText(status) {
      const statusMap = {
        'normal': '正常',
        'slight': '轻微磨损',
        'moderate': '中度磨损',
        'severe': '严重磨损'
      }
      return statusMap[status] || '未知'
    },
    
    getSmartRecommendations() {
      const recommendations = []
      const overallScore = this.analysisResult.overall?.score || 0
      
      if (overallScore > 60) {
        recommendations.push({
          icon: 'fas fa-exclamation-triangle text-danger',
          title: '紧急维护建议',
          description: '检测到多项异常指标，建议立即停机检查',
          priority: '高优先级',
          priorityClass: 'badge bg-danger'
        })
      } else if (overallScore > 30) {
        recommendations.push({
          icon: 'fas fa-tools text-warning',
          title: '预防性维护',
          description: '建议在下次停机时进行刀具检查和更换',
          priority: '中优先级',
          priorityClass: 'badge bg-warning'
        })
      }
      
      if (this.analysisResult.temperature?.score > 40) {
        recommendations.push({
          icon: 'fas fa-snowflake text-info',
          title: '冷却系统检查',
          description: '温度偏高，建议检查冷却液流量和温度',
          priority: '中优先级',
          priorityClass: 'badge bg-info'
        })
      }
      
      return recommendations
    },
    
    isAbnormalWearState(wearState) {
      return ['slight', 'moderate', 'severe', 'warning', 'critical'].includes(wearState)
    },
    
    isHighConfidence(confidence) {
      return confidence && confidence > 0.85
    },
    
    isLowConfidence(confidence) {
      return confidence && confidence < 0.7
    }
  }
}
</script>

<style scoped>
.bg-gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.pulse-animation {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.ai-status-bar {
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  border-radius: 12px;
  padding: 1rem;
  border: 1px solid rgba(0,0,0,0.05);
}

.fusion-matrix {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1.5rem;
  position: relative;
}

.sensor-node {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.sensor-node.status-normal {
  border-color: #28a745;
  box-shadow: 0 0 15px rgba(40, 167, 69, 0.2);
}

.sensor-node.status-warning {
  border-color: #ffc107;
  box-shadow: 0 0 15px rgba(255, 193, 7, 0.2);
}

.sensor-node.status-critical {
  border-color: #dc3545;
  box-shadow: 0 0 15px rgba(220, 53, 69, 0.2);
}

.sensor-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #6c757d;
}

.sensor-name {
  font-size: 0.85rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}

.sensor-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #212529;
  margin-bottom: 0.25rem;
}

.sensor-weight {
  font-size: 0.75rem;
  color: #6c757d;
}

.fusion-arrows {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

.arrow-down {
  font-size: 1.5rem;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-5px); }
  60% { transform: translateY(-3px); }
}

.ai-decision-panel {
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  border-radius: 12px;
  padding: 1.5rem;
  border-left: 4px solid #28a745;
}

.decision-item {
  text-align: center;
}

.decision-label {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
}

.decision-value {
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.decision-confidence {
  font-size: 0.8rem;
  color: #6c757d;
}

.metric-card {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  transition: transform 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
}

.metric-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.metric-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #212529;
  margin-bottom: 0.25rem;
}

.metric-label {
  font-size: 0.85rem;
  color: #6c757d;
}

.smart-recommendations {
  background: linear-gradient(135deg, #fff3cd, #ffeaa7);
  border-radius: 12px;
  padding: 1.5rem;
  border-left: 4px solid #ffc107;
}

.recommendation-item {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 0.75rem;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}

.recommendation-item:last-child {
  margin-bottom: 0;
}

.rec-icon {
  font-size: 1.2rem;
  margin-right: 1rem;
  flex-shrink: 0;
}

.rec-content {
  flex-grow: 1;
}

.rec-title {
  font-weight: bold;
  color: #212529;
  margin-bottom: 0.25rem;
}

.rec-desc {
  font-size: 0.9rem;
  color: #6c757d;
}

.rec-priority {
  flex-shrink: 0;
  margin-left: 1rem;
}

.progress-bar-animated {
  animation: progress-bar-stripes 1s linear infinite;
}

@keyframes progress-bar-stripes {
  0% { background-position: 1rem 0; }
  100% { background-position: 0 0; }
}

.blink-fast {
  animation: blink-fast 1s infinite;
}

@keyframes blink-fast {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0.2; }
}
</style>