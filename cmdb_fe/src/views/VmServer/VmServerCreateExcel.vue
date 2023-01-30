<template>
  <el-dialog :model-value="visible" width="30%" @close="dialogClose">
    <!--标题-->
    <template #header>
      <div style="font-size: 18px; color: #409eff; font-weight: bold">虚拟机Excel导入</div>
    </template>
    <el-form :model="form" ref="formRef" :rules="formRules" label-width="100px">
      <el-form-item label="模板下载：">
        <el-link  @click="outFile" type="primary">虚拟机导入模板</el-link>
      </el-form-item>
      <el-form-item label="IDC机房：" prop="idc">
        <el-select class="m-2" v-model="form.idc" @click="getIdc" placeholder="请选择">
          <el-option v-for="row in idc" :key="row.id" :label="row.name" :value="row.id"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="主机分组：" prop="server_group">
        <el-select class="m-2" multiple v-model="form.server_group" @click="getServerGroup" placeholder="请选择">
          <el-option v-for="row in serverGroup" :key="row.id" :label="row.name" :value="row.id"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="虚拟主机：" prop="vm_host">
        <el-select class="m-2" v-model="form.vm_host" @click="getVmHost" placeholder="请选择">
          <el-option v-for="row in vmhost" :key="row.id" :label="`${row.name}-${row.ssh_ip}`" :value="row.id"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="导入数据：">
        <el-upload :limit="1" v-model:file-list="fileList" :auto-upload="false">
          <template #trigger>
            <el-button type="primary">选择文件</el-button>
          </template>
          <template #tip>
            <div class="el-upload__tip text-red">导入完成后可通过验证功能批量验证</div>
          </template>
        </el-upload>
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
import { expotOut } from '../../api/export.js' 
export default {
  name: 'VmServerCreate',
  props: {
    visible: Boolean
  },
  data() {
    return {
      idc: '',
      serverGroup: '',
      vmhost: '',
      fileList: [],
      form: [],
      formRules: {
        idc: [{ required: true, message: '请选择IDC机房', trigger: 'blur' }],
        vm_host: [{ required: true, message: '请选择关联虚拟主机', trigger: 'blur' }],
        server_group: [{ required: true, message: '请选择主机分组', trigger: 'blur' }]
      }
    }
  },
  methods: {
    submit() {
      this.$refs.formRef.validate(valid => {
        console.log(this.form.vm_host)
        if (valid) {
          let fd = new FormData()
          fd.append('file', this.fileList[0].raw)
          fd.append('idc', this.form.idc)
          fd.append('vm_host', this.form.vm_host)
          fd.append('server_group', this.form.server_group)
          this.$http
          .post('cmdb/vm_server_excel_create_host/', fd)
          .then(res => {
            if (res.data.code == 200) {
              this.$message.success('创建成功')
              this.$parent.getallVmServer() // 调用父组件方法，获取所有数据
              this.dialogClose() // 关闭窗口
              this.$refs.formRef.resetFields() // 清空表单数据
            }
          })
        } else {
          this.$message.error('格式错误！')
        }
      })
    },
    // 导出文件调用
    outFile() {
      expotOut(this.query, 'userList', '虚拟机信息模板', 'cmdb/vm_server_excel_create_host/')
    },
    // 点击关闭，子组件通知父组件更新属性
    dialogClose() {
      this.$emit('update:visible', false) // 父组件必须使用v-model
    },
    getIdc() {
      this.$http.get('cmdb/idc/?page_size=100').then(res => {
        this.idc = res.data.data
      })
    },
    getServerGroup() {
      this.$http.get('cmdb/server_group/?page_size=100').then(res => {
        this.serverGroup = res.data.data
      })
    },
     // 获取虚拟主机信息
    getVmHost() {
      this.$http.get('cmdb/physics_server/?search=vmware&page_size=100').then(res => {
        this.vmhost = res.data.data
      })
    },
  }
}
</script>
