<template>
  <div class="work-order-form-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>{{ isEditMode ? '编辑工单' : '创建工单' }}</span>
        </div>
      </template>

      <!-- 批量替换区域（仅编辑模式显示） -->
      <div v-if="isEditMode" class="batch-replace-section">
        <el-divider content-position="left">批量替换日期</el-divider>
        <div class="batch-replace-form">
          <el-form-item label="原始日期">
            <el-date-picker
              v-model="originalDate"
              type="date"
              placeholder="选择原始日期"
              style="width: 200px"
            />
          </el-form-item>
          <el-form-item label="替换日期">
            <el-date-picker
              v-model="replaceDate"
              type="date"
              placeholder="选择替换日期"
              style="width: 200px"
            />
          </el-form-item>
          <el-button type="primary" @click="batchReplaceDates">批量替换</el-button>
        </div>
      </div>

      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="140px"
        class="work-order-form"
      >
        <!-- 左侧可折叠目录导航 -->
        <div class="form-layout">
          <div class="sidebar-nav">
            <el-affix :offset="0">
              <el-menu
                :default-active="activeSection"
                class="section-menu"
                @select="handleSectionSelect"
              >
                <el-menu-item index="basic">基本信息</el-menu-item>
                <el-menu-item index="detail">详情信息</el-menu-item>
                <el-menu-item index="operation">操作记录</el-menu-item>
                <el-menu-item index="product">产品信息</el-menu-item>
                <el-menu-item index="node">节点信息</el-menu-item>
                <el-menu-item index="settlement">结算信息</el-menu-item>
                <el-menu-item index="attachment">附件上传</el-menu-item>
                <el-menu-item index="service-require">子信息阅读栏</el-menu-item>
              </el-menu>
            </el-affix>
          </div>

          <!-- 右侧表单主体 -->
          <div class="form-main">
            <!-- Section 1: 基本信息 -->
            <div id="basic" class="form-section">
              <h3 class="section-title">基本信息</h3>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="工单编号" prop="orderid">
                    <el-input
                      v-model="formData.orderid"
                      placeholder="请输入工单编号"
                      :disabled="isEditMode"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="新工单编号" prop="newOrderid">
                    <el-input v-model="formData.newOrderid" placeholder="请输入新工单编号" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="联系人姓名" prop="contactName">
                    <el-input v-model="formData.contactName" placeholder="请输入联系人姓名" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="联系人手机号" prop="contactPhone">
                    <el-input v-model="formData.contactPhone" placeholder="请输入联系人手机号" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="创建时间" prop="createdDate">
                    <el-date-picker
                      v-model="formData.createdDate"
                      type="datetime"
                      placeholder="选择创建时间"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="预约开始时间" prop="appointmentStartTime">
                    <el-date-picker
                      v-model="formData.appointmentStartTime"
                      type="datetime"
                      placeholder="选择预约开始时间"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="预约结束时间" prop="appointmentEndTime">
                    <el-date-picker
                      v-model="formData.appointmentEndTime"
                      type="datetime"
                      placeholder="选择预约结束时间"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="完工时间" prop="completeTime">
                    <el-date-picker
                      v-model="formData.completeTime"
                      type="datetime"
                      placeholder="选择完工时间"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="评价时间" prop="evaluationTime">
                    <el-date-picker
                      v-model="formData.evaluationTime"
                      type="datetime"
                      placeholder="选择评价时间"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
              </el-row>
            </div>

            <!-- Section 2: 详情信息 -->
            <div id="detail" class="form-section">
              <h3 class="section-title">详情信息</h3>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="评价时间" prop="evaluationTime">
                    <el-date-picker
                      v-model="formData.evaluationTime"
                      type="datetime"
                      placeholder="选择评价时间"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="期望上门开始时间" prop="expectedStartTime">
                    <el-date-picker
                      v-model="formData.expectedStartTime"
                      type="datetime"
                      placeholder="选择期望上门开始时间"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="期望上门结束时间" prop="expectedEndTime">
                    <el-date-picker
                      v-model="formData.expectedEndTime"
                      type="datetime"
                      placeholder="选择期望上门结束时间"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="出库时间" prop="outboundTime">
                    <el-date-picker
                      v-model="formData.outboundTime"
                      type="datetime"
                      placeholder="选择出库时间"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="工单信息-签到定位" prop="signInLocation">
                    <el-input v-model="formData.signInLocation" placeholder="请输入签到定位" />
                  </el-form-item>
                </el-col>
              </el-row>
            </div>

            <!-- Section 3: 操作记录 -->
            <div id="operation" class="form-section">
              <h3 class="section-title">
                操作记录
                <el-button type="primary" size="small" :icon="Plus" @click="addOperationRecord">
                  添加操作记录
                </el-button>
              </h3>
              <el-table :data="formData.operationRecords" border style="width: 100%">
                <el-table-column label="操作记录时间" width="200">
                  <template #default="{ row, $index }">
                    <el-date-picker
                      v-model="row.lastModifiedDate"
                      type="datetime"
                      placeholder="选择时间"
                      style="width: 100%"
                    />
                  </template>
                </el-table-column>
                <el-table-column label="操作内容">
                  <template #default="{ row, $index }">
                    <el-input v-model="row.content" placeholder="请输入操作内容" />
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="80">
                  <template #default="{ $index }">
                    <el-button
                      type="danger"
                      size="small"
                      :icon="Delete"
                      @click="removeOperationRecord($index)"
                    />
                  </template>
                </el-table-column>
              </el-table>
            </div>

            <!-- Section 4: 产品信息 -->
            <div id="product" class="form-section">
              <h3 class="section-title">
                产品信息
                <el-button type="primary" size="small" :icon="Plus" @click="addProduct">
                  添加产品
                </el-button>
              </h3>
              <el-table :data="formData.products" border style="width: 100%">
                <el-table-column label="产品购买时间" width="200">
                  <template #default="{ row, $index }">
                    <el-date-picker
                      v-model="row.buyTime"
                      type="datetime"
                      placeholder="选择时间"
                      style="width: 100%"
                    />
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="80">
                  <template #default="{ $index }">
                    <el-button
                      type="danger"
                      size="small"
                      :icon="Delete"
                      @click="removeProduct($index)"
                    />
                  </template>
                </el-table-column>
              </el-table>
            </div>

            <!-- Section 5: 节点信息 -->
            <div id="node" class="form-section">
              <h3 class="section-title">节点信息</h3>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="网点完工时间">
                    <div class="node-hint">填写后自动创建4条相同数据</div>
                    <el-date-picker
                      v-model="formData.completeFeedbackTime"
                      type="datetime"
                      placeholder="选择完工时间"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="创建时间">
                    <div class="node-hint">1条记录</div>
                    <el-date-picker
                      v-model="formData.createdFeedbackTime"
                      type="datetime"
                      placeholder="选择创建时间"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="服务中时间">
                    <div class="node-hint">填写后自动创建3条相同数据</div>
                    <el-date-picker
                      v-model="formData.inServiceFeedbackTime"
                      type="datetime"
                      placeholder="选择服务中时间"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="派单时间">
                    <div class="node-hint">填写后自动创建3条相同数据</div>
                    <el-date-picker
                      v-model="formData.sendOrdersFeedbackTime"
                      type="datetime"
                      placeholder="选择派单时间"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
              </el-row>
            </div>

            <!-- Section 6: 结算信息 -->
            <div id="settlement" class="form-section">
              <h3 class="section-title">结算信息</h3>
              <el-row :gutter="20" style="margin-bottom: 20px;">
                <el-col :span="12">
                  <el-form-item label="购买时间">
                    <div class="node-hint">固定输入，只允许一个</div>
                    <el-date-picker
                      v-model="formData.settlementBuyTime"
                      type="datetime"
                      placeholder="选择购买时间"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="安装时间">
                    <div class="node-hint">固定输入，只允许一个</div>
                    <el-date-picker
                      v-model="formData.settlementInstallTime"
                      type="datetime"
                      placeholder="选择安装时间"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
              </el-row>
              <h4 style="margin-bottom: 10px;">操作时间（可填写多个）</h4>
              <div style="margin-bottom: 10px;">
                <el-button type="primary" size="small" :icon="Plus" @click="addSettlement">
                  添加操作时间
                </el-button>
              </div>
              <el-table :data="formData.settlementList" border style="width: 100%">
                <el-table-column label="操作时间" width="200">
                  <template #default="{ row, $index }">
                    <el-date-picker
                      v-model="row.fksj"
                      type="datetime"
                      placeholder="选择操作时间"
                      style="width: 100%"
                    />
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="80">
                  <template #default="{ $index }">
                    <el-button
                      type="danger"
                      size="small"
                      :icon="Delete"
                      @click="removeSettlement($index)"
                    />
                  </template>
                </el-table-column>
              </el-table>
            </div>

            <!-- Section 7: 子信息阅读栏 -->
            <div id="service-require" class="form-section">
              <h3 class="section-title">
                子信息阅读栏
                <el-button type="primary" size="small" :icon="Plus" @click="addServiceRequire">
                  添加子信息
                </el-button>
              </h3>
              <div class="service-requires">
                <div
                  v-for="(require, reqIndex) in formData.serviceRequirements"
                  :key="reqIndex"
                  class="service-require-item"
                >
                  <div class="service-require-header">
                    <span>子信息 {{ reqIndex + 1 }}</span>
                    <el-button
                      type="danger"
                      size="small"
                      :icon="Delete"
                      @click="removeServiceRequire(reqIndex)"
                    />
                  </div>
                  <el-form-item label="子信息类型">
                    <el-input v-model="require.serviceRequireTypeDesc" placeholder="请输入子信息类型" />
                  </el-form-item>
                  <el-form-item label="子信息内容">
                    <el-input v-model="require.serviceRequireContent" placeholder="请输入子信息内容" />
                  </el-form-item>
                  <el-form-item label="操作时间">
                    <el-date-picker
                      v-model="require.createdDate"
                      type="datetime"
                      placeholder="选择操作时间"
                      style="width: 100%"
                    />
                  </el-form-item>
                </div>
              </div>
            </div>

            <!-- Section 8: 附件上传 -->
            <div id="attachment" class="form-section">
              <h3 class="section-title">
                附件上传
                <el-button type="primary" size="small" :icon="Plus" @click="addAttachmentGroup">
                  添加附件组
                </el-button>
              </h3>
              <div class="attachment-groups">
                <div
                  v-for="(group, groupIndex) in formData.attachmentGroups"
                  :key="groupIndex"
                  class="attachment-group"
                >
                  <div class="attachment-group-header">
                    <span>附件组 {{ groupIndex + 1 }}</span>
                    <el-button
                      type="danger"
                      size="small"
                      :icon="Delete"
                      @click="removeAttachmentGroup(groupIndex)"
                    />
                  </div>
                  <div
                    v-for="(img, imgIndex) in group.imgreplace"
                    :key="imgIndex"
                    class="img-item"
                  >
                    <el-form-item label="图片名称">
                      <el-input v-model="img.annexName" placeholder="请输入图片名称（如：内机条码图）" />
                    </el-form-item>
                    <el-form-item label="上传图片">
                      <div style="display: flex; align-items: center; gap: 10px;">
                        <el-upload
                          :ref="el => setUploadRef(el, groupIndex, imgIndex)"
                          :file-list="img.fileList || []"
                          action="/api/work-orders/upload"
                          list-type="picture-card"
                          :on-success="(res) => handleUploadSuccess(res, group, imgIndex)"
                          :on-remove="(file, fileList) => handleUploadRemove(file, fileList, group, imgIndex)"
                          :before-upload="beforeUpload"
                          :limit="1"
                          style="flex: 1;"
                        >
                          <el-icon><Plus /></el-icon>
                        </el-upload>
                        <el-button
                          type="danger"
                          size="small"
                          :icon="Delete"
                          @click="removeImgItem(groupIndex, imgIndex)"
                          class="remove-img-btn"
                        >
                          移除
                        </el-button>
                      </div>
                    </el-form-item>
                  </div>
                  <el-button
                    type="primary"
                    size="small"
                    :icon="Plus"
                    @click="addImgItem(groupIndex)"
                    class="add-img-btn"
                  >
                    添加图片
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-form>

      <!-- 底部固定保存/取消按钮 -->
      <div class="form-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          保存
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus, Delete } from '@element-plus/icons-vue'
import { workOrdersAPI } from '@/api'

const router = useRouter()
const route = useRoute()
const formRef = ref(null)
const submitting = ref(false)
const loading = ref(false)
const activeSection = ref('basic')

const isEditMode = computed(() => !!route.params.id)
const formId = computed(() => route.params.id)

// 表单数据
const formData = reactive({
  // 基本信息
  orderid: '',
  newOrderid: '',
  contactName: '',
  contactPhone: '',
  createdDate: null,
  appointmentStartTime: null,
  appointmentEndTime: null,
  completeTime: null,
  evaluationTime: null,

  // 详情信息
  expectedStartTime: null,
  expectedEndTime: null,
  outboundTime: null,
  signInLocation: '',

  // 操作记录
  operationRecords: [],

  // 产品信息
  products: [],

  // 节点信息（单个值，提交时自动生成多条）
  completeFeedbackTime: null,
  createdFeedbackTime: null,
  inServiceFeedbackTime: null,
  sendOrdersFeedbackTime: null,

  // 结算信息
  settlementBuyTime: null,
  settlementInstallTime: null,
  settlementList: [],

  // 附件上传 - download结构
  // 每个group是一个imgreplace，包含多个图片
  attachmentGroups: [],

  // 子信息阅读栏
  serviceRequirements: []
})

// upload组件ref映射
const uploadRefs = ref({})

// 批量替换日期相关变量
const originalDate = ref(null)
const replaceDate = ref(null)

// 批量替换日期函数
const batchReplaceDates = () => {
  if (!originalDate.value || !replaceDate.value) {
    ElMessage.warning('请选择原始日期和替换日期')
    return
  }

  // 格式化日期为 YYYY-MM-DD
  const formatDate = (date) => {
    const d = new Date(date)
    const year = d.getFullYear()
    const month = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  }

  const originalDateStr = formatDate(originalDate.value)
  const replaceDateStr = formatDate(replaceDate.value)

  // 替换日期时间对象中的日期部分
  const replaceDateInDateTime = (dateObj) => {
    if (!dateObj) return dateObj
    const d = new Date(dateObj)
    const newDate = new Date(replaceDate.value)
    d.setFullYear(newDate.getFullYear())
    d.setMonth(newDate.getMonth())
    d.setDate(newDate.getDate())
    return d
  }

  // 替换文本中的日期
  const replaceDateInText = (text) => {
    if (!text) return text
    // 匹配 YYYY-MM-DD 格式的日期
    const regex = new RegExp(originalDateStr.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&'), 'g')
    return text.replace(regex, replaceDateStr)
  }

  // 递归处理对象中的所有字段
  const processObject = (obj) => {
    if (!obj) return

    for (const key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        const value = obj[key]

        // 处理 Date 类型
        if (value instanceof Date) {
          const valueDateStr = formatDate(value)
          if (valueDateStr === originalDateStr) {
            obj[key] = replaceDateInDateTime(value)
          }
        }
        // 处理 String 类型
        else if (typeof value === 'string') {
          obj[key] = replaceDateInText(value)
        }
        // 处理 Array 类型
        else if (Array.isArray(value)) {
          value.forEach(item => {
            if (typeof item === 'object' && item !== null) {
              processObject(item)
            } else if (typeof item === 'string') {
              // 直接替换数组中的字符串
              const index = value.indexOf(item)
              value[index] = replaceDateInText(item)
            }
          })
        }
        // 处理嵌套 Object 类型
        else if (typeof value === 'object' && value !== null) {
          processObject(value)
        }
      }
    }
  }

  // 处理 formData 中的所有数据
  processObject(formData)

  ElMessage.success('批量替换完成')
}

// 表单验证规则
const formRules = {
  orderid: [
    { required: true, message: '请输入工单编号', trigger: 'blur' }
  ],
  contactName: [
    { required: true, message: '请输入联系人姓名', trigger: 'blur' }
  ],
  contactPhone: [
    { required: true, message: '请输入联系人手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ]
}

// 添加操作记录
const addOperationRecord = () => {
  formData.operationRecords.push({
    lastModifiedDate: null,
    content: ''
  })
}

// 移除操作记录
const removeOperationRecord = (index) => {
  formData.operationRecords.splice(index, 1)
}

// 添加产品
const addProduct = () => {
  formData.products.push({
    buyTime: null
  })
}

// 移除产品
const removeProduct = (index) => {
  formData.products.splice(index, 1)
}

// 添加结算记录
const addSettlement = () => {
  formData.settlementList.push({
    fksj: null
  })
}

// 移除结算记录
const removeSettlement = (index) => {
  formData.settlementList.splice(index, 1)
}

// 添加附件组
const addAttachmentGroup = () => {
  formData.attachmentGroups.push({
    imgreplace: []
  })
}

// 移除附件组
const removeAttachmentGroup = (index) => {
  formData.attachmentGroups.splice(index, 1)
}

// 添加图片项到指定组
const addImgItem = (groupIndex) => {
  formData.attachmentGroups[groupIndex].imgreplace.push({
    annexName: '',
    imageFilePath: '',
    fileList: []
  })
}

// 移除图片项
const removeImgItem = (groupIndex, imgIndex) => {
  formData.attachmentGroups[groupIndex].imgreplace.splice(imgIndex, 1)
}

// 添加子信息
const addServiceRequire = () => {
  formData.serviceRequirements.push({
    serviceRequireTypeDesc: '',
    serviceRequireContent: '',
    createdDate: null
  })
}

// 移除子信息
const removeServiceRequire = (index) => {
  formData.serviceRequirements.splice(index, 1)
}

// 设置upload组件ref
const setUploadRef = (el, groupIndex, imgIndex) => {
  if (el) {
    const key = `${groupIndex}-${imgIndex}`
    uploadRefs.value[key] = el
  }
}

// 上传成功回调
const handleUploadSuccess = (response, group, imgIndex) => {
  if (response.success) {
    // 保存返回的图片路径
    group.imgreplace[imgIndex].imageFilePath = response.data.path
    ElMessage.success('上传成功')
  } else {
    ElMessage.error(response.message || '上传失败')
  }
}

// 上传移除回调
const handleUploadRemove = (file, fileList, group, imgIndex) => {
  group.imgreplace[imgIndex].fileList = fileList
  if (fileList.length === 0) {
    group.imgreplace[imgIndex].imageFilePath = ''
  }
}

// 上传前校验
const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('只能上传图片文件')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过10MB')
    return false
  }
  return true
}

// 重置表单
const resetForm = () => {
  formData.orderid = ''
  formData.newOrderid = ''
  formData.contactName = ''
  formData.contactPhone = ''
  formData.createdDate = null
  formData.appointmentStartTime = null
  formData.appointmentEndTime = null
  formData.completeTime = null
  formData.evaluationTime = null
  formData.expectedStartTime = null
  formData.expectedEndTime = null
  formData.outboundTime = null
  formData.signInLocation = ''
  formData.operationRecords.splice(0, formData.operationRecords.length)
  formData.products.splice(0, formData.products.length)
  formData.completeFeedbackTime = null
  formData.createdFeedbackTime = null
  formData.inServiceFeedbackTime = null
  formData.sendOrdersFeedbackTime = null
  formData.settlementBuyTime = null
  formData.settlementInstallTime = null
  formData.settlementList.splice(0, formData.settlementList.length)
  formData.attachmentGroups.splice(0, formData.attachmentGroups.length)
  formData.serviceRequirements.splice(0, formData.serviceRequirements.length)
}

// 目录导航选中
const handleSectionSelect = (index) => {
  activeSection.value = index
  const element = document.getElementById(index)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

// 加载工单详情
const loadWorkOrderDetail = async () => {
  if (!formId.value) return

  loading.value = true
  try {
    const response = await workOrdersAPI.getDetail(formId.value)
    if (response.success) {
      const data = response.data

      // 重置表单
      resetForm()

      // 设置工单编号
      formData.orderid = data.orderid || ''

      // 从searchWorkOrderListEs中提取基本信息
      const listEs = data.searchWorkOrderListEs || []
      listEs.forEach(item => {
        const key = item.key
        const value = item.value
        if (key === 'newOrderid') formData.newOrderid = value || ''
        if (key === 'contactName') formData.contactName = value
        if (key === 'contactPhone') formData.contactPhone = value
        if (key === 'createdDate') formData.createdDate = value ? new Date(value) : null
        if (key === 'appointBeginTime') formData.appointmentStartTime = value ? new Date(value) : null
        if (key === 'appointEndTime') formData.appointmentEndTime = value ? new Date(value) : null
        if (key === 'workOrderCompleteTime') formData.completeTime = value ? new Date(value) : null
        if (key === 'lastEvaluationTime') formData.evaluationTime = value ? new Date(value) : null
      })

      // 从searchWorkOrderDetail中提取详情信息
      const detail = data.searchWorkOrderDetail || []
      detail.forEach(item => {
        const key = item.key
        const value = item.value
        if (key === 'evaluationTime') formData.evaluationTime = value ? new Date(value) : null
        if (key === 'appointBeginTime') formData.appointmentStartTime = value ? new Date(value) : null
        if (key === 'appointEndTime') formData.appointmentEndTime = value ? new Date(value) : null
        if (key === 'expectDoorToDoorBeginTime') formData.expectedStartTime = value ? new Date(value) : null
        if (key === 'expectDoorToDoorEndTime') formData.expectedEndTime = value ? new Date(value) : null
        if (key === 'deliveryTime') formData.outboundTime = value ? new Date(value) : null
        if (key === 'signInLocation') formData.signInLocation = value || ''
        if (key === 'lastModifiedDate' || key === 'content') {
          if (item.path && item.path.includes('workOrderFeedbackRespList')) {
            const match = item.path.match(/workOrderFeedbackRespList\[(\d+)\]/)
            if (match) {
              const idx = parseInt(match[1])
              while (formData.operationRecords.length <= idx) {
                formData.operationRecords.push({ lastModifiedDate: null, content: '' })
              }
              if (key === 'lastModifiedDate') {
                formData.operationRecords[idx].lastModifiedDate = value ? new Date(value) : null
              }
              if (key === 'content') {
                formData.operationRecords[idx].content = value || ''
              }
            }
          }
        }
      })

      // 从getWorkOrderDetailList中提取产品购买时间
      const products = data.getWorkOrderDetailList || []
      products.forEach(item => {
        if (item.key === 'buyTime' && item.path && item.path.includes('workOrderDetailProductInfoVOList')) {
          const match = item.path.match(/workOrderDetailProductInfoVOList\[(\d+)\]/)
          if (match) {
            const idx = parseInt(match[1])
            while (formData.products.length <= idx) {
              formData.products.push({ buyTime: null })
            }
            formData.products[idx].buyTime = item.value ? new Date(item.value) : null
          }
        }
      })

      // 从searchAzWgmxDetail中提取结算信息
      const settlements = data.searchAzWgmxDetail || []
      formData.settlementList = []
      settlements.forEach(item => {
        if (item.key === 'gmsj') {
          // 购买时间 - 固定输入
          formData.settlementBuyTime = item.value ? new Date(item.value) : null
        } else if (item.key === 'scazsj') {
          // 安装时间 - 固定输入
          formData.settlementInstallTime = item.value ? new Date(item.value) : null
        } else if (item.key === 'fksj' && item.path && item.path.includes('azdMxSpgcList')) {
          // 操作时间 - 可填写多个
          const match = item.path.match(/azdMxSpgcList\[(\d+)\]/)
          if (match) {
            const idx = parseInt(match[1])
            while (formData.settlementList.length <= idx) {
              formData.settlementList.push({ fksj: null })
            }
            formData.settlementList[idx].fksj = item.value ? new Date(item.value) : null
          }
        }
      })

      // 从searchWorkOrderNodeResp中提取节点信息
      const nodes = data.searchWorkOrderNodeResp || []
      const completeList = []
      const createdList = []
      const inServiceList = []
      const sendOrdersList = []
      nodes.forEach(item => {
        if (item.path && item.value) {
          const nodeData = { createdDate: item.value ? new Date(item.value) : null }
          if (item.path.includes('completeFeedbackList')) completeList.push(nodeData)
          if (item.path.includes('createdFeedbackList')) createdList.push(nodeData)
          if (item.path.includes('inServiceFeedbackList')) inServiceList.push(nodeData)
          if (item.path.includes('sendOrdersFeedbackList')) sendOrdersList.push(nodeData)
        }
      })
      if (completeList.length > 0) formData.completeFeedbackTime = completeList[0].createdDate
      if (createdList.length > 0) formData.createdFeedbackTime = createdList[0].createdDate
      if (inServiceList.length > 0) formData.inServiceFeedbackTime = inServiceList[0].createdDate
      if (sendOrdersList.length > 0) formData.sendOrdersFeedbackTime = sendOrdersList[0].createdDate

      // 从download中提取附件
      const download = data.download || []
      formData.attachmentGroups = download.map(group => ({
        imgreplace: (group.imgreplace || []).map(img => {
          const imagePath = (img.imageFilePath || '').trim()
          return {
            annexName: img.annexName || '',
            imageFilePath: imagePath,
            fileList: imagePath ? [{
              name: imagePath.split('/').pop(),
              url: imagePath.startsWith('http') ? imagePath : `/api/work-orders/uploads/${imagePath}`
            }] : []
          }
        })
      }))

      // 从getServiceRequireByPage中提取子信息阅读栏数据
      const serviceRequireList = data.getServiceRequireByPage || []
      const serviceRequireMap = {}
      serviceRequireList.forEach(item => {
        const key = item.key
        const value = item.value
        const path = item.path || ''
        const match = path.match(/data\[(\d+)\]/)
        if (match) {
          const idx = parseInt(match[1])
          if (!serviceRequireMap[idx]) {
            serviceRequireMap[idx] = {
              serviceRequireTypeDesc: '',
              serviceRequireContent: '',
              createdDate: null
            }
          }
          if (key === 'serviceRequireTypeDesc') {
            serviceRequireMap[idx].serviceRequireTypeDesc = value || ''
          } else if (key === 'serviceRequireContent') {
            serviceRequireMap[idx].serviceRequireContent = value || ''
          } else if (key === 'createdDate') {
            serviceRequireMap[idx].createdDate = value ? new Date(value) : null
          }
        }
      })
      formData.serviceRequirements = Object.keys(serviceRequireMap)
        .sort((a, b) => parseInt(a) - parseInt(b))
        .map(key => serviceRequireMap[key])
    } else {
      ElMessage.error(response.message || '加载工单详情失败')
    }
  } catch (error) {
    ElMessage.error('加载工单详情失败')
  } finally {
    loading.value = false
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitting.value = true
    try {
      // 将节点信息单个值转换为数组
      const completeFeedbackList = []
      for (let i = 0; i < 4; i++) {
        completeFeedbackList.push({
          createdDate: formData.completeFeedbackTime ? formData.completeFeedbackTime.toISOString() : null
        })
      }

      const createdFeedbackList = [{
        createdDate: formData.createdFeedbackTime ? formData.createdFeedbackTime.toISOString() : null
      }]

      const inServiceFeedbackList = []
      for (let i = 0; i < 3; i++) {
        inServiceFeedbackList.push({
          createdDate: formData.inServiceFeedbackTime ? formData.inServiceFeedbackTime.toISOString() : null
        })
      }

      const sendOrdersFeedbackList = []
      for (let i = 0; i < 3; i++) {
        sendOrdersFeedbackList.push({
          createdDate: formData.sendOrdersFeedbackTime ? formData.sendOrdersFeedbackTime.toISOString() : null
        })
      }

      // 构建结算数据 - 把购买时间和安装时间放到每个结算记录中
      const settlementData = formData.settlementList.map(item => ({
        fksj: item.fksj ? item.fksj.toISOString() : null,
        gmsj: formData.settlementBuyTime ? formData.settlementBuyTime.toISOString() : null,
        scazsj: formData.settlementInstallTime ? formData.settlementInstallTime.toISOString() : null
      }))

      const submitData = {
        ...formData,
        // 格式化时间字段
        createdDate: formData.createdDate ? formData.createdDate.toISOString() : null,
        appointmentStartTime: formData.appointmentStartTime ? formData.appointmentStartTime.toISOString() : null,
        appointmentEndTime: formData.appointmentEndTime ? formData.appointmentEndTime.toISOString() : null,
        completeTime: formData.completeTime ? formData.completeTime.toISOString() : null,
        evaluationTime: formData.evaluationTime ? formData.evaluationTime.toISOString() : null,
        expectedStartTime: formData.expectedStartTime ? formData.expectedStartTime.toISOString() : null,
        expectedEndTime: formData.expectedEndTime ? formData.expectedEndTime.toISOString() : null,
        outboundTime: formData.outboundTime ? formData.outboundTime.toISOString() : null,
        // 节点数组
        completeFeedbackList,
        createdFeedbackList,
        inServiceFeedbackList,
        sendOrdersFeedbackList,
        // 结算数组
        settlementList: settlementData,
        // 子信息阅读栏
        serviceRequirements: formData.serviceRequirements.map(item => ({
          serviceRequireTypeDesc: item.serviceRequireTypeDesc,
          serviceRequireContent: item.serviceRequireContent,
          createdDate: item.createdDate ? item.createdDate.toISOString() : null
        }))
      }

      let response
      if (isEditMode.value) {
        response = await workOrdersAPI.update(formId.value, submitData)
      } else {
        response = await workOrdersAPI.create(submitData)
      }

      if (response.success) {
        ElMessage.success(isEditMode.value ? '更新成功' : '创建成功')
        router.push({ name: 'WorkOrderList' })
      } else {
        ElMessage.error(response.message || '操作失败')
      }
    } catch (error) {
      ElMessage.error(error.message || '操作失败')
    } finally {
      submitting.value = false
    }
  })
}

