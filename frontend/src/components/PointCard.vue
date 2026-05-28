<script setup>
defineProps({
  point: Object,
})

function formatArea(point) {
  return [point.district, point.street].filter(Boolean).join(' / ')
}
</script>

<template>
  <RouterLink
    :to="`/points/${point.id}`"
    class="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm transition hover:-translate-y-1 hover:shadow-xl"
  >
    <img
      :src="point.image_url || 'https://placehold.co/600x360?text=%E4%BE%BF%E6%B0%91%E7%82%B9%E4%BD%8D'"
      :alt="point.name"
      class="h-52 w-full object-cover"
    />
    <div class="p-5">
      <div class="flex items-center justify-between gap-4">
        <span class="rounded-full bg-cyan-50 px-3 py-1 text-xs font-medium text-cyan-700">
          {{ point.category?.name }}
        </span>
        <span v-if="point.is_featured" class="text-xs font-semibold text-amber-600">推荐点位</span>
      </div>
      <h3 class="mt-3 text-xl font-semibold text-slate-900">{{ point.name }}</h3>
      <p class="mt-3 line-clamp-3 text-sm leading-6 text-slate-600">{{ point.description }}</p>
      <div class="mt-4 text-sm text-slate-500">
        <p v-if="formatArea(point)">{{ formatArea(point) }}</p>
        <p class="mt-1">{{ point.address }}</p>
        <p v-if="point.landmark" class="mt-1">附近地标：{{ point.landmark }}</p>
        <p class="mt-1">{{ point.opening_hours || '开放时间以现场公告为准' }}</p>
      </div>
    </div>
  </RouterLink>
</template>
