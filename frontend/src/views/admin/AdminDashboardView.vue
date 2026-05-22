<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import api from '../../api/client'
import EmptyState from '../../components/EmptyState.vue'
import FeaturePanel from '../../components/FeaturePanel.vue'
import LoadingState from '../../components/LoadingState.vue'
import SectionTitle from '../../components/SectionTitle.vue'
import StatCard from '../../components/StatCard.vue'
import AdminTable from '../../components/admin/AdminTable.vue'
import { useAdminStore } from '../../stores/admin'

const router = useRouter()
const store = useAdminStore()
const loading = ref(true)
const metrics = ref(null)
const categories = ref([])
const points = ref([])
const newsList = ref([])
const error = ref('')

const categoryForm = ref({
  name: '',
  slug: '',
  icon: '',
  cover_image: '',
  sort_order: 0,
  description: '',
})

const pointForm = ref({
  name: '',
  category_id: '',
  address: '',
  opening_hours: '',
  description: '',
  service_content: '',
  target_people: '',
  image_url: '',
  is_featured: false,
  status: 'published',
})

const newsForm = ref({
  title: '',
  summary: '',
  content: '',
  status: 'published',
})

const adminSteps = [
  '先录入分类，确保点位表单可关联分类。',
  '再录入点位信息，优先补足名称、地址、开放时间和简介。',
  '最后补充资讯，用于首页和资讯页展示动态内容。',
]

async function loadAdminData() {
  loading.value = true
  error.value = ''
  try {
    const [dashboard, categoryRes, pointRes, newsRes] = await Promise.all([
      api.get('/admin/dashboard'),
      api.get('/admin/categories'),
      api.get('/admin/points'),
      api.get('/admin/news'),
    ])
    metrics.value = dashboard.data
    categories.value = categoryRes.data
    points.value = pointRes.data.items
    newsList.value = newsRes.data.items
  } catch (err) {
    error.value = err.response?.data?.detail || '后台数据加载失败，请重新登录。'
    if (err.response?.status === 401) {
      store.logout()
      router.push('/admin/login')
    }
  } finally {
    loading.value = false
  }
}

async function createCategory() {
  await api.post('/admin/categories', categoryForm.value)
  categoryForm.value = {
    name: '',
    slug: '',
    icon: '',
    cover_image: '',
    sort_order: 0,
    description: '',
  }
  await loadAdminData()
}

async function createPoint() {
  await api.post('/admin/points', {
    ...pointForm.value,
    category_id: Number(pointForm.value.category_id),
  })
  pointForm.value = {
    name: '',
    category_id: '',
    address: '',
    opening_hours: '',
    description: '',
    service_content: '',
    target_people: '',
    image_url: '',
    is_featured: false,
    status: 'published',
  }
  await loadAdminData()
}

async function createNews() {
  await api.post('/admin/news', newsForm.value)
  newsForm.value = {
    title: '',
    summary: '',
    content: '',
    status: 'published',
  }
  await loadAdminData()
}

function logout() {
  store.logout()
  router.push('/admin/login')
}

onMounted(loadAdminData)
</script>

<template>
  <div class="space-y-8">
    <section class="flex flex-col gap-5 rounded-[2rem] bg-slate-900 p-8 text-white shadow-xl lg:flex-row lg:items-end lg:justify-between">
      <div>
        <p class="text-sm uppercase tracking-[0.2em] text-cyan-200">后台管理</p>
        <h1 class="mt-3 text-3xl font-semibold">便民资源维护台</h1>
        <p class="mt-3 text-sm leading-6 text-slate-300">
          当前登录账号：{{ store.username || 'admin' }}。可在此录入课程演示所需的分类、点位和资讯。
        </p>
      </div>
      <button class="rounded-2xl bg-white px-5 py-3 text-sm font-medium text-slate-900" @click="logout">
        退出登录
      </button>
    </section>

    <LoadingState v-if="loading" />
    <EmptyState v-else-if="error" title="后台加载失败" :description="error" />

    <template v-else>
      <section class="grid gap-5 lg:grid-cols-[1.1fr_0.9fr]">
        <div class="grid gap-5 md:grid-cols-3">
          <StatCard eyebrow="分类数量" :value="String(metrics?.category_count || 0)" description="分类是点位组织的基础。" tone="cyan" />
          <StatCard eyebrow="点位数量" :value="String(metrics?.point_count || 0)" description="点位数据决定前台展示丰富度。" tone="emerald" />
          <StatCard eyebrow="资讯数量" :value="String(metrics?.news_count || 0)" description="资讯用于首页动态和公告展示。" tone="amber" />
        </div>
        <FeaturePanel
          badge="录入建议"
          title="先保证内容完整，再追求内容多。"
          description="对于课程演示版，优先确保每类至少有基础样例，且一条点位信息字段尽量完整，这会比堆很多残缺数据更有说服力。"
        >
          <ul class="space-y-2 text-sm leading-7 text-slate-300">
            <li v-for="step in adminSteps" :key="step">{{ step }}</li>
          </ul>
        </FeaturePanel>
      </section>

      <section class="space-y-5">
        <SectionTitle title="内容录入" subtitle="先搭好基础数据骨架，前台页面就能立即展示。" />
        <div class="grid gap-6 xl:grid-cols-3">
        <form class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm" @submit.prevent="createCategory">
          <h2 class="text-xl font-semibold text-slate-900">新增分类</h2>
          <div class="mt-4 space-y-3">
            <input v-model="categoryForm.name" required placeholder="分类名称" class="admin-input" />
            <input v-model="categoryForm.slug" required placeholder="slug" class="admin-input" />
            <input v-model="categoryForm.icon" placeholder="图标标识" class="admin-input" />
            <input v-model="categoryForm.cover_image" placeholder="封面图片链接" class="admin-input" />
            <input v-model.number="categoryForm.sort_order" type="number" placeholder="排序" class="admin-input" />
            <textarea v-model="categoryForm.description" rows="4" placeholder="分类说明" class="admin-input"></textarea>
            <button class="admin-button">保存分类</button>
          </div>
        </form>

        <form class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm" @submit.prevent="createPoint">
          <h2 class="text-xl font-semibold text-slate-900">新增点位</h2>
          <div class="mt-4 space-y-3">
            <input v-model="pointForm.name" required placeholder="点位名称" class="admin-input" />
            <select v-model="pointForm.category_id" required class="admin-input">
              <option value="">选择分类</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
            <input v-model="pointForm.address" required placeholder="详细地址" class="admin-input" />
            <input v-model="pointForm.opening_hours" placeholder="开放时间" class="admin-input" />
            <textarea v-model="pointForm.description" rows="3" required placeholder="点位简介" class="admin-input"></textarea>
            <textarea v-model="pointForm.service_content" rows="3" placeholder="服务内容" class="admin-input"></textarea>
            <input v-model="pointForm.target_people" placeholder="适用人群" class="admin-input" />
            <input v-model="pointForm.image_url" placeholder="图片链接" class="admin-input" />
            <label class="flex items-center gap-2 text-sm text-slate-600">
              <input v-model="pointForm.is_featured" type="checkbox" />
              设为推荐点位
            </label>
            <button class="admin-button">保存点位</button>
          </div>
        </form>

        <form class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm" @submit.prevent="createNews">
          <h2 class="text-xl font-semibold text-slate-900">新增资讯</h2>
          <div class="mt-4 space-y-3">
            <input v-model="newsForm.title" required placeholder="资讯标题" class="admin-input" />
            <textarea v-model="newsForm.summary" rows="3" required placeholder="资讯摘要" class="admin-input"></textarea>
            <textarea v-model="newsForm.content" rows="6" required placeholder="资讯正文" class="admin-input"></textarea>
            <button class="admin-button">发布资讯</button>
          </div>
        </form>
        </div>
      </section>

      <section class="space-y-6">
        <SectionTitle title="已录入数据" subtitle="方便课堂演示时快速查看当前系统中的内容规模。" />
        <AdminTable
          :columns="[
            { key: 'name', label: '分类名称' },
            { key: 'slug', label: 'Slug' },
            { key: 'sort_order', label: '排序' },
          ]"
          :rows="categories"
        />
        <AdminTable
          :columns="[
            { key: 'name', label: '点位名称' },
            { key: 'address', label: '地址' },
            { key: 'status', label: '状态' },
          ]"
          :rows="points"
        />
        <AdminTable
          :columns="[
            { key: 'title', label: '资讯标题' },
            { key: 'summary', label: '摘要' },
            { key: 'status', label: '状态' },
          ]"
          :rows="newsList"
        />
      </section>
    </template>
  </div>
</template>
