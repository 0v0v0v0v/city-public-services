<script setup>
import { computed } from 'vue'

const props = defineProps({
  page: {
    type: Number,
    default: 1,
  },
  pageSize: {
    type: Number,
    default: 10,
  },
  total: {
    type: Number,
    default: 0,
  },
})

const emit = defineEmits(['change'])

const totalPages = computed(() => Math.max(1, Math.ceil(props.total / props.pageSize) || 1))
const start = computed(() => (props.total ? (props.page - 1) * props.pageSize + 1 : 0))
const end = computed(() => Math.min(props.page * props.pageSize, props.total))
</script>

<template>
  <div class="flex flex-col gap-3 rounded-3xl border border-slate-200 bg-white px-5 py-4 text-sm text-slate-600 shadow-sm sm:flex-row sm:items-center sm:justify-between">
    <p>当前显示 {{ start }} - {{ end }} 条，共 {{ total }} 条，第 {{ page }} / {{ totalPages }} 页</p>
    <div class="flex gap-3">
      <button class="admin-button-secondary w-auto px-4 py-2" :disabled="page <= 1" @click="emit('change', page - 1)">
        上一页
      </button>
      <button
        class="admin-button-secondary w-auto px-4 py-2"
        :disabled="page >= totalPages"
        @click="emit('change', page + 1)"
      >
        下一页
      </button>
    </div>
  </div>
</template>
