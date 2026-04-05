import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response
      if (status === 401) {
        // 未授权，清除token并跳转登录
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
      return Promise.reject({ status, message: data.message || '请求失败' })
    }
    return Promise.reject({ status: -1, message: '网络错误' })
  }
)

// 认证相关API
export const authAPI = {
  login: (data) => api.post('/login', data),
  logout: () => api.post('/logout'),
  checkStatus: () => api.get('/auth/status')
}

// 账号管理API
export const accountsAPI = {
  getList: () => api.get('/accounts'),
  add: (data) => api.post('/accounts', data),
  updatePassword: (id, password) => api.put(`/accounts/${id}/password`, { password }),
  delete: (id) => api.delete(`/accounts/${id}`)
}

// 工单管理API
export const workOrdersAPI = {
  getList: (params) => api.get('/work-orders', { params }),
  getDetail: (id) => api.get(`/work-orders/${id}`),
  create: (data) => api.post('/work-orders', data),
  update: (id, data) => api.put(`/work-orders/${id}`, data),
  delete: (id) => api.delete(`/work-orders/${id}`),
  search: (params) => api.get('/work-orders/search', { params }),
  upload: (data) => api.post('/work-orders/upload', data)
}

export default api