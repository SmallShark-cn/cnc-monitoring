<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100 login-bg" style="background-color: #ffffff;">
    <div class="card border-0 shadow rounded-3" style="width: 400px;">
      <div class="card-body p-4">
        <h2 class="card-title text-center mb-4">CNC机床刀具管理</h2>
        <form @submit.prevent="login">
          <!-- 用户名输入框 -->
          <div class="mb-3">
            <label for="username" class="form-label">用户名</label>
            <input 
              type="text" 
              class="form-control rounded-pill"
              id="username" 
              v-model="username"
              required
            >
          </div>
          <!-- 密码输入框 -->
          <div class="mb-3">
            <label for="password" class="form-label">密码</label>
            <input 
              type="password" 
              class="form-control rounded-pill" 
              id="password" 
              v-model="password" 
              required
            >
          </div>
          <!-- 记住密码复选框 -->
          <div class="mb-3 d-flex justify-content-center">
            <div class="form-check" style="max-width: 40%;">
              <input 
                type="checkbox" 
                class="form-check-input" 
                id="rememberMe"
                v-model="rememberMe"
              >
              <label class="form-check-label" for="rememberMe">记住密码</label>
            </div>
          </div>
          <!-- 登录按钮，宽度100%，圆角 -->
          <button type="submit" class="btn btn-primary w-100 rounded-pill">登录</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios';

export default {
    name:'Login',

  data() {
    return {
      username: '',
      password: '',
      rememberMe: false
    }
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://localhost:8000/api/login", {
            username: this.username,
            password: this.password,
        });
        const result = response.data; 

        if (result.success) {
          // 保存用户登录状态
          localStorage.setItem('isLoggedIn', 'true');
          localStorage.setItem('username', this.username);
          
          // 处理记住密码逻辑
          if (this.rememberMe) {
            localStorage.setItem('savedPassword', this.password);
          } else {
            localStorage.removeItem('savedPassword');
          }
          
          // 跳转到仪表盘
          this.$router.push('/dashboard');
        } else {
          alert(result.message);
        }
      } catch (error) {
        console.error('登录失败:', error);
        alert('登录失败，请稍后重试');
      }
    }
  },
  mounted() {
    // 检查是否有记住的密码
    const savedUsername = localStorage.getItem('username');
    const savedPassword = localStorage.getItem('savedPassword');
    if (savedUsername && savedPassword) {
      this.username = savedUsername;
      this.password = savedPassword;
      this.rememberMe = true;
    }
  }
}
</script>

<style scoped>
.card {
  background-color: #f8f9fa;
}

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.form-control {
  border-radius: 20px;
  padding: 10px 20px;
}

.form-check-input {
  margin-top: 0.3em;
}

.login-bg {
    background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
}
</style>
