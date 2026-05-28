<script setup>
defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: '',
  },
  description: {
    type: String,
    default: '',
  },
  maxWidthClass: {
    type: String,
    default: 'max-w-3xl',
  },
})

const emit = defineEmits(['update:modelValue'])

function close() {
  emit('update:modelValue', false)
}
</script>

<template>
  <Teleport to="body">
    <div
      v-if="modelValue"
      class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 px-4 py-6"
      @click.self="close"
    >
      <div :class="maxWidthClass" class="max-h-[90vh] w-full overflow-y-auto rounded-[2rem] bg-white p-6 shadow-2xl">
        <div class="flex items-start justify-between gap-4">
          <div>
            <h2 class="text-2xl font-semibold text-slate-900">{{ title }}</h2>
            <p v-if="description" class="mt-2 text-sm leading-6 text-slate-500">{{ description }}</p>
          </div>
          <button class="rounded-2xl border border-slate-200 px-3 py-2 text-sm text-slate-500" @click="close">
            关闭
          </button>
        </div>
        <div class="mt-6">
          <slot />
        </div>
      </div>
    </div>
  </Teleport>
</template>
