<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import api from '../api/client'
import EmptyState from '../components/EmptyState.vue'
import HeroBanner from '../components/HeroBanner.vue'
import LoadingState from '../components/LoadingState.vue'
import PointCard from '../components/PointCard.vue'
import SectionTitle from '../components/SectionTitle.vue'

const route = useRoute()
const router = useRouter()
const categories = ref([])
const points = ref([])
const total = ref(0)
const loading = ref(true)

const filters = ref({
  keyword: route.query.keyword || '',
  category_id: route.query.category_id || '',
  is_featured: route.query.is_featured || '',
})

const currentCategoryLabel = computed(() => {
  const item = categories.value.find((entry) => String(entry.id) === String(filters.value.category_id))
  return item?.name || '全部分类'
})

async function loadCategories() {
  const { data } = await api.get('/categories')
  categories.value = data
}

async function loadPoints() {
  loading.value = true
  try {
    const params = {
      keyword: filters.value.keyword || undefined,
      category_id: filters.value.category_id || undefined,
      is_featured:
        filters.value.is_featured === ''
          ? undefined
          : filters.value.is_featured === 'true',
    }
    const { data } = await api.get('/points', { params })
    points.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

async function syncFromRoute() {
  filters.value = {
    keyword: route.query.keyword || '',
    category_id: route.query.category_id || '',
    is_featured: route.query.is_featured || '',
  }
  await loadPoints()
}

function submitFilters() {
  router.push({
    path: '/points',
    query: {
      keyword: filters.value.keyword || undefined,
      category_id: filters.value.category_id || undefined,
      is_featured: filters.value.is_featured || undefined,
    },
  })
}

watch(() => route.query, syncFromRoute)

onMounted(async () => {
  await loadCategories()
  await syncFromRoute()
})
</script>

<template>
  <div class="space-y-10">
    <HeroBanner
      title="便民点位列表"
      subtitle="通过关键词、分类和推荐标签筛选点位信息，首版以文字地址和服务介绍为核心。"
    />

    <section class="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
      <SectionTitle
        title="筛选条件"
        :subtitle="`当前分类：${currentCategoryLabel}，共找到 ${total} 条结果。`"
      />
      <form class="grid gap-4 lg:grid-cols-4" @submit.prevent="submitFilters">
        <input
          v-model="filters.keyword"
          type="text"
          placeholder="输入关键词"
          class="rounded-2xl border border-slate-300 px-4 py-3 outline-none focus:border-cyan-500"
        />
        <select
          v-model="filters.category_id"
          class="rounded-2xl border border-slate-300 px-4 py-3 outline-none focus:border-cyan-500"
        >
          <option value="">全部分类</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>
        <select
          v-model="filters.is_featured"
          class="rounded-2xl border border-slate-300 px-4 py-3 outline-none focus:border-cyan-500"
        >
          <option value="">全部点位</option>
          <option value="true">仅看推荐</option>
          <option value="false">仅看非推荐</option>
        </select>
        <button class="rounded-2xl bg-cyan-700 px-6 py-3 font-medium text-white hover:bg-cyan-800">
          应用筛选
        </button>
      </form>
    </section>

    <LoadingState v-if="loading" />
    <EmptyState
      v-else-if="!points.length"
      title="没有找到匹配点位"
      description="可以尝试更换关键词，或清空筛选条件后重新查询。"
    />
    <div v-else class="grid gap-6 lg:grid-cols-3">
      <PointCard v-for="point in points" :key="point.id" :point="point" />
    </div>
  </div>
</template>
