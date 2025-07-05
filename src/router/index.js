import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import DataMonitor from '../views/DataMonitor.vue'
import Login from '../views/UserManagements/Login.vue'
import UserManagement from '../views/UserManagement.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/datamonitor', name: 'DataMonitor', component: DataMonitor},
  { path: '/usermanagement', name: 'UserManagement', component: UserManagement},
  // { path }
]


export default createRouter({
  history: createWebHistory(),
  routes
})