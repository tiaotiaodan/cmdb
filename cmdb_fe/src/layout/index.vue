<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="200px">
        <el-menu
          active-text-color="#ffd04b"
          background-color="#545c64"
          class="el-menu-vertical-demo"
          default-active="2"
          text-color="#fff"
          router
        >
          <template v-for="menu in this.$router.options.routes" :key="menu">
            <!--处理一级菜单没有子路由-->
            <el-menu-item v-if="!menu.children" :index="menu.path">
              <!--字体图标-->
              <el-icon><icon-menu /></el-icon>
              <span>{{ menu.name }}</span>
            </el-menu-item>

            <!-- 处理仪表盘 -->
            <el-menu-item
              v-if="menu.path == '/'"
              :index="menu.children[0].path"
            >
              <!--字体图标-->
              <el-icon
                ><component :is="menu.children[0].icon"></component
              ></el-icon>
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
              <el-menu-item
                v-for="child in menu.children"
                :key="child"
                :index="child.path"
              >
                {{ child.name }}
              </el-menu-item>
            </el-sub-menu>
          </template>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header>顶部</el-header>
        <el-main>
          <!--路由占位符-->
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: "LayoutView",
};
</script>

<style scoped>
.el-header {
  background-color: orange;
}
.el-aside {
  background-color: green;
}
.el-main {
  background-color: skyblue;
}
</style>
