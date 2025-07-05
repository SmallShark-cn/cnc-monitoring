<template>
    <div class="d-flex min-vh-100 w-100" style="background-color: rgb(235, 243, 248); margin: 0; padding: 0;">
      <!-- 侧边栏 -->
      <Sidebar />
      
      <!-- 主内容 -->
      <div class="flex-grow-1 p-4 w-100 d-flex justify-content-center" style="background-color: rgb(235, 243, 248);">
        <div class="card border-0 mb-4 rounded-big" style="max-width: 100%; width: 100%; background-color: rgb(235, 243, 248);">
          <!-- 修改密码组件 -->
          <ChangePassword @password-changed="handlePasswordChanged" />
          
          <!-- 退出登录按钮 -->
          <div class="card-body text-center">
            <button class="btn btn-lg text-danger" style="background-color: rgb(218, 218, 218);" @click="handleLogout">
              <i class="fas fa-sign-out-alt me-2"></i>退出登录
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>

<script>
import Sidebar from '../components/Sidebar.vue';
import ChangePassword from '../components/ChangePassword.vue';

export default {
    name: 'UserManagement',
    components: {
        Sidebar,
        ChangePassword,
    },
    methods: {
        handlePasswordChanged(result) {
            console.log('密码修改结果:', result);
        },
        handleLogout() {
            localStorage.removeItem('username');
            localStorage.removeItem('isLoggedIn');
            this.$router.push('/login');
        }
    }
}
</script>

<style scoped>
/* 用户管理页面样式 */
</style>