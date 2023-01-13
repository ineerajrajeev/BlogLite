import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("../views/LoginView.vue"),
  },
  {
    path: "/signup",
    name: "signup",
    component: () => import("../views/RegisterView.vue"),
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: () => import("../views/HomeView.vue"),
  },
  {
    path: "/analytics",
    name: "analytics",
    component: () => import("../views/AnalyticView.vue"),
  },
  {
    path: "/profile",
    name: "profile",
    component: () => import("../views/ProfileView.vue"),
  },
  {
    path: "/settings",
    name: "settings",
    component: () => import("../views/SettingsView.vue"),
  },
  {
    path: "/search",
    name: "search",
    component: () => import("../views/SearchView.vue"),
  },
  {
    path: "/user/:id",
    name: "user",
    component: () => import("../views/UserView.vue"),
  },
  {
    path: "/followers",
    name: "followers",
    component: () => import("../views/followView.vue"),
  },
  {
    path: "/newBlog",
    name: "newBlog",
    component: () => import("../views/NewBlogView.vue"),
  },
  {
    path: "/editBlog/:id",
    name: "editBlog",
    component: () => import("../views/EditBlog.vue"),
  },
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("../views/NotFound.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
