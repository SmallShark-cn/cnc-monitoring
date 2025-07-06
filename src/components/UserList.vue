<template>
  <div class="card border-0 mb-4 rounded-big shadow-sm">
    <div class="card-body">
      <h4 class="mb-4 text-center">用户列表</h4>
      
      <!-- 用户列表 -->
      <div class="table-responsive">
        <table class="table table-hover">
          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>用户名</th>
              <th>用户组</th>
              <th>手机号</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>
                <span class="badge" :class="getUserGroupBadgeClass(user.user_group)">
                  {{ user.user_group || '普通用户' }}
                </span>
              </td>
              <td>{{ user.phone || '-' }}</td>
              <td>{{ formatDate(user.created_at) }}</td>
              <td>
                <button 
                  class="btn btn-danger btn-sm" 
                  @click="deleteUser(user.id, user.username)"
                  :disabled="loading"
                >
                  <i class="fas fa-trash"></i> 删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="text-center py-3">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">加载中...</span>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="!loading && users.length === 0" class="text-center py-4">
        <p class="text-muted">暂无用户数据</p>
      </div>

      <!-- 操作按钮 -->
      <div class="d-flex justify-content-between mt-4">
        <button class="btn btn-secondary" @click="refreshUsers" :disabled="loading">
          <i class="fas fa-refresh"></i> 刷新
        </button>
        <router-link to="/register" class="btn btn-primary">
          <i class="fas fa-plus"></i> 新建用户
        </router-link>
      </div>

      <!-- 消息提示 -->
      <div v-if="message" class="alert mt-3" :class="{'alert-success': success, 'alert-danger': !success}">
        {{ message }}
      </div>
    </div>


  </div>
</template>

<script>
export default {
  name: 'UserList',
  data() {
    return {
      users: [],
      loading: false,
      message: '',
      success: false
    }
  },
  mounted() {
    this.loadUsers();
  },
  methods: {
    async loadUsers() {
      this.loading = true;
      this.message = '';
      
      try {
        const response = await fetch('http://localhost:8000/api/users');
        const data = await response.json();
        
        if (response.ok) {
          this.users = data.users || [];
        } else {
          this.message = data.detail || '获取用户列表失败';
          this.success = false;
        }
      } catch (error) {
        console.error('获取用户列表错误:', error);
        this.message = '网络错误，请稍后重试';
        this.success = false;
      } finally {
        this.loading = false;
      }
    },



    async deleteUser(userId, username) {
      if (!confirm(`确定要删除用户 "${username}" 吗？`)) {
        return;
      }

      this.loading = true;
      
      try {
        const response = await fetch(`http://localhost:8000/api/users/${userId}`, {
          method: 'DELETE'
        });

        const data = await response.json();

        if (response.ok) {
          this.message = data.message || '用户删除成功';
          this.success = true;
          this.loadUsers(); // 刷新用户列表
        } else {
          this.message = data.detail || '用户删除失败';
          this.success = false;
        }
      } catch (error) {
        console.error('删除用户错误:', error);
        this.message = '网络错误，请稍后重试';
        this.success = false;
      } finally {
        this.loading = false;
      }
    },

    refreshUsers() {
      this.loadUsers();
    },



    formatDate(dateString) {
      if (!dateString) return '-';
      const date = new Date(dateString);
      return date.toLocaleString('zh-CN');
    },

    getUserGroupBadgeClass(userGroup) {
      const groupClasses = {
        '管理员': 'bg-danger',
        '操作员': 'bg-primary',
        '维护员': 'bg-warning',
        '普通用户': 'bg-secondary'
      };
      return groupClasses[userGroup] || 'bg-secondary';
    }
  }
}
</script>

<style scoped>
.card {
  background-color: #ffffff;
  border-radius: 15px;
}

.table th {
  border-top: none;
  font-weight: 600;
  color: #495057;
}

.table td {
  vertical-align: middle;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
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

.badge {
  font-size: 0.75rem;
  padding: 0.375rem 0.75rem;
}
</style> 