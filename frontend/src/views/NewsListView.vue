<script setup>
import { onMounted, ref } from 'vue'

import api from '../api/client'
import EmptyState from '../components/EmptyState.vue'
import HeroBanner from '../components/HeroBanner.vue'
import LoadingState from '../components/LoadingState.vue'
import NewsCard from '../components/NewsCard.vue'
import SectionTitle from '../components/SectionTitle.vue'

const items = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await api.get('/news')
    items.value = data.items
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="space-y-10">
    <HeroBanner
      title="便民资讯"
      subtitle="收录与公共服务点位有关的开放提醒、设施公告和阶段性民生安排。"
    />
    <section>
      <SectionTitle title="资讯列表" subtitle="适合课堂演示的公益型资讯模块。" />
      <LoadingState v-if="loading" />
      <EmptyState
        v-else-if="!items.length"
        title="暂无资讯"
        description="请在后台录入资讯后再查看。"
      />
      <div v-else class="grid gap-5 lg:grid-cols-3">
        <NewsCard v-for="item in items" :key="item.id" :item="item" />
      </div>
    </section>
  </div>
</template>
