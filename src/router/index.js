import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import DataMonitor from '../views/DataMonitor.vue'
import Login from '../views/UserManagements/Login.vue'
import Register from '../views/UserManagements/Register.vue'
import UserManagement from '../views/UserManagement.vue'
import ParameterChange from '../views/ParameterChange.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/datamonitor', name: 'DataMonitor', component: DataMonitor},
  { path: '/usermanagement', name: 'UserManagement', component: UserManagement},
  { path: '/parameterchange', name: 'ParameterChange', component: ParameterChange }
]


export default createRouter({
  history: createWebHistory(),
  routes
})