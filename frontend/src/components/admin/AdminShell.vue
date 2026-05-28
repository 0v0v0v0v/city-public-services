<script setup>
import { useRouter, useRoute } from 'vue-router'

import { useAdminStore } from '../../stores/admin'

defineProps({
  title: {
    type: String,
    default: '',
  },
  description: {
    type: String,
    default: '',
  },
})

const router = useRouter()
const route = useRoute()
const store = useAdminStore()

const navItems = [
  { label: '后台总览', to: '/admin', description: '查看数据规模和管理入口。' },
  { label: '分类管理', to: '/admin/categories', description: '维护分类名称、排序和展示说明。' },
  { label: '点位管理', to: '/admin/points', description: '维护点位详情、推荐位和发布状态。' },
  { label: '资讯管理', to: '/admin/news', description: '维护资讯正文、摘要和发布状态。' },
]

function logout() {
  store.logout()
  router.push('/admin/login')
}
</script>

<template>
  <div class="space-y-6">
    <section class="rounded-[2rem] bg-slate-950 p-8 text-white shadow-xl">
      <div class="flex flex-col gap-5 xl:flex-row xl:items-end xl:justify-between">
        <div>
          <p class="text-sm uppercase tracking-[0.2em] text-cyan-200">后台管理</p>
          <h1 class="mt-3 text-3xl font-semibold">{{ title }}</h1>
          <p class="mt-3 max-w-3xl text-sm leading-7 text-slate-300">
            {{ description }}
          </p>
          <p class="mt-3 text-sm text-slate-400">当前登录账号：{{ store.username || 'admin' }}</p>
        </div>
        <div class="flex flex-wrap gap-3">
          <slot name="actions" />
          <button
            class="rounded-2xl border border-slate-700 bg-slate-900 px-5 py-3 text-sm font-medium text-slate-100 transition hover:border-slate-600 hover:bg-slate-800"
            @click="logout"
          >
            退出登录
          </button>
        </div>
      </div>

      <div class="mt-6 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="rounded-3xl border px-5 py-4 transition"
          :class="
            route.path === item.to
              ? 'border-cyan-400 bg-cyan-500/10 text-white'
              : 'border-white/10 bg-white/5 text-slate-200 hover:border-cyan-400/40 hover:bg-white/8'
          "
        >
          <p class="text-sm font-semibold">{{ item.label }}</p>
          <p class="mt-2 text-xs leading-6 text-slate-300">{{ item.description }}</p>
        </RouterLink>
      </div>
    </section>
    <slot />
  </div>
</template>
