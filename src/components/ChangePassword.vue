<template>
  <div class="card border-0 mb-4 rounded-big shadow-sm" style="max-width: 50%;">
    <div class="card-body">
      <h4 class="mb-4 text-center">修改密码</h4>
      <form @submit.prevent="handleChangePassword">
        <div class="mb-3">
          <label for="oldPassword" class="form-label">原密码</label>
          <input 
            type="password" 
            class="form-control mx-auto" 
            id="oldPassword" 
            v-model="form.oldPassword" 
            required 
            style="width: 60%;"
            :disabled="loading"
          >
        </div>
        <div class="mb-3">
          <label for="newPassword" class="form-label">新密码</label>
          <input 
            type="password" 
            class="form-control mx-auto" 
            id="newPassword" 
            v-model="form.newPassword" 
            required 
            style="width: 60%;"
            :disabled="loading"
          >
        </div>
        <div class="mb-3">
          <label for="confirmPassword" class="form-label">确认新密码</label>
          <input 
            type="password" 
            class="form-control mx-auto" 
            id="confirmPassword" 
            v-model="form.confirmPassword" 
            required 
            style="width: 60%;"
            :disabled="loading"
          >
        </div>
        <div class="d-grid">
          <button 
            type="submit" 
            class="btn btn-primary mx-auto mt-3" 
            style="max-width: 60%;" 
            :disabled="loading"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            {{ loading ? '处理中...' : '提交修改' }}
          </button>
        </div>
        <div 
          v-if="message" 
          class="alert mt-3" 
          :class="{'alert-success': success, 'alert-danger': !success}" 
          style="max-width: 60%; margin: 0 auto;"
        >
          {{ message }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChangePassword',
  data() {
    return {
      form: {
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      loading: false,
      message: '',
      success: false
    }
  },
  methods: {
    async handleChangePassword() {
      if (this.form.newPassword !== this.form.confirmPassword) {
        this.message = '新密码和确认密码不一致';
        this.success = false;
        return;
      }

      if (this.form.newPassword.length < 3) {
        this.message = '新密码长度至少3位';
        this.success = false;
        return;
      }

      this.loading = true;
      this.message = '';

      try {
        const username = localStorage.getItem('username');
        if (!username) {
          this.message = '用户信息不存在，请重新登录';
          this.success = false;
          return;
        }

        const response = await fetch('http://localhost:8000/api/change-password', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: username,
            old_password: this.form.oldPassword,
            new_password: this.form.newPassword
          })
        });

        const data = await response.json();

        if (response.ok) {
          this.message = data.message || '密码修改成功';
          this.success = true;
          // 清空表单
          this.form.oldPassword = '';
          this.form.newPassword = '';
          this.form.confirmPassword = '';
          // 触发成功事件
          this.$emit('password-changed', { success: true, message: this.message });
        } else {
          this.message = data.detail || '密码修改失败';
          this.success = false;
          // 触发失败事件
          this.$emit('password-changed', { success: false, message: this.message });
        }
      } catch (error) {
        console.error('修改密码错误:', error);
        this.message = '网络错误，请稍后重试';
        this.success = false;
        // 触发失败事件
        this.$emit('password-changed', { success: false, message: this.message });
      } finally {
        this.loading = false;
      }
    },
    
    // 清空表单和消息
    clearForm() {
      this.form.oldPassword = '';
      this.form.newPassword = '';
      this.form.confirmPassword = '';
      this.message = '';
      this.success = false;
    }
  }
}
</script>

<style scoped>
.card {
  background-color: #ffffff;
  border-radius: 15px;
}

.form-control {
  border-radius: 8px;
  border: 1px solid #ced4da;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.form-control:disabled {
  background-color: #e9ecef;
  opacity: 0.65;
}

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  background-color: #6c757d;
  border-color: #6c757d;
  transform: none;
}

.alert {
  border-radius: 8px;
  border: none;
}

.alert-success {
  background-color: #d1e7dd;
  color: #0f5132;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
</style> 