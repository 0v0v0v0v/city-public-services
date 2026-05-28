<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: {
    type: String,
    default: 'draft',
  },
})

const label = computed(() => (props.value === 'published' ? '已发布' : '草稿'))
const chipClass = computed(() => (props.value === 'published' ? 'admin-chip-published' : 'admin-chip-draft'))
</script>

<template>
  <span class="admin-chip" :class="chipClass">{{ label }}</span>
</template>
