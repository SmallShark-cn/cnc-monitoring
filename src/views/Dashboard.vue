<template>
  <div class="d-flex min-vh-100" style="background-color: #ffffff; margin: 0; padding: 0;">
    <!-- 侧边栏 -->
    <Sidebar />
    
    <!-- 主内容 -->
    <div class="flex-grow-1 p-4 w-100" style="margin: 0; background-color: rgb(235, 243, 248);">
      <DashboardHeader @refresh="refreshAllData" />
      <div class="row">
        <div class="col-md-8">
          <PerformanceChart ref="performanceChart" />
        </div>
        <div class="col-md-4 ">
          <WarningCounter />
        </div>
      </div>
      <StatsCards ref="statsCards" />
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue'
import DashboardHeader from '@/components/DashboardHeader.vue'
import PerformanceChart from '@/components/PerformanceChart.vue'
import StatsCards from '@/components/StatsCards.vue'
import WarningCounter from '@/components/WarningCounter.vue'

export default {
  name: 'Dashboard',
  components: {
    Sidebar,
    DashboardHeader,
    PerformanceChart,
    StatsCards,
    WarningCounter,
    
  },
  methods: {
    async refreshAllData() {
      // 刷新所有组件的数据
      if (this.$refs.performanceChart) {
        await this.$refs.performanceChart.fetchData()
      }
      if (this.$refs.statsCards) {
        await this.$refs.statsCards.fetchStats()
      }
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
</style>