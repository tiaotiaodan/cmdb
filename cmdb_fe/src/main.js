import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// 导入elementui和css
import Elementplus from 'element-plus'
import 'element-plus/dist/index.css'

// 注册icon图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
// 使用中文
import locale from 'element-plus/lib/locale/lang/zh-cn'

// 导入axios封装模块
import axios from './api/http'

// 创建实例
const app = createApp(App)

// 统一注册el-icon图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// axios全局注册
app.config.globalProperties.$http = axios
// 设置请求默认路径
app.config.globalProperties.$wsbaseURL = "ws://127.0.0.1:8000/server/terminal"


// 注册store
app.use(store)
// 注册router
app.use(router)
// 注册Elementplus并用中文国际化显示
app.use(Elementplus, { locale })
// 挂载实例
app.mount('#app')
