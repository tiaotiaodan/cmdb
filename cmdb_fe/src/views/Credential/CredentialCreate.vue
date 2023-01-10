<template>
  <el-dialog :model-value="visible" width="30%" @close="dialogClose">
    <!--标题-->
    <template #header>
      <div style="font-size:18px; color:#409eff; font-weight:bold;">创建凭据管理</div>
    </template>

    <el-form :model="form" ref="formRef" :rules="formRules" label-width="100px">
      <el-form-item label="凭据名称：" prop="name">
        <el-input v-model="form.name"></el-input>
      </el-form-item>
      <el-form-item label="用户名：" prop="username">
        <el-input v-model="form.username"></el-input>
      </el-form-item>
      <el-form-item label="认证方式：">
        <el-radio-group v-model="form.auth_mode">
          <el-radio border label="1">密码</el-radio>
          <el-radio border label="2">秘钥</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="密码：" prop="password" v-if="form.auth_mode == '1'">
        <el-input v-model="form.password" ></el-input>
      </el-form-item>
      <el-form-item label="私钥：" prop="private_key" v-if="form.auth_mode == '2'">
        <el-input v-model="form.private_key" type="textarea"></el-input>
      </el-form-item>
      <el-form-item label="备注：">
        <el-input v-model="form.note" type="textarea"></el-input>
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogClose">取消</el-button>
        <el-button type="primary" @click="submit">确定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
export default {
  name: 'CredentialCreate',
  props: {
    visible: Boolean
  },
  data() {
    return {
      form: {
        name: '',
        username: '',
        auth_mode: '1',
        password: '',
        private_key: '',
        note: ''
      },
      formRules: {
        name: [
          { required: true, message: '请输入凭据名称', trigger: 'blur' },
          { min: 2, message: '凭据名称长度应不小于2个字符', trigger: 'blur' }
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
    submit() {
      this.$refs.formRef.validate(valid => {
        if (valid) {
          this.$http.post('config/credential/', this.form).then(res => {
            if (res.data.code == 200) {
              this.$message.success('创建主机分组成功')
              this.$parent.getallCredential() // 调用父组件方法，更新数据
              this.dialogClose() // 关闭窗口
              this.$refs.formRef.resetFields() // 清空表单数据
            }
          })
        } else {
          this.$message.error('格式错误！')
        }
      })
    },
    // 点击关闭，子组件通知父组件更新属性
    dialogClose() {
      this.$emit('update:visible', false) // 父组件必须使用v-model
    }
  }
}
</script>
