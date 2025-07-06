<template>
    <div class="d-flex min-vh-100 w-100" style="background-color: rgb(235, 243, 248); margin: 0; padding: 0;">
      <!-- 侧边栏 -->
      <Sidebar />
      
      <!-- 主内容 -->
      <div class="flex-grow-1 p-4 w-100 align-items-stretch" style="background-color: rgb(235, 243, 248);">
        <div class="row">
          <!-- 左侧：修改密码 -->
          <div class="col-md-6">
            <ChangePassword @password-changed="handlePasswordChanged" />
          </div>
          
          <!-- 右侧：用户管理 -->
          <div class="col-md-6">
            <UserList />
          </div>
        </div>
        
        <!-- 退出登录按钮 -->
        <div class="text-center mt-4">
          <button class="btn btn-lg text-danger" style="background-color: rgb(218, 218, 218);" @click="handleLogout">
            <i class="fas fa-sign-out-alt me-2"></i>退出登录
          </button>
        </div>
      </div>
    </div>
  </template>

<script>
import Sidebar from '../components/Sidebar.vue';
import ChangePassword from '../components/ChangePassword.vue';
import UserList from '../components/UserList.vue';

export default {
    name: 'UserManagement',
    components: {
        Sidebar,
        ChangePassword,
        UserList,
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