<template>
  <el-row :gutter="24" style="margin-top: 10px">
    <el-col :span="4">
      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <span>机房数量</span>
          </div>
        </template>
        <div>
          <el-progress type="circle" :percentage="100" status="success" width="50" />
          <span class="number">{{ idc_number }}</span>
        </div>
      </el-card>
    </el-col>
    <el-col :span="4">
      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <span>项目数量</span>
          </div>
        </template>
        <div>
          <el-progress type="circle" :percentage="100" status="success" width="50" />
          <span class="number">{{ project_number }}</span>
        </div>
      </el-card>
    </el-col>
    <el-col :span="4">
      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <span>云服务器数量</span>
          </div>
        </template>
        <div>
          <el-progress type="circle" :percentage="100" status="success" width="50" />
          <span class="number">{{ cloud_server_number }}</span>
        </div>
      </el-card>
    </el-col>
    <el-col :span="4">
      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <span>物理主机数量</span>
          </div>
        </template>
        <div>
          <el-progress type="circle" :percentage="100" status="success" width="50" />
          <span class="number">{{ Physics_server_number }}</span>
        </div>
      </el-card>
    </el-col>
    <el-col :span="4">
      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <span>虚拟机数量</span>
          </div>
        </template>
        <div>
          <el-progress type="circle" :percentage="100" status="success" width="50" />
          <span class="number">{{ vm_server_number }}</span>
        </div>
      </el-card>
    </el-col>
    <el-col :span="4">
      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <span>凭据管理数量</span>
          </div>
        </template>
        <div>
          <el-progress type="circle" :percentage="100" status="success" width="50" />
          <span class="number">{{ config_number }}</span>
        </div>
      </el-card>
    </el-col>
  </el-row>
  <br />
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <span>服务器数量</span>
      </div>
    </template>
    <div id="myChart" style="width: 100%; height: 400px"></div>
  </el-card>
</template>

<script>
import * as echarts from 'echarts'
export default {
  name: 'Dashboard',
  data() {
    return {
      idc_number: 0,
      project_number: 0,
      cloud_server_number: 0,
      Physics_server_number: 0,
      vm_server_number: 0,
      config_number: 0,
      dashboardlist: ''
    }
  },
  mounted() {
    this.getNumber()
    this.getEchat()
    this.releaseEchat()
  },
  methods: {
    getNumber() {
      this.$http.get('cmdb/idc/').then(res => {
        this.idc_number = res.data.count
      })
      this.$http.get('cmdb/server_group/').then(res => {
        this.project_number = res.data.count
      })
      this.$http.get('cmdb/cloud_server/').then(res => {
        this.cloud_server_number = res.data.count
      })
      this.$http.get('cmdb/physics_server/').then(res => {
        this.Physics_server_number = res.data.count
      })
      this.$http.get('cmdb/vm_server/').then(res => {
        this.vm_server_number = res.data.count
      })
      this.$http.get('config/credential/').then(res => {
        this.config_number = res.data.count
      })
    },
    releaseEchat() {
      // 基于准备好的dom，初始化echarts实例
      var myChart = echarts.init(document.getElementById('myChart'))
      // 绘制图表
      var option = {
        xAxis: {
          type: 'category',
          data: ['云主机', '物理机', '虚拟机']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            type: 'bar',
            barWidth: 60,
            showBackground: true,
            backgroundStyle: {
              color: 'rgba(180, 180, 180, 0.2)'
            },
            data: this.dashboardlist
          }
        ]
      }
      myChart.setOption(option) // 使用刚指定的配置项和数据显示图表。
    },
    // 请求后端数据赋值
    getEchat() {
      this.$http.get('cmdb/echart/').then(res => {
        if (res.data.code == 200) {
          // 重新赋值
          this.dashboardlist = res.data.data
          // 调用图表，进行渲染
          this.releaseEchat()
        }
      })
    }
  }
}
</script>

<style scoped>
.number {
  margin-left: 40%;
  font-size: 40px;
}
</style>
