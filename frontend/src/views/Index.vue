<template>
  <div class="index-container">
    <el-card class="welcome-card">
      <template #header>
        <div class="card-header">
          <span>欢迎使用</span>
        </div>
      </template>
      <div class="welcome-content">
        <h2>HTTP Proxy 管理后台</h2>
        <p>工单代理管理平台</p>
        <el-row :gutter="20" class="stats-row">
          <el-col :span="12">
            <el-statistic title="在线状态" value="正常" />
          </el-col>
          <el-col :span="12">
            <el-statistic title="系统版本" value="1.0.0" />
          </el-col>
        </el-row>
        
        <div class="config-section">
          <div class="config-item">
            <span class="config-label">是否启用本系统工单数据：</span>
            <el-switch
              v-model="enableWorkOrder"
              @change="handleConfigChange"
              active-text="启用"
              inactive-text="禁用"
            />
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const enableWorkOrder = ref(false)

const loadConfig = async () => {
  try {
    const response = await axios.get('/api/config/system')
    if (response.data.success) {
      enableWorkOrder.value = response.data.data.enable_work_order
    }
  } catch (error) {
    console.error('加载配置失败:', error)
  }
}

const handleConfigChange = async (value) => {
  try {
    const response = await axios.put('/api/config/system', {
      enable_work_order: value
    })
    if (response.data.success) {
      ElMessage.success('配置更新成功')
    } else {
      ElMessage.error(response.data.message || '配置更新失败')
      enableWorkOrder.value = !value
    }
  } catch (error) {
    console.error('更新配置失败:', error)
    ElMessage.error('配置更新失败')
    enableWorkOrder.value = !value
  }
}

onMounted(() => {
  loadConfig()
})
</script>

<style scoped>
.index-container {
  padding: 20px;
}

.welcome-card {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  font-size: 20px;
  font-weight: 600;
}

.welcome-content {
  text-align: center;
  padding: 20px 0;
}

.welcome-content h2 {
  margin-bottom: 10px;
  color: #409eff;
}

.welcome-content p {
  color: #909399;
  margin-bottom: 30px;
}

.stats-row {
  margin-top: 30px;
}

.config-section {
  margin-top: 40px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.config-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.config-label {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}
</style>