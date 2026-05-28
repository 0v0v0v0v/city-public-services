import { createRouter, createWebHistory } from 'vue-router'

import AboutView from '../views/AboutView.vue'
import AdminCategoriesView from '../views/admin/AdminCategoriesView.vue'
import AdminDashboardView from '../views/admin/AdminDashboardView.vue'
import AdminLoginView from '../views/admin/AdminLoginView.vue'
import AdminNewsView from '../views/admin/AdminNewsView.vue'
import AdminPointsView from '../views/admin/AdminPointsView.vue'
import CategoriesView from '../views/CategoriesView.vue'
import HomeView from '../views/HomeView.vue'
import NewsDetailView from '../views/NewsDetailView.vue'
import NewsListView from '../views/NewsListView.vue'
import PointDetailView from '../views/PointDetailView.vue'
import PointsView from '../views/PointsView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/categories', component: CategoriesView },
  { path: '/points', component: PointsView },
  { path: '/points/:id', component: PointDetailView, props: true },
  { path: '/news', component: NewsListView },
  { path: '/news/:id', component: NewsDetailView, props: true },
  { path: '/about', component: AboutView },
  { path: '/admin/login', component: AdminLoginView },
  {
    path: '/admin',
    component: AdminDashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/categories',
    component: AdminCategoriesView,
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/points',
    component: AdminPointsView,
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/news',
    component: AdminNewsView,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  const token = localStorage.getItem('admin_token')
  if (to.meta.requiresAuth && !token) {
    return '/admin/login'
  }
  if (to.path === '/admin/login' && token) {
    return '/admin'
  }
  return true
})

export default router
