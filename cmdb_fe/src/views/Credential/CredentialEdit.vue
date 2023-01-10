<template>
  <!--操作栏：编辑对话框-->
  <el-dialog :model-value="visible" @close="dialogClose" width="30%">
   <!--标题-->
    <template #header>
      <div style="font-size:18px; color:#409eff; font-weight:bold;">修改凭据信息</div>
    </template>

    <el-form :model="row" ref="formRef" :rules="formRules" label-width="100px">
      <el-form-item label="凭据名称：" prop="name">
        <el-input v-model="row.name"></el-input>
      </el-form-item>
      <el-form-item label="用户名：" prop="username">
        <el-input v-model="row.username"></el-input>
      </el-form-item>
      <el-form-item label="密码：" prop="password" v-if="form.auth_mode == 1">
        <el-input v-model="row.password" type="password" show-password></el-input>
      </el-form-item>
      <el-form-item label="私钥：" prop="private_key" v-if="form.auth_mode == 2">
        <el-input v-model="row.private_key" type="textarea"></el-input>
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
  name: 'CredentialEdit',
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
      form: [],
      formRules: {
        name: [
          { required: true, message: '请输入机房名称', trigger: 'blur' },
          { min: 2, message: '机房名称长度应不小于2个字符', trigger: 'blur' }
        ],
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 2, message: '用户名长度应不小于2个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码长度应不小于6个字符', trigger: 'blur' }
        ],
        private_key: [
          { required: true, message: '请输入私钥', trigger: 'blur' },
          { min: 20, message: '私钥长度应不小于20个字符', trigger: 'blur' }
        ]
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
          this.$http.put('config/credential/' + this.row.id + '/', this.row).then(res => {
            if (res.data.code == 200) {
              // 反馈请求接口情况
              this.$message.success('修改凭据数据成功')
              this.$parent.getallCredential() // 调用父组件方法，更新数据
              // 关闭弹出窗口
              this.dialogClose()
            }
          })
        }
      })
    }
  },
  // 监听窗口打开，进行数据请求
  watch: {
    visible() {
      if (this.visible) {
        // 关闭窗口不请求
        this.$http.get('config/credential/' + this.row.id + '/').then(res => {
          if (res.data.code == 200) {
            this.form = res.data.data
          }
        })
      }
    }
  }
}
</script>

<style scoped></style>
