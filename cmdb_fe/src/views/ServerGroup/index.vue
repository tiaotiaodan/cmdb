<template>
  <el-card class="box-card">
    <!--数据搜索-->
    <div style="margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between">
      <div>
        <el-row>
          <el-col :span="22">
            <!--
              v-model="urlParams.search" 是绑定搜索的数据
              @keyup.enter="onSearch"  是输入完后，使用回车键进行快捷搜索
              clearable   属性即可得到一个可一键清空的输入框
              @clear="onSearch"   搜索框进行清空数据回调函数
            -->
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
        <!--新建-->
        <el-button type="primary" @click="handelServerGroupCreate"><el-icon><CirclePlus /></el-icon>&nbsp;新建</el-button>
        
        <!--展示列弹出框-->
        <el-popover placement="left" :width="100" v-model:visible="columnVisible">
          <template #reference>
            <el-button type="primary" @click="columnVisible = true">
              <el-icon><Tools /></el-icon>
              &nbsp;展示列
            </el-button>
          </template>
          <el-checkbox v-model="showColumn.name" disabled>分组名称</el-checkbox>
          <el-checkbox v-model="showColumn.create_time">创建时间</el-checkbox>
          <el-checkbox v-model="showColumn.note">备注</el-checkbox>
          <div style="text-align: right; margin: 0">
            <el-button size="small" type="primary" @click="columnVisible = false">取消</el-button>
            <el-button size="small" type="primary" @click="saveColumn">确认</el-button>
          </div>
        </el-popover>
      </div>
    </div>

    <div>
      <!--数据表格-->
      <el-table :data="ServerGroupData" border style="width: 100%" :header-cell-style="{ backgroundColor: '#409EFF', color: '#fff', fontsize: '14px' }">
        <el-table-column prop="name" label="分组名称" width="280" />
        <el-table-column prop="note" label="备注" v-if="showColumn.note" />
        <el-table-column prop="create_time" label="创建时间" :formatter='dateFormat' v-if="showColumn.create_time" />
        <!--操作栏-->
        <el-table-column label="操作栏" fixed="right" width="140">
          <!--定义获取行内数据参数-->
          <template #default="scope">
            <!--通过回调函数获取行内数据-->
            <!-- 编辑按钮 -->
            <el-button type="primary" size="small"  @click="handelServerGroupEdit(scope.$index, scope.row)">编辑</el-button>
            <el-button type="danger" size="small"  @click="handelServerGroupDelete(scope.$index, scope.row)">删除</el-button>
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
  <ServerGroupEdit v-model:visible="dialogServerGroupEdit" :row="row"></ServerGroupEdit>
  <ServerGroupCreate v-model:visible="dialogServerGroupCreate"></ServerGroupCreate>
</template>

<script>
// 导入子组件ServerGroup编辑
import ServerGroupEdit from './ServerGroupEdit.vue'
import ServerGroupCreate from './ServerGroupCreate.vue'
export default {
  name: 'ServerGroup',
  // 引用子组件
  components: {
    ServerGroupEdit,
    ServerGroupCreate
  },
  data() {
    return {
      ServerGroupData: [], // 存放数据表格列表

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
      dialogServerGroupEdit: false,
      row: '',

      // ============================== 创建 ===================
      dialogServerGroupCreate: false,

      // ============================== 展示列 ==================
      columnVisible: false, // 可展示列显示与隐藏
      showColumn: {
        // 字段默认是否展示
        name: true,
        city: true,
        provider: true,
        note: true,
        create_time: true
      }
    }
  },
  // 页面渲染完后挂载
  mounted() {
    // 渲染完后挂载数据
    this.getallServerGroup()
    // 从浏览器本地存储获取历史存储展示
    const  columnSet = localStorage.getItem(this.$route.path + '-columnSet')
    // 如果本地有存储就使用
    if(columnSet) {
      this.showColumn = JSON.parse(columnSet)
    }
  },
  // 请求方法
  methods: {
    getallServerGroup() {
      this.$http.get('cmdb/server_group/', { params: this.urlParams }).then(res => {
        if (res.data.code == 200) {
          // 把获取数据重新赋值到表格
          this.ServerGroupData = res.data.data
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
      this.getallServerGroup()
    },
    // 新建ServerGroup机房
    handelServerGroupCreate() {
      // 重新赋值允许打开编辑弹出框
      this.dialogServerGroupCreate = true
    },
    // 编辑进行数据重新赋值
    handelServerGroupEdit(index, row) {
      // 重新赋值允许打开编辑弹出框
      this.dialogServerGroupEdit = true
      this.row = row
    },
    // 删除单条数据
    handelServerGroupDelete(index,row) {
      this.$confirm('你确定要删除选中的吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$http
          .delete('/cmdb/server_group/' + row.id + '/')
          .then(res => {
            if (res.data.code == 200) {
              this.$message.success('删除成功')
              this.ServerGroupData.splice(index,1) // 根据表格索引临时删除数据
            }
          })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    // 展示列事件调用
    saveColumn() {
      // 将可显示的字段存储到浏览器本地存储, 使用路由+key保存唯一key值
      localStorage.setItem(this.$route.path + '-columnSet', JSON.stringify(this.showColumn))
      // 关闭展示列
      this.columnVisible = false
    },
    // 分页：监听【选择每页数量】的事件
    handleSizeChange(pageSize) {
      // console.log(pageSize)
      this.pageSize = pageSize // 重新设置分页显示
      this.urlParams.page_size = pageSize // 将最新值设置到数据里，用于下面用新值重新获取数据
      this.getallServerGroup()
    },
    // 分页：监听【点击页码】的事件
    handleCurrentChange(currentPage) {
      // console.log(currentPage)
      this.currentPage = currentPage // 重新设置分页显示
      this.urlParams.page_num = currentPage
      this.getallServerGroup()
    },

    // drf返回时间戳进行转换为标准显示格式
    dateFormat(row, col) {
      let data = row[col.property]
      if (data == null) {
        return ''
      }

      let currDate = new Date(data)
      // 例如 2022-8-15 10:21:30
      let getMonth = currDate.getMonth() + 1
      let getDay = currDate.getDate()
      let getHours = currDate.getHours()
      let getMinutes = currDate.getMinutes()
      let getSeconds = currDate.getSeconds()
      if (getMonth < 10) {
        getMonth =  '0' + getMonth
      }
      if (getDay < 10) {
        getDay =  '0' + getDay
      }
      if (getHours < 10) {
        getHours =  '0' + getHours
      }
      if (getMinutes < 10) {
        getMinutes =  '0' + getMinutes
      }
      if (getSeconds < 10) {
        getSeconds =  '0' + getSeconds
      }
      // 组合进行返回时间操作
      return currDate.getFullYear() + '-' + getMonth + '-' + getDay + ' ' + getHours + ':' + getMinutes + ':' + getSeconds
    }
  }
}
</script>

<style scoped></style>
