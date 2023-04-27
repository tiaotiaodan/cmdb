<template>
  <el-card class="box-card">
    <div style="margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between">
      <div>
      <!--
        v-model="urlParams.search" 是绑定搜索的数据
        @keyup.enter="onSearch"  是输入完后，使用回车键进行快捷搜索
        clearable   属性即可得到一个可一键清空的输入框
        @clear="onSearch"   搜索框进行清空数据回调函数
      -->
        <el-row>
          <el-col :span="22">
            <el-input v-model="urlParams.search" placeholder="请输入搜索域名名称或平台" @keyup.enter="onSearch" clearable @clear="onSearch" class="search" />
          </el-col>
          <el-col :span="1" style="margin-left: 5px">
            <el-button type="primary" @click="onSearch">
              <el-icon><search /></el-icon>
              &nbsp;搜索
            </el-button>
          </el-col>
        </el-row>
      </div>
      <div>
        <!--新建阿里云导入-->
        <el-dropdown style="margin-right: 12px">
          <el-button type="primary">
            <el-icon><CirclePlus /></el-icon>
            &nbsp;新建
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="handelDomainCreateCloud_btn">
                <el-icon color="#409EFC" :size="21"><MostlyCloudy /></el-icon>
                云主机
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <div>
      <!--数据表格-->
      <el-table :data="DomainData" border style="width: 100%">
        <el-table-column prop="name" label="域名名称" width="180" />
        <el-table-column prop="platform" label="平台管理" width="180" />
        <!--域名状态显示-->
        <el-table-column prop="status" label="域名状态" sortable>
          <template #default="scope">
            <el-icon :size="18" color="#409EFC" v-if="scope.row.status == '域名持有者信息修改中'"><Avatar /></el-icon>
            <el-icon :size="18" color="#F56C6C" v-else-if="scope.row.status == '急需续费'"><WarningFilled /></el-icon>
            <el-icon :size="18" color="#F56C6C" v-else-if="scope.row.status == '急需赎回'"><WarningFilled /></el-icon>
            <el-icon :size="18" color="#E6A23C" v-else-if="scope.row.status == '转出中'"><WarnTriangleFilled /></el-icon>
            <el-icon :size="18" color="#909399" v-else-if="scope.row.status == '未认证'"><WarnTriangleFilled /></el-icon>
            <el-icon :size="18" color="#F56C6C" v-else-if="scope.row.status == '实名认证失败'"><WarnTriangleFilled /></el-icon>
            <el-icon :size="18" color="#E6A23C" v-else-if="scope.row.status == '实名认证审核中'"><WarnTriangleFilled /></el-icon>
            <el-icon :size="18" color="#67C23A" v-else="scope.row.status == '正常'"><SuccessFilled /></el-icon>
            {{ scope.row.status }}
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" />
        <el-table-column prop="expire_time" label="到期时间" />
        <!--修改过期时间显示-->
        <el-table-column prop="ExpirationTime" label="过期时间提示" sortable>
          <template #default="scope">
            <el-tag class="ml-2" type="success" v-if="scope.row.ExpirationDateStatus == 1">还有{{ scope.row.ExpirationTime }}天过期</el-tag>
            <el-tag class="ml-2" type="danger" v-if="scope.row.ExpirationDateStatus == 2">已过期{{ scope.row.ExpirationTime }}天</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="note" label="备注" />
        <!--操作栏-->
        <el-table-column label="操作栏" fixed="right" width="180">
          <!--定义获取行内数据参数-->
          <template #default="scope">
            <!--通过回调函数获取行内数据-->
            <el-button type="primary" size="small" round @click="DomainManageEdit_btn(scope.$index, scope.row)">编辑</el-button>
            <el-button type="danger" size="small" round @click="DomainManageDelete_btn(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!--分页-->
      <div style="margin-top: 20px">
        <el-pagination v-model:currentPage="currentPage" :page-sizes="[10, 20, 50, 100]" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="total" background @size-change="handleSizeChange" @current-change="handleCurrentChange"></el-pagination>
      </div>
    </div>
  </el-card>

  <!--使用子组件-->
  <DomainEdit v-model:visible="dialogDomainManageEdit" :row="row"></DomainEdit>
  <DomainCreateCloud v-model:visible="dialogDomainManageColudCreate"></DomainCreateCloud>
</template>

<script>
// 导入子组件idc编辑
import DomainEdit from './DomainEdit'
import DomainCreateCloud from './DomainCreateColud'

export default {
  name: 'DomainManage',
  // 引用子组件
  components: {
    DomainEdit,
    DomainCreateCloud
  },
  data() {
    return {
      DomainData: [], // 存放数据表格列表

      // ================================ 分页配置 ============
      currentPage: 1, // 默认开始页面
      pageSize: 10, // 默认每页的数据条数
      total: 0, // 总数据条数
      urlParams: {
        // URL查询参数，传递服务端，放这里方便修改值
        page_num: 1,
        page_size: 10,
        search: ''
      },

      // =============================== 编辑配置 ===============
      dialogDomainManageEdit: false,
      row: '',
      // =============================== 编辑配置 ===============
      dialogDomainManageColudCreate: false,
    }
  },
  // 页面渲染完后挂载
  mounted() {
    this.getallDomain()
  },
  // 请求方法
  methods: {
    getallDomain() {
      this.$http
        .get('domain/domain_manage/', { params: this.urlParams })
        .then(res => {
          if (res.data.code == 200) {
            // 把获取数据重新赋值到表格
            this.DomainData = res.data.data
            // 把获取的数据总量重新赋值给total
            this.total = res.data.count
            // 反馈请求接口情况
            this.$message.success('获取数据成功')
          } else {
            this.$message.info('获取数据失败')
          }
        })
        .catch(error => {
          this.$message.error('服务端接口请求错误！' + error)
        })
    },
     handelDomainCreateCloud_btn() {
    // 重新赋值允许打开导入对话框
      this.dialogDomainManageColudCreate = true
    },
    // 搜索查询
    onSearch() {
      // 获取搜索后的数据
      this.getallDomain()
    },
    // 编辑进行数据重新赋值
    DomainManageEdit_btn(index, row) {
      // 重新赋值允许打开编辑弹出框
      this.dialogDomainManageEdit = true
      this.row = row
    },
    // 删除单条数据
    DomainManageDelete_btn(index, row) {
      console.log(index, row)
      this.$confirm('你确定要删除选中的吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.$http
            .delete('domain/domain_manage/' + row.id + '/')
            .then(res => {
              if (res.data.code == 200) {
                this.$message.success('删除成功')
                this.DomainData.splice(index, 1) // 根据表格索引临时删除数据
              }
            })
            .catch(error => {
              this.$message.error('域名管理服务接口删除请求错误' + error)
            })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },
    // 分页：监听【选择每页数量】的事件
    handleSizeChange(pageSize) {
      // console.log(pageSize)
      this.pageSize = pageSize // 重新设置分页显示
      this.urlParams.page_size = pageSize // 将最新值设置到数据里，用于下面用新值重新获取数据
      this.getallDomain()
    },
    // 分页：监听【点击页码】的事件
    handleCurrentChange(currentPage) {
      // console.log(currentPage)
      this.currentPage = currentPage // 重新设置分页显示
      this.urlParams.page_num = currentPage
      this.getallDomain()
    }
  }
}
</script>

<style scoped></style>
