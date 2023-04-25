<template>
  <!--操作栏：编辑对话框-->
  <el-dialog :model-value="visible" title="修改主机分组信息" @close="dialogClose" width="35%">
    <el-form :model="row" ref="formRef" :rules="formRules" label-width="120px">
      <el-form-item label="机器名称：" prop="name">
        <el-input v-model="row.name" placeholder="例如：测试机"></el-input>
      </el-form-item>
      <el-form-item label="主机名称：" prop="hostname">
        <el-input v-model="row.hostname" disabled></el-input>
      </el-form-item>
      <el-form-item label="IDC机房：" prop="idc">
        <el-input v-model="row.idc"></el-input>
      </el-form-item>
      <el-form-item label="主机分组：" prop="server_group">
        <el-input v-model="row.server_group"></el-input>
      </el-form-item>
      <el-form-item label="租约过期时间：" prop="expire_datetime">
        <el-date-picker v-model="row.expire_datetime" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" placeholder="请选择时间"></el-date-picker>
      </el-form-item>
      <el-form-item label="备注：">
        <el-input v-model="row.note" type="textarea"></el-input>
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogClose">取消</el-button>
        <el-button type="primary" @click="dialogidcedit_btn">确定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
export default {
  name: 'ServerEdit',
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
      formRules: {
        name: [
          { required: true, message: '请输入机器名称', trigger: 'blur' },
          { min: 2, message: '机器名称长度应不小于2个字符', trigger: 'blur' }
        ],
        idc: [{ required: true, message: '请选择IDC机房', trigger: 'change' }],
        server_group: [{ required: true, message: '请选择主机分组', trigger: 'change' }],
        hostname: [{ required: true, message: '请输入hostname主机名', trigger: 'change' }],
        machine_type: [{ required: true, message: '请输入主机类型', trigger: 'change' }],
        os_version: [{ required: true, message: '请输入系统版本', trigger: 'change' }],
        public_ip: [{ required: true, message: '请输入公网ip', trigger: 'change' }],
        private_ip: [{ required: true, message: '请输入私有ip', trigger: 'change' }],
        cpu_num: [{ required: true, message: '请输入cpu数量', trigger: 'change' }],
        cpu_model: [{ required: true, message: '请输入CPU型号', trigger: 'change' }],
        memory: [{ required: true, message: '请输入内存大小', trigger: 'change' }],
        disk: [{ required: true, message: '请输入磁盘大小', trigger: 'change' }],
        put_shelves_date: [{ required: true, message: '请选择上架时间', trigger: 'change' }],
        off_shelves_date: [{ required: true, message: '请选择下架时间', trigger: 'change' }],
        expire_datetime: [{ required: true, message: '请选择租约过期时间', trigger: 'change' }],
      }
    }
  },
  methods: {
    // 点击关闭，子组件通知父组件更新属性
    dialogClose() {
      this.$emit('update:visible', false) // 父组件必须使用 v-model
    },
    dialogidcedit_btn() {
      // 验证表单是否通过
      this.$refs.formRef.validate(valid => {
        if (valid) {
          this.$http
            .put('cmdb/server/' + this.row.id + '/', this.row)
            .then(res => {
              if (res.data.code == 200) {
                // 反馈请求接口情况
                this.$message.success('修改数据成功')
                // 关闭弹出窗口
                this.dialogClose()
              } else {
                this.$message.info('修改数据失败')
              }
            })
            .catch(error => {
              this.$message.error('idc服务端接口请求错误！' + error)
            })
        } else {
          console.log('格式错误')
        }
      })
    }
  }
}
</script>

<style scoped></style>

