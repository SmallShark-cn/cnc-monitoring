<template>
  <div class="row g-3">
    <!-- 声学传感器卡片 -->
    <div class="col-md-4">
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
    <!-- 振动传感器卡片 -->
    <div class="col-md-4">
      <div class="card border-0 h-100 gradbg rounded-big shadow-sm">
        <div class="card-body p-4">
          <div class="d-flex align-items-center mb-4">
            <i class="fas fa-wave-square text-primary me-3 fs-2"></i>
            <div>
              <h6 class="text-muted mb-1">振动传感器</h6>
              <h2 class="text-dark mb-0">{{ formatNumber(latestVibrationData.rms, 3) }}</h2>
              <small class="text-muted">RMS</small>
            </div>
          </div>
          <div class="row g-2 mb-2">
            <div class="col-4">
              <div class="mini-card">
                <div class="mini-title">Peak</div>
                <div class="mini-value">{{ formatNumber(latestVibrationData.peak, 3) }}</div>
              </div>
            </div>
            <div class="col-4">
              <div class="mini-card">
                <div class="mini-title">Kurtosis</div>
                <div class="mini-value">{{ formatNumber(latestVibrationData.kurtosis, 2) }}</div>
              </div>
            </div>
            <div class="col-4">
              <div class="mini-card">
                <div class="mini-title">Skewness</div>
                <div class="mini-value">{{ formatNumber(latestVibrationData.skewness, 2) }}</div>
              </div>
            </div>
          </div>
          <div class="row g-2">
            <div class="col-4">
              <div class="mini-card">
                <div class="mini-title">Std</div>
                <div class="mini-value">{{ formatNumber(latestVibrationData.std, 3) }}</div>
              </div>
            </div>
            <div class="col-4">
              <div class="mini-card text-center" style="opacity:0.3;">
                <div class="mini-title">-</div>
                <div class="mini-value">-</div>
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
    <div class="col-md-4">
      <div class="card border-0 h-100 gradbg rounded-big shadow-sm">
        <div class="card-body p-4">
          <div class="d-flex align-items-center mb-4">
            <i class="fas fa-tools text-warning me-3 fs-2"></i>
            <div>
              <h6 class="text-muted mb-1">刀具磨损状态</h6>
              <h2 class="text-dark mb-0">{{ getWearStateText(latestToolWearData.wear_state) }}</h2>
              <small class="text-muted">状态</small>
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
    }
  },
  computed: {
    latestAcousticData() {
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
        'severe_wear': '严重磨损'
      }
      return stateMap[wearState] || '未知'
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
</style>