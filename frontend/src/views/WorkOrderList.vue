<template>
  <div class="work-order-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>工单管理</span>
          <el-button type="primary" :icon="Plus" @click="openAddDialog">
            创建工单
          </el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="工单ID">
            <el-input
              v-model="searchForm.orderid"
              placeholder="请输入工单ID"
              clearable
              style="width: 200px"
            />
          </el-form-item>
          <el-form-item label="联系人手机">
            <el-input
              v-model="searchForm.contactPhone"
              placeholder="请输入联系人手机号"
              clearable
              style="width: 200px"
            />
          </el-form-item>
          <el-form-item label="联系人姓名">
            <el-input
              v-model="searchForm.contactName"
              placeholder="请输入联系人姓名"
              clearable
              style="width: 200px"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :icon="Search" @click="handleSearch">
              搜索
            </el-button>
            <el-button :icon="Refresh" @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 工单表格 -->
      <el-table
        v-loading="loading"
        :data="workOrders"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="orderid" label="工单编号" width="180" />
        <el-table-column prop="newOrderid" label="新工单编号" width="180" />
        <el-table-column prop="contactName" label="联系人姓名" width="120" />
        <el-table-column prop="contactPhone" label="联系人手机" width="150" />
        <el-table-column prop="createdDate" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.createdDate) }}
          </template>
        </el-table-column>
        <el-table-column prop="appointmentStartTime" label="预约开始时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.appointmentStartTime) }}
          </template>
        </el-table-column>
        <el-table-column prop="appointmentEndTime" label="预约结束时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.appointmentEndTime) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button
              type="warning"
              size="small"
              :icon="Edit"
              @click="handleEdit(row)"
            >
              编辑
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

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Refresh, Edit, Delete } from '@element-plus/icons-vue'
import { workOrdersAPI } from '@/api'

const router = useRouter()

const loading = ref(false)
const workOrders = ref([])

const searchForm = reactive({
  orderid: '',
  contactPhone: '',
  contactName: ''
})

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

const loadWorkOrders = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      pageSize: pagination.pageSize
    }
    if (searchForm.orderid) {
      params.orderid = searchForm.orderid
    }
    if (searchForm.contactPhone) {
      params.contactPhone = searchForm.contactPhone
    }
    if (searchForm.contactName) {
      params.contactName = searchForm.contactName
    }

    const response = await workOrdersAPI.getList(params)
    if (response.success) {
      const rawData = response.data.records || response.data || []
      workOrders.value = rawData.map(item => ({
        ...item,
        newOrderid: item.new_orderid,
        contactName: item.contact_name,
        contactPhone: item.contact_phone,
        createdDate: item.created_date,
        appointmentStartTime: item.appoint_begin_time,
        appointmentEndTime: item.appoint_end_time,
        workOrderCompleteTime: item.work_order_complete_time,
        lastEvaluationTime: item.last_evaluation_time
      }))
      pagination.total = response.data.total || workOrders.value.length
    } else {
      ElMessage.error(response.message || '加载工单列表失败')
    }
  } catch (error) {
    ElMessage.error('加载工单列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadWorkOrders()
}

const handleReset = () => {
  searchForm.orderid = ''
  searchForm.contactPhone = ''
  searchForm.contactName = ''
  pagination.page = 1
  loadWorkOrders()
}

const handleSizeChange = (val) => {
  pagination.pageSize = val
  pagination.page = 1
  loadWorkOrders()
}

const handleCurrentChange = (val) => {
  pagination.page = val
  loadWorkOrders()
}

const openAddDialog = () => {
  router.push({ name: 'WorkOrderCreate' })
}

const handleEdit = (row) => {
  router.push({ name: 'WorkOrderEdit', params: { id: row.id } })
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除工单 "${row.orderid}" 吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const response = await workOrdersAPI.delete(row.id)
    if (response.success) {
      ElMessage.success('删除成功')
      await loadWorkOrders()
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
  loadWorkOrders()
})
</script>

<style scoped>
.work-order-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-bar {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
