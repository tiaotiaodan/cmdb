import { createRouter, createWebHistory } from 'vue-router'
import LayoutView from '../layout/index.vue'
import Login from '../views/Login.vue'

const routes = [
  // 配置登陆导航
  {
    path: '/login',
    name: '登陆',
    component: Login
  },

  // 配置首页导航并强制跳转仪表盘
  {
    path: '/',
    name: '首页',
    component: LayoutView,
    redirect: '/dashboard', // 重定向跳转到仪表盘
    children: [
      {
        path: '/dashboard',
        name: '仪表盘',
        icon: 'HomeFilled',
        component: () => import('../views/Dashboard/index.vue')
      }
    ]
  },
  {
    path: '/host',
    name: '主机管理',
    icon: 'Platform',
    component: LayoutView,
    children: [
      {
        path: '/host/idc',
        name: '机房管理',
        component: () => import('../views/idc/index.vue')
      },
      {
        path: '/host/servergroup',
        name: '主机分组',
        component: () => import('../views/ServerGroup/index.vue')
      },
      {
        path: '/host/cloud_server',
        name: '云主机管理',
        component: () => import('../views/CloudServer/index.vue')
      },
      {
        path: '/host/physics_server',
        name: '物理主机管理',
        component: () => import('../views/PhysicsServer/index.vue')
      },
      {
        path: '/host/vm_server',
        name: '虚拟机管理',
        component: () => import('../views/VmServer/index.vue')
      }
    ]
  },
  {
    path: '/domain',
    name: '域名管理',
    icon: 'Setting',
    component: LayoutView,
    children: [
      {
        path: '/domain/domain_manage',
        name: '域名管理',
        component: () => import('../views/DomainManage/index.vue')
      },
      {
        path: '/domain/domain_analysis',
        name: '域名解析',
        component: () => import('../views/DomainAnalysis/index.vue')
      }
    ]
  },
  {
    path: '/ssl',
    name: '证书管理',
    icon: 'Setting',
    component: LayoutView,
    children: [
      {
        path: '/ssl/ssl_manage',
        name: '证书管理',
        component: () => import('../views/SslManage/index.vue')
      }
    ]
  },
  {
    path: '/software',
    name: '软件管理',
    icon: 'Setting',
    component: LayoutView,
    children: [
      {
        path: '/software/software_manage',
        name: '软件信息管理',
        component: () => import('../views/SoftwareManage/index.vue')
      }
    ]
  },
  {
    path: '/config',
    name: '系统配置',
    icon: 'Setting',
    component: LayoutView,
    children: [
      {
        path: '/config/credential',
        name: '凭据管理',
        component: () => import('../views/Credential/index.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 为路由对象，添加 beforeEach 导航守卫
router.beforeEach((to, form, next) => {
  /*
   to 将要访问的路径
   from 代表从那个路径跳转而来
   next 是一个函数，表示放行
      next() 放行   next('/login') 强制跳转
  */

  // 如果用户访问的登录页，直接放行
  if (to.path === '/login') return next()
  // 从 sessionStorage 中获取到 保存的 token 值
  const tokenStr = window.sessionStorage.getItem('token')
  // 没有token，强制跳转到登录页
  if (!tokenStr) return next('/login')
  next()
})

export default router
