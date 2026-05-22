<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAdminStore } from '../../stores/admin'

const router = useRouter()
const store = useAdminStore()
const form = ref({
  username: 'admin',
  password: 'admin123',
})
const error = ref('')
const loading = ref(false)

async function submit() {
  loading.value = true
  error.value = ''
  try {
    await store.login(form.value)
    router.push('/admin')
  } catch (err) {
    error.value = err.response?.data?.detail || '登录失败，请重试。'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="mx-auto max-w-xl rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
    <p class="text-sm font-medium uppercase tracking-[0.2em] text-cyan-700">后台管理</p>
    <h1 class="mt-4 text-3xl font-semibold text-slate-900">管理员登录</h1>
    <p class="mt-3 text-sm leading-6 text-slate-500">默认演示账号为 `admin / admin123`，登录后可维护分类、点位和资讯。</p>
    <form class="mt-8 space-y-4" @submit.prevent="submit">
      <input
        v-model="form.username"
        type="text"
        placeholder="用户名"
        class="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none focus:border-cyan-500"
      />
      <input
        v-model="form.password"
        type="password"
        placeholder="密码"
        class="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none focus:border-cyan-500"
      />
      <p v-if="error" class="text-sm text-rose-600">{{ error }}</p>
      <button
        class="w-full rounded-2xl bg-cyan-700 px-6 py-3 font-medium text-white hover:bg-cyan-800"
        :disabled="loading"
      >
        {{ loading ? '登录中…' : '登录后台' }}
      </button>
    </form>
  </section>
</template>
