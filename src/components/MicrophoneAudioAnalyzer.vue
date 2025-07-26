<template>
  <div class="microphone-analyzer" style="display: none;">
    <!-- 隐藏组件，仅用于数据处理 -->
  </div>
</template>

<script>
export default {
  name: 'MicrophoneAudioAnalyzer',
  props: {
    autoStart: {
      type: Boolean,
      default: false
    },
    updateInterval: {
      type: Number,
      default: 100
    }
  },
  data() {
    return {
      isSupported: false,
      isRecording: false,
      audioContext: null,
      mediaStream: null,
      analyzerNode: null,
      dataArray: null,
      timeDataArray: null,
      updateTimer: null,
      audioData: {
        rms: 0,
        peak: 0,
        spl: 0,
        kurtosis: 0,
        skewness: 0,
        std: 0,
        dominantFreq: 0,
        zeroCrossings: 0
      }
    }
  },
  emits: ['audioData'],
  mounted() {
    this.checkSupport()
    if (this.autoStart && this.isSupported) {
      this.startRecording()
    }
  },
  beforeUnmount() {
    this.stopRecording()
  },
  methods: {
    checkSupport() {
      this.isSupported = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia && window.AudioContext)
    },

    async toggleRecording() {
      if (this.isRecording) {
        this.stopRecording()
      } else {
        await this.startRecording()
      }
    },

    async startRecording() {
      try {
        this.mediaStream = await navigator.mediaDevices.getUserMedia({ 
          audio: {
            echoCancellation: false,
            noiseSuppression: false,
            autoGainControl: false
          }
        })
        
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)()
        const source = this.audioContext.createMediaStreamSource(this.mediaStream)
        
        this.analyzerNode = this.audioContext.createAnalyser()
        this.analyzerNode.fftSize = 2048
        this.analyzerNode.smoothingTimeConstant = 0.3
        
        source.connect(this.analyzerNode)
        
        this.dataArray = new Uint8Array(this.analyzerNode.frequencyBinCount)
        this.timeDataArray = new Float32Array(this.analyzerNode.fftSize)
        
        this.isRecording = true
        this.analyze()
      } catch (error) {
        console.error('获取麦克风权限失败:', error)
        alert('无法访问麦克风，请检查权限设置')
      }
    },

    stopRecording() {
      this.isRecording = false
      
      if (this.updateTimer) {
        clearInterval(this.updateTimer)
        this.updateTimer = null
      }
      
      if (this.mediaStream) {
        this.mediaStream.getTracks().forEach(track => track.stop())
        this.mediaStream = null
      }
      
      if (this.audioContext) {
        this.audioContext.close()
        this.audioContext = null
      }
    },

    analyze() {
      if (!this.isRecording) return
      
      this.updateTimer = setInterval(() => {
        if (!this.isRecording) return
        
        this.analyzerNode.getByteFrequencyData(this.dataArray)
        this.analyzerNode.getFloatTimeDomainData(this.timeDataArray)
        
        this.calculateAudioMetrics()
        this.$emit('audioData', this.audioData)
      }, this.updateInterval)
    },

    calculateAudioMetrics() {
      const timeData = this.timeDataArray
      const freqData = Array.from(this.dataArray)
      
      // RMS计算
      let sumSquares = 0
      for (let i = 0; i < timeData.length; i++) {
        sumSquares += timeData[i] * timeData[i]
      }
      this.audioData.rms = Math.sqrt(sumSquares / timeData.length)
      
      // Peak计算
      this.audioData.peak = Math.max(...timeData.map(Math.abs))
      
      // SPL计算 (简化版本)
      const referenceLevel = 0.00002 // 20 micropascals
      this.audioData.spl = 20 * Math.log10(this.audioData.rms / referenceLevel)
      
      // 主导频率
      const maxIndex = freqData.indexOf(Math.max(...freqData))
      this.audioData.dominantFreq = (maxIndex * this.audioContext.sampleRate) / (2 * this.analyzerNode.frequencyBinCount)
      
      // 统计指标
      const mean = timeData.reduce((a, b) => a + b, 0) / timeData.length
      const variance = timeData.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / timeData.length
      this.audioData.std = Math.sqrt(variance)
      
      // Skewness
      const skewnessSum = timeData.reduce((a, b) => a + Math.pow(b - mean, 3), 0)
      this.audioData.skewness = (skewnessSum / timeData.length) / Math.pow(this.audioData.std, 3)
      
      // Kurtosis
      const kurtosisSum = timeData.reduce((a, b) => a + Math.pow(b - mean, 4), 0)
      this.audioData.kurtosis = (kurtosisSum / timeData.length) / Math.pow(this.audioData.std, 4) - 3
      
      // Zero Crossings
      let crossings = 0
      for (let i = 1; i < timeData.length; i++) {
        if ((timeData[i] >= 0) !== (timeData[i-1] >= 0)) {
          crossings++
        }
      }
      this.audioData.zeroCrossings = crossings
    }
  }
}
</script>

<style scoped>
.microphone-analyzer {
  display: none;
}
</style>