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
    props: {
      tableData: {
        type: Array,
        default: () => []
      }
    },
    methods: {
      exportData() {
        if (!this.tableData.length) {
          alert('没有可导出的数据');
          return;
        }
        const keys = Object.keys(this.tableData[0]);
        const csvRows = [
          keys.join(','), // 表头
          ...this.tableData.map(row => keys.map(k => `"${row[k]}"`).join(','))
        ];
        const csvString = csvRows.join('\n');
        const blob = new Blob([csvString], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = '数据导出.csv';
        a.click();
        URL.revokeObjectURL(url);
      },
      refreshData() {
        this.$emit('refresh');
      }
    }
  }
  </script>
  
  <style scoped>
  .btn {
    transition: all 0.2s;
  }
  </style>