<template>
  <div class="row g-3">
    <!-- 声学传感器卡片 -->
    <div class="col-md-6">
      <div class="card border-0 h-100 gradbg rounded-big shadow-sm">
        <div class="card-body p-4">
          <div class="d-flex align-items-center mb-4">
            <i class="fas fa-microphone text-success me-3 fs-2"></i>
            <div>
              <h6 class="text-muted mb-1">声学传感器</h6>
              <h2 class="text-dark mb-0">{{ formatNumber(latestAcousticData.spl, 1) }}</h2>
              <small class="text-muted">SPL</small>
            </div>
          </div>
          <div class="row g-2 mb-2">
            <div class="col-4">
              <div class="mini-card">
                <div class="mini-title">RMS</div>
                <div class="mini-value">{{ formatNumber(latestAcousticData.rms, 3) }}</div>
              </div>
            </div>
            <div class="col-4">
              <div class="mini-card">
                <div class="mini-title">Peak</div>
                <div class="mini-value">{{ formatNumber(latestAcousticData.peak, 3) }}</div>
              </div>
            </div>
            <div class="col-4">
              <div class="mini-card">
                <div class="mini-title">Kurtosis</div>
                <div class="mini-value">{{ formatNumber(latestAcousticData.kurtosis, 2) }}</div>
              </div>
            </div>
          </div>
          <div class="row g-2">
            <div class="col-4">
              <div class="mini-card">
                <div class="mini-title">Skewness</div>
                <div class="mini-value">{{ formatNumber(latestAcousticData.skewness, 2) }}</div>
              </div>
            </div>
            <div class="col-4">
              <div class="mini-card">
                <div class="mini-title">Std</div>
                <div class="mini-value">{{ formatNumber(latestAcousticData.std, 3) }}</div>
              </div>
            </div>
            <div class="col-4">
              <div class="mini-card text-center" style="opacity:0.3;">
                <div class="mini-title">-</div>
                <div class="mini-value">-</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- 刀具磨损卡片 -->
    <div class="col-md-6">
      <div class="card border-0 h-100 gradbg rounded-big shadow-sm" :class="getWearStateCardClass(latestToolWearData.wear_state)">
        <div class="card-body p-4">
          <div class="d-flex align-items-center mb-4">
            <i class="fas fa-tools me-3 fs-2" :class="getWearStateIconClass(latestToolWearData.wear_state)"></i>
            <div>
              <h6 class="text-muted mb-1">刀具磨损状态</h6>
              <h2 class="mb-0" :class="getWearStateTextClass(latestToolWearData.wear_state)">
                {{ getWearStateText(latestToolWearData.wear_state) }}
                <i v-if="isAbnormalState(latestToolWearData.wear_state)" class="fas fa-exclamation-triangle ms-2 blink-animation"></i>
              </h2>
              <small class="text-muted">{{ getWearStateDescription(latestToolWearData.wear_state) }}</small>
            </div>
          </div>
          <div class="row g-2 mb-2">
            <div class="col-6">
              <div class="mini-card">
                <div class="mini-title">置信度</div>
                <div class="mini-value">{{ formatNumber(latestToolWearData.confidence * 100, 1) }}%</div>
              </div>
            </div>
            <div class="col-6">
              <div class="mini-card">
                <div class="mini-title">剩余寿命</div>
                <div class="mini-value">{{ latestToolWearData.rul }}h</div>
              </div>
            </div>
          </div>
          <div class="row g-2">
            <div class="col-6">
              <div class="mini-card">
                <div class="mini-title">振动贡献</div>
                <div class="mini-value">{{ formatNumber(latestToolWearData.contributions.vibration * 100, 1) }}%</div>
              </div>
            </div>
            <div class="col-6">
              <div class="mini-card">
                <div class="mini-title">声学贡献</div>
                <div class="mini-value">{{ formatNumber(latestToolWearData.contributions.acoustic * 100, 1) }}%</div>
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
  name: 'StatsCards',
  props: {
    acousticHistory: {
      type: Array,
      default: () => []
    },
    vibrationHistory: {
      type: Array,
      default: () => []
    },
    toolWearHistory: {
      type: Array,
      default: () => []
    },
    microphoneData: {
      type: Object,
      default: () => null
    },
    useMicrophone: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    latestAcousticData() {
      if (this.useMicrophone && this.microphoneData) {
        return {
          timestamp: new Date().toISOString(),
          rms: this.microphoneData.rms || 0,
          peak: this.microphoneData.peak || 0,
          kurtosis: this.microphoneData.kurtosis || 0,
          skewness: this.microphoneData.skewness || 0,
          std: this.microphoneData.std || 0,
          spl: this.microphoneData.spl || 0
        }
      }
      if (this.acousticHistory.length > 0) {
        return this.acousticHistory[0]
      }
      return {
        timestamp: '',
        rms: 0,
        peak: 0,
        kurtosis: 0,
        skewness: 0,
        std: 0,
        spl: 0
      }
    },
    latestVibrationData() {
      if (this.vibrationHistory.length > 0) {
        return this.vibrationHistory[0]
      }
      return {
        timestamp: '',
        rms: 0,
        peak: 0,
        kurtosis: 0,
        skewness: 0,
        std: 0
      }
    },
    latestToolWearData() {
      if (this.toolWearHistory.length > 0) {
        return this.toolWearHistory[0]
      }
      return {
        timestamp: '',
        wear_state: 'normal',
        confidence: 0,
        rul: 0,
        contributions: { vibration: 0, acoustic: 0 }
      }
    }
  },
  methods: {
    formatNumber(num, decimals = 0) {
      if (typeof num !== 'number') return '0'
      return num.toLocaleString('zh-CN', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
      })
    },
    getWearStateText(wearState) {
      const stateMap = {
        'normal': '正常',
        'warning': '警告',
        'critical': '严重',
        'mild_wear': '轻微磨损',
        'moderate_wear': '中度磨损',
        'severe_wear': '严重磨损',
        'slight': '轻微磨损',
        'moderate': '中度磨损',
        'severe': '严重磨损'
      }
      return stateMap[wearState] || '未知'
    },
    
    getWearStateTextClass(wearState) {
      const classMap = {
        'normal': 'text-success',
        'slight': 'text-warning',
        'moderate': 'text-warning',
        'severe': 'text-danger',
        'warning': 'text-warning',
        'critical': 'text-danger'
      }
      return classMap[wearState] || 'text-dark'
    },
    
    getWearStateIconClass(wearState) {
      const classMap = {
        'normal': 'text-success',
        'slight': 'text-warning pulse-slow',
        'moderate': 'text-warning pulse-medium',
        'severe': 'text-danger pulse-fast shake-animation',
        'warning': 'text-warning pulse-slow',
        'critical': 'text-danger pulse-fast shake-animation'
      }
      return classMap[wearState] || 'text-warning'
    },
    
    getWearStateCardClass(wearState) {
      const classMap = {
        'normal': 'normal-state',
        'slight': 'warning-state',
        'moderate': 'warning-state',
        'severe': 'critical-state',
        'warning': 'warning-state',
        'critical': 'critical-state'
      }
      return classMap[wearState] || ''
    },
    
    getWearStateDescription(wearState) {
      const descMap = {
        'normal': '设备运行正常',
        'slight': '需要关注',
        'moderate': '建议检查',
        'severe': '立即维护',
        'warning': '需要关注',
        'critical': '立即维护'
      }
      return descMap[wearState] || '状态'
    },
    
    isAbnormalState(wearState) {
      return ['slight', 'moderate', 'severe', 'warning', 'critical'].includes(wearState)
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
.mini-card {
  background: #f6f8fa;
  border-radius: 0.75rem;
  padding: 0.5rem 0.25rem;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}
.mini-title {
  font-size: 0.85rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}
.mini-value {
  font-size: 1.15rem;
  font-weight: 600;
  color: #1f2937;
}

/* 异常状态卡片样式 */
.normal-state {
  border-left: 4px solid #28a745;
}

.warning-state {
  border-left: 4px solid #ffc107;
  background: linear-gradient(135deg, #fff3cd, #ffffff);
}

.critical-state {
  border-left: 4px solid #dc3545;
  background: linear-gradient(135deg, #f8d7da, #ffffff);
  box-shadow: 0 0 15px rgba(220, 53, 69, 0.2) !important;
}

/* 动画效果 */
.blink-animation {
  animation: blink 1.5s infinite;
}

.pulse-slow {
  animation: pulse 3s infinite;
}

.pulse-medium {
  animation: pulse 2s infinite;
}

.pulse-fast {
  animation: pulse 1s infinite;
}

.shake-animation {
  animation: shake 0.8s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0.3; }
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.7;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-2px); }
  20%, 40%, 60%, 80% { transform: translateX(2px); }
}

/* 异常状态时的特殊效果 */
.warning-state:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 193, 7, 0.3) !important;
}

.critical-state:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(220, 53, 69, 0.4) !important;
}
</style>