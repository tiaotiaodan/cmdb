<template>
  <!--操作栏：编辑对话框-->
  <el-dialog :model-value="visible" @close="dialogClose" width="30%">
    <!--标题-->
    <template #header>
      <div style="font-size: 18px; color: #409eff; font-weight: bold">修改域名管理信息</div>
    </template>

    <el-form :model="row" ref="formRef" :rules="formRules" label-width="100px">
      <el-form-item label="域名名称：" prop="name">
        <el-input v-model="row.name"></el-input>
      </el-form-item>
      <el-form-item label="平台管理：" prop="platform">
        <el-input v-model="row.platform"></el-input>
      </el-form-item>
      <el-form-item label="域名状态：" prop="status">
        <el-select v-model="row.status" placeholder="请选择域名状态类型" style="width: 100%">
          <el-option label="正常" value="正常" />
          <el-option label="急需续费" value="急需续费" />
          <el-option label="急需赎回" value="急需赎回" />
          <el-option label="转出中" value="转出中" />
          <el-option label="未认证" value="未认证" />
          <el-option label="实名认证失败" value="实名认证失败" />
          <el-option label="实名认证审核中" value="实名认证审核中" />
          <el-option label="域名持有者信息修改中" value="域名持有者信息修改中" />
        </el-select>
      </el-form-item>
      <el-form-item label="创建日期：">
        <el-date-picker v-model="row.create_time" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" placeholder="请选择日期" style="width: 100%"></el-date-picker>
      </el-form-item>
      <el-form-item label="过期日期：">
        <el-date-picker v-model="row.expire_time" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" placeholder="请选择时间" style="width: 100%"></el-date-picker>
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
      formRules: {
        name: [
          { required: true, message: '请输入域名名称', trigger: 'blur' },
          { min: 1, message: '域名名称长度应不小于1个字符', trigger: 'blur' }
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
      this.$refs.formRef.validate(valid => {
        if (valid) {
          this.$http.put('domain/domain_manage/' + this.row.id + '/', this.row).then(res => {
            if (res.data.code == 200) {
              // 反馈请求接口情况
              this.$message.success('修改域名数据信息成功')
              // 关闭弹出窗口
              this.dialogClose()
              // 调用父组件方法，更新数据
              this.$parent.getallDomain()
            }
          })
        }
      })
    }
  }
}
</script>

<style scoped></style>
