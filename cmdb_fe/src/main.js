import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

// 导入elementui和css
import Elementplus from "element-plus";
import "element-plus/dist/index.css";

// 注册icon图标
import * as ElementPlusIconsVue from "@element-plus/icons-vue";

// 创建实例
const app = createApp(App);

// 统一注册el-icon图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

// 注册store
app.use(store);
// 注册router
app.use(router);
// 注册Elementplus
app.use(Elementplus);
// 挂载实例
app.mount("#app");
