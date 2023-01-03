<template>
  <div class="main">
    <div class="login_box">
      <div class="title">欢迎访问运维资产管理系统</div>
      <div class="login_form">
        <!--
          :model  绑定form表单存储数据
          :reles  进行form表单格式填写验证
          ref   进行提交前的预验证绑定  
        -->
        <el-form :model="form" :rules="rules" ref="form" label-width="120px">
          <el-form-item label="用户名:" prop="username">
            <el-input v-model="form.username" />
          </el-form-item>
          <el-form-item label="密码:" prop="password">
            <el-input v-model="form.password" type="password" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="login_but">登陆</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, message: '用户名长度应不小于3个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '用户名长度应不小于6个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    login_but() {
      // 添加预验证，确认表单是否ok，不ok就返回
      this.$refs.form.validate(valid => {
        // 判断表单预验证返回是否为真
        if (valid) {
          // 返回表单为真，进行表单提交
          this.$http.post('login/', this.form).then(res => {
            if (res.data.code == 200) {
              this.$message.success('登陆成功')
              // 保存token和用户到会话存储
              window.sessionStorage.setItem('token', res.data.token)
              window.sessionStorage.setItem('username', res.data.username)
              // 登陆成功后跳转到首页
              this.$router.push('/')
            }
          })
        } else {
          this.$message.info('用户名或密码格式错误！')
        }
      })
    }
  }
}
</script>

<style scoped>
.main {
  background-image: url('../assets/login_backup.jpeg');
  background-size: 100% 100%; /* 设置图片宽高100%显示 */
  height: 100%; /* 设置 高度100% */
}
.login_box {
  height: 300px;
  width: 400px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 3px 20px 0 #f5f5f5;

  /* 移动居中显示实现 */
  position: absolute;
  top: 0px;
  bottom: 0px;
  right: 0px;
  left: 0px;
  margin: auto;
}
.title {
  font-size: 20px;
  font-weight: bold;
  color: dodgerblue;
  text-align: center;
  margin-top: 30px;
}
.login_form {
  margin-right: 50px;
  margin-top: 30px;
}
.login_form el-button {
  margin-left: 50%;
  width: 180px;
}
</style>