// 取消
const handleCancel = () => {
  router.push({ name: 'WorkOrderList' })
}

onMounted(() => {
  if (isEditMode.value) {
    loadWorkOrderDetail()
  }
})
</script>

<style scoped>
.work-order-form-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.batch-replace-section {
  margin-bottom: 20px;
  padding: 15px 20px;
  background: #f0f9ff;
  border-radius: 4px;
}

.batch-replace-form {
  display: flex;
  align-items: flex-end;
  gap: 20px;
  flex-wrap: wrap;
}

.batch-replace-form .el-form-item {
  margin-bottom: 0;
}

.form-layout {
  display: flex;
  gap: 20px;
}

.sidebar-nav {
  width: 200px;
  flex-shrink: 0;
}

.section-menu {
  border-right: 1px solid #dcdfe6;
}

.form-main {
  flex: 1;
  max-height: calc(100vh - 250px);
  overflow-y: auto;
  padding-right: 10px;
}

.form-section {
  margin-bottom: 40px;
  padding: 20px;
  background: #fafafa;
  border-radius: 4px;
}

.section-title {
  margin: 0 0 20px 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.node-hint {
  font-size: 12px;
  color: #909399;
  margin-bottom: 5px;
}

.attachment-groups {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.attachment-group {
  padding: 15px;
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
}

.attachment-group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  font-weight: bold;
}

.service-requires {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.service-require-item {
  padding: 15px;
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
}

.service-require-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  font-weight: bold;
}

.form-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 15px 30px;
  background: #fff;
  border-top: 1px solid #e4e7ed;
  display: flex;
  justify-content: center;
  gap: 15px;
  z-index: 100;
}

:deep(.el-form-item) {
  margin-bottom: 18px;
}
</style>
