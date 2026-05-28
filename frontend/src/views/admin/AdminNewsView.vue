<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import api from '../../api/client'
import EmptyState from '../../components/EmptyState.vue'
import SectionTitle from '../../components/SectionTitle.vue'
import AdminConfirmDialog from '../../components/admin/AdminConfirmDialog.vue'
import AdminDialog from '../../components/admin/AdminDialog.vue'
import AdminPagination from '../../components/admin/AdminPagination.vue'
import AdminShell from '../../components/admin/AdminShell.vue'
import AdminStatusBadge from '../../components/admin/AdminStatusBadge.vue'
import AdminTable from '../../components/admin/AdminTable.vue'
import { useAdminStore } from '../../stores/admin'

const route = useRoute()
const router = useRouter()
const store = useAdminStore()

const rows = ref([])
const total = ref(0)
const loading = ref(true)
const pageError = ref('')
const notice = ref('')
const noticeTone = ref('success')
const dialogOpen = ref(false)
const confirmOpen = ref(false)
const submitting = ref(false)
const deleting = ref(false)
const togglingId = ref(null)
const formError = ref('')
const editingId = ref(null)
const deletingRow = ref(null)
const pageSize = 8

const filters = ref({
  keyword: '',
  status: '',
  page: 1,
})

const form = ref(createNewsForm())

const columns = [
  { key: 'title', label: '资讯标题' },
  { key: 'summary', label: '摘要', className: 'max-w-md' },
  { key: 'status', label: '状态' },
  { key: 'published_at', label: '发布时间' },
  { key: 'actions', label: '操作', className: 'w-72' },
]

function createNewsForm() {
  return {
    title: '',
    summary: '',
    content: '',
    status: 'draft',
  }
}

function newsPayload(source, overrides = {}) {
  return {
    title: source.title,
    summary: source.summary,
    content: source.content,
    status: overrides.status || source.status,
  }
}

function readRouteState() {
  return {
    keyword: String(route.query.keyword || ''),
    status: String(route.query.status || ''),
    page: Math.max(Number(route.query.page || 1), 1),
  }
}

function buildQuery(nextState = filters.value) {
  return {
    keyword: nextState.keyword || undefined,
    status: nextState.status || undefined,
    page: nextState.page > 1 ? String(nextState.page) : undefined,
  }
}

function showNotice(message, tone = 'success') {
  notice.value = message
  noticeTone.value = tone
}

function handleAuthError(err, fallbackMessage) {
  pageError.value = err.response?.data?.detail || fallbackMessage
  if (err.response?.status === 401) {
    store.logout()
    router.push('/admin/login')
  }
}

async function loadNews() {
  loading.value = true
  pageError.value = ''
  try {
    const { data } = await api.get('/admin/news', {
      params: {
        keyword: filters.value.keyword || undefined,
        status: filters.value.status || undefined,
        page: filters.value.page,
        page_size: pageSize,
      },
    })
    rows.value = data.items
    total.value = data.total
    const totalPages = Math.max(1, Math.ceil(data.total / pageSize) || 1)
    if (!data.items.length && data.total > 0 && filters.value.page > totalPages) {
      changePage(totalPages)
      return
    }
  } catch (err) {
    handleAuthError(err, '资讯列表加载失败，请稍后重试。')
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editingId.value = null
  form.value = createNewsForm()
  formError.value = ''
  dialogOpen.value = true
}

async function openEdit(row) {
  formError.value = ''
  try {
    const { data } = await api.get(`/admin/news/${row.id}`)
    editingId.value = data.id
    form.value = {
      title: data.title,
      summary: data.summary,
      content: data.content,
      status: data.status,
    }
    dialogOpen.value = true
  } catch (err) {
    showNotice(err.response?.data?.detail || '资讯详情加载失败。', 'error')
    if (err.response?.status === 401) {
      store.logout()
      router.push('/admin/login')
    }
  }
}

async function submitForm() {
  submitting.value = true
  formError.value = ''
  try {
    const payload = newsPayload(form.value)
    if (editingId.value) {
      await api.put(`/admin/news/${editingId.value}`, payload)
      showNotice('资讯已更新。')
    } else {
      await api.post('/admin/news', payload)
      showNotice('资讯已创建。')
    }
    dialogOpen.value = false
    await loadNews()
  } catch (err) {
    formError.value = err.response?.data?.detail || '资讯保存失败，请重试。'
    if (err.response?.status === 401) {
      store.logout()
      router.push('/admin/login')
    }
  } finally {
    submitting.value = false
  }
}

async function toggleStatus(row) {
  togglingId.value = row.id
  try {
    const nextStatus = row.status === 'published' ? 'draft' : 'published'
    await api.put(`/admin/news/${row.id}`, newsPayload(row, { status: nextStatus }))
    showNotice(`资讯已切换为${nextStatus === 'published' ? '已发布' : '草稿'}。`)
    await loadNews()
  } catch (err) {
    showNotice(err.response?.data?.detail || '资讯状态切换失败。', 'error')
    if (err.response?.status === 401) {
      store.logout()
      router.push('/admin/login')
    }
  } finally {
    togglingId.value = null
  }
}

function askDelete(row) {
  deletingRow.value = row
  confirmOpen.value = true
}

async function confirmDelete() {
  if (!deletingRow.value) {
    return
  }
  deleting.value = true
  try {
    await api.delete(`/admin/news/${deletingRow.value.id}`)
    confirmOpen.value = false
    showNotice(`资讯“${deletingRow.value.title}”已删除。`)
    const shouldGoPrev = rows.value.length === 1 && filters.value.page > 1
    deletingRow.value = null
    if (shouldGoPrev) {
      changePage(filters.value.page - 1)
    } else {
      await loadNews()
    }
  } catch (err) {
    showNotice(err.response?.data?.detail || '资讯删除失败。', 'error')
    if (err.response?.status === 401) {
      store.logout()
      router.push('/admin/login')
    }
  } finally {
    deleting.value = false
  }
}

function submitFilters() {
  router.push({
    path: '/admin/news',
    query: buildQuery({ ...filters.value, page: 1 }),
  })
}

function changePage(page) {
  router.push({
    path: '/admin/news',
    query: buildQuery({ ...filters.value, page }),
  })
}

async function syncFromRoute() {
  filters.value = readRouteState()
  await loadNews()
}

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize) || 1))

watch(() => route.query, syncFromRoute)

onMounted(syncFromRoute)
</script>

<template>
  <AdminShell
    title="资讯管理"
    description="维护资讯标题、摘要、正文和发布状态。发布后的资讯会进入前台资讯页，并参与首页最新资讯展示。"
  >
    <section class="space-y-5">
      <SectionTitle title="资讯列表" subtitle="支持关键词、状态筛选以及草稿/发布状态切换。">
        <button class="admin-button-secondary w-auto px-5" @click="openCreate">新建资讯</button>
      </SectionTitle>

      <div class="rounded-[2rem] border border-slate-200 bg-white p-5 shadow-sm">
        <form class="grid gap-3 xl:grid-cols-[1.4fr_0.8fr_auto]" @submit.prevent="submitFilters">
          <input v-model="filters.keyword" class="admin-input" placeholder="按标题、摘要或正文搜索" />
          <select v-model="filters.status" class="admin-input">
            <option value="">全部状态</option>
            <option value="draft">草稿</option>
            <option value="published">已发布</option>
          </select>
          <button class="admin-button">应用筛选</button>
        </form>
      </div>

      <div
        v-if="notice"
        class="rounded-3xl border px-5 py-4 text-sm shadow-sm"
        :class="noticeTone === 'error' ? 'border-rose-200 bg-rose-50 text-rose-700' : 'border-emerald-200 bg-emerald-50 text-emerald-700'"
      >
        {{ notice }}
      </div>

      <EmptyState v-if="pageError" title="资讯加载失败" :description="pageError" />
      <template v-else>
        <AdminTable
          :columns="columns"
          :rows="rows"
          :loading="loading"
          empty-title="暂无资讯"
          empty-description="可以先录入一条资讯，用于前台资讯页和首页动态展示。"
        >
          <template #cell-summary="{ row }">
            <p class="line-clamp-3 text-sm leading-6 text-slate-600">{{ row.summary }}</p>
          </template>
          <template #cell-status="{ row }">
            <AdminStatusBadge :value="row.status" />
          </template>
          <template #cell-published_at="{ row }">
            {{ new Date(row.published_at).toLocaleString('zh-CN') }}
          </template>
          <template #cell-actions="{ row }">
            <div class="flex flex-wrap gap-2">
              <button class="admin-button-secondary w-auto px-4 py-2 text-sm" @click="openEdit(row)">编辑</button>
              <button
                class="admin-button-secondary w-auto px-4 py-2 text-sm"
                :disabled="togglingId === row.id"
                @click="toggleStatus(row)"
              >
                {{ togglingId === row.id ? '切换中…' : row.status === 'published' ? '转为草稿' : '立即发布' }}
              </button>
              <button class="admin-button-danger w-auto px-4 py-2 text-sm" @click="askDelete(row)">删除</button>
            </div>
          </template>
        </AdminTable>

        <AdminPagination
          v-if="!loading && totalPages > 1"
          :page="filters.page"
          :page-size="pageSize"
          :total="total"
          @change="changePage"
        />
      </template>
    </section>

    <AdminDialog
      v-model="dialogOpen"
      :title="editingId ? '编辑资讯' : '新建资讯'"
      description="摘要建议控制在一到两句话内，正文可直接使用纯文本，不引入额外富文本能力。"
    >
      <form class="space-y-4" @submit.prevent="submitForm">
        <input v-model="form.title" required class="admin-input" placeholder="资讯标题" />
        <textarea v-model="form.summary" rows="4" required class="admin-input" placeholder="资讯摘要"></textarea>
        <textarea v-model="form.content" rows="10" required class="admin-input" placeholder="资讯正文"></textarea>
        <select v-model="form.status" class="admin-input">
          <option value="draft">草稿</option>
          <option value="published">已发布</option>
        </select>
        <p v-if="formError" class="text-sm text-rose-600">{{ formError }}</p>
        <div class="flex flex-wrap justify-end gap-3">
          <button type="button" class="admin-button-secondary w-auto px-5" @click="dialogOpen = false">取消</button>
          <button class="admin-button w-auto px-5" :disabled="submitting">{{ submitting ? '保存中…' : '保存资讯' }}</button>
        </div>
      </form>
    </AdminDialog>

    <AdminConfirmDialog
      v-model="confirmOpen"
      title="确认删除资讯"
      :description="deletingRow ? `删除“${deletingRow.title}”后将无法恢复，前台相关资讯入口也会同步消失。` : ''"
      :loading="deleting"
      confirm-text="确认删除"
      @confirm="confirmDelete"
    />
  </AdminShell>
</template>
