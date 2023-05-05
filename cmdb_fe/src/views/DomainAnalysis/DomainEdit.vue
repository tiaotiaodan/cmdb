<template>
  <!--操作栏：编辑对话框-->
  <el-dialog :model-value="visible" @close="dialogClose" width="30%">
    <!--标题-->
    <template #header>
      <div style="font-size: 18px; color: #409eff; font-weight: bold">修改域名解析信息</div>
    </template>

    <el-form :model="row" ref="formRef" :rules="formRules" label-width="100px">
      <!-- 配置idc选择，通过下拉框选择-->
      <el-form-item label="域名名称：" prop="domain_name">
        <el-select class="m-2" v-model="row.domain_name" @click="getDomain" placeholder="请选择" style="width:100%;">
          <el-option v-for="row in domain" :key="row.id" :label="`${row.name}`" :value="row.id"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="主机记录：" prop="platform">
        <el-input v-model="row.host_name"></el-input>
      </el-form-item>
      <el-form-item label="记录类型：">
        <el-input v-model="row.RecordType"></el-input>
      </el-form-item>
      <el-form-item label="解析地址：">
        <el-input v-model="row.analyshost"></el-input>
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
  name: 'ServerGroupEdit',
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
      domain: '', // 获取域名管理
      formRules: {
        domain_name: [{ required: true, message: '请选择域名', trigger: 'change' }]
      }
    }
  },
  methods: {
    // 点击关闭，子组件通知父组件更新属性
    dialogClose() {
      this.$emit('update:visible', false) // 父组件必须使用 v-model
    },
    // 获取域名管理信息
    getDomain() {
      this.$http.get('domain/domain_manage/?page_size=100').then(res => {
        this.domain = res.data.data
      })
    },
    dialogidcedit_btn() {
      this.$refs.formRef.validate(valid => {
        if (valid) {
          this.$http.put('domain/domain_analysis/' + this.row.id + '/', this.row).then(res => {
            if (res.data.code == 200) {
              // 反馈请求接口情况
              this.$message.success('修改域名解析数据信息成功')
              // 关闭弹出窗口
              this.dialogClose()
              // 调用父组件方法，更新数据
              this.$parent.getallDomain()
            }
          })
        }
      })
    }
  },
  // 监听窗口打开，
  watch: {
    visible() {
      if (this.visible) {
        // 关闭窗口不请求
        this.$http.get('domain/domain_analysis/' + this.row.id + '/').then(res => {
          if (res.data.code == 200) {
            // 域名管理：从对象中提取ID字段重新赋值
            this.row.domain_name = res.data.data.domain_name.id

            // 重新渲染编辑对话框域名管理
            this.getDomain()
          }
        })
      }
    }
  }
}
</script>

<style scoped></style>
