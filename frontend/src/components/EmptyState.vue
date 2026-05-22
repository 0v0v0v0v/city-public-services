<script setup>
defineProps({
  title: {
    type: String,
    default: '暂无内容',
  },
  description: {
    type: String,
    default: '当前条件下还没有可展示的数据。',
  },
})
</script>

<template>
  <div class="rounded-3xl border border-dashed border-slate-300 bg-white px-5 py-10 text-center">
    <h3 class="text-lg font-semibold text-slate-900">{{ title }}</h3>
    <p class="mt-2 text-sm text-slate-500">{{ description }}</p>
  </div>
</template>
