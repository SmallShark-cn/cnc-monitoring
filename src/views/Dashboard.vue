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
            :microphoneData="microphoneData"
            :useMicrophone="useMicrophone"
          />
        </div>
      </div>

      <!-- 隐藏的麦克风音频分析器 -->
      <MicrophoneAudioAnalyzer 
        v-show="false" 
        @audioData="onAudioData" 
        :autoStart="true"
        :updateInterval="1000"
      />
      
      <!-- 震动数据图表 -->
      <div class="row mb-3">
        <div class="col-12">
          <div class="card bg-white border-0 rounded-big shadow-sm gradbg">
            <div class="card-body p-3" style="padding-bottom: 0.5rem !important;">
              <h5 class="text-dark mb-3" style="margin-bottom: 0.75rem !important;">震动数据</h5>
              <div style="min-height:280px;">
                <VibrationTrendChart :rmsHistory="rmsHistory" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 声学数据图表 -->
      <div class="row mb-3">
        <div class="col-12">
          <div class="card bg-white border-0 rounded-big shadow-sm gradbg">
            <div class="card-body p-3" style="padding-bottom: 0.5rem !important;">
              <h5 class="text-dark mb-3" style="margin-bottom: 0.75rem !important;">声学数据</h5>
              <div style="min-height:280px;">
                <AcousticTrendChart :microphoneHistory="microphoneHistory" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 告警信息区域 -->
      <div class="row mb-3">
        <div class="col-12">
          <WarningCounter :analysisResult="analysisResult" />
        </div>
      </div>
      
      <!-- 测试控制面板（开发调试用） -->
      <div class="row mb-3" v-if="showTestPanel">
        <div class="col-12">
          <div class="card bg-light border-0 rounded-big shadow-sm">
            <div class="card-body p-3">
              <h6 class="text-muted mb-3">
                <i class="fas fa-flask me-2"></i>异常状态测试面板
              </h6>
              <div class="row g-2">
                <div class="col-auto">
                  <button class="btn btn-success btn-sm" @click="simulateNormalState">
                    <i class="fas fa-check me-1"></i>正常状态
                  </button>
                </div>
                <div class="col-auto">
                  <button class="btn btn-warning btn-sm" @click="simulateWarningState">
                    <i class="fas fa-exclamation-triangle me-1"></i>警告状态
                  </button>
                </div>
                <div class="col-auto">
                  <button class="btn btn-danger btn-sm" @click="simulateCriticalState">
                    <i class="fas fa-times-circle me-1"></i>严重异常
                  </button>
                </div>
                <div class="col-auto">
                  <button class="btn btn-secondary btn-sm" @click="toggleTestPanel">
                    <i class="fas fa-eye-slash me-1"></i>隐藏面板
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- AI算法融合分析中心 -->
      <div class="row mb-4">
        <div class="col-12">
          <AIAnalysisCenter :analysisResult="analysisResult" />
        </div>
      </div>
      
      <!-- AI智能异常检测雷达 -->
      <div class="row mb-4">
        <div class="col-12">
          <AIRadarChart :analysisResult="analysisResult" />
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
import AcousticTrendChart from '@/components/AcousticTrendChart.vue'
import AIAnalysisCenter from '@/components/AIAnalysisCenter.vue'
import AIRadarChart from '@/components/AIRadarChart.vue'
import MicrophoneAudioAnalyzer from '@/components/MicrophoneAudioAnalyzer.vue'
import CNCAnalysisAlgorithm from '@/utils/cncAnalysisAlgorithm.js'

export default {
  name: 'Dashboard',
  components: {
    Sidebar,
    DashboardHeader,
    PerformanceChart,
    StatsCards,
    WarningCounter,
    VibrationTrendChart,
    AcousticTrendChart,
    AIAnalysisCenter,
    AIRadarChart,
    MicrophoneAudioAnalyzer
  },
  data() {
    return {
      rmsHistory: [],
      acousticHistory: [],
      vibrationHistory: [],
      toolWearHistory: [],
      performanceData: [],
      // 麦克风相关数据
      useMicrophone: true,
      microphoneData: null,
      microphoneHistory: [], // 新增：存储麦克风历史数据
      // 分析结果
      analysisResult: {},
      cncAnalyzer: null,
      // 测试面板
      showTestPanel: true, // 设为true以便演示
      // WebSocket对象
      wsVibrationStatistics: null,
      wsAcousticStatistics: null,
      wsToolWear: null,
      wsPerformance: null
    }
  },
  mounted() {
    this.cncAnalyzer = new CNCAnalysisAlgorithm()
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
            
            // 执行算法分析
            this.performAnalysis()
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
            
            // 执行算法分析
            this.performAnalysis()
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
    },
    onAudioData(audioData) {
      this.microphoneData = audioData
      // 将麦克风数据添加到历史记录中，用于图表显示
      if (audioData && audioData.spl !== undefined) {
        // 添加时间戳
        const dataPoint = {
          ...audioData,
          timestamp: new Date().toISOString()
        }
        
        // 添加到历史数据中
        this.microphoneHistory.push(dataPoint)
        
        // 限制历史数据长度，保持最新30个数据点
        if (this.microphoneHistory.length > 30) {
          this.microphoneHistory.shift()
        }
        
        // 执行算法分析
        this.performAnalysis()
      }
    },
    fetchAllData() {
      // 现有的数据获取逻辑
    },
    
    performAnalysis() {
      if (!this.cncAnalyzer) return

      // 获取最新的传感器数据
      const latestVibration = this.vibrationHistory.length > 0 ? this.vibrationHistory[0] : null
      const latestAcoustic = this.acousticHistory.length > 0 ? this.acousticHistory[0] : null
      const latestMicrophone = this.microphoneData
      
      // 提取温度数据（从振动传感器数据或其他来源）
      let temperature = null
      if (latestVibration && latestVibration.temperature !== undefined) {
        temperature = latestVibration.temperature
      }

      // 合并声学数据（后端数据 + 麦克风数据）
      const mergedAcousticData = {
        ...latestAcoustic,
        ...latestMicrophone
      }

      // 执行综合分析
      this.analysisResult = this.cncAnalyzer.comprehensiveAnalysis(
        latestVibration,
        temperature,
        mergedAcousticData
      )

      console.log('Analysis Result:', this.analysisResult)
    },

    // 测试控制方法
    toggleTestPanel() {
      this.showTestPanel = !this.showTestPanel
    },

    simulateNormalState() {
      // 模拟正常状态数据
      const mockVibrationData = {
        rms: 0.2,
        peak: 0.5,
        kurtosis: 3.0,
        skewness: 0.1,
        std: 0.05
      }
      const mockTemperature = 21.5
      const mockAcousticData = {
        rms: 0.25,
        spl: 65,
        kurtosis: 3.2,
        peak: 0.6
      }

      this.analysisResult = this.cncAnalyzer.comprehensiveAnalysis(
        mockVibrationData,
        mockTemperature,
        mockAcousticData
      )
      console.log('模拟正常状态:', this.analysisResult)
    },

    simulateWarningState() {
      // 模拟警告状态数据
      const mockVibrationData = {
        rms: 0.6, // 较高的RMS值
        peak: 1.2,
        kurtosis: 4.8,
        skewness: 0.9,
        std: 0.15
      }
      const mockTemperature = 26.5 // 较高温度
      const mockAcousticData = {
        rms: 0.55,
        spl: 78, // 较高噪声
        kurtosis: 4.6,
        peak: 1.1
      }

      this.analysisResult = this.cncAnalyzer.comprehensiveAnalysis(
        mockVibrationData,
        mockTemperature,
        mockAcousticData
      )
      console.log('模拟警告状态:', this.analysisResult)
    },

    simulateCriticalState() {
      // 模拟严重异常状态数据
      const mockVibrationData = {
        rms: 1.2, // 很高的RMS值
        peak: 2.5,
        kurtosis: 7.2,
        skewness: 1.8,
        std: 0.35
      }
      const mockTemperature = 32.0 // 很高温度
      const mockAcousticData = {
        rms: 0.95,
        spl: 95, // 很高噪声
        kurtosis: 6.8,
        peak: 2.2
      }

      this.analysisResult = this.cncAnalyzer.comprehensiveAnalysis(
        mockVibrationData,
        mockTemperature,
        mockAcousticData
      )
      console.log('模拟严重异常状态:', this.analysisResult)
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