<template>
  <!--操作栏：编辑对话框-->
  <el-dialog :model-value="visible" @close="dialogClose" width="35%">
    <!--标题-->
    <template #header>
      <div style="font-size: 18px; color: #409eff; font-weight: bold">修改物理主机信息</div>
    </template>

    <el-form :model="row" ref="formRef" :rules="formRules" label-width="160px">
      <el-form-item label="机器名称：" prop="name">
        <el-input v-model="row.name" placeholder="例如：测试机"></el-input>
      </el-form-item>
      <el-form-item label="主机名称：" prop="hostname">
        <el-input v-model="row.hostname" disabled></el-input>
      </el-form-item>
      <!-- 配置idc选择，通过下拉框选择-->
      <el-form-item label="IDC机房：" prop="idc">
        <el-select class="m-2" v-model="row.idc" @click="getIdc" placeholder="请选择" style="width:100%;">
          <el-option v-for="row in idc" :key="row.id" :label="`${row.city}-${row.name}`" :value="row.id"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="主机分组：" prop="server_group">
        <!--表单多选multiple-->
        <el-select class="m-2" v-model="row.server_group" @click="getServerGroup" multiple placeholder="请选择" style="width:100%;">
          <el-option v-for="row in serverGroup" :key="row.id" :label="row.name" :value="row.id"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="机器类型：" prop="machine_type">
        <el-select v-model="row.machine_type" placeholder="请选择机器类型" style="width:100%;">
          <el-option label="linux" value="linux" />
          <el-option label="windows" value="windows" />
          <el-option label="vmware" value="vmware" />
        </el-select>
      </el-form-item>
      <!-- 配置idc选择，通过下拉框选择-->
      <el-form-item label="虚拟主机：" prop="vm_host">
        <el-select class="m-2" v-model="row.vm_host" @click="getIdc" placeholder="请选择" style="width:100%;">
          <el-option v-for="row in vmhost" :key="row.id" :label="`${row.ssh_ip}`" :value="row.id"></el-option>
        </el-select>
      </el-form-item>
      <!--配置ssh连接显示格式配置-->
      <!--配置ssh连接显示格式配置-->
      <el-form-item label="SSH 连接：" required>
          <el-col :span="1.5">
            <el-tag size="large" type="info">IP</el-tag>
          </el-col>
          <el-col :span="15">
            <el-form-item prop="ssh_ip">
              <el-input v-model="row.ssh_ip"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="1.5">
            <el-tag size="large" type="info">端口</el-tag>
          </el-col>
          <el-col :span="4">
            <el-form-item prop="ssh_port">
              <el-input v-model="row.ssh_port"></el-input>
            </el-form-item>
          </el-col>
          <el-tag class="ml-2" type="warning">
          <el-icon><InfoFilled /></el-icon>
          linux和windows端口默认填写为22，vmware填写管理页面端口443
          </el-tag>
      </el-form-item>
      <el-form-item label="SSH凭据：" prop="credential">
        <el-select class="m-2" v-model="row.credential" @click="getCredential" placeholder="请选择" >
          <el-option v-for="row in credential" :key="row.id" :label="`${row.name}-${row.username}`" :value="row.id"></el-option>
        </el-select>
      </el-form-item>

      <!--更多详情按钮-->
      <el-divider content-position="left"><el-button type="primary" round size="small" @click="serverDetal">更多详情</el-button></el-divider>
      <!-- 通过div使用v-show是否显示里面内容-->
      <div v-show="serverDetalVisible">
        <el-form-item label="系统版本：">
          <el-input v-model="row.os_version"></el-input>
        </el-form-item>
        <el-form-item label="公网IP：">
          <el-input v-model="row.public_ip" disabled></el-input>
        </el-form-item>
        <el-form-item label="私有IP：">
          <el-input v-model="row.private_ip" disabled></el-input>
        </el-form-item>
        <el-form-item label="CPU数量：">
          <el-input v-model="row.cpu_num"></el-input>
        </el-form-item>
        <el-form-item label="内存：">
          <el-input v-model="row.memory"></el-input>
        </el-form-item>
        <el-form-item label="硬盘：">
          <el-input v-model="row.disk" disabled></el-input>
        </el-form-item>
        <el-form-item label="带宽：">
          <el-input v-model="row.network"></el-input>
        </el-form-item>
        <el-form-item label="上架日期：">
          <el-date-picker v-model="row.put_shelves_date" type="date" value-format="YYYY-MM-DD" placeholder="请选择日期" style="width:100%;"></el-date-picker>
        </el-form-item>
        <el-form-item label="下架日期：">
          <el-date-picker v-model="row.off_shelves_date" type="date" value-format="YYYY-MM-DD" placeholder="请选择日期" style="width:100%;"></el-date-picker>
        </el-form-item>
        <el-form-item label="备注：">
          <el-input v-model="row.note" type="textarea"></el-input>
        </el-form-item>
      </div>
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
  name: 'VmServerEdit',
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
      idc: '', // 获取idc所有数据
      serverGroup: '', // 获取servergroup所有数据
      credential: '', // 获取credential所有数据
      serverDetalVisible: false, // 默认是否显示更多详情里的内容
      vmhost:'',

      formRules: {
        name: [
          { required: true, message: '请输入机器名称', trigger: 'blur' },
          { min: 2, message: '机器名称长度应不小于2个字符', trigger: 'blur' }
        ],
        idc: [{ required: true, message: '请选择IDC机房', trigger: 'change' }],
        server_group: [{ required: true, message: '请选择主机分组', trigger: 'change' }],
        hostname: [{ required: true, message: '请输入hostname主机名', trigger: 'change' }],
        machine_type: [{ required: true, message: '请选择主机类型', trigger: 'change' }],
        vm_host: [{ required: true, message: '请选择虚拟主机', trigger: 'change' }],
        credential: [{ required: true, message: '请选择SSH凭据', trigger: 'change' }],
      }
    }
  },
  methods: {
    // 点击关闭，子组件通知父组件更新属性
    dialogClose() {
      this.$emit('update:visible', false) // 父组件必须使用 v-model
      this.serverDetalVisible = false // 点击取消和x掉关闭，把详情设置为false关闭状态
      this.$parent.getallVmServer() // 点击取消和x掉关闭，进行重新获取数据
    },
    // 获取idc机房信息
    getIdc() {
      this.$http.get('/cmdb/idc/?page_size=100').then(res => {
        this.idc = res.data.data
      })
    },
    // 获取主机分组信息
    getServerGroup() {
      this.$http.get('/cmdb/server_group/?page_size=100').then(res => {
        this.serverGroup = res.data.data
      })
    },
    // 获取凭据信息
    getCredential() {
      this.$http.get('/config/credential/?page_size=100').then(res => {
        this.credential = res.data.data
      })
    },

    // 获取凭据信息
    getVmHost() {
      this.$http.get('cmdb/physics_server/?search=vmware&page_size=100').then(res => {
        this.vmhost = res.data.data
      })
    },

    dialogidcedit_btn() {
      // 验证表单是否通过
      this.$refs.formRef.validate(valid => {
        if (valid) {
          this.$http.put('cmdb/vm_server/' + this.row.id + '/', this.row).then(res => {
            if (res.data.code == 200) {
              // 反馈请求接口情况
              this.$message.success('修改数据成功')
              // 关闭弹出窗口
              this.dialogClose()
              // 调用父组件方法，更新数据
              this.$parent.getallVmServer() 
            }
          })
        } else {
          this.$message.warning('格式错误')
        }
      })
    },

    // 进行关闭或者显示更多详情
    serverDetal() {
      // 点击更多详情进行取反操作，为真就返回假，为假就返回真
      this.serverDetalVisible = !this.serverDetalVisible
    }
  },
  // 监听窗口打开，
  watch: {
    visible() {
      if (this.visible) {
        // 关闭窗口不请求
        this.$http.get('cmdb/vm_server/' + this.row.id + '/').then(res => {
          if (res.data.code == 200) {
            // IDC机房：从对象中提取ID字段重新赋值
            this.row.idc = res.data.data.idc.id
            // 主机分组：从对象中提取ID（多个）ID字段重新赋值
            const group_id = new Array()
            const server_group = res.data.data.server_group
            for (let i in server_group) {
              group_id.push(server_group[i].id)
            }
            this.row.server_group = group_id

            // 给虚拟主机重新赋值
            this.row.vm_host = res.data.data.vm_host.id


            // 重新渲染编辑对话框IDC机房和主机分组
            this.getIdc()
            this.getServerGroup()
            this.getCredential()
            this.getVmHost()
          }
        })
      }
    }
  }
}
</script>

<style scoped></style>
