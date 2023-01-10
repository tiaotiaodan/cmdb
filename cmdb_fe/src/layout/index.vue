<template>
  <div class="common-layout">
    <el-container>
      <!--为了实现头部折叠菜单，我们需要把原来导航栏的固定宽度width="200px"修改width="auto"自适应-->
      <el-aside width="auto">
        <!--
        :default-active="this.$route.path"  绑定菜单栏index索引
        router    开启路由导航
        :collapse="isCollapse"   导航栏显示与隐藏
        unique-opened   开启导航栏同时只显示一个菜单
        :collapse-transition='false'  关闭折叠动画
        -->
        <el-menu active-text-color="#ffd04b" background-color="#545c64" class="el-menu-vertical-demo" default-active="this.$route.path" text-color="#fff" router unique-opened :collapse="isCollapse" :collapse-transition="false">
          <!-- 给页面添加logo -->
          <div class="logo-title">
            <img src="../assets/touxiang.jpeg" />
            <!--默认显示logo字体，侧边栏搜索隐藏logo字体-->
            <span v-if="isTitle">运维资产管理系统</span>
          </div>
          <template v-for="menu in this.$router.options.routes" :key="menu">
            <!--处理一级菜单没有子路由-->
            <el-menu-item v-if="!menu.children" v-show="false" :index="menu.path">
              <!--字体图标-->
              <span>{{ menu.name }}</span>
            </el-menu-item>

            <!-- 处理仪表盘 -->
            <el-menu-item v-if="menu.path == '/'" :index="menu.children[0].path">
              <!--字体图标-->
              <el-icon>
                <component :is="menu.children[0].icon"></component>
              </el-icon>
              <span>{{ menu.children[0].name }}</span>
            </el-menu-item>
            <!--处理一级菜单有子路由-->
            <el-sub-menu v-else-if="menu.children" :index="menu.path">
              <template #title>
                <!--字体图标-->
                <el-icon><component :is="menu.icon"></component></el-icon>
                <span>{{ menu.name }}</span>
              </template>
              <!--循环二级菜单-->
              <el-menu-item v-for="child in menu.children" :key="child" :index="child.path">
                {{ child.name }}
              </el-menu-item>
            </el-sub-menu>
          </template>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header>
          <!-- 折叠 -->
          <div class="toggle-butten">
            <!--绑定一个触发的折叠按钮-->
            <el-icon :size="25">
              <!-- 使用v-show进行控制导航栏图标展示，显示收缩图标栏先进行取反，由于导航栏默认是false取反就成了true就显示，收缩我们判断的是false才显示 -->
              <i v-show="!isCollapse" @click="toggleCollapse"><Fold /></i>
              <i v-show="isCollapse" @click="toggleCollapse"><Expand /></i>
            </el-icon>
          </div>

          <!--用户标识-->
          <div>
            <img src="../assets/touxiang.jpeg" class="touxiang" />
            <el-dropdown>
              <span class="el-dropdown-link">
                {{ username }}
                <el-icon class="el-icon--right">
                  <arrow-down />
                </el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="UserList">用户信息</el-dropdown-item>
                  <el-dropdown-item @click="UserPasswordDialog = true">修改密码</el-dropdown-item>
                  <el-dropdown-item @click="logout">退出登陆</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        <el-main>
          <!--路由占位符-->
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>

  <!--修改密码对话框-->
  <el-dialog v-model="UserPasswordDialog" width="30%" v-on:close="closDialogForm()">
   <!--标题-->
    <template #header>
      <div style="font-size:18px; color:#409eff; font-weight:bold;">用户密码修改</div>
    </template>

    <!--内容-->
    <el-form :model="UserPasswordForm" label-width="100px" :rules="rules" ref="UserPasswordForm">
      <el-form-item label="原密码：" prop="old_password">
        <el-input v-model="UserPasswordForm.old_password" type="password" show-password></el-input>
      </el-form-item>
      <el-form-item label="新密码：" prop="new_password">
        <el-input v-model="UserPasswordForm.new_password" type="password" show-password></el-input>
      </el-form-item>
      <el-form-item label="再次确认：" prop="confirm_password">
        <el-input v-model="UserPasswordForm.confirm_password" type="password" show-password></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="closDialogForm">取消</el-button>
        <el-button type="primary" @click="changePasswordSubmit">确定</el-button>
      </span>
    </template>
  </el-dialog>

  <!-- 用户信息展示 -->
  <el-dialog v-model="UserListDialog" width="30%" center  v-on:close="closUserListDialog()">
    <!--标题-->
    <template #header>
      <div style="font-size:18px; color:#409eff; font-weight:bold;">用户信息展示</div>
    </template>

    <!--内容-->
    <el-descriptions direction="horizontal" :column="2">
      <el-descriptions-item label-align=center align=center label="用户名：">{{ username }}</el-descriptions-item>
      <el-descriptions-item label-align=center align=center label="用户邮箱:"></el-descriptions-item>
    </el-descriptions>
  </el-dialog>
</template>

<script>
export default {
  name: 'LayoutView',
  data() {
    // 表单自定义数据判断
    const checkNewOldPassword = (rule, value, callback) => {
      if (value == this.UserPasswordForm.old_password) {
        callback(new Error('新密码不能与旧密码一样！'))
      } else {
        return callback()
      }
    }
    const checkNewPassword = (rule, value, callback) => {
      if (value != this.UserPasswordForm.new_password) {
        callback(new Error('两次输入密码不一致！'))
      } else {
        return callback()
      }
    }

    return {
      isCollapse: false, // 导航栏显示与隐藏
      isTitle: true, // 显示与隐藏标题
      username: window.sessionStorage.getItem('username'), // 获取login保存到会话存储的username
      UserPasswordDialog: false, // 显示修改密码对话框
      UserListDialog: false, // 显示用户信息对话框

      // ======================== 修改密码弹出框配置 ======================
      UserPasswordForm: {
        username: window.sessionStorage.getItem('username'),
        old_password: '',
        new_password: '',
        confirm_password: ''
      },
      // ======================== 查看用户信息弹出框配置 ====================
      UserListinfo: [],
      UserListinfoForm: {
        username: window.sessionStorage.getItem('username'),
      },
      // ======================== 修改密码表单验证 ======================
      rules: {
        old_password: [
          { required: true, message: '请输入原密码', trigger: 'blur' },
          { min: 6, message: '用户名长度应不小于6个字符', trigger: 'blur' }
        ],
        new_password: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 6, message: '用户名长度应不小于6个字符', trigger: 'blur' },
          { validator: checkNewOldPassword, trigger: 'blur' }
        ],
        confirm_password: [
          { required: true, message: '请确认新密码', trigger: 'blur' },
          { min: 6, message: '用户名长度应不小于6个字符', trigger: 'blur' },
          { validator: checkNewPassword, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    // 触发折叠按钮
    toggleCollapse() {
      // 根据已有的值进行取反，是true就取false，是false取反就是true
      this.isCollapse = !this.isCollapse
      this.isTitle = !this.isTitle
    },
    // 退出登陆
    logout() {
      // 清除token
      window.sessionStorage.clear()
      // 跳转到登陆
      this.$router.push('/login')
    },
    // 修改密码
    changePasswordSubmit() {
      this.$refs.UserPasswordForm.validate(valid => {
        if (valid) {
          this.$http.post('change_password/', this.UserPasswordForm).then(res => {
            if (res.data.code == 200) {
              this.$message.success('修改密码成功')
              // 调用关闭弹框函数
              this.closDialogForm()
            }
          })
        }
      })
    },
    UserList() {
      this.UserListDialog = true  // 开启弹出框
      this.$http.post('user_info/', this.UserListinfoForm).then(res => {
        if (res.data.code == 200) {
          this.UserListinfo = res.data.data
        }
      })
    },
    // 关闭修改弹出框的表单
    closDialogForm() {
      // 清空表单数据
      this.UserPasswordForm.old_password = ''
      this.UserPasswordForm.new_password = ''
      this.UserPasswordForm.confirm_password = ''

      // 关闭弹出框
      this.UserPasswordDialog = false
    },
    // 关闭查看用户信息弹出框
    closUserListDialog() {
      this.UserListDialog = false
    }
  }
}
</script>

<style scoped>
.el-header {
  height: 50px;
  background: linear-gradient(to left, rgba(1, 170, 237, 1), rgba(82, 183, 109, 1));
  display: flex; /* 使用flex布局 */
  align-items: center; /* flex水平居中 */
  justify-content: space-between; /* flex水平平分 */
  color: #fff;
}
.el-dropdown-link {
  color: #fff;
  margin: 3px 5px 0px 10px;
}
.el-aside {
  background-color: #545c64;
  height: 100%;
}
.el-main {
}

/* 处理左侧边框无法对齐，修改代码 */
.el-menu {
  border-right: none;
}

/* 优化左侧菜单宽度 */
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}

/* 处理头像图片大小 */
.touxiang {
  width: 25px;
  height: 25px;
  border-radius: 3px;
}

.logo-title {
  background-color: rgba(82, 183, 109, 1);
  margin-bottom: 10px;
  height: 50px;
  border: none;
  line-height: 50px;
  display: flex;
  align-items: center;
  padding-left: 15px;
  color: #fff;
}
.logo-title img {
  width: 32px;
  height: 32px;
  margin-right: 10px;
  border-radius: 50%;
}
.logo-title span {
  font-weight: bold;
  font-size: 16px;
  line-height: 50px;
  font-family: Averir, Helvetica Neue, Arial, Helvetica, sans-serif;
  vertical-align: middle;
}
</style>
