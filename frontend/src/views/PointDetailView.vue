<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import api from '../api/client'
import EmptyState from '../components/EmptyState.vue'
import LoadingState from '../components/LoadingState.vue'

const route = useRoute()
const point = ref(null)
const loading = ref(true)
const error = ref('')

const areaLabel = computed(() => {
  if (!point.value) {
    return ''
  }
  return [point.value.district, point.value.street].filter(Boolean).join(' / ')
})

onMounted(async () => {
  try {
    const { data } = await api.get(`/points/${route.params.id}`)
    point.value = data
  } catch (err) {
    error.value = err.response?.data?.detail || '加载点位信息失败。'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <LoadingState v-if="loading" />
  <EmptyState
    v-else-if="error"
    title="点位不存在"
    :description="error"
  />
  <article v-else-if="point" class="overflow-hidden rounded-[2rem] border border-slate-200 bg-white shadow-sm">
    <img
      :src="point.image_url || 'https://placehold.co/1200x520?text=%E4%BE%BF%E6%B0%91%E7%82%B9%E4%BD%8D'"
      :alt="point.name"
      class="h-72 w-full object-cover lg:h-[26rem]"
    />
    <div class="grid gap-8 p-6 lg:grid-cols-[1.7fr_1fr] lg:p-10">
      <div>
        <div class="flex flex-wrap items-center gap-3">
          <span class="rounded-full bg-cyan-50 px-3 py-1 text-sm font-medium text-cyan-700">
            {{ point.category?.name }}
          </span>
          <span v-if="point.is_featured" class="rounded-full bg-amber-50 px-3 py-1 text-sm font-medium text-amber-700">
            推荐点位
          </span>
        </div>
        <h1 class="mt-4 text-3xl font-semibold text-slate-900">{{ point.name }}</h1>
        <p class="mt-4 text-base leading-8 text-slate-600">{{ point.description }}</p>

        <div class="mt-6 rounded-3xl bg-slate-50 p-5">
          <h2 class="text-lg font-semibold text-slate-900">服务内容</h2>
          <p class="mt-3 leading-7 text-slate-600">{{ point.service_content || '暂无额外说明。' }}</p>
        </div>

        <div v-if="point.navigation_notes" class="mt-6 rounded-3xl border border-cyan-100 bg-cyan-50 p-5">
          <h2 class="text-lg font-semibold text-slate-900">怎么找更方便</h2>
          <p class="mt-3 leading-7 text-slate-700">{{ point.navigation_notes }}</p>
        </div>
      </div>

      <aside class="rounded-3xl bg-slate-900 p-6 text-slate-100">
        <h2 class="text-xl font-semibold">基础信息</h2>
        <div class="mt-5 space-y-4 text-sm leading-7 text-slate-300">
          <p v-if="areaLabel"><span class="font-medium text-white">所在区域：</span>{{ areaLabel }}</p>
          <p><span class="font-medium text-white">详细地址：</span>{{ point.address }}</p>
          <p v-if="point.landmark"><span class="font-medium text-white">附近地标：</span>{{ point.landmark }}</p>
          <p><span class="font-medium text-white">开放时间：</span>{{ point.opening_hours || '以现场公告为准' }}</p>
          <p><span class="font-medium text-white">适用人群：</span>{{ point.target_people || '全体市民' }}</p>
          <p><span class="font-medium text-white">发布状态：</span>{{ point.status }}</p>
        </div>
      </aside>
    </div>
  </article>
</template>
