<template>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="text-black-80 mb-1">数据概览</h2>
      </div>
      <div class="d-flex gap-2">
        <button class="btn btn-outline-dark btn-sm" @click="exportData">
          <i class="fas fa-download me-2"></i>导出
        </button>
        <button class="btn btn-sm text-white" @click="refreshData" style="background-color: rgba(107,126,221);">
          <i class="fas fa-refresh me-2"></i>刷新
        </button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DashboardHeader',
    methods: {
      exportData() {
        // 导出数据逻辑
        console.log('导出数据')
      },
      refreshData() {
        // 刷新数据逻辑
        this.$emit('refresh')
      }
    }
  }
  </script>
  
  <style scoped>
  .btn {
    transition: all 0.2s;
  }
  </style>