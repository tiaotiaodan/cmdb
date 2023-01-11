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
        <el-dropdown style="margin-right: 12px">
          <el-button type="primary">
            <el-icon><CirclePlus /></el-icon>
            &nbsp;新建
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="handelCloudServerCreate">
                <el-icon color="#409EFC" :size="20"><Edit /></el-icon>
                新建单台主机
              </el-dropdown-item>
              <el-dropdown-item>
                <el-icon color="#409EFC" :size="20"><Folder /></el-icon>
                Excel
              </el-dropdown-item>
              <el-dropdown-item @click="cloudDialogVisible = true">
                <el-icon color="#409EFC" :size="21"><MostlyCloudy /></el-icon>
                云主机
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>

        <!--展示列弹出框-->
        <el-popover placement="left" :width="100" v-model:visible="columnVisible">
          <template #reference>
            <el-button type="primary" @click="columnVisible = true">
              <el-icon><Tools /></el-icon>
              &nbsp;展示列
            </el-button>
          </template>
          <el-checkbox v-model="showColumn.name" disabled>名称</el-checkbox>
          <el-checkbox v-model="showColumn.hostname" disabled>主机名</el-checkbox>
          <el-checkbox v-model="showColumn.idc">IDC机房</el-checkbox>
          <el-checkbox v-model="showColumn.server_group">主机分组</el-checkbox>
          <el-checkbox v-model="showColumn.machine_type">机器类型</el-checkbox>
          <el-checkbox v-model="showColumn.os_version">系统版本</el-checkbox>
          <el-checkbox v-model="showColumn.public_ip">公网IP</el-checkbox>
          <el-checkbox v-model="showColumn.private_ip">私有IP</el-checkbox>
          <el-checkbox v-model="showColumn.cpu_num">CPU数量</el-checkbox>
          <el-checkbox v-model="showColumn.memory">内存</el-checkbox>
          <el-checkbox v-model="showColumn.disk">硬盘</el-checkbox>
          <el-checkbox v-model="showColumn.network">带宽</el-checkbox>
          <el-checkbox v-model="showColumn.put_shelves_date">上架日期</el-checkbox>
          <el-checkbox v-model="showColumn.off_shelves_date">下架日期</el-checkbox>
          <el-checkbox v-model="showColumn.expire_datetime">租约过期时间</el-checkbox>
          <el-checkbox v-model="showColumn.is_verified">SSH验证状态</el-checkbox>
          <el-checkbox v-model="showColumn.note">备注</el-checkbox>
          <el-checkbox v-model="showColumn.update_time">更新时间</el-checkbox>
          <el-checkbox v-model="showColumn.create_time">创建时间</el-checkbox>
          <div style="text-align: right; margin: 0">
            <el-button size="small" type="primary" @click="columnVisible = false">取消</el-button>
            <el-button size="small" type="primary" @click="saveColumn">确认</el-button>
          </div>
        </el-popover>
      </div>
    </div>

    <div>
      <!--数据表格-->
      <el-table :data="CloudServerData" border style="width: 100%" :header-cell-style="{ backgroundColor: '#409EFF', color: '#fff', fontsize: '14px' }">
        <el-table-column type="selection" width="60"  align="center" />
        <el-table-column prop="name" label="名称"  fixed="left"  width="120"  sortable  v-if="showColumn.name"/>
        <el-table-column prop="hostname" label="主机名"  width="120" sortable v-if="showColumn.hostname" />
        <!--修改一对多idc机房-->
        <el-table-column prop="idc" label="IDC机房" width="160" sortable v-if="showColumn.idc">
          <template #default="scope">
            <img src="../../assets/img/aliyun.png" style="width: 18px; height: 18px" v-if="showColumn.idc.provider == '阿里云'" />
            <img src="../../assets/img/tencend.png" style="width: 18px; height: 18px" v-if="showColumn.idc.provider == '腾讯云'" />
            <el-icon :size="18" color="#409EFC" v-else><office-building /></el-icon>
            {{ scope.row.idc.city }}-{{ scope.row.idc.name }}
          </template>
        </el-table-column>
        <!--修改多对多主机分组-->
        <el-table-column prop="server_group" label="主机分组" width="150" sortable v-if="showColumn.server_group">
          <template #default="scope">
            <el-tag class="ml-2" type="info" v-for="group in scope.row.server_group" :key="group.id">{{ group.name }}</el-tag>
          </template>
        </el-table-column>
        <!--通过elementpuls进行筛选，进行自定义格式显示-->
        <el-table-column prop="machine_type" label="机器类型" width="110" sortable v-if="showColumn.machine_type">
          <template #default="scope">
            <span v-if="scope.row.machine_type == 'linux'">
              <img src="../../assets/img/linux.png" style="width: 18px; height: 18px" />
              linux
            </span>
            <span v-else-if="scope.row.machine_type == 'windows'">
              <img src="../../assets/img/windows.png" style="width: 18px; height: 18px" />
              &nbsp;windows
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="os_version" label="系统版本" width="120" sortable v-if="showColumn.os_version"  />
        <!--修改IP显示-->
        <el-table-column prop="public_ip" label="公网IP" width="180" sortable v-if="showColumn.public_ip">
          <template #default="scope">
            <!--使用tag标签进行后台标记-->
            <el-tag type="info" v-for="(ip, index) in scope.row.public_ip" :key="index">{{ ip }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="private_ip" label="私有IP" width="180" sortable v-if="showColumn.private_ip" >
            <template #default="scope">
            <!--使用tag标签进行后台标记-->
            <el-tag type="info" v-for="(ip, index) in scope.row.private_ip" :key="index">{{ ip }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cpu_num" label="CPU"  width="120" sortable  v-if="showColumn.cpu_num" />
        <el-table-column prop="memory" label="内存" width="120" sortable v-if="showColumn.memory" />
        <!--由于后端model修改为json存储，再次通过提取字段内嵌表格方式展示-->
        <el-table-column prop="disk" label="硬盘" width="200" sortable v-if="showColumn.disk">
          <template #default="scope">
            <table style="background: #ebeef5; width: 100%" v-if="scope.row.disk">
              <!--表格背景设置灰色，表格内默认白色-->
              <thead>
                <tr>
                  <th>设备</th>
                  <th>类型</th>
                  <th>容量</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(disk, index) in scope.row.disk" :key="index">
                  <td>{{ disk.device }}</td>
                  <td>{{ disk.type }}</td>
                  <td>{{ disk.size }}</td>
                </tr>
              </tbody>
            </table>
            <span v-else>{{ scope.row.disk }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="network" label="带宽"  width="120" sortable v-if="showColumn.network" />
        <el-table-column prop="put_shelves_date" label="上架时间" width="120" sortable v-if="showColumn.put_shelves_date" />
        <el-table-column prop="off_shelves_date" label="下架时间" width="120" sortable v-if="showColumn.off_shelves_date"  />
        <el-table-column prop="expire_datetime" label="租约过期时间" width="160" sortable v-if="showColumn.expire_datetime" />
        <!--通过elementpuls进行筛选，进行自定义格式显示-->
        <el-table-column prop="is_verified" label="SSH状态" width="120" sortable v-if="showColumn.is_verified">
          <template #default="scope">
            <!--使用el-tag进行背景样式显示-->
            <el-tag type="success" v-if="scope.row.is_verified == 'verified'">已验证</el-tag>
            <el-tag type="warning" v-if="scope.row.is_verified == 'unverified'">未验证</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="note" label="备注" v-if="showColumn.note" />
        <el-table-column prop="update_time" label="更新时间" width="160" sortable v-if="showColumn.update_time" />
        <el-table-column prop="create_time" label="创建时间" width="160" sortable v-if="showColumn.create_time" />
        <!--操作栏-->
        <el-table-column label="操作栏" fixed="right" width="100">
          <!--定义获取行内数据参数-->
          <template #default="scope">
            <!--通过回调函数获取行内数据-->
            <!-- 编辑按钮 -->
            <el-button type="primary" size="small" circle @click="handelCloudServerEdit(scope.$index, scope.row)">
              <el-icon><Edit /></el-icon>
            </el-button>
            <el-button type="danger" size="small" circle @click="handelCloudServerDelete(scope.$index, scope.row)">
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
  <CloudServerEdit v-model:visible="dialogCloudServerEdit" :row="row"></CloudServerEdit>
  <CloudServerCreate v-model:visible="dialogCloudServerCreate"></CloudServerCreate>
</template>

<script>
// 导入子组件CloudServer编辑
import CloudServerEdit from './CloudServerEdit.vue'
import CloudServerCreate from './CloudServerCreate.vue'
export default {
  name: 'CloudServer',
  // 引用子组件
  components: {
    CloudServerEdit,
    CloudServerCreate
  },
  data() {
    return {
      CloudServerData: [], // 存放数据表格列表

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
      dialogCloudServerEdit: false,
      row: '',

      // ============================== 创建 ===================
      dialogCloudServerCreate: false,

      // ============================== 展示列 ==================
      columnVisible: false, // 可展示列显示与隐藏
      showColumn: {
        // 字段默认是否展示
        name: true,
        hostname: true,
        idc: true,
        server_group: true,
        machine_type: false,
        os_version: true,
        public_ip: true,
        private_ip: true,
        cpu_num: true,
        memory: true,
        disk: true,
        network: true,
        put_shelves_date: false,
        off_shelves_date: false,
        expire_datetime: false,
        is_verified: false,
        update_time: false,
        create_time: false,
        note: false
      }
    }
  },
  // 页面渲染完后挂载
  mounted() {
    // 渲染完后挂载数据
    this.getallCloudServer()
    // 从浏览器本地存储获取历史存储展示
    const  columnSet = localStorage.getItem(this.$route.path + '-columnSet')
    // 如果本地有存储就使用
    if(columnSet) {
      this.showColumn = JSON.parse(columnSet)
    }
  },
  // 请求方法
  methods: {
    getallCloudServer() {
      this.$http.get('cmdb/cloud_server/', { params: this.urlParams }).then(res => {
        if (res.data.code == 200) {
          // 把获取数据重新赋值到表格
          this.CloudServerData = res.data.data
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
      this.getallCloudServer()
    },
    // 新建CloudServer机房
    handelCloudServerCreate() {
      // 重新赋值允许打开编辑弹出框
      this.dialogCloudServerCreate = true
    },
    // 编辑进行数据重新赋值
    handelCloudServerEdit(index, row) {
      // 重新赋值允许打开编辑弹出框
      this.dialogCloudServerEdit = true
      this.row = row
    },
    // 删除单条数据
    handelCloudServerDelete(index,row) {
      this.$confirm('你确定要删除选中的吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$http
          .delete('cmdb/cloud_server/' + row.id + '/')
          .then(res => {
            if (res.data.code == 200) {
              this.$message.success('删除成功')
              this.CloudServerData.splice(index,1) // 根据表格索引临时删除数据
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
      this.getallCloudServer()
    },
    // 分页：监听【点击页码】的事件
    handleCurrentChange(currentPage) {
      // console.log(currentPage)
      this.currentPage = currentPage // 重新设置分页显示
      this.urlParams.page_num = currentPage
      this.getallCloudServer()
    }
  }
}
</script>

<style scoped></style>
