<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import api from '../../api/client'
import EmptyState from '../../components/EmptyState.vue'
import FeaturePanel from '../../components/FeaturePanel.vue'
import LoadingState from '../../components/LoadingState.vue'
import StatCard from '../../components/StatCard.vue'
import AdminShell from '../../components/admin/AdminShell.vue'
import { useAdminStore } from '../../stores/admin'

const router = useRouter()
const store = useAdminStore()
const loading = ref(true)
const error = ref('')
const metrics = ref(null)

const resourceCards = [
  {
    title: '分类管理',
    description: '维护分类名称、slug、图标、排序和说明，为点位挂接提供基础结构。',
    to: '/admin/categories',
  },
  {
    title: '点位管理',
    description: '维护点位详情、分类归属、推荐标记与草稿或发布状态，是后台的核心内容库。',
    to: '/admin/points',
  },
]

async function loadDashboard() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/admin/dashboard')
    metrics.value = data
  } catch (err) {
    error.value = err.response?.data?.detail || '后台总览加载失败，请稍后重试。'
    if (err.response?.status === 401) {
      store.logout()
      router.push('/admin/login')
    }
  } finally {
    loading.value = false
  }
}

onMounted(loadDashboard)
</script>

<template>
  <AdminShell
    title="便民资源维护台"
    description="把后台收敛为清晰的资源管理入口。先看总览，再进入分类和点位两个模块做增删查改。"
  >
    <LoadingState v-if="loading" />
    <EmptyState v-else-if="error" title="后台加载失败" :description="error" />

    <template v-else>
      <section class="grid gap-5 lg:grid-cols-[1.15fr_0.85fr]">
        <div class="grid gap-5 md:grid-cols-2">
          <StatCard eyebrow="分类数量" :value="String(metrics?.category_count || 0)" description="分类决定点位组织方式。" tone="cyan" />
          <StatCard eyebrow="点位数量" :value="String(metrics?.point_count || 0)" description="点位是前台展示的主体内容。" tone="emerald" />
        </div>
        <FeaturePanel
          badge="管理建议"
          title="先让每类数据可维护，再追求数量规模。"
          description="课程演示版最重要的是闭环：管理员能录入、编辑、删除内容，前台能依据发布状态稳定展示结果。"
        >
          <ul class="space-y-2 text-sm leading-7 text-slate-300">
            <li>先在分类管理中整理分类结构，再进入点位管理录入具体点位。</li>
            <li>点位建议先以草稿保存，核对后再发布到前台。</li>
            <li>如果分类下已有点位，系统会阻止直接删除，避免误删内容。</li>
          </ul>
        </FeaturePanel>
      </section>

      <section class="grid gap-5 xl:grid-cols-2">
        <RouterLink
          v-for="card in resourceCards"
          :key="card.to"
          :to="card.to"
          class="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-0.5 hover:border-cyan-300 hover:shadow-md"
        >
          <p class="text-sm font-semibold uppercase tracking-[0.18em] text-cyan-700">资源管理</p>
          <h2 class="mt-4 text-2xl font-semibold text-slate-900">{{ card.title }}</h2>
          <p class="mt-3 text-sm leading-7 text-slate-600">{{ card.description }}</p>
          <p class="mt-6 text-sm font-medium text-cyan-700">进入模块</p>
        </RouterLink>
      </section>
    </template>
  </AdminShell>
</template>
