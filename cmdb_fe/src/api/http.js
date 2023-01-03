import axios from 'axios'
import { ElMessage } from 'element-plus'

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 5000
  // headers: {'X-Custom-Header': 'foobar'}
})

// 拦截器：请求拦截
instance.interceptors.request.use(
  config => {
    // 在请求被发送之前做些什么
    const token = window.sessionStorage.getItem('token')
    if (token) {
      config.headers = {
        Authorization: 'token' + token
      }
    }
    return config
  },
  error => {
    // 处理请求错误
    return Promise.reject(error)
  }
)

// 拦截器： 响应拦截
instance.interceptors.response.use(
  response => {
    // console.log('响应拦截处理');
    if (response.data.code != 200) {
      ElMessage.warning(response.data.msg) // 这里应根据后端返回消息显示
    }
    return response
  },
  error => {
    // 处理响应错误（catch）
    ElMessage.error('请求服务端接口错误：' + error.message)
    return Promise.reject(error)
  }
)

// 导出实例
export default instance
