<script setup>
defineProps({
  title: {
    type: String,
    default: '',
  },
  description: {
    type: String,
    default: '',
  },
  to: {
    type: String,
    default: '/',
  },
  tag: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <RouterLink
    :to="to"
    class="group rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-1 hover:border-cyan-300 hover:shadow-lg"
  >
    <div class="flex items-center justify-between gap-4">
      <h3 class="text-lg font-semibold text-slate-900">{{ title }}</h3>
      <span v-if="tag" class="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
        {{ tag }}
      </span>
    </div>
    <p class="mt-3 text-sm leading-6 text-slate-600">{{ description }}</p>
    <p class="mt-5 text-sm font-medium text-cyan-700 transition group-hover:translate-x-1">
      进入模块
    </p>
  </RouterLink>
</template>
