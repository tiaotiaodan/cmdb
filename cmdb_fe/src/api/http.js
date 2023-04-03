import axios from 'axios'
import { ElMessage } from 'element-plus'

const instance = axios.create({
  // api请求地址，根据实际需求修改
  baseURL: 'http://127.0.0.1:8000/',
  timeout: 30000   // 超时时间，默认是ms秒单位
  // headers: {'X-Custom-Header': 'foobar'}
})

// 拦截器：请求拦截
instance.interceptors.request.use(
  config => {
    // 在请求被发送之前做些什么
    const token = window.sessionStorage.getItem('token')
    if (token) {
      config.headers = {
        Authorization: 'token  ' + token
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
    if (response.data.code == 400) {
      ElMessage.warning('错误请求: ' + response.data.msg)
    } else if (response.data.code == 401) {
      ElMessage.warning('未授权，请重新登录')
    } else if (response.data.code == 403) {
      ElMessage.warning('拒绝访问')
    } else if (response.data.code == 404) {
      ElMessage.warning('请求错误,未找到该资源')
    } else if (response.data.code == 405) {
      ElMessage.warning('请求方法未允许')
    } else if (response.data.code == 408) {
      ElMessage.warning('请求超时')
    } else if (response.data.code == 500) {
      ElMessage.warning('服务器端出错:' + response.data.msg)
    } else if (response.data.code == 501) {
      ElMessage.warning('网络未实现')
    } else if (response.data.code == 502) {
      ElMessage.warning('网络错误')
    } else if (response.data.code == 503) {
      ElMessage.warning('服务不可用')
    } else if (response.data.code == 504) {
      ElMessage.warning('网络超时')
    } else if (response.data.code != 200) {
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
