<template>
  <div class="d-flex min-vh-100" style="background-color: #ffffff; margin: 0; padding: 0;">
    <!-- 侧边栏 -->
    <Sidebar />
    <!-- 主内容 -->
    <div class="flex-grow-1 p-4 w-100" style="margin: 0; background-color: rgb(235, 243, 248);">
      <h2 class="mb-4">维护记录</h2>
      <!-- 筛选与操作栏 -->
      <div class="d-flex flex-wrap gap-2 mb-3 align-items-center">
        <input v-model="searchText" class="form-control w-auto" placeholder="搜索设备/维护人/类型..." />
        <input v-model="filterDate" type="date" class="form-control w-auto" />
        <select v-model="filterType" class="form-select w-auto">
          <option value="">全部类型</option>
          <option v-for="type in typeOptions" :key="type" :value="type">{{ type }}</option>
        </select>
        <button class="btn btn-primary" @click="showAddModal = true">新增维护记录</button>
        <button class="btn btn-success" @click="exportRecords">导出记录</button>
      </div>

      <!-- 统计信息 -->
      <div class="row mb-3">
        <div class="col-md-3 col-6 mb-2">
          <div class="card text-center p-3">
            <div class="fw-bold fs-4">{{ stats.total }}</div>
            <div class="text-muted">总维护次数</div>
          </div>
        </div>
        <div class="col-md-3 col-6 mb-2">
          <div class="card text-center p-3">
            <div class="fw-bold fs-4">{{ stats.thisMonth }}</div>
            <div class="text-muted">本月维护</div>
          </div>
        </div>
        <div class="col-md-3 col-6 mb-2">
          <div class="card text-center p-3">
            <div class="fw-bold fs-4">{{ stats.uniqueDevices }}</div>
            <div class="text-muted">涉及设备</div>
          </div>
        </div>
        <div class="col-md-3 col-6 mb-2">
          <div class="card text-center p-3">
            <div class="fw-bold fs-4">{{ stats.commonType }}</div>
            <div class="text-muted">最常见类型</div>
          </div>
        </div>
      </div>

      <!-- 维护类型分布图表 -->
      <div class="card mb-4 p-3">
        <canvas ref="typeChart" height="60"></canvas>
      </div>

      <!-- 维护记录表格 -->
      <div class="card p-3">
        <table class="table table-hover align-middle">
          <thead>
            <tr>
              <th>日期</th>
              <th>设备</th>
              <th>维护人</th>
              <th>类型</th>
              <th>结果</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in pagedRecords" :key="record.id">
              <td>{{ record.date }}</td>
              <td>{{ record.device }}</td>
              <td>{{ record.maintainer }}</td>
              <td>{{ record.type }}</td>
              <td>{{ record.result }}</td>
              <td>
                <button class="btn btn-link btn-sm" @click="showDetail(record)">详情</button>
                <button class="btn btn-link btn-sm text-primary" @click="editRecord(record)">编辑</button>
                <button class="btn btn-link btn-sm text-danger" @click="deleteRecord(record.id)">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
        <!-- 分页 -->
        <nav v-if="pageCount > 1">
          <ul class="pagination justify-content-end">
            <li class="page-item" :class="{disabled: page === 1}">
              <a class="page-link" href="#" @click.prevent="page = Math.max(1, page-1)">上一页</a>
            </li>
            <li class="page-item" v-for="p in pageCount" :key="p" :class="{active: page === p}">
              <a class="page-link" href="#" @click.prevent="page = p">{{ p }}</a>
            </li>
            <li class="page-item" :class="{disabled: page === pageCount}">
              <a class="page-link" href="#" @click.prevent="page = Math.min(pageCount, page+1)">下一页</a>
            </li>
          </ul>
        </nav>
      </div>

      <!-- 详情弹窗 -->
      <div v-if="showDetailModal" class="modal-mask">
        <div class="modal-wrapper">
          <div class="modal-container">
            <h5>维护详情</h5>
            <ul class="list-group mb-3">
              <li class="list-group-item"><b>日期：</b>{{ detailRecord.date }}</li>
              <li class="list-group-item"><b>设备：</b>{{ detailRecord.device }}</li>
              <li class="list-group-item"><b>维护人：</b>{{ detailRecord.maintainer }}</li>
              <li class="list-group-item"><b>类型：</b>{{ detailRecord.type }}</li>
              <li class="list-group-item"><b>结果：</b>{{ detailRecord.result }}</li>
              <li class="list-group-item"><b>描述：</b>{{ detailRecord.description }}</li>
            </ul>
            <button class="btn btn-secondary" @click="showDetailModal = false">关闭</button>
          </div>
        </div>
      </div>

      <!-- 新增/编辑弹窗 -->
      <div v-if="showAddModal || showEditModal" class="modal-mask">
        <div class="modal-wrapper">
          <div class="modal-container">
            <h5>{{ showAddModal ? '新增维护记录' : '编辑维护记录' }}</h5>
            <form @submit.prevent="showAddModal ? addRecord() : updateRecord()">
              <div class="mb-2">
                <label>日期</label>
                <input v-model="form.date" type="date" class="form-control" required />
              </div>
              <div class="mb-2">
                <label>设备</label>
                <input v-model="form.device" class="form-control" required />
              </div>
              <div class="mb-2">
                <label>维护人</label>
                <input v-model="form.maintainer" class="form-control" required />
              </div>
              <div class="mb-2">
                <label>类型</label>
                <select v-model="form.type" class="form-select" required>
                  <option v-for="type in typeOptions" :key="type" :value="type">{{ type }}</option>
                </select>
              </div>
              <div class="mb-2">
                <label>结果</label>
                <input v-model="form.result" class="form-control" required />
              </div>
              <div class="mb-2">
                <label>描述</label>
                <textarea v-model="form.description" class="form-control" rows="2" required></textarea>
              </div>
              <div class="d-flex gap-2">
                <button class="btn btn-primary" type="submit">保存</button>
                <button class="btn btn-secondary" @click.prevent="closeModal">取消</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, reactive, computed, watch } from 'vue'
// Chart.js 用于绘制类型分布图
import Chart from 'chart.js/auto'
import Sidebar from '@/components/Sidebar.vue'

export default {
  name: 'Maintenance',
  components:{
    Sidebar
  },
  setup() {
    const records = ref([
      { id: 1, date: '2024-06-01', device: 'CNC-001', maintainer: '张三', type: '更换刀具', description: '定期更换主刀具，检查磨损情况。', result: '正常' },
      { id: 2, date: '2024-06-03', device: 'CNC-002', maintainer: '李四', type: '清洁维护', description: '清理设备内部杂质。', result: '正常' },
      { id: 3, date: '2024-06-05', device: 'CNC-001', maintainer: '王五', type: '软件升级', description: '升级监控系统软件。', result: '成功' },
      { id: 4, date: '2024-06-07', device: 'CNC-003', maintainer: '赵六', type: '更换刀具', description: '更换副刀具。', result: '正常' },
      { id: 5, date: '2024-06-10', device: 'CNC-002', maintainer: '张三', type: '故障排查', description: '排查报警原因。', result: '已修复' },
    ])
    const typeOptions = ['更换刀具', '清洁维护', '软件升级', '故障排查']
    const searchText = ref('')
    const filterDate = ref('')
    const filterType = ref('')
    const page = ref(1)
    const pageSize = 5

    const stats = computed(() => {
      const total = records.value.length
      const thisMonth = records.value.filter(r => r.date.startsWith('2024-06')).length
      const uniqueDevices = new Set(records.value.map(r => r.device)).size
      const typeCount = {}
      let commonType = ''
      let max = 0
      records.value.forEach(r => {
        typeCount[r.type] = (typeCount[r.type] || 0) + 1
        if (typeCount[r.type] > max) {
          max = typeCount[r.type]
          commonType = r.type
        }
      })
      return { total, thisMonth, uniqueDevices, commonType }
    })

    const filteredRecords = computed(() => {
      return records.value.filter(r => {
        const matchText =
          r.device.includes(searchText.value) ||
          r.maintainer.includes(searchText.value) ||
          r.type.includes(searchText.value)
        const matchDate = filterDate.value ? r.date === filterDate.value : true
        const matchType = filterType.value ? r.type === filterType.value : true
        return matchText && matchDate && matchType
      })
    })
    const pageCount = computed(() => Math.ceil(filteredRecords.value.length / pageSize))
    const pagedRecords = computed(() => {
      const start = (page.value - 1) * pageSize
      return filteredRecords.value.slice(start, start + pageSize)
    })

    const showDetailModal = ref(false)
    const detailRecord = ref({})
    function showDetail(record) {
      detailRecord.value = { ...record }
      showDetailModal.value = true
    }

    const showAddModal = ref(false)
    const showEditModal = ref(false)
    const form = reactive({ id: null, date: '', device: '', maintainer: '', type: '', description: '', result: '' })
    function closeModal() {
      showAddModal.value = false
      showEditModal.value = false
      Object.assign(form, { id: null, date: '', device: '', maintainer: '', type: '', description: '', result: '' })
    }
    function addRecord() {
      records.value.push({ ...form, id: Date.now() })
      closeModal()
    }
    function editRecord(record) {
      Object.assign(form, record)
      showEditModal.value = true
    }
    function updateRecord() {
      const idx = records.value.findIndex(r => r.id === form.id)
      if (idx !== -1) records.value[idx] = { ...form }
      closeModal()
    }
    function deleteRecord(id) {
      if (confirm('确定要删除该记录吗？')) {
        records.value = records.value.filter(r => r.id !== id)
      }
    }

    // 导出功能（CSV）
    function exportRecords() {
      const header = '日期,设备,维护人,类型,结果,描述\n'
      const rows = records.value.map(r => `${r.date},${r.device},${r.maintainer},${r.type},${r.result},${r.description.replace(/\n/g, ' ')}\n`).join('')
      const blob = new Blob([header + rows], { type: 'text/csv' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = '维护记录.csv'
      a.click()
      URL.revokeObjectURL(url)
    }

    // 图表
    const typeChart = ref(null)
    let chartInstance = null
    onMounted(() => {
      renderChart()
    })
    function renderChart() {
      if (chartInstance) chartInstance.destroy()
      const typeCount = {}
      records.value.forEach(r => {
        typeCount[r.type] = (typeCount[r.type] || 0) + 1
      })
      const data = {
        labels: Object.keys(typeCount),
        datasets: [{
          label: '维护类型分布',
          data: Object.values(typeCount),
          backgroundColor: ['#6b7edd', '#4bc0c0', '#ff6384', '#ffcd56'],
        }]
      }
      chartInstance = new Chart(typeChart.value, {
        type: 'bar',
        data,
        options: {
          plugins: { legend: { display: false } },
          responsive: true,
          scales: { y: { beginAtZero: true } }
        }
      })
    }
    // 监听 records 变化刷新图表
    watch(records, renderChart, { deep: true })

    return {
      records, typeOptions, searchText, filterDate, filterType, page, pageCount, pagedRecords,
      showDetailModal, detailRecord, showDetail,
      showAddModal, showEditModal, form, closeModal, addRecord, editRecord, updateRecord, deleteRecord,
      exportRecords, stats, typeChart
    }
  }
}
</script>

<style scoped>
.container-fluid {
  max-width: 1200px;
}
.card {
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-wrapper {
  width: 100%;
  max-width: 400px;
}
.modal-container {
  background: #fff;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
</style> 