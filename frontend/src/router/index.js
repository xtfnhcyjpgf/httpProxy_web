import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/components/Layout.vue'),
    redirect: '/index',
    meta: { requiresAuth: true },
    children: [
      {
        path: '/index',
        name: 'Index',
        component: () => import('@/views/Index.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/accounts',
        name: 'Accounts',
        component: () => import('@/views/Account.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/work-orders',
        name: 'WorkOrderList',
        component: () => import('@/views/WorkOrderList.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/work-orders/create',
        name: 'WorkOrderCreate',
        component: () => import('@/views/WorkOrderForm.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/work-orders/:id',
        name: 'WorkOrderDetail',
        component: () => import('@/views/WorkOrderForm.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/work-orders/:id/edit',
        name: 'WorkOrderEdit',
        component: () => import('@/views/WorkOrderForm.vue'),
        meta: { requiresAuth: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // 检查是否需要登录
  if (to.meta.requiresAuth) {
    // 尝试获取登录状态
    if (!authStore.isAuthenticated) {
      try {
        await authStore.checkAuthStatus()
      } catch (error) {
        // 未登录，跳转到登录页
        next({ name: 'Login' })
        return
      }
    }

    // 已登录，允许访问
    if (authStore.isAuthenticated) {
      next()
    } else {
      // 未登录，跳转到登录页
      next({ name: 'Login' })
    }
  } else {
    // 不需要登录的页面
    if (to.name === 'Login' && authStore.isAuthenticated) {
      // 已登录访问登录页，跳转到首页
      next({ name: 'Index' })
    } else {
      next()
    }
  }
})

export default router