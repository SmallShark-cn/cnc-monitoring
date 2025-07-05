# 修改密码功能使用说明

## 功能概述
本系统已实现完整的修改密码功能，包括前端界面和后端API。

## 后端实现

### 1. API接口
- **URL**: `POST /api/change-password`
- **请求体**:
```json
{
    "username": "用户名",
    "old_password": "原密码",
    "new_password": "新密码"
}
```
- **响应**:
```json
{
    "success": true,
    "message": "密码修改成功"
}
```

### 2. 后端文件
- `backend/Login.py`: 包含修改密码的API接口
- `backend/UserManagement.py`: 包含修改密码的业务逻辑

## 前端实现

### 1. 页面位置
- 文件: `src/views/UserManagement.vue`
- 路由: `/user-management`

### 2. 功能特性
- ✅ 原密码验证
- ✅ 新密码和确认密码一致性检查
- ✅ 新密码长度验证（最少6位）
- ✅ 加载状态显示
- ✅ 成功/失败提示信息
- ✅ 表单自动清空
- ✅ 退出登录功能

### 3. 组件特性
- 独立可复用组件
- 事件驱动设计（`@password-changed`事件）
- 支持ref调用方法（`clearForm()`）
- 美观的Bootstrap样式
- 响应式设计
- 实时表单验证
- 清晰的错误提示

### 4. 使用方法
```vue
<template>
  <!-- 基本使用 -->
  <ChangePassword />
  
  <!-- 带事件监听 -->
  <ChangePassword @password-changed="handlePasswordChanged" />
  
  <!-- 通过ref调用方法 -->
  <ChangePassword ref="changePasswordRef" />
</template>

<script>
import ChangePassword from '../components/ChangePassword.vue'

export default {
  components: { ChangePassword },
  methods: {
    handlePasswordChanged(result) {
      console.log('密码修改结果:', result);
    },
    clearForm() {
      this.$refs.changePasswordRef.clearForm();
    }
  }
}
</script>
```

## 使用步骤

### 1. 启动后端服务
```bash
cd backend
python Login.py
```

### 2. 启动前端服务
```bash
npm run dev
```

### 3. 访问修改密码页面
1. 登录系统
2. 导航到用户管理页面
3. 填写修改密码表单
4. 提交修改

## 安全特性

1. **密码加密**: 使用werkzeug.security进行密码哈希
2. **原密码验证**: 必须验证原密码才能修改
3. **输入验证**: 前端和后端双重验证
4. **错误处理**: 完善的错误处理和用户提示

## 测试

可以使用提供的测试脚本验证功能：
```bash
python test_change_password.py
```

## 注意事项

1. 确保数据库连接正常
2. 确保用户已登录且localStorage中有用户信息
3. 新密码长度至少3位
4. 修改成功后会自动清空表单 