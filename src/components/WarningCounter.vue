<template>
    <div class="card bg-white mb-4 border-0 rounded-big shadow-sm gradbg" style="min-height: 385px;">
      <div class="card-body">
        <h5 class="text-dark mb-4">系统状态监控</h5>
        
        <!-- 状态指示器 -->
        <div class="row mb-4">
          <div class="col-6">
            <div class="status-card" :class="getStatusClass(analysisResult.overall?.status)">
              <div class="status-label">系统状态</div>
              <div class="status-value">{{ analysisResult.overall?.status || '正常' }}</div>
            </div>
          </div>
          <div class="col-6">
            <div class="status-card" :class="getTemperatureClass(analysisResult.overall?.temperatureStatus)">
              <div class="status-label">温度状态</div>
              <div class="status-value">{{ analysisResult.overall?.temperatureStatus || '正常' }}</div>
            </div>
          </div>
        </div>

        <!-- 告警信息 -->
        <h6 class="text-dark mb-3">实时告警</h6>
        <div class="alerts-container">
          <div v-if="analysisResult.alerts && analysisResult.alerts.length > 0">
            <div v-for="(alert, idx) in analysisResult.alerts" :key="idx" 
                 class="alert-item mb-2 p-2 rounded" 
                 :class="getAlertClass(alert.type)">
              <div class="d-flex justify-content-between align-items-center">
                <div class="fw-bold">{{ alert.type }}</div>
                <div class="small">{{ alert.time }}</div>
              </div>
              <div class="alert-message mt-1">{{ alert.message }}</div>
            </div>
          </div>
          <div v-else class="text-center text-muted py-3">
            <i class="fas fa-check-circle fa-2x mb-2 text-success"></i>
            <div>系统运行正常，暂无告警</div>
          </div>
        </div>

        <!-- 综合评分 -->
        <div class="mt-4">
          <h6 class="text-dark mb-2">综合评分</h6>
          <div class="progress mb-2" style="height: 8px;">
            <div class="progress-bar" 
                 :class="getScoreBarClass(analysisResult.overall?.score)" 
                 :style="`width: ${analysisResult.overall?.score || 0}%`">
            </div>
          </div>
          <small class="text-muted">
            当前评分: {{ (analysisResult.overall?.score || 0).toFixed(1) }}/100
          </small>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'WarningCounter',
    props: {
      analysisResult: {
        type: Object,
        default: () => ({})
      }
    },
    methods: {
      getStatusClass(status) {
        switch(status) {
          case '异常': return 'status-error'
          case '正常': return 'status-normal'
          default: return 'status-normal'
        }
      },
      getTemperatureClass(tempStatus) {
        switch(tempStatus) {
          case '高温': return 'status-error'
          case '正常': return 'status-normal'
          default: return 'status-normal'
        }
      },
      getAlertClass(type) {
        switch(type) {
          case '温度': return 'alert-temperature'
          case '振动': return 'alert-vibration'
          case '声学': return 'alert-acoustic'
          case '系统': return 'alert-system'
          default: return 'alert-default'
        }
      },
      getScoreBarClass(score) {
        if (score > 60) return 'bg-danger'
        if (score > 30) return 'bg-warning'
        return 'bg-success'
      }
    }
  }
  </script>
  
  <style scoped>
  .card.rounded-big{
    border-radius: 2rem !important;
  }

  .card.gradbg {
    background: linear-gradient(180deg, #ffffff, #ffffff);
    transition: all 0.3s ease;
    border: 1px solid rgba(0,0,0,0.05);
  }

  .card.gradbg:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.1) !important;
  }

  /* 状态卡片样式 */
  .status-card {
    padding: 1rem;
    border-radius: 0.5rem;
    text-align: center;
    transition: all 0.3s ease;
  }

  .status-card.status-normal {
    background: linear-gradient(135deg, #28a745, #20c997);
    color: white;
  }

  .status-card.status-error {
    background: linear-gradient(135deg, #dc3545, #fd7e14);
    color: white;
  }

  .status-label {
    font-size: 0.85rem;
    opacity: 0.9;
    margin-bottom: 0.25rem;
  }

  .status-value {
    font-size: 1.1rem;
    font-weight: bold;
  }

  /* 告警项样式 */
  .alerts-container {
    max-height: 200px;
    overflow-y: auto;
  }

  .alert-item {
    border-left: 4px solid;
    color: white;
  }

  .alert-temperature {
    background: rgba(220, 53, 69, 0.9);
    border-left-color: #dc3545;
  }

  .alert-vibration {
    background: rgba(255, 193, 7, 0.9);
    border-left-color: #ffc107;
    color: #212529;
  }

  .alert-acoustic {
    background: rgba(13, 202, 240, 0.9);
    border-left-color: #0dcaf0;
    color: #212529;
  }

  .alert-system {
    background: rgba(108, 117, 125, 0.9);
    border-left-color: #6c757d;
  }

  .alert-default {
    background: rgba(221, 52, 52, 0.9);
    border-left-color: #dd3434;
  }

  .alert-message {
    font-size: 0.9rem;
    opacity: 0.95;
  }

  /* 进度条动画 */
  .progress-bar {
    transition: width 0.6s ease;
  }

  /* 滚动条样式 */
  .alerts-container::-webkit-scrollbar {
    width: 4px;
  }

  .alerts-container::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 2px;
  }

  .alerts-container::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 2px;
  }

  .alerts-container::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
  }
  </style>
  