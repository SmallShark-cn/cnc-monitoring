<template>
  <div class="d-flex min-vh-100 w-100" style="background-color: rgb(235, 243, 248); margin: 0; padding: 0;">
    <!-- 侧边栏 -->
    <Sidebar />
    <!-- 主内容 -->
    <div class="flex-grow-1 p-4 w-100 align-items-stretch" style="background-color: rgb(235, 243, 248);">
      <DataMonitorHeader />
      
      <!-- 隐藏的麦克风音频分析器 -->
      <MicrophoneAudioAnalyzer 
        v-show="false" 
        @audioData="onAudioData" 
        :autoStart="true"
        :updateInterval="1000"
      />
      <div class="row">
        <!-- 左侧：振动传感器卡片 -->
        <div class="col-md-6 mb-4">
          <div class="card bg-white border-0 rounded-big shadow-sm h-100">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0">振动传感器数据监控</h5>
            </div>
            <div class="card-body">
              <!-- 时域波形数据 -->
              <h6 class="text-dark mb-3">时域波形数据</h6>
              <div class="row mb-3">
                <div class="col-6 mb-2">
                  <div class="text-center">
                    <div class="big-label">加速度 (m/s²)</div>
                    <div class="big-value text-primary">X: {{ vibrationTimeDomain.acceleration?.x || '0.000' }}</div>
                    <div class="big-value text-primary">Y: {{ vibrationTimeDomain.acceleration?.y || '0.000' }}</div>
                    <div class="big-value text-primary">Z: {{ vibrationTimeDomain.acceleration?.z || '0.000' }}</div>
                  </div>
                </div>
                <div class="col-6 mb-2">
                  <div class="text-center">
                    <div class="big-label">速度 (m/s)</div>
                    <div class="big-value text-success">X: {{ vibrationTimeDomain.velocity?.x || '0.000' }}</div>
                    <div class="big-value text-success">Y: {{ vibrationTimeDomain.velocity?.y || '0.000' }}</div>
                    <div class="big-value text-success">Z: {{ vibrationTimeDomain.velocity?.z || '0.000' }}</div>
                  </div>
                </div>
                <div class="col-6 mb-2">
                  <div class="text-center">
                    <div class="big-label">位移 (m)</div>
                    <div class="big-value text-warning">X: {{ vibrationTimeDomain.displacement?.x || '0.000' }}</div>
                    <div class="big-value text-warning">Y: {{ vibrationTimeDomain.displacement?.y || '0.000' }}</div>
                    <div class="big-value text-warning">Z: {{ vibrationTimeDomain.displacement?.z || '0.000' }}</div>
                  </div>
                </div>
                <div class="col-6 mb-2">
                  <div class="text-center">
                    <div class="big-label">温度 (°C)</div>
                    <div class="big-value text-danger">{{ vibrationTimeDomain.temperature || '0.0' }}</div>
                  </div>
                </div>
              </div>
              <!-- 频域谱数据 -->
              <h6 class="text-dark mb-3">频域谱数据</h6>
              <div class="row mb-3">
                <div class="col-6 mb-2">
                  <div class="text-center">
                    <div class="big-label">频率范围</div>
                    <div class="big-value">0 - 500 Hz</div>
                    <div class="big-label">数据点数</div>
                    <div class="big-value">{{ vibrationFrequencyDomain.frequencies?.length || 0 }}</div>
                  </div>
                </div>
                <div class="col-6 mb-2">
                  <div class="text-center">
                    <div class="big-label">最大幅值</div>
                    <div class="big-value text-success">{{ maxVibrationAmplitude }}</div>
                    <div class="big-label">最大PSD</div>
                    <div class="big-value text-info">{{ maxVibrationPSD }}</div>
                  </div>
                </div>
              </div>
              <!-- 时频分析数据 -->
              <h6 class="text-dark mb-3">时频分析数据</h6>
              <div class="row mb-3">
                <div class="col-6 mb-2">
                  <div class="text-center">
                    <div class="big-label">时间窗口</div>
                    <div class="big-value">10秒</div>
                    <div class="big-label">时间点数</div>
                    <div class="big-value">{{ vibrationTimeFrequency.time?.length || 0 }}</div>
                  </div>
                </div>
                <div class="col-6 mb-2">
                  <div class="text-center">
                    <div class="big-label">频率点数</div>
                    <div class="big-value">{{ vibrationTimeFrequency.frequencies?.length || 0 }}</div>
                    <div class="big-label">时频谱矩阵</div>
                    <div class="big-value">{{ vibrationTimeFrequency.spectrogram?.length || 0 }} x {{ vibrationTimeFrequency.spectrogram?.[0]?.length || 0 }}</div>
                  </div>
                </div>
              </div>
              <!-- 统计特征数据 -->
              <h6 class="text-dark mb-3">统计特征数据</h6>
              <div class="row mb-3">
                <div class="col-4 mb-2 text-center">
                  <div class="big-label">RMS</div>
                  <div class="big-value text-primary">{{ vibrationStatistics.rms || '0.000' }}</div>
                </div>
                <div class="col-4 mb-2 text-center">
                  <div class="big-label">峰值</div>
                  <div class="big-value text-warning">{{ vibrationStatistics.peak || '0.000' }}</div>
                </div>
                <div class="col-4 mb-2 text-center">
                  <div class="big-label">峰度</div>
                  <div class="big-value text-info">{{ vibrationStatistics.kurtosis || '0.000' }}</div>
                </div>
                <div class="col-4 mb-2 text-center">
                  <div class="big-label">偏度</div>
                  <div class="big-value text-success">{{ vibrationStatistics.skewness || '0.000' }}</div>
                </div>
                <div class="col-4 mb-2 text-center">
                  <div class="big-label">标准差</div>
                  <div class="big-value text-danger">{{ vibrationStatistics.std || '0.000' }}</div>
                </div>
                <div class="col-4 mb-2 text-center">
                  <div class="big-label">更新时间</div>
                  <div class="big-value">{{ vibrationStatistics.timestamp || '未连接' }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- 右侧：声学传感器卡片 -->
        <div class="col-md-6 mb-4">
          <div class="card bg-white border-0 rounded-big shadow-sm h-100">
            <div class="card-header bg-success text-white">
              <h5 class="mb-0">声学传感器数据监控</h5>
            </div>
            <div class="card-body">
              <!-- 时域音频波形数据 -->
              <h6 class="text-dark mb-3">时域音频波形</h6>
              <div class="row mb-3">
                <div class="col-6 mb-2">
                  <div class="text-center">
                    <div class="big-label">幅值 (amplitude)</div>
                    <div class="big-value text-info">{{ acousticTimeDomain.data?.[0]?.amplitude?.toFixed(3) ?? '0.000' }}</div>
                  </div>
                </div>
                <div class="col-6 mb-2">
                  <div class="text-center">
                    <div class="big-label">采样点数</div>
                    <div class="big-value text-primary">{{ acousticTimeDomain.data?.length || 0 }}</div>
                  </div>
                </div>
              </div>
              <!-- 频域谱数据 -->
              <h6 class="text-dark mb-3">频域谱数据</h6>
              <div class="row mb-3">
                <div class="col-4 mb-2">
                  <div class="text-center">
                    <div class="big-label">频率范围</div>
                    <div class="big-value">0 - 22050 Hz</div>
                  </div>
                </div>
                <div class="col-4 mb-2">
                  <div class="text-center">
                    <div class="big-label">数据点数</div>
                    <div class="big-value">{{ acousticFrequencyDomain.frequencies?.length || 0 }}</div>
                  </div>
                </div>
                <div class="col-4 mb-2">
                  <div class="text-center">
                    <div class="big-label">主导频率</div>
                    <div class="big-value text-warning">{{ getDominantFrequency(acousticFrequencyDomain) }} Hz</div>
                  </div>
                </div>
                <div class="col-4 mb-2">
                  <div class="text-center">
                    <div class="big-label">最大幅值</div>
                    <div class="big-value text-success">{{ maxAcousticAmplitude }}</div>
                  </div>
                </div>
                <div class="col-4 mb-2">
                  <div class="text-center">
                    <div class="big-label">最大PSD</div>
                    <div class="big-value text-info">{{ maxAcousticPSD }}</div>
                  </div>
                </div>
                <div class="col-4 mb-2">
                  <div class="text-center">
                    <div class="big-label">频谱重心</div>
                    <div class="big-value text-primary">{{ getSpectralCentroid(acousticFrequencyDomain) }} Hz</div>
                  </div>
                </div>
              </div>
              <!-- 时频分析数据 -->
              <h6 class="text-dark mb-3">时频分析数据</h6>
              <div class="row mb-3">
                <div class="col-4 mb-2">
                  <div class="text-center">
                    <div class="big-label">时间窗口</div>
                    <div class="big-value">{{ getTimeWindow(acousticTimeFrequency) }}ms</div>
                  </div>
                </div>
                <div class="col-4 mb-2">
                  <div class="text-center">
                    <div class="big-label">时间点数</div>
                    <div class="big-value">{{ acousticTimeFrequency.time?.length || 0 }}</div>
                  </div>
                </div>
                <div class="col-4 mb-2">
                  <div class="text-center">
                    <div class="big-label">频率点数</div>
                    <div class="big-value">{{ acousticTimeFrequency.frequencies?.length || 0 }}</div>
                  </div>
                </div>
                <div class="col-6 mb-2">
                  <div class="text-center">
                    <div class="big-label">时频谱矩阵</div>
                    <div class="big-value">{{ acousticTimeFrequency.spectrogram?.length || 0 }} x {{ acousticTimeFrequency.spectrogram?.[0]?.length || 0 }}</div>
                  </div>
                </div>
                <div class="col-6 mb-2">
                  <div class="text-center">
                    <div class="big-label">能量集中度</div>
                    <div class="big-value text-warning">{{ getEnergyConcentration(acousticTimeFrequency) }}%</div>
                  </div>
                </div>
              </div>
              <!-- 统计特征数据 -->
              <h6 class="text-dark mb-3">统计特征数据</h6>
              <div class="row mb-3">
                <div class="col-3 mb-2 text-center">
                  <div class="big-label">RMS</div>
                  <div class="big-value text-primary">{{ formatStatValue(acousticStatistics.rms) }}</div>
                </div>
                <div class="col-3 mb-2 text-center">
                  <div class="big-label">峰值</div>
                  <div class="big-value text-warning">{{ formatStatValue(acousticStatistics.peak) }}</div>
                </div>
                <div class="col-3 mb-2 text-center">
                  <div class="big-label">峰度</div>
                  <div class="big-value text-info">{{ formatStatValue(acousticStatistics.kurtosis, 2) }}</div>
                </div>
                <div class="col-3 mb-2 text-center">
                  <div class="big-label">偏度</div>
                  <div class="big-value text-success">{{ formatStatValue(acousticStatistics.skewness, 2) }}</div>
                </div>
                <div class="col-3 mb-2 text-center">
                  <div class="big-label">标准差</div>
                  <div class="big-value text-danger">{{ formatStatValue(acousticStatistics.std) }}</div>
                </div>
                <div class="col-3 mb-2 text-center">
                  <div class="big-label">声压级 SPL</div>
                  <div class="big-value text-info">{{ formatStatValue(acousticStatistics.spl, 1) }} dB</div>
                </div>
                <div class="col-3 mb-2 text-center">
                  <div class="big-label">零交叉率</div>
                  <div class="big-value text-secondary">{{ getZeroCrossingRate(acousticStatistics) }}</div>
                </div>
                <div class="col-3 mb-2 text-center">
                  <div class="big-label">更新时间</div>
                  <div class="big-value">{{ formatTimestamp(acousticStatistics.timestamp) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- 融合分析模块 -->
      <div class="row">
        <div class="col-md-12 mb-4">
          <div class="card bg-white border-0 rounded-big shadow-sm h-100">
            <div class="card-header bg-info text-white">
              <h5 class="mb-0">融合分析</h5>
            </div>
            <div class="card-body">
              <div class="row">
                <!-- 刀具磨损状态 -->
                <div class="col-md-6 mb-3">
                  <h6 class="text-dark mb-3">刀具磨损状态</h6>
                  <div class="fusion-block">
                    <div class="fusion-label">状态</div>
                    <div class="fusion-value">{{ analysisResult.toolWear?.wear_state || '-' }}</div>
                    <div class="fusion-label">置信度</div>
                    <div class="fusion-value">{{ analysisResult.toolWear?.confidence != null ? (analysisResult.toolWear.confidence * 100).toFixed(1) + '%' : '-' }}</div>
                    <div class="fusion-label">剩余寿命(RUL)</div>
                    <div class="fusion-value">{{ analysisResult.toolWear?.rul || '-' }}</div>
                    <div class="fusion-label">贡献度</div>
                    <div class="fusion-value">
                      振动: {{ analysisResult.toolWear?.contributions?.vibration ?? '-' }}
                      &nbsp; 声学: {{ analysisResult.toolWear?.contributions?.acoustic ?? '-' }}
                      &nbsp; 温度: {{ analysisResult.toolWear?.contributions?.temperature ?? '-' }}
                    </div>
                    <div class="fusion-label">更新时间</div>
                    <div class="fusion-value">{{ analysisResult.timestamp ? new Date(analysisResult.timestamp).toLocaleString('zh-CN') : '-' }}</div>
                  </div>
                </div>
                <!-- 相关性分析 -->
                <div class="col-md-6 mb-3">
                  <h6 class="text-dark mb-3">相关性分析</h6>
                  <div class="fusion-block">
                    <div v-if="fusionCorrelation.correlation_matrix">
                      <div v-for="(val, key) in fusionCorrelation.correlation_matrix" :key="key" class="d-flex justify-content-between align-items-center mb-2">
                        <span class="fusion-label">{{ key }}</span>
                        <span class="fusion-value">{{ val }}</span>
                      </div>
                    </div>
                    <div v-else class="text-muted">暂无数据</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- 状态指示器 -->
      <div class="row">
        <div class="col-12">
          <div class="card bg-white border-0 rounded-big shadow-sm">
            <div class="card-header bg-dark text-white">
              <h5 class="mb-0">数据拉取状态</h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-md-6">
                  <h6>振动传感器数据拉取</h6>
                  <div class="connection-status">
                    <span class="badge" :class="vibrationDataOk ? 'bg-success' : 'bg-danger'">
                      数据: {{ vibrationDataOk ? '正常' : '异常' }}
                    </span>
                  </div>
                </div>
                <div class="col-md-6">
                  <h6>声学传感器数据拉取</h6>
                  <div class="connection-status">
                    <span class="badge" :class="acousticDataOk ? 'bg-success' : 'bg-danger'">
                      数据: {{ acousticDataOk ? '正常' : '异常' }}
                    </span>
                  </div>
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
import Sidebar from '@/components/Sidebar.vue'
import DataMonitorHeader from '@/components/DataMonitorHeader.vue'
import MicrophoneAudioAnalyzer from '@/components/MicrophoneAudioAnalyzer.vue'
import CNCAnalysisAlgorithm from '@/utils/cncAnalysisAlgorithm.js'

export default {
  name: 'DataMonitor',
  components: {
    Sidebar,
    DataMonitorHeader,
    MicrophoneAudioAnalyzer
  },
  data() {
    return {
      // 振动传感器数据
      vibrationTimeDomain: {},
      vibrationFrequencyDomain: {},
      vibrationTimeFrequency: {},
      vibrationStatistics: {},
      // 声学传感器数据
      acousticTimeDomain: {},
      acousticFrequencyDomain: {},
      acousticTimeFrequency: {},
      acousticStatistics: {},
      // 融合分析
      fusionToolWear: {},
      fusionCorrelation: {},
      // 分析算法
      analysisResult: {},
      cncAnalyzer: null,
      // 麦克风相关数据
      microphoneData: null,
      microphoneHistory: [],
      // WebSocket对象
      wsVibrationTimeDomain: null,
      wsVibrationFrequencyDomain: null,
      wsVibrationTimeFrequency: null,
      wsVibrationStatistics: null,
      // 声学WebSocket已移除，使用麦克风数据
      // 拉取状态
      vibrationDataOk: true,
      acousticDataOk: true
    }
  },
  computed: {
    maxVibrationAmplitude() {
      if (!this.vibrationFrequencyDomain.amplitudes) return '0.000'
      return Math.max(...this.vibrationFrequencyDomain.amplitudes).toFixed(3)
    },
    maxVibrationPSD() {
      if (!this.vibrationFrequencyDomain.psd) return '0.000000'
      return Math.max(...this.vibrationFrequencyDomain.psd).toFixed(6)
    },
    maxAcousticAmplitude() {
      if (!this.acousticFrequencyDomain.amplitudes) return '0.000'
      return Math.max(...this.acousticFrequencyDomain.amplitudes).toFixed(3)
    },
    maxAcousticPSD() {
      if (!this.acousticFrequencyDomain.psd) return '0.000000'
      return Math.max(...this.acousticFrequencyDomain.psd).toFixed(6)
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
      // 振动相关
      this.wsVibrationTimeDomain = new WebSocket('ws://localhost:8000/ws/vibration/time-domain')
      this.wsVibrationTimeDomain.onmessage = (e) => {
        try {
          const msg = JSON.parse(e.data)
          if (msg.data && Array.isArray(msg.data)) {
            this.vibrationTimeDomain = msg.data[0] || {}
          }
        } catch (err) { this.vibrationDataOk = false }
      }
      this.wsVibrationFrequencyDomain = new WebSocket('ws://localhost:8000/ws/vibration/frequency-domain')
      this.wsVibrationFrequencyDomain.onmessage = (e) => {
        try { this.vibrationFrequencyDomain = JSON.parse(e.data) } catch (err) { this.vibrationDataOk = false }
      }
      this.wsVibrationTimeFrequency = new WebSocket('ws://localhost:8000/ws/vibration/time-frequency')
      this.wsVibrationTimeFrequency.onmessage = (e) => {
        try { this.vibrationTimeFrequency = JSON.parse(e.data) } catch (err) { this.vibrationDataOk = false }
      }
      this.wsVibrationStatistics = new WebSocket('ws://localhost:8000/ws/vibration/statistics')
      this.wsVibrationStatistics.onmessage = (e) => {
        try { 
          this.vibrationStatistics = JSON.parse(e.data)
          this.performAnalysis()
        } catch (err) { this.vibrationDataOk = false }
      }
      // 声学数据现在使用麦克风，不需要WebSocket连接
      // 设置声学数据状态为正常，因为我们使用麦克风
      this.acousticDataOk = true
    },
    closeAllWebSockets() {
      [
        this.wsVibrationTimeDomain,
        this.wsVibrationFrequencyDomain,
        this.wsVibrationTimeFrequency,
        this.wsVibrationStatistics
        // 声学WebSocket已移除，使用麦克风数据
      ].forEach(ws => { if (ws) ws.close() })
    },
    
    performAnalysis() {
      if (!this.cncAnalyzer) return

      // 获取温度数据
      const temperature = this.vibrationTimeDomain?.temperature || null

      // 执行综合分析
      this.analysisResult = this.cncAnalyzer.comprehensiveAnalysis(
        this.vibrationStatistics,
        temperature,
        this.acousticStatistics
      )

      console.log('DataMonitor Analysis Result:', this.analysisResult)
    },

    onAudioData(audioData) {
      this.microphoneData = audioData
      // 将麦克风数据添加到历史记录中
      if (audioData && audioData.spl !== undefined) {
        const dataPoint = {
          ...audioData,
          timestamp: new Date().toISOString()
        }
        
        this.microphoneHistory.push(dataPoint)
        
        // 限制历史数据长度
        if (this.microphoneHistory.length > 30) {
          this.microphoneHistory.shift()
        }
        
        // 使用麦克风数据替换声学传感器数据
        this.updateAcousticDataFromMicrophone(audioData)
      }
    },

    updateAcousticDataFromMicrophone(micData) {
      // 更新时域数据
      this.acousticTimeDomain = {
        data: [{
          amplitude: micData.rms || 0,
          timestamp: new Date().toISOString()
        }]
      }

      // 更新频域数据 (基于麦克风数据估算)
      const sampleRate = 44100
      const fftSize = 2048
      const frequencies = []
      const amplitudes = []
      const psd = []

      // 生成频率数组和估算的幅值
      for (let i = 0; i < fftSize / 2; i++) {
        frequencies.push((i * sampleRate) / fftSize)
        const amp = micData.rms * Math.exp(-i / 200) * (1 + 0.1 * Math.sin(i / 50))
        amplitudes.push(amp)
        psd.push(amp * amp)
      }

      this.acousticFrequencyDomain = {
        frequencies: frequencies,
        amplitudes: amplitudes,
        psd: psd,
        timestamp: new Date().toISOString()
      }

      // 更新时频数据
      this.acousticTimeFrequency = {
        time: [new Date().toISOString()],
        frequencies: frequencies.slice(0, 100), // 取前100个频率点
        spectrogram: [amplitudes.slice(0, 100)],
        timestamp: new Date().toISOString()
      }

      // 更新统计数据
      this.acousticStatistics = {
        rms: micData.rms || 0,
        peak: micData.peak || 0,
        kurtosis: micData.kurtosis || 0,
        skewness: micData.skewness || 0,
        std: micData.std || 0,
        spl: micData.spl || 0,
        timestamp: new Date().toISOString()
      }

      // 执行分析
      this.performAnalysis()
    },
    
    // 获取主导频率
    getDominantFrequency(frequencyData) {
      if (!frequencyData.frequencies || !frequencyData.amplitudes) return '0'
      const maxIndex = frequencyData.amplitudes.indexOf(Math.max(...frequencyData.amplitudes))
      return frequencyData.frequencies[maxIndex]?.toFixed(0) || '0'
    },
    
    // 获取频谱重心
    getSpectralCentroid(frequencyData) {
      if (!frequencyData.frequencies || !frequencyData.amplitudes) return '0'
      let weightedSum = 0
      let totalWeight = 0
      
      for (let i = 0; i < frequencyData.frequencies.length; i++) {
        const freq = frequencyData.frequencies[i]
        const amp = frequencyData.amplitudes[i]
        weightedSum += freq * amp
        totalWeight += amp
      }
      
      return totalWeight > 0 ? (weightedSum / totalWeight).toFixed(0) : '0'
    },
    
    // 获取时间窗口大小
    getTimeWindow(timeFreqData) {
      if (!timeFreqData.time || timeFreqData.time.length < 2) return '0'
      // 简化计算，假设固定窗口大小
      return '50'
    },
    
    // 获取能量集中度
    getEnergyConcentration(timeFreqData) {
      if (!timeFreqData.spectrogram || !timeFreqData.spectrogram[0]) return '0'
      
      const totalEnergy = timeFreqData.spectrogram[0].reduce((sum, val) => sum + (val * val), 0)
      const maxEnergy = Math.max(...timeFreqData.spectrogram[0].map(val => val * val))
      
      return totalEnergy > 0 ? ((maxEnergy / totalEnergy) * 100).toFixed(1) : '0'
    },
    
    // 获取零交叉率
    getZeroCrossingRate(statistics) {
      // 基于标准差和峰值估算零交叉率
      if (!statistics.std || !statistics.peak) return '0'
      const estimatedRate = (statistics.std / statistics.peak * 1000).toFixed(0)
      return estimatedRate || '0'
    },
    
    // 格式化统计值
    formatStatValue(value, decimals = 3) {
      if (value === null || value === undefined) return '0'
      return typeof value === 'number' ? value.toFixed(decimals) : '0'
    },
    
    // 格式化时间戳
    formatTimestamp(timestamp) {
      if (!timestamp) return '未连接'
      try {
        return new Date(timestamp).toLocaleTimeString('zh-CN')
      } catch {
        return '未连接'
      }
    }
  }
}
</script>

<style scoped>
.big-label {
  font-size: 1rem;
  font-weight: 600;
  color: #666;
  margin-bottom: 0.15rem;
}
.big-value {
  font-size: 1.15rem;
  font-weight: bold;
  margin-bottom: 0.15rem;
}
.fusion-block {
  background: #f8f9fa;
  border-radius: 0.5rem;
  padding: 1rem 1.5rem;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}
.fusion-label {
  font-size: 0.95rem;
  color: #888;
  font-weight: 500;
  margin-bottom: 0.1rem;
}
.fusion-value {
  font-size: 1.15rem;
  font-weight: bold;
  margin-bottom: 0.2rem;
}
.vibration-value {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.connection-status {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.badge {
  font-size: 1rem;
  padding: 0.5rem;
}
.card-header {
  border-bottom: none;
}
.card-body {
  padding: 1.2rem;
}
.text-center h6 {
  margin-bottom: 0.5rem;
  font-weight: 600;
}
.card.border {
  border-color: #dee2e6 !important;
}
.card.border .card-body {
  padding: 1rem;
}
</style>