<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100 login-bg" style="background-color: #ffffff;">
    <div class="card border-0 shadow rounded-3" style="width: 400px;">
      <div class="card-body p-4">
        <h2 class="card-title text-center mb-4">用户注册</h2>
        <form @submit.prevent="register">
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
          <!-- 确认密码输入框 -->
          <div class="mb-3">
            <label for="confirmPassword" class="form-label">确认密码</label>
            <input 
              type="password" 
              class="form-control rounded-pill" 
              id="confirmPassword" 
              v-model="confirmPassword" 
              required
            >
          </div>
          <!-- 手机号输入框 -->
          <div class="mb-3">
            <label for="phone" class="form-label">手机号（可选）</label>
            <input 
              type="tel" 
              class="form-control rounded-pill" 
              id="phone" 
              v-model="phone"
            >
          </div>
          <!-- 用户组选择 -->
          <div class="mb-3">
            <label for="userGroup" class="form-label">用户组</label>
            <select 
              class="form-select rounded-pill"
              id="userGroup" 
              v-model="userGroup"
              required
            >
              <option value="普通用户">普通用户</option>
              <option value="管理员">管理员</option>
              <option value="操作员">操作员</option>
              <option value="维护员">维护员</option>
            </select>
          </div>
          <!-- 注册按钮，宽度100%，圆角 -->
          <button type="submit" class="btn btn-primary w-100 rounded-pill mt-4">注册</button>
        </form>
        
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      phone: '',
      userGroup: '普通用户'
    }
  },
  methods: {
    async register() {
      // 验证密码一致性
      if (this.password !== this.confirmPassword) {
        alert('两次输入的密码不一致');
        return;
      }

      // 验证密码长度
      if (this.password.length < 3) {
        alert('密码长度至少3位');
        return;
      }

      try {
        const response = await axios.post("http://localhost:8000/api/register", {
          username: this.username,
          password: this.password,
          phone: this.phone || null,
          user_group: this.userGroup
        });
        
        const result = response.data;

        if (result.success) {
          alert('注册成功！请登录');
          // 跳转到登录页面
          this.$router.push('/login');
        } else {
          alert(result.message || '注册失败');
        }
      } catch (error) {
        console.error('注册失败:', error);
        if (error.response && error.response.data && error.response.data.detail) {
          alert(error.response.data.detail);
        } else {
          alert('注册失败，请稍后重试');
        }
      }
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

.login-bg {
  background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
}
</style>
  