<template>
  <div class="d-flex min-vh-100" style="background-color: #ffffff; margin: 0; padding: 0;">
    <!-- 侧边栏 -->
    <Sidebar />
    
    <!-- 主内容 -->
    <div class="flex-grow-1 p-4 w-100" style="margin: 0; background-color: rgb(235, 243, 248);">
      <DashboardHeader :tableData="performanceData" @refresh="fetchAllData" />
      
      <!-- 统计卡片区域 -->
      <div class="row mb-4">
        <div class="col-12">
          <StatsCards 
            :acousticHistory="acousticHistory"
            :vibrationHistory="vibrationHistory"
            :toolWearHistory="toolWearHistory"
          />
        </div>
      </div>
      
      <!-- 性能趋势和告警区域 -->
      <div class="row mb-2 d-flex align-items-stretch">
        <div class="col-lg-8 d-flex align-items-stretch">
          <div class="card bg-white border-0 mb-2 rounded-big shadow-sm gradbg h-100 w-100">
            <div class="card-body p-3" style="padding-bottom: 0.5rem !important;">
              <h5 class="text-dark mb-3" style="margin-bottom: 0.75rem !important;">震动数据</h5>
              <div style="min-height:220px;">
                <VibrationTrendChart :rmsHistory="rmsHistory" />
        </div>
      </div>
          </div>
        </div>
        <div class="col-lg-4 d-flex align-items-stretch">
          <div class="h-100 w-100">
            <WarningCounter />
          </div>
        </div>
      </div>
      <!-- 主要内容区域 -->
      <div class="row mb-4">
        <div class="col-12">
          <PerformanceChart />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue'
import DashboardHeader from '@/components/DashboardHeader.vue'
import PerformanceChart from '@/components/PerformanceChart.vue'
import StatsCards from '@/components/StatsCards.vue'
import WarningCounter from '@/components/WarningCounter.vue'
import VibrationTrendChart from '@/components/VibrationTrendChart.vue'

export default {
  name: 'Dashboard',
  components: {
    Sidebar,
    DashboardHeader,
    PerformanceChart,
    StatsCards,
    WarningCounter,
    VibrationTrendChart
  },
  data() {
    return {
      rmsHistory: [],
      acousticHistory: [],
      vibrationHistory: [],
      toolWearHistory: [],
      performanceData: [],
      // WebSocket对象
      wsVibrationStatistics: null,
      wsAcousticStatistics: null,
      wsToolWear: null,
      wsPerformance: null
    }
  },
  mounted() {
    this.initAllWebSockets()
  },
  beforeUnmount() {
    this.closeAllWebSockets()
  },
  methods: {
    initAllWebSockets() {
      // 振动统计
      this.wsVibrationStatistics = new WebSocket('ws://localhost:8000/ws/vibration/statistics')
      this.wsVibrationStatistics.onmessage = (e) => {
        try {
          const msg = JSON.parse(e.data)
          if (msg && Object.keys(msg).length > 0) {
            this.rmsHistory.unshift(msg)
            if (this.rmsHistory.length > 30) this.rmsHistory.pop()
            this.vibrationHistory = this.rmsHistory // 保证StatsCards能拿到数据
          }
        } catch (err) { }
      }
      // 声学统计
      this.wsAcousticStatistics = new WebSocket('ws://localhost:8000/ws/acoustic/statistics')
      this.wsAcousticStatistics.onmessage = (e) => {
        try {
          const msg = JSON.parse(e.data)
          if (msg && Object.keys(msg).length > 0) {
            this.acousticHistory.unshift(msg)
            if (this.acousticHistory.length > 30) this.acousticHistory.pop()
          }
        } catch (err) { }
      }
      // 刀具磨损
      this.wsToolWear = new WebSocket('ws://localhost:8000/ws/tool-wear')
      this.wsToolWear.onmessage = (e) => {
        try {
          const msg = JSON.parse(e.data)
          if (msg && Object.keys(msg).length > 0) {
            this.toolWearHistory.unshift(msg)
            if (this.toolWearHistory.length > 30) this.toolWearHistory.pop()
          }
        } catch (err) { }
      }
      // 性能数据（如有WebSocket端点，可加，否则保留原有API）
      // this.wsPerformance = new WebSocket('ws://localhost:8000/ws/performance')
      // this.wsPerformance.onmessage = (e) => {
      //   try {
      //     const msg = JSON.parse(e.data)
      //     this.performanceData = msg.data || []
      //   } catch (err) { }
      // }
    },
    closeAllWebSockets() {
      [
        this.wsVibrationStatistics,
        this.wsAcousticStatistics,
        this.wsToolWear,
        this.wsPerformance
      ].forEach(ws => { if (ws) ws.close() })
    }
  }
}
</script>

<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

html, body, #app {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  max-width: none;
  max-height: none;
}

.container-fluid {
  padding-left: 0 !important;
  padding-right: 0 !important;
}

.gap-2 {
  gap: 0.5rem;
}

.cursor-pointer {
  cursor: pointer;
}

.bg-opacity-20 {
  background-color: rgba(255, 0, 43, 0.3) !important;
}

.text-muted {
  color: #6c757d !important;
}
/* 鼠标悬浮效果 */
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