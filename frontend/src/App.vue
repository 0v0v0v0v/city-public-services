<script setup>
import AppFooter from './components/AppFooter.vue'
import AppHeader from './components/AppHeader.vue'
</script>

<template>
  <div class="min-h-screen bg-slate-100 text-slate-700">
    <AppHeader />
    <main class="mx-auto max-w-6xl px-4 py-8 lg:px-8 lg:py-10">
      <RouterView />
    </main>
    <AppFooter />
  </div>
</template>
