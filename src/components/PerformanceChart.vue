<template>
    <div class="card bg-white border-0 mb-4 rounded-big shadow-sm" style="min-height: 30px; max-width: 900px; background: linear-gradient(180deg, #ffffff, #ffffff);">
      <div class="card-body">
        <h5 class="text-dark mb-4">Performance</h5>
        <div style="height: 300px;">
          <Line
            :data="chartData"
            :options="chartOptions"
          />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { Line } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  } from 'chart.js'
  
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  )
  
  export default {
    name: 'PerformanceChart',
    components: {
      Line
    },
    data() {
      return {
        chartData: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          datasets: [
            {
              label: 'Performance',
              data: [80, 75, 85, 78, 90, 88, 92, 95, 89, 93, 96, 94],
              borderColor: '#10B981',
              backgroundColor: 'rgba(16, 185, 129, 0.1)',
              borderWidth: 2,
              pointBackgroundColor: '#10B981',
              pointBorderColor: '#10B981',
              pointRadius: 4,
              fill: true,
              tension: 0.4
            }
          ]
        },
        chartOptions: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              backgroundColor: '#1F2937',
              titleColor: '#fff',
              bodyColor: '#fff',
              borderColor: '#374151',
              borderWidth: 1
            }
          },
          scales: {
            x: {
              grid: {
                color: '#374151',
                drawBorder: false
              },
              ticks: {
                color: '#9CA3AF'
              }
            },
            y: {
              grid: {
                color: '#374151',
                drawBorder: false
              },
              ticks: {
                color: '#9CA3AF'
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
    async mounted() {
      await this.fetchData()
    },
    methods: {
      async fetchData() {
        try {
          // 从API获取数据
          // const response = await axios.get('/api/performance')
          // this.chartData.datasets[0].data = response.data
        } catch (error) {
          console.error('获取性能数据失败:', error)
        }
      }
    }
  }
  </script>


<style>

.card.rounded-big{
  border-radius: 1rem ;
}

</style>