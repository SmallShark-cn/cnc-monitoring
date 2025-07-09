<template>
  <div class="d-flex min-vh-100 w-100" style="background-color: #ffffff;">
    <Sidebar />
    <div class="flex-grow-1 p-4 w-100" style="background-color: rgb(235, 243, 248);">
      <div class="card border-0 p-4 mx-auto bg-white shadow-lg param-card">
        <h2 class="text-center mb-4">RWKV参数调整</h2>
        <form @submit.prevent="saveSettings">
          <div class="row g-3">
            <div class="col-md-6">
              <label for="modelSize" class="form-label">模型规模</label>
              <select v-model="settings.modelSize" class="form-control form-control-lg rounded-pill" id="modelSize">
                <option value="169M">169M 参数</option>
                <option value="430M">430M 参数</option>
                <option value="1.5B">1.5B 参数</option>
                <option value="3B">3B 参数</option>
                <option value="7B">7B 参数</option>
              </select>
              <div class="form-text">选择RWKV模型的参数规模。</div>
            </div>
            <div class="col-md-6">
              <label for="tokenShift" class="form-label">Token Shift (μ)</label>
              <input v-model.number="settings.tokenShift" type="number" step="0.01" min="0" max="1" class="form-control form-control-lg rounded-pill" id="tokenShift" />
              <div class="form-text">控制token偏移，范围0~1。</div>
            </div>
            <div class="col-md-6">
              <label for="layers" class="form-label">层数</label>
              <input v-model.number="settings.layers" type="number" min="1" max="4" class="form-control form-control-lg rounded-pill" id="layers" />
              <div class="form-text">RWKV网络层数，推荐2~4。</div>
            </div>
            <div class="col-md-6">
              <label for="contextLength" class="form-label">上下文长度</label>
              <input v-model.number="settings.contextLength" type="number" min="512" max="4096" class="form-control form-control-lg rounded-pill" id="contextLength" />
              <div class="form-text">模型可感知的最大token数。</div>
            </div>
            <div class="col-md-6">
              <label for="samplingRate" class="form-label">采样率 (Hz)</label>
              <input v-model.number="settings.samplingRate" type="number" min="2000" max="51200" class="form-control form-control-lg rounded-pill" id="samplingRate" />
              <div class="form-text">输入数据的采样频率。</div>
            </div>
            <div class="col-md-6">
              <label for="alertThreshold" class="form-label">告警阈值 (mm/s)</label>
              <input v-model.number="settings.alertThreshold" type="number" step="0.1" min="0" class="form-control form-control-lg rounded-pill" id="alertThreshold" />
              <div class="form-text">超过该阈值将触发告警。</div>
            </div>
          </div>
          <button type="submit" class="btn btn-primary w-100 mt-4 py-2 rounded-pill fs-5" :disabled="loading">
            <span v-if="loading"><i class="fas fa-spinner fa-spin"></i> 保存中...</span>
            <span v-else>保存设置</span>
          </button>
          <div class="text-center">
            <p v-if="error" class="text-danger mt-2">{{ error }}</p>
            <p v-if="success" class="text-success mt-2">{{ success }}</p>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import Sidebar from '../components/Sidebar.vue';

export default {
  name: 'ParameterChange',
  components: { Sidebar },
  setup() {
    const router = useRouter();
    const settings = ref({
      modelSize: '1.5B',
      tokenShift: 0.5,
      layers: 2,
      contextLength: 1024,
      samplingRate: 51200,
      alertThreshold: 7.0,
    });
    const error = ref('');
    const success = ref('');
    const loading = ref(false);

    const saveSettings = async () => {
      loading.value = true;
      try {
        const response = await axios.post('http://localhost:8000/api/rwkv-settings', settings.value);
        success.value = response.data.message;
        error.value = '';
        setTimeout(() => router.push('/data-monitor'), 1000);
      } catch (err) {
        error.value = err.response?.data?.detail || '保存失败，请重试';
        success.value = '';
      } finally {
        loading.value = false;
      }
    };

    return { settings, error, success, loading, saveSettings };
  },
};
</script>

<style scoped>
.param-card {
  background: rgb(255, 255, 255);
  border-radius: 1.5rem;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.12);
  max-width: 700px;
}
.form-label {
  font-weight: 600;
  color: #196b69;
}
.form-control-lg {
  font-size: 1.1rem;
  padding: 0.7rem 1.2rem;
}
.form-control:focus {
  border-color: #196b69;
  box-shadow: 0 0 0 0.2rem rgba(25,107,105,.1);
}
.btn-primary {
  background: linear-gradient(90deg, #196b69 60%, #3bb2b8 100%);
  border: none;
  font-weight: 600;
  letter-spacing: 1px;
}
.btn-primary:active, .btn-primary:focus {
  background: #196b69;
}
.form-text {
  color: #888;
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
}
</style>