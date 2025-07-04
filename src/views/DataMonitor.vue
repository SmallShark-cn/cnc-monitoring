<template>
    <div class="d-flex min-vh-100 w-100" style="background-color: rgb(235, 243, 248); margin: 0; padding: 0;">
      <!-- 侧边栏 -->
      <Sidebar />
      
      <!-- 主内容 -->
      <div class="flex-grow-1 p-4 w-100">
        <h2>Data Monitor</h2>
        <div class="card border-0 mb-4 rounded-big">
          <div class="card-body">
            <ul class="list-group list-group-flush">
              <li v-for="(item, index) in dataList" :key="index" class="list-group-item">
                {{ item }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Sidebar from '@/components/Sidebar.vue';
  import DataMonitorHeader from '@/components/DataMonitorHeader.vue';
  
  export default {
    name: 'DataMonitor',
    components: { Sidebar },
    data() {
      return {
        dataList: [],
      };
    },
    mounted() {
      // 示例：获取数据
      this.fetchData();
    },
    methods: {
      fetchData() {
        // 替换为你的数据获取逻辑，例如从 API 获取
        this.dataList = ['Data 1', 'Data 2', 'Data 3']; // 示例数据
      },
    },
  };
  </script>
  
  <style scoped>
  /* .card {
    background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
  } */
  </style>