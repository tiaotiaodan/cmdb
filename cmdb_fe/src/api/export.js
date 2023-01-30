// 导出Excel功能
import axios from './http'

export function expotOut(searchList, pathName, xlsName, url) {
    // 获取时间，这一步是在下载时文件名带下载日期，例如：用户信息-2020-04-27.xls,如无需要可以去掉
    let d = new Date()
    let month = (d.getMonth() + 1)
    let day = d.getDate()
    let time = d.getFullYear() + '-' + (String(month).length > 1 ? month : '0' + month) + '-' + (String(day).length > 1 ? day : '0' + day)
    // 地址
    let baseURL = axios.defaults.baseURL // 域名
    const PATH = {
            userList: url // 后台接口地址
        }
        // 参数
    let params = '?'
    for (let key in searchList) {
        params = params + key + '=' + searchList[key] + '&'
    }

    function createObjectURL(object) { return (window.URL) ? window.URL.createObjectURL(object) : window.webkitURL.createObjectURL(object) }
    var xhr = new XMLHttpRequest()
    var formData = new FormData()
    xhr.open('get', baseURL + PATH[pathName] + params) // url填写后台的接口地址，如果是post，在formData append参数（参考原文地址）
    xhr.setRequestHeader('Authorization', 'token  ' + window.sessionStorage.getItem('token'))
    xhr.responseType = 'blob'
    xhr.onload = function(e) {
        if (this.status === 200) {
            var blob = this.response
                // xlsx文件名称
            var filename = `${xlsName}-${time}.xlsx`
            if (window.navigator.msSaveOrOpenBlob) {
                navigator.msSaveBlob(blob, filename)
            } else {
                var a = document.createElement('a')
                var url = createObjectURL(blob)
                a.href = url
                a.download = filename
                document.body.appendChild(a)
                a.click()
                window.URL.revokeObjectURL(url)
            }
        }
    }
    xhr.send(formData)
}
