import { createRouter, createWebHistory } from "vue-router";
import LayoutView from "../layout/index.vue";

const routes = [
  {
    path: "/",
    name: "首页",
    component: LayoutView,
    redirect: "/dashboard", // 重定向跳转到仪表盘
    children: [
      {
        path: "/dashboard",
        name: "仪表盘",
        icon: "HomeFilled",
        component: () => import("../views/Dashboard.vue"),
      },
    ],
  },
  {
    path: "/nav1",
    name: "一级菜单",
    icon: "Menu",
    component: LayoutView,
    children: [
      {
        path: "/nav1/a",
        name: "页面A",
        component: () => import("../views/A.vue"),
      },
      {
        path: "/nav1/b",
        name: "页面B",
        component: () => import("../views/B.vue"),
      },
    ],
  },
  {
    path: "/nav2",
    name: "二级菜单",
    icon: "Grid",
    component: LayoutView,
    children: [
      {
        path: "/nav2/c",
        name: "页面C",
        component: () => import("../views/C.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
