<script setup>
import EmptyState from '../EmptyState.vue'
import LoadingState from '../LoadingState.vue'

defineProps({
  columns: {
    type: Array,
    default: () => [],
  },
  rows: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  emptyTitle: {
    type: String,
    default: '暂无数据',
  },
  emptyDescription: {
    type: String,
    default: '当前筛选条件下还没有可展示的数据。',
  },
})
</script>

<template>
  <LoadingState v-if="loading" />
  <div v-else-if="rows.length" class="overflow-x-auto rounded-3xl border border-slate-200 bg-white shadow-sm">
    <table class="min-w-full divide-y divide-slate-200 text-left text-sm">
      <thead class="bg-slate-50 text-slate-600">
        <tr>
          <th v-for="column in columns" :key="column.key" class="px-4 py-3 font-medium">
            {{ column.label }}
          </th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-100">
        <tr v-for="row in rows" :key="row.id" class="align-top">
          <td
            v-for="column in columns"
            :key="column.key"
            class="px-4 py-3 text-slate-700"
            :class="column.className"
          >
            <slot :name="column.slot || `cell-${column.key}`" :row="row" :value="row[column.key]">
              {{ row[column.key] ?? '—' }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <EmptyState v-else :title="emptyTitle" :description="emptyDescription" />
</template>
