<template>
  <div class="resource-chart-container">
    <Line :data="chartData" :options="chartOptions" ref="chart" />
  </div>
</template>

<script>
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale)

export default {
  name: 'AcousticTrendChart',
  components: { Line },
  props: {
    microphoneHistory: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      chartInstance: null
    }
  },
  computed: {
    chartData() {
      console.log('AcousticTrendChart - microphoneHistory:', this.microphoneHistory) // 调试日志
      // 如果没有数据，返回默认数据
      if (!this.microphoneHistory || this.microphoneHistory.length === 0) {
        console.log('No microphone data, showing default chart')
        return {
          labels: ['1', '2', '3', '4', '5'],
          datasets: [
            {
              label: 'SPL',
              data: [0, 0, 0, 0, 0],
              borderColor: '#FF6B35',
              backgroundColor: 'rgba(255,107,53,0.1)',
              fill: true,
              tension: 0.2,
              pointRadius: 0,
              borderWidth: 2
            }
          ]
        }
      }
      // 限制最多显示30个数据点
      const maxPoints = 30
      const data = this.microphoneHistory.slice(-maxPoints) // 取最新的30个数据点
      console.log('Microphone chart data:', data) // 调试日志
      // 生成标签，从左到右编号（最新的数据在右边）
      const labels = Array.from({ length: data.length }, (_, idx) => idx + 1)
      return {
        labels: labels,
        datasets: [
          {
            label: 'SPL',
            data: data.map(item => item.spl || 0), // 取spl字段，如果没有则默认为0dB
            borderColor: '#FF6B35',
            backgroundColor: 'rgba(255,107,53,0.1)',
            fill: true,
            tension: 0.2,
            pointRadius: 0,
            borderWidth: 2
          }
        ]
      }
    },
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { 
            enabled: true,
            mode: 'index',
            intersect: false,
            backgroundColor: 'rgba(0,0,0,0.8)',
            titleColor: '#fff',
            bodyColor: '#fff',
            borderColor: '#FF6B35',
            borderWidth: 1,
            callbacks: {
              label: function(context) {
                return `SPL: ${context.parsed.y.toFixed(1)} dB`
              }
            }
          }
        },
        scales: {
          x: { 
            display: true, 
            grid: { 
              display: true,
              color: 'rgba(0,0,0,0.1)',
              drawBorder: false
            },
            ticks: { 
              display: true,
              color: '#666',
              font: {
                size: 10
              }
            },
            title: {
              display: true,
              text: '时间',
              color: '#666',
              font: {
                size: 12
              }
            }
          },
          y: { 
            display: true, 
            grid: { 
              display: true,
              color: 'rgba(0,0,0,0.1)',
              drawBorder: false
            }, 
            min: 0, 
            max: 120,
            ticks: { 
              display: true,
              color: '#666',
              font: {
                size: 10
              },
              stepSize: 20,
              callback: function(value) {
                return value + ' dB'
              }
            },
            title: {
              display: true,
              text: 'SPL值 (dB)',
              color: '#666',
              font: {
                size: 12
              }
            }
          }
        },
        elements: { 
          line: { borderJoinStyle: 'miter' },
          point: { radius: 0 }
        },
        animation: false,
        transitions: {
          active: {
            animation: {
              duration: 0
            }
          }
        },
        interaction: {
          intersect: false,
          mode: 'index'
        }
      }
    }
  },
  watch: {
    microphoneHistory: {
      handler(newData, oldData) {
        console.log('microphoneHistory changed:', newData) // 调试日志
        // 当数据更新时，立即更新图表，不使用动画
        this.$nextTick(() => {
          if (this.$refs.chart) {
            this.$refs.chart.update('none')
          }
        })
      },
      deep: true,
      immediate: true
    }
  },
  mounted() {
    console.log('AcousticTrendChart mounted, microphoneHistory:', this.microphoneHistory) // 调试日志
    // 组件挂载后，确保图表正确渲染，不使用动画
    this.$nextTick(() => {
      if (this.$refs.chart) {
        this.$refs.chart.update('none')
      }
    })
  }
}
</script>

<style scoped>
.resource-chart-container {
  width: 100%;
  height: 100%;
  min-height: 200px;
  background: #ffffff;
  border-radius: 0.75rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

/* 确保图表容器内的所有元素正确显示并占满容器 */
.resource-chart-container canvas {
  width: 100%;
  height: 100%;
  max-width: none;
  max-height: 280px;
}

/* 确保父容器也占满可用空间 */
.card-body {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.card-body h5 {
  margin-bottom: 1rem;
  flex-shrink: 0;
}

.card-body .resource-chart-container {
  flex: 1;
  min-height: 0;
}
</style>