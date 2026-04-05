<template>
  <div class="account-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>账号管理</span>
          <el-button type="primary" :icon="Plus" @click="openAddDialog">
            添加账号
          </el-button>
        </div>
      </template>

      <el-table :data="accounts" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="created_at" label="创建时间">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              :icon="Edit"
              @click="openEditDialog(row)"
            >
              修改密码
            </el-button>
            <el-button
              type="danger"
              size="small"
              :icon="Delete"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/修改密码对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="400px"
      @close="resetForm"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username" v-if="isAddMode">
          <el-input v-model="formData.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item v-else label="用户名">
          <el-input v-model="formData.username" disabled />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="formData.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import { accountsAPI } from '@/api'

const accounts = ref([])
const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const currentEditId = ref(null)

const formData = reactive({
  username: '',
  password: ''
})

const formRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ]
}

const isAddMode = computed(() => currentEditId.value === null)
const dialogTitle = computed(() => isAddMode.value ? '添加账号' : '修改密码')

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

const loadAccounts = async () => {
  try {
    const response = await accountsAPI.getList()
    if (response.success) {
      accounts.value = response.data
    }
  } catch (error) {
    ElMessage.error('加载账号列表失败')
  }
}

const openAddDialog = () => {
  currentEditId.value = null
  formData.username = ''
  formData.password = ''
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  currentEditId.value = row.id
  formData.username = row.username
  formData.password = ''
  dialogVisible.value = true
}

const resetForm = () => {
  formRef.value?.resetFields()
  formData.username = ''
  formData.password = ''
  currentEditId.value = null
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitting.value = true
    try {
      if (isAddMode.value) {
        // 添加账号
        const response = await accountsAPI.add({
          username: formData.username,
          password: formData.password
        })
        if (response.success) {
          ElMessage.success('添加成功')
          dialogVisible.value = false
          await loadAccounts()
        } else {
          ElMessage.error(response.message || '添加失败')
        }
      } else {
        // 修改密码
        const response = await accountsAPI.updatePassword(
          currentEditId.value,
          formData.password
        )
        if (response.success) {
          ElMessage.success('密码修改成功')
          dialogVisible.value = false
          await loadAccounts()
        } else {
          ElMessage.error(response.message || '修改失败')
        }
      }
    } catch (error) {
      ElMessage.error(error.message || '操作失败')
    } finally {
      submitting.value = false
    }
  })
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除账号 "${row.username}" 吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const response = await accountsAPI.delete(row.id)
    if (response.success) {
      ElMessage.success('删除成功')
      await loadAccounts()
    } else {
      ElMessage.error(response.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadAccounts()
})
</script>

<style scoped>
.account-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>