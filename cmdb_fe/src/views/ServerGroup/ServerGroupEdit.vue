<template>
  <!--操作栏：编辑对话框-->
  <el-dialog :model-value="visible" @close="dialogClose" width="30%">
   <!--标题-->
    <template #header>
      <div style="font-size:18px; color:#409eff; font-weight:bold;">修改主机分组信息</div>
    </template>

    <el-form :model="row" ref="formRef" :rules="formRules" label-width="100px">
      <el-form-item label="机房名称：" prop="name">
        <el-input v-model="row.name"></el-input>
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
          { required: true, message: '请输入机房名称', trigger: 'blur' },
          { min: 2, message: '机房名称长度应不小于2个字符', trigger: 'blur' }
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
          this.$http.put('cmdb/server_group/' + this.row.id + '/', this.row).then(res => {
            if (res.data.code == 200) {
              // 反馈请求接口情况
              this.$message.success('修改主机分组数据成功')
              // 关闭弹出窗口
              this.dialogClose()
            }
          })
        }
      })
    }
  }
}
</script>

<style scoped></style>
