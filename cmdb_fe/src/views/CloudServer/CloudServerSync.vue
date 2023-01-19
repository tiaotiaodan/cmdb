<template>
  <!--操作栏：点击同步选择凭据对话框-->
  <el-dialog :model-value="visible" width="15%" title="请选择SSH连接凭据" @close="dialogClose">
    <el-col :span="2">
      <el-icon :size="23"><lock /></el-icon>
    </el-col>
    <el-col :span="22" :offset="1">
      <el-select class="m-2" v-model="credentialId" @click="getCredential" placeholder="请选择">
        <el-option v-for="row in credential" :key="row.id" :label="`${row.name}-${row.username}`" :value="row.id"></el-option>
      </el-select>
    </el-col>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogClose">取消</el-button>
        <el-button type="primary" @click="dialogeServerSync_btn">确定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
export default {
  name: 'ServerSync',
  // 介绍父组件的值
  props: {
    visible: Boolean, // 获取dialog是否打开变量
    row: {
      type: [Object, String, Number],
      default: 0
    }
  },
  data() {
    return {
      credential: '',
      credentialId: '',
    }
  },
  methods: {
    dialogeServerSync_btn(index, row) {
      // 如果主机有凭据，就直接同步
      this.$http
        .get('cmdb/cloud_server_host_collect/', { params: { hostname: this.row.hostname, credential_id: this.credentialId } })
        .then(res => {
          if (res.data.code == 200) {
            this.$message.success('同步成功')
            // 关闭弹出窗口
            this.dialogClose()
            // 调用父组件方法，更新数据
            this.$parent.getallCloudServer() 
          }
        })
    },
    getCredential() {
      this.$http.get('config/credential/').then(res => {
        this.credential = res.data.data
      })
    },
    // 点击关闭，子组件通知父组件更新属性
    dialogClose() {
      this.$emit('update:visible', false) // 父组件必须使用 v-model
    }
  }
}
</script>
