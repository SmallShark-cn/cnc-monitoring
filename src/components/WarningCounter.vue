<template>
    <div class="card bg-white mb-4 border-0 rounded-big" style="min-height: 444px; max-width: 417.65px;">
      <div class="card-body">
        <h5 class="text-dark mb-4">告警信息</h5>
        <div>
          <div v-for="(alert, idx) in alerts" :key="idx" class="d-flex justify-content-between align-items-center mb-3 p-2 rounded" style="background:rgb(221, 52, 52);">
            <div class="fw-bold text-warning">{{ alert.type }}</div>
            <div class="text-white small">{{ alert.time }}</div>
            <div class="text-white flex-fill ms-3">{{ alert.message }}</div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'WarningCounter',
    data() {
      return {
        alerts: [
          { type: '高温', time: '2024-06-01 14:23', message: '主轴温度高' },
          { type: '振动', time: '2024-06-01 13:58', message: '检测到异常振动' },
          { type: '电流', time: '2024-06-01 13:45', message: '主轴电流过高' },
          { type: '润滑', time: '2024-06-01 13:30', message: '润滑油位低' }
        ]
      }
    }
  }
  </script>
  
  <!-- <style>
  .card.rounded-big{
    border-radius: 2rem !important;
  }
  </style>
   -->