<template>
  <div class="d-flex justify-content-between align-items-center mb-4">
    <div>
      <h2 class="text-dark mb-1">数据监控</h2>
      <p class="text-muted mb-0">实时监控振动和声学传感器数据</p>
    </div>
    <div class="d-flex align-items-center gap-3">
      <div class="text-center">
        <div class="status-indicator" :class="{ 'connected': isConnected }"></div>
        <small class="text-muted">{{ isConnected ? '已连接' : '已连接' }}</small>
      </div>
      <div class="text-end">
        <div class="text-muted small">最后更新</div>
        <div class="text-dark">{{ lastUpdateTime }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DataMonitorHeader',
  data() {
    return {
      isConnected: false,
      lastUpdateTime: '--:--:--'
    }
  },
  mounted() {
    this.updateTime()
    setInterval(this.updateTime, 1000)
  },
  methods: {
    updateTime() {
      this.lastUpdateTime = new Date().toLocaleTimeString()
    }
  }
}
</script>

<style scoped>
.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #dc3545;
  margin: 0 auto 0.25rem;
  animation: pulse 2s infinite;
}

.status-indicator.connected {
  background-color: #28a745;
}

@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 1;
  }
}
</style>