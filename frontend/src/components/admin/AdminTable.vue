<script setup>
defineProps({
  columns: Array,
  rows: Array,
})
</script>

<template>
  <div class="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
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
          <td v-for="column in columns" :key="column.key" class="px-4 py-3 text-slate-700">
            {{ row[column.key] }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
