<script setup>
defineProps({
  eyebrow: {
    type: String,
    default: '',
  },
  value: {
    type: String,
    default: '',
  },
  description: {
    type: String,
    default: '',
  },
  tone: {
    type: String,
    default: 'cyan',
  },
})

const toneClasses = {
  cyan: 'border-cyan-200 bg-cyan-50/80 text-cyan-900',
  emerald: 'border-emerald-200 bg-emerald-50/80 text-emerald-900',
  amber: 'border-amber-200 bg-amber-50/80 text-amber-900',
  slate: 'border-slate-200 bg-white text-slate-900',
}
</script>

<template>
  <article
    class="rounded-3xl border p-5 shadow-sm"
    :class="toneClasses[tone] || toneClasses.slate"
  >
    <p class="text-xs font-semibold uppercase tracking-[0.22em] opacity-70">{{ eyebrow }}</p>
    <p class="mt-4 text-3xl font-semibold">{{ value }}</p>
    <p class="mt-3 text-sm leading-6 opacity-80">{{ description }}</p>
  </article>
</template>
