<template>
  <el-dialog :model-value="visible" width="30%" @close="dialogClose">
    <!--标题-->
    <template #header>
      <div style="font-size: 18px; color: #409eff; font-weight: bold">创建物理主机信息</div>
    </template>

    <el-form :model="form" ref="formRef" :rules="formRules" label-width="120px">
      <el-form-item label="机器名称：" prop="name">
        <el-input v-model="form.name" placeholder="例如：测试机"></el-input>
      </el-form-item>
      <el-form-item label="主机名称：" prop="hostname">
        <el-input v-model="form.hostname"></el-input>
        <el-tag class="ml-2" type="warning">
          <el-icon><InfoFilled /></el-icon>
          必须与实际主机名一致
        </el-tag>
      </el-form-item>
      <el-form-item label="IDC机房：" prop="idc">
        <el-select class="m-2" v-model="form.idc" @click="getIdc" placeholder="请选择" style="width:100%;">
          <el-option v-for="row in idc" :key="row.id" :label="row.name" :value="row.id"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="主机分组：" prop="server_group">
        <el-select class="m-2" multiple v-model="form.server_group" @click="getServerGroup" placeholder="请选择" style="width:100%;">
          <el-option v-for="row in serverGroup" :key="row.id" :label="row.name" :value="row.id"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="机器类型：" prop="machine_type">
        <el-select v-model="form.machine_type" placeholder="请选择机器类型" style="width:100%;">
          <el-option label="linux" value="linux" />
          <el-option label="windows" value="windows" />
          <el-option label="vmware" value="vmware" />
        </el-select>
      </el-form-item>
      <el-form-item label="资产编码：" prop="asset_code">
        <el-input v-model="form.asset_code" placeholder="请输入资产编码"></el-input>
      </el-form-item>
      <el-form-item label="SSH连接：" required>
        <el-col :span="1.5">
          <el-tag size="large" type="info">IP</el-tag>
        </el-col>
        <el-col :span="10">
          <el-form-item prop="ssh_ip">
            <el-input v-model="form.ssh_ip"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="1.5">
          <el-tag size="large" type="info">端口</el-tag>
        </el-col>
        <el-col :span="5">
          <el-form-item prop="ssh_port">
            <el-input v-model="form.ssh_port"></el-input>
          </el-form-item>
        </el-col>
        <el-tag class="ml-2" type="warning">
          <el-icon><InfoFilled /></el-icon>
          linux和windows端口默认填写为22，vmware填写管理页面端口443
        </el-tag>
      </el-form-item>

      <el-form-item label="SSH凭据：" prop="credential">
        <el-select class="m-2" v-model="form.credential" @click="getCredential" placeholder="请选择">
          <el-option v-for="row in credential" :key="row.id" :label="`${row.name}-${row.username}`" :value="row.id"></el-option>
        </el-select>
        <el-col :span="3" :offset="1">
          <el-button type="primary" plain @click="this.$router.push('/config/credential')">新建</el-button>
        </el-col>
      </el-form-item>
      <el-form-item label="备注：" prop="note">
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
  name: 'PhysicsServerCreate',
  props: {
    visible: Boolean
  },
  data() {
    return {
      idc: '',
      serverGroup: '',
      credential: '',

      form: {
        idc: '',
        server_group: '',
        name: '',
        hostname: '',
        machine_type: '',
        ssh_ip: '',
        ssh_port: null,
        credential: '',
        note: ''
      },
      formRules: {
        idc: [{ required: true, message: '请选择IDC机房', trigger: 'change' }],
        server_group: [{ required: true, message: '请选择主机分组', trigger: 'change' }],
        name: [
          { required: true, message: '请输入机器名称', trigger: 'blur' },
          { min: 2, message: '主机名长度应不小于2个字符', trigger: 'blur' }
        ],
        hostname: [
          { required: true, message: '请输入主机名称', trigger: 'blur' },
          { min: 4, message: '主机名长度不小于4个字符', trigger: 'blur' }
        ],
        ssh_ip: [
          { required: true, message: '请输入SSH IP地址', trigger: 'blur' },
          { min: 7, message: '主机名长度不小于8个字符', trigger: 'blur' }
        ],
        ssh_port: [
          { required: true, message: '请输入SSH端口', trigger: 'blur' },
          { min: 2, message: 'SSH端口长度不小于2个数字', trigger: 'blur' }
          // {type: 'number', message: 'SSH端口必须是数字', trigger: 'blur'}
        ],
        credential: [{ required: true, message: '请选择SSH连接凭据', trigger: 'change' }],
        machine_type: [{ required: true, message: '请选择SSH连接凭据', trigger: 'change' }],
        asset_code: [
          { required: true, message: '请输入固定资产编码', trigger: 'blur' },
          { pattern: /^[A-Za-z0-9]\w*$/, message: '请输入大小写和数字', trigger: 'blur' }
        ],
      }
    }
  },
  methods: {
    submit() {
      this.$refs.formRef.validate(valid => {
        if (valid) {
          this.$http.post('cmdb/physics_server_create_host/', this.form).then(res => {
            if (res.data.code == 200) {
              this.$message.success('创建成功')
              this.$parent.getallPhysicsServer() // 调用父组件方法，更新数据
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
    },
    getIdc() {
      this.$http.get('cmdb/idc/?page_size=1000').then(res => {
        this.idc = res.data.data
      })
    },
    getServerGroup() {
      this.$http.get('cmdb/server_group/?page_size=100').then(res => {
        this.serverGroup = res.data.data
      })
    },
    getCredential() {
      this.$http.get('config/credential/?page_size=100').then(res => {
        this.credential = res.data.data
      })
    }
  }
}
</script>
