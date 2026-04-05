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
        <p>这是一个轻量级的代理管理平台</p>
        <el-row :gutter="20" class="stats-row">
          <el-col :span="8">
            <el-statistic title="账号总数" :value="stats.accounts" />
          </el-col>
          <el-col :span="8">
            <el-statistic title="在线状态" value="正常" />
          </el-col>
          <el-col :span="8">
            <el-statistic title="系统版本" value="1.0.0" />
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { accountsAPI } from '@/api'

const stats = ref({
  accounts: 0
})

const loadStats = async () => {
  try {
    const response = await accountsAPI.getList()
    if (response.code === 200) {
      stats.value.accounts = response.data.length
    }
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

onMounted(() => {
  loadStats()
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
</style>