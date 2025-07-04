import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import DataMonitor from '../views/DataMonitor.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/datamonitor', name: 'DataMonitor', component: DataMonitor}
]


export default createRouter({
  history: createWebHistory(),
  routes
})