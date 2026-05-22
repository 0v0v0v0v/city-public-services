<script setup>
defineProps({
  category: Object,
})
</script>

<template>
  <RouterLink
    :to="`/points?category_id=${category.id}`"
    class="group rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-1 hover:border-cyan-300 hover:shadow-lg"
  >
    <div class="flex h-12 w-12 items-center justify-center rounded-2xl bg-cyan-50 text-xl font-semibold text-cyan-700">
      {{ category.name.slice(0, 1) }}
    </div>
    <h3 class="mt-4 text-lg font-semibold text-slate-900">{{ category.name }}</h3>
    <p class="mt-2 line-clamp-3 text-sm leading-6 text-slate-600">
      {{ category.description || '提供分类化浏览，帮助居民更快找到所需便民资源。' }}
    </p>
  </RouterLink>
</template>
