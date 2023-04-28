<template>
  <el-dialog :model-value="visible" width="35%" title="导入云主机" @close="dialogClose">
    <el-steps :space="300" :active="active" align-center style="margin-bottom: 10%">
      <el-step title="公有云"></el-step>
      <el-step title="访问凭据"></el-step>
      <el-step title="导入确认"></el-step>
    </el-steps>

    <el-form :model="form" ref="formRef" :rules="formRules" label-width="155px">
      <!--第一步-->
      <div v-show="active == 1">
        <el-form-item prop="cloud" label-width="180px">
          <el-radio-group v-model="form.cloud">
            <el-radio label="阿里云"><img src="../../assets/img/aliyun.png" /></el-radio>
            <el-radio label="腾讯云"><img src="../../assets/img/tencend.png" /></el-radio>
          </el-radio-group>
        </el-form-item>
      </div>
      <!--第二步-->
      <div v-show="active == 2">
        <el-form-item label="AccessKey ID：" prop="secret_id">
          <el-input v-model="form.secret_id" clearable></el-input>
        </el-form-item>
        <el-form-item label="AccessKey Secret：" prop="secret_key">
          <el-input v-model="form.secret_key" clearable></el-input>
          <el-link v-if="form.cloud == '阿里云'" href="https://ram.console.aliyun.com/manage/ak" target="_blank" type="primary">如何获取AccessKey？</el-link>
          <el-link v-if="form.cloud == '腾讯云'" href="https://console.cloud.tencent.com/cam/capi" target="_blank" type="primary">如何获取AccessKey？</el-link>
        </el-form-item>
      </div>

      <!--第三步-->
      <div v-show="active == 3">
        <el-form-item label="选择域名：" prop="cloudDomainId">
          <el-select class="m-2" v-model="form.cloudDomainId" @click="getCloudDomain" placeholder="请选择" style="width: 100%">
            <el-option v-for="row in cloudDomain" :key="row.id" :label="row.name" :value="row.id" ></el-option>
          </el-select>
        </el-form-item>
      </div>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogClose" v-if="active == 1">取消</el-button>
        <el-button type="primary" @click="dialogToggle('pre')" v-if="active > 1">上一步</el-button>
        <el-button type="primary" @click="dialogToggle('next')" v-if="active < 3">下一步</el-button>
        <el-button type="primary" @click="submit" v-if="active == 3">确定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
export default {
  name: 'DomainCreate',
  props: {
    visible: Boolean
  },
  data() {
    return {
      form: {
        cloud: '',
        secret_id: '',
        secret_key: '',
        cloudDomainId: ''
      },
      formRules: {
        cloud: [{ required: true, message: '请选择', trigger: 'blur' }],
        cloudDomainId: [{ required: true, message: '请选择域名', trigger: 'change' }],
        secret_id: [
          { required: true, message: '请输入密钥ID', trigger: 'blur' },
          { min: 20, message: '密钥ID长度应不小于20个字符', trigger: 'blur' }
        ],
        secret_key: [
          { required: true, message: '请输入密钥Key', trigger: 'blur' },
          { min: 20, message: '密钥Key长度应不小于20个字符', trigger: 'blur' }
        ]
      },
      cloudDomain: '',
      active: 1
    }
  },
  methods: {
    submit() {
      this.$refs.formRef.validate(valid => {
        if (valid) {
          if (this.form.cloud == '阿里云') {
            this.$http.post('domain/ali_domain_analysis_create/', this.form).then(res => {
              if (res.data.code == 200) {
                this.$message.success('导入云主机成功')
                this.$parent.getallDomain()
                this.dialogClose() // 关闭窗口
                this.$refs.formRef.resetFields() // 清空表单数据
              }
            })
          } else if (this.form.cloud == '腾讯云') {
            this.$http.post('cmdb/tencent_cloud/', this.form).then(res => {
              if (res.data.code == 200) {
                this.$message.success('导入云主机成功')
                this.$parent.getallDomain()
                this.dialogClose() // 关闭窗口
                this.$refs.formRef.resetFields() // 清空表单数据
              }
            })
          }
          this.cloudDialogVisible = false
        } else {
          this.$message.error('格式错误！')
        }
      })
    },
    // 点击关闭，子组件通知父组件更新属性
    dialogClose() {
      this.$emit('update:visible', false) // 父组件必须使用v-model
    },
    // 获取域名管理信息
    getCloudDomain() {
      this.$http.get('domain/domain_manage/?page_size=100').then(res => {
        console.log(res)
        // if this.form.cloud == "res.data."
        this.cloudDomain = res.data.data
      })
    },
    // 云主机导入第一步和第二步对话框切换
    dialogToggle(action) {
      if (action == 'pre') {
        if (this.active-- < 2) {
          this.active = 1
        }
      } else if (action == 'next') {
        if (this.active++ > 3) {
          this.active = 1
        }
      }
    }
  }
}
</script>
