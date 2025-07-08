<template>

    <div class="d-flex min-vh-100 w-100" style="background-color: #196b69;">
      <Sidebar />
      <div class="flex-grow-1 p-4 w-100" style="background-color: rgb(235, 243, 248);">
        <div class="card border-0 p-4 mx-auto bg-white" style="background: rgb(255,255,255); max-width: 600px;">
          <h2 class="text-center mb-4">RWKV Parameter Settings</h2>
          <form @submit.prevent="saveSettings">
            <div class="mb-3">
              <label for="modelSize" class="form-label">Model Size</label>
              <select v-model="settings.modelSize" class="form-control" id="modelSize">
                <option value="169M">169M Parameters</option>
                <option value="430M">430M Parameters</option>
                <option value="1.5B">1.5B Parameters</option>
                <option value="3B">3B Parameters</option>
                <option value="7B">7B Parameters</option>
              </select>
            </div>
            <div class="mb-3">
              <label for="tokenShift" class="form-label">Token Shift (μ)</label>
              <input v-model.number="settings.tokenShift" type="number" step="0.1" min="0" max="1" class="form-control" id="tokenShift" />
            </div>
            <div class="mb-3">
              <label for="layers" class="form-label">Number of Layers</label>
              <input v-model.number="settings.layers" type="number" min="1" max="4" class="form-control" id="layers" />
            </div>
            <div class="mb-3">
              <label for="contextLength" class="form-label">Context Length</label>
              <input v-model.number="settings.contextLength" type="number" min="512" max="4096" class="form-control" id="contextLength" />
            </div>
            <div class="mb-3">
              <label for="samplingRate" class="form-label">Sampling Rate (Hz)</label>
              <input v-model.number="settings.samplingRate" type="number" min="2000" max="51200" class="form-control" id="samplingRate" />
            </div>
            <div class="mb-3">
              <label for="alertThreshold" class="form-label">Alert Threshold (mm/s)</label>
              <input v-model.number="settings.alertThreshold" type="number" step="0.1" min="0" class="form-control" id="alertThreshold" />
            </div>
            <button type="submit" class="btn btn-primary w-100">Save Settings</button>
            <p v-if="error" class="text-danger mt-2">{{ error }}</p>
            <p v-if="success" class="text-success mt-2">{{ success }}</p>
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
    components:{
      Sidebar

    },
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
  
      const saveSettings = async () => {
        try {
          const response = await axios.post('http://localhost:8000/api/rwkv-settings', settings.value);
          success.value = response.data.message;
          error.value = '';
          setTimeout(() => router.push('/data-monitor'), 1000);
        } catch (err) {
          error.value = err.response?.data?.detail || 'Failed to save settings';
          success.value = '';
        }
      };
  
      return { settings, error, success, saveSettings };
    },
  };
  </script>
  
  <style scoped>
  .card {
    background: linear-gradient(135deg, #a1c4fd, #c2e9fb) !important;
  }
  </style>