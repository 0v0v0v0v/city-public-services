<script setup>
import { onMounted, ref } from 'vue'

import api from '../api/client'
import CategoryCard from '../components/CategoryCard.vue'
import EmptyState from '../components/EmptyState.vue'
import HeroBanner from '../components/HeroBanner.vue'
import LoadingState from '../components/LoadingState.vue'
import SectionTitle from '../components/SectionTitle.vue'

const categories = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await api.get('/categories')
    categories.value = data
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="space-y-10">
    <HeroBanner
      title="按分类浏览城市公共服务资源"
      subtitle="从城市公园到社区服务中心，用清晰分类帮助不同年龄和需求的用户更快找到合适点位。"
    />

    <section>
      <SectionTitle title="全部分类" subtitle="首版按课程演示场景内置常用民生资源分类。" />
      <LoadingState v-if="loading" />
      <EmptyState
        v-else-if="!categories.length"
        title="暂无分类"
        description="请先在后台录入分类数据。"
      />
      <div v-else class="grid gap-5 md:grid-cols-2 lg:grid-cols-4">
        <CategoryCard v-for="category in categories" :key="category.id" :category="category" />
      </div>
    </section>
  </div>
</template>
