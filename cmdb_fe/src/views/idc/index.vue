<template>
  <el-card class="box-card">
    <!--数据搜索-->
    <div style="margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between">
      <div>
        <el-row>
          <el-col :span="22">
            <el-input v-model="urlParams.search" placeholder="请输入关键字" @keyup.enter="onSearch" clearable @clear="onSearch" class="search" />
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
        <el-button type="primary">新建</el-button>
      </div>
    </div>

    <div>
      <!--数据表格-->
      <el-table :data="IdcData" border style="width: 100%" :header-cell-style="{ backgroundColor: '#409EFF', color: '#fff', fontsize: '14px' }">
        <el-table-column prop="name" label="机房名称" width="180" />
        <el-table-column prop="city" label="城市" width="180" />
        <el-table-column prop="provider" label="运营商" />
        <el-table-column prop="note" label="备注" />
        <el-table-column prop="create_time" label="创建时间" />
        <!--操作栏-->
        <el-table-column label="操作栏" fixed="right" width="180">
          <!--定义获取行内数据参数-->
          <template #default="scope">
            <!--通过回调函数获取行内数据-->
            <!-- 编辑按钮 -->
            <el-button type="primary" size="small" circle @click="handelIdcEdit(scope.$index, scope.row)">
              <el-icon><Edit /></el-icon>
            </el-button>
            <el-button type="danger" size="small" circle @click="handelIdcDelete(scope.$index, scope.row)">
              <el-icon><Delete /></el-icon>
            </el-button>
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
  <idcEdit v-model:visible="dialogIdcEdit" :row="row"></idcEdit>
</template>

<script>
// 导入子组件idc编辑
import idcEdit from './IdcEdit.vue'
export default {
  name: 'idc',
  // 引用子组件
  components: {
    idcEdit
  },
  data() {
    return {
      IdcData: [], // 存放数据表格列表

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
      dialogIdcEdit: false,
      row: ''
    }
  },
  // 页面渲染完后挂载
  mounted() {
    this.getallIdc()
  },
  // 请求方法
  methods: {
    getallIdc() {
      this.$http.get('cmdb/idc/', { params: this.urlParams }).then(res => {
        if (res.data.code == 200) {
          // 把获取数据重新赋值到表格
          this.IdcData = res.data.data
          // 把获取的数据总量重新赋值给total
          this.total = res.data.count
          // 反馈请求接口情况
          this.$message.success('获取数据成功')
        } else {
          this.$message.info('请求数据接口失败')
        }
      })
    },
    // 搜索查询
    onSearch() {
      // 获取搜索后的数据
      this.getallIdc()
    },
    // 编辑进行数据重新赋值
    handelIdcEdit(index, row) {
      // 重新赋值允许打开编辑弹出框
      this.dialogIdcEdit = true
      this.row = row
    },
    // 分页：监听【选择每页数量】的事件
    handleSizeChange(pageSize) {
      // console.log(pageSize)
      this.pageSize = pageSize // 重新设置分页显示
      this.urlParams.page_size = pageSize // 将最新值设置到数据里，用于下面用新值重新获取数据
      this.getallIdc()
    },
    // 分页：监听【点击页码】的事件
    handleCurrentChange(currentPage) {
      // console.log(currentPage)
      this.currentPage = currentPage // 重新设置分页显示
      this.urlParams.page_num = currentPage
      this.getallIdc()
    }
  }
}
</script>

<style scoped></style>
