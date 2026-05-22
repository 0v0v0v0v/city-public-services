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
  badge: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <article class="rounded-3xl border border-white/15 bg-slate-950/80 p-6 text-slate-100 shadow-xl">
    <p v-if="badge" class="text-xs font-semibold uppercase tracking-[0.22em] text-cyan-300">
      {{ badge }}
    </p>
    <h3 class="mt-3 text-xl font-semibold">{{ title }}</h3>
    <p class="mt-3 text-sm leading-7 text-slate-300">{{ description }}</p>
    <div v-if="$slots.default" class="mt-5">
      <slot />
    </div>
  </article>
</template>
