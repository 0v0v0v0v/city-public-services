<script setup>
defineProps({
  item: Object,
})
</script>

<template>
  <RouterLink
    :to="`/news/${item.id}`"
    class="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-emerald-300 hover:shadow-lg"
  >
    <p class="text-xs font-medium uppercase tracking-[0.2em] text-emerald-600">便民资讯</p>
    <h3 class="mt-3 text-lg font-semibold text-slate-900">{{ item.title }}</h3>
    <p class="mt-3 line-clamp-3 text-sm leading-6 text-slate-600">{{ item.summary }}</p>
    <p class="mt-4 text-xs text-slate-400">
      {{ new Date(item.published_at).toLocaleDateString('zh-CN') }}
    </p>
  </RouterLink>
</template>
