<template>
    <div class="row">
      <!-- 总产量卡片 -->
      <div class="col-md-4">
        <div class="card border-0 h-100 gradbg rounded-big shadow-sm">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <div>
                <h6 class="text-muted mb-2">总产量</h6>
                <h3 class="text-white mb-0">{{ formatNumber(stats.total) }}</h3>
              </div>
              <div class="bg-success bg-opacity-20 p-2 rounded">
                <i class="fas fa-chart-line text-success"></i>
              </div>
            </div>
            <div style="height: 120px;">
              <Line
                :data="miniChartData1"
                :options="miniChartOptions"
              />
            </div>
          </div>
        </div>
      </div>
  
      <!-- 效率分析卡片 -->
      <div class="col-md-4">
        <div class="card gradbg border-0 h-100 rounded-big shadow-sm">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <div>
                <h6 class="text-muted mb-2">效率分析</h6>
                <h3 class="text-white mb-0">{{ formatNumber(stats.efficiency) }}</h3>
              </div>
              <div class="bg-primary bg-opacity-20 p-2 rounded">
                <i class="fas fa-chart-bar text-primary"></i>
              </div>
            </div>
            <div style="height: 120px;">
              <Bar
                :data="miniBarData"
                :options="miniBarOptions"
              />
            </div>
          </div>
        </div>
      </div>
  
      <!-- 质量指标卡片 -->
      <div class="col-md-4">
        <div class="card gradbg border-0 h-100 rounded-big shadow-sm">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <div>
                <h6 class="text-muted mb-2">环境温度</h6>
                <h3 class="text-white mb-0">{{ formatNumber(stats.quality) }}</h3>
              </div>
              <div class="bg-warning bg-opacity-20 p-2 rounded">
                <i class="fas fa-exclamation-triangle text-warning"></i>
              </div>
            </div>
            <div style="height: 120px;">
              <Line
                :data="miniChartData2"
                :options="miniChartOptions"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { Line, Bar } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend
  } from 'chart.js'
  
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend
  )
  
  export default {
    name: 'StatsCards',
    components: {
      Line,
      Bar
    },
    data() {
      return {
        stats: {
          total: 785200,
          efficiency: 58000,
          quality: 92000
        },
        miniChartData1: {
          labels: ['1', '2', '3', '4', '5', '6', '7'],
          datasets: [{
            data: [80, 75, 85, 78, 90, 88, 92],
            borderColor: '#10B981',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4
          }]
        },
        miniBarData: {
          labels: ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
          datasets: [{
            data: [20, 35, 25, 40, 30, 45, 38],
            backgroundColor: '#3B82F6',
            borderRadius: 2
          }]
        },
        miniChartData2: {
          labels: ['1', '2', '3', '4', '5', '6', '7'],
          datasets: [{
            data: [30, 45, 35, 50, 40, 60, 55],
            borderColor: '#F59E0B',
            backgroundColor: 'rgba(245, 158, 11, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4
          }]
        },
        miniChartOptions: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: { enabled: false }
          },
          scales: {
            x: { display: false },
            y: { display: false }
          },
          elements: {
            point: { radius: 0 }
          }
        },
        miniBarOptions: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: { enabled: false }
          },
          scales: {
            x: { display: false },
            y: { display: false }
          }
        }
      }
    },
    async mounted() {
      await this.fetchStats()
    },
    methods: {
      formatNumber(num) {
        return num.toLocaleString()
      },
      async fetchStats() {
        try {
          // 从API获取统计数据
          // const response = await axios.get('/api/stats')
          // this.stats = response.data
        } catch (error) {
          console.error('获取统计数据失败:', error)
        }
      }
    }
  }
  </script>

  <style>

  .card.gradbg{
    background: linear-gradient(180deg, #ffffff, #ffffff);
  }

  </style>