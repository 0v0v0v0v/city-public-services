<script setup>
defineProps({
  title: String,
  subtitle: String,
})
</script>

<template>
  <div class="mb-6 flex items-end justify-between gap-4">
    <div>
      <h2 class="text-2xl font-semibold text-slate-900">{{ title }}</h2>
      <p v-if="subtitle" class="mt-2 text-sm text-slate-600">{{ subtitle }}</p>
    </div>
    <slot />
  </div>
</template>
