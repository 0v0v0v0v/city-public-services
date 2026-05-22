<script setup>
defineProps({
  title: String,
  subtitle: String,
})
</script>

<template>
  <section class="overflow-hidden rounded-[2rem] bg-gradient-to-br from-cyan-800 via-cyan-700 to-emerald-600 px-6 py-10 text-white shadow-2xl lg:px-10 lg:py-14">
    <div class="max-w-3xl">
      <p class="mb-3 inline-flex rounded-full bg-white/15 px-3 py-1 text-sm font-medium">
        公益便民 · 城市治理视角
      </p>
      <h1 class="text-3xl font-semibold leading-tight lg:text-5xl">
        {{ title }}
      </h1>
      <p class="mt-4 text-base leading-7 text-cyan-50 lg:text-lg">
        {{ subtitle }}
      </p>
    </div>
  </section>
</template>
