import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(null)
  const loading = ref(false)

  // 计算属性
  const isAuthenticated = computed(() => !!token.value)

  // 检查登录状态
  const checkAuthStatus = async () => {
    try {
      loading.value = true
      const response = await authAPI.checkStatus()
      if (response.success && response.data?.isLoggedIn) {
        token.value = localStorage.getItem('token') || 'has-token'
        user.value = response.data.user
        return true
      }
      token.value = ''
      user.value = null
      return false
    } catch (error) {
      token.value = ''
      user.value = null
      return false
    } finally {
      loading.value = false
    }
  }

  // 登录
  const login = async (username, password) => {
    try {
      loading.value = true
      const response = await authAPI.login({ username, password })
      if (response.success) {
        token.value = 'logged-in'
        user.value = response.data
        localStorage.setItem('token', token.value)
        return { success: true }
      }
      return { success: false, message: response.message }
    } catch (error) {
      return { success: false, message: error.message || '登录失败' }
    } finally {
      loading.value = false
    }
  }

  // 登出
  const logout = async () => {
    try {
      await authAPI.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      token.value = ''
      user.value = null
      localStorage.removeItem('token')
    }
  }

  return {
    token,
    user,
    loading,
    isAuthenticated,
    checkAuthStatus,
    login,
    logout
  }
})