<template>
  <el-dialog :model-value="visible" width="60%" title="SSH终端" @close="dialogClose">
    <div ref="xterm" class="terminal" />
  </el-dialog>
</template>

<script>
import 'xterm/css/xterm.css'
import { Terminal } from 'xterm'
import { FitAddon } from 'xterm-addon-fit' // xterm窗口自适应
export default {
  name: 'SSH',
  props: {
    visible: Boolean, // 获取dialog是否打开变量
    row: {
      type: [Object, String, Number],
      default: 0
    }
  },
  data() {
    return {
      term: '', // term实例
      ws: '' // ws连接
    }
  },
  methods: {
    // 初始化Terminal
    init() {
      this.term = new Terminal({
        fontSize: 18,
        convertEol: true, // 启用时，光标将设置为下一行的开头
        rendererType: 'canvas', // 渲染类型
        cursorBlink: true, // 光标闪烁
        cursorStyle: 'bar', // 光标样式 underline
        theme: {
          background: '#060101', // 背景色
          cursor: 'help' // 设置光标
        }
      })
    },
    // 初始化Websocket
    initSocket() {
      const fitPlugin = new FitAddon()
      fitPlugin.activate(this.term)
      // this.term.loadAddon(fitPlugin)

      // 建立ws连接
      this.ws = new WebSocket(`ws://127.0.0.1:8000/server/terminal/${this.row.ssh_ip}/${this.row.ssh_port}/${this.row.credential}/`)

      // 建立ws连接成功后回调
      this.ws.onopen = () => {
        // 将term挂载到标签上
        this.term.open(this.$refs.xterm)
        this.term.focus()
        fitPlugin.fit()
      }

      // 获取后端传回的数据
      this.ws.onmessage = res => {
        const reader = new window.FileReader()
        reader.onload = () => this.term.write(reader.result)
        reader.readAsText(res.data, 'utf-8')
      }

      // 用户输入发送到后端
      this.term.onData(data => this.ws.send(JSON.stringify({ data })))

      // 动态设置终端窗口大小
      this.term.onResize(({ cols, rows }) => {
        this.ws.send(JSON.stringify({ resize: [cols, rows] }))
      })
      window.onresize = () => fitPlugin.fit()

      // ws关闭连接
      this.ws.onclose = e => {
        this.term.write('\r\nConnection is closed.\r\n')
      }
    },

    // 点击关闭，子组件通知父组件更新属性
    dialogClose() {
      this.ws.close()
      this.term.dispose()
      this.$emit('update:visible', false) // 父组件必须使用v-model
      window.location.reload()
    }
  },
  // 监听窗口打开
  watch: {
    visible() {
      this.init()
      this.initSocket()
    }
  }
}
</script>

<style scoped>
.terminal {
  margin-top: -30px;
  padding: 5px;
  background-color: #000000;
}
/*.terminal::-webkit-scrollbar {         !*滚动条整体样式*!*/
/*  width: 8px;*/
/*  height: 3px;*/
/*}*/
/*.terminal::-webkit-scrollbar-thumb {   !*滚动条里面小方块样式*!*/
/*  border-radius: 100px;*/
/*  background: #323C46;*/
/*}*/
</style>
