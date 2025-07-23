<template>
    <div class="bg-sidebar" style="width: 280px; min-height: 100vh;">
      <div class="p-4">
        <h5 class="text-white mb-5">CNC刀具状态监测系统</h5>
        <nav>
          <div
            v-for="(item, index) in menuItems"
            :key="index"
            class="sidebar-item d-flex align-items-center p-2 mb-3 rounded text-white rounded-big"
            :class="{ active: isActive(item.route) }"
            @click="selectItem(item)"
          >
            <i :class="item.icon" class="me-3"></i>
            <span>{{ item.label }}</span>
          </div>
        </nav>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Sidebar',
    data() {
      return {
        menuItems: [
          { icon: 'fas fa-home', label: '仪表板', route: '/dashboard' },
          { icon: 'fas fa-chart-bar', label: '数据监控', route: '/datamonitor' },
          { icon: 'fas fa-cog', label: '参数调整', route: '/parameterchange' },
          { icon: 'fas fa-clock', label: '维护记录', route: '/maintenance' },
          { icon: 'fas fa-users', label: '用户管理', route: '/usermanagement' }
        ]
      }
    },
    methods: {
      selectItem(item) {
        this.$router.push(item.route)
      },
      isActive(route) {
        return this.$route.path === route
      }
    }
  }
  </script>
  
  <style scoped>
  .sidebar-item {
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .sidebar-item:hover {
    background-color: rgba(255, 255, 255, 0.142);
  }
  
  .sidebar-item.active {
    background-color: rgba(255, 255, 255, 0.347);
  }
  
  .bg-sidebar{
    background-color: rgba(107,126,221);
  }

  .card.rounded-big{
  border-radius: 1rem ;
}

  </style>