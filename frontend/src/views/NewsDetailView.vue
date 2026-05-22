<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import api from '../api/client'
import EmptyState from '../components/EmptyState.vue'
import LoadingState from '../components/LoadingState.vue'

const route = useRoute()
const item = ref(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const { data } = await api.get(`/news/${route.params.id}`)
    item.value = data
  } catch (err) {
    error.value = err.response?.data?.detail || '加载资讯失败。'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <LoadingState v-if="loading" />
  <EmptyState v-else-if="error" title="资讯不存在" :description="error" />
  <article v-else-if="item" class="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm lg:p-10">
    <p class="text-sm font-medium uppercase tracking-[0.2em] text-emerald-600">便民资讯</p>
    <h1 class="mt-4 text-3xl font-semibold text-slate-900">{{ item.title }}</h1>
    <p class="mt-4 text-sm text-slate-400">{{ new Date(item.published_at).toLocaleString('zh-CN') }}</p>
    <p class="mt-6 text-lg leading-8 text-slate-600">{{ item.summary }}</p>
    <div class="mt-8 rounded-3xl bg-slate-50 p-6 text-base leading-8 text-slate-700">
      {{ item.content }}
    </div>
  </article>
</template>
