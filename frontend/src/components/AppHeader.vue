<script setup>
import { ref } from 'vue'

const publicLinks = [
  { label: '首页', to: '/' },
  { label: '分类浏览', to: '/categories' },
  { label: '便民点位', to: '/points' },
  { label: '项目介绍', to: '/about' },
]

const links = publicLinks

const mobileOpen = ref(false)

function toggleMenu() {
  mobileOpen.value = !mobileOpen.value
}

function closeMenu() {
  mobileOpen.value = false
}
</script>

<template>
  <header class="sticky top-0 z-30 border-b border-slate-200 bg-white/90 backdrop-blur">
    <div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 lg:px-8">
      <RouterLink to="/" class="flex items-center gap-3 text-slate-900">
        <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-cyan-700 text-lg font-semibold text-white">
          民
        </div>
        <div>
          <div class="text-lg font-semibold">城市公共便民点位整合平台</div>
          <div class="text-xs text-slate-500">面向市民的公益型服务信息入口</div>
        </div>
      </RouterLink>
      <nav class="hidden gap-5 text-sm font-medium text-slate-600 lg:flex">
        <RouterLink
          v-for="link in links"
          :key="link.to"
          :to="link.to"
          class="transition hover:text-cyan-700"
        >
          {{ link.label }}
        </RouterLink>
      </nav>
      <button
        type="button"
        class="inline-flex rounded-2xl border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 lg:hidden"
        @click="toggleMenu"
      >
        菜单
      </button>
    </div>
    <div v-if="mobileOpen" class="border-t border-slate-200 bg-white lg:hidden">
      <nav class="mx-auto flex max-w-6xl flex-col px-4 py-3 text-sm font-medium text-slate-600">
        <RouterLink
          v-for="link in links"
          :key="link.to"
          :to="link.to"
          class="rounded-2xl px-3 py-3 transition hover:bg-slate-50 hover:text-cyan-700"
          @click="closeMenu"
        >
          {{ link.label }}
        </RouterLink>
      </nav>
    </div>
  </header>
</template>
