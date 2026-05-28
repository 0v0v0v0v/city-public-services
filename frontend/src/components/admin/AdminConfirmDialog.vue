<script setup>
import AdminDialog from './AdminDialog.vue'

defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: '确认删除',
  },
  description: {
    type: String,
    default: '',
  },
  confirmText: {
    type: String,
    default: '确认删除',
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue', 'confirm'])
</script>

<template>
  <AdminDialog
    :model-value="modelValue"
    :title="title"
    :description="description"
    max-width-class="max-w-xl"
    @update:model-value="emit('update:modelValue', $event)"
  >
    <div class="flex flex-wrap justify-end gap-3">
      <button class="admin-button-secondary w-auto px-5" @click="emit('update:modelValue', false)">取消</button>
      <button class="admin-button-danger w-auto px-5" :disabled="loading" @click="emit('confirm')">
        {{ loading ? '处理中…' : confirmText }}
      </button>
    </div>
  </AdminDialog>
</template>
