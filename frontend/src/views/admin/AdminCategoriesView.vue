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
const formError = ref('')
const editingId = ref(null)
const deletingRow = ref(null)
const pageSize = 8

const filters = ref({
  keyword: '',
  page: 1,
})

const form = ref(createCategoryForm())

const columns = [
  { key: 'name', label: '分类名称' },
  { key: 'slug', label: 'Slug' },
  { key: 'sort_order', label: '排序' },
  { key: 'description', label: '说明', className: 'max-w-xs' },
  { key: 'actions', label: '操作', className: 'w-44' },
]

function createCategoryForm() {
  return {
    name: '',
    slug: '',
    icon: '',
    cover_image: '',
    sort_order: 0,
    description: '',
  }
}

function readRouteState() {
  return {
    keyword: String(route.query.keyword || ''),
    page: Math.max(Number(route.query.page || 1), 1),
  }
}

function buildQuery(nextState = filters.value) {
  return {
    keyword: nextState.keyword || undefined,
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

async function loadCategories() {
  loading.value = true
  pageError.value = ''
  try {
    const { data } = await api.get('/admin/categories', {
      params: {
        keyword: filters.value.keyword || undefined,
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
    handleAuthError(err, '分类列表加载失败，请稍后重试。')
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editingId.value = null
  form.value = createCategoryForm()
  formError.value = ''
  dialogOpen.value = true
}

async function openEdit(row) {
  formError.value = ''
  try {
    const { data } = await api.get(`/admin/categories/${row.id}`)
    editingId.value = data.id
    form.value = {
      name: data.name,
      slug: data.slug,
      icon: data.icon || '',
      cover_image: data.cover_image || '',
      sort_order: data.sort_order ?? 0,
      description: data.description || '',
    }
    dialogOpen.value = true
  } catch (err) {
    showNotice(err.response?.data?.detail || '分类详情加载失败。', 'error')
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
    if (editingId.value) {
      await api.put(`/admin/categories/${editingId.value}`, form.value)
      showNotice('分类已更新。')
    } else {
      await api.post('/admin/categories', form.value)
      showNotice('分类已创建。')
    }
    dialogOpen.value = false
    await loadCategories()
  } catch (err) {
    formError.value = err.response?.data?.detail || '分类保存失败，请重试。'
    if (err.response?.status === 401) {
      store.logout()
      router.push('/admin/login')
    }
  } finally {
    submitting.value = false
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
    await api.delete(`/admin/categories/${deletingRow.value.id}`)
    confirmOpen.value = false
    showNotice(`分类“${deletingRow.value.name}”已删除。`)
    const shouldGoPrev = rows.value.length === 1 && filters.value.page > 1
    deletingRow.value = null
    if (shouldGoPrev) {
      changePage(filters.value.page - 1)
    } else {
      await loadCategories()
    }
  } catch (err) {
    showNotice(err.response?.data?.detail || '分类删除失败。', 'error')
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
    path: '/admin/categories',
    query: buildQuery({ ...filters.value, page: 1 }),
  })
}

function changePage(page) {
  router.push({
    path: '/admin/categories',
    query: buildQuery({ ...filters.value, page }),
  })
}

async function syncFromRoute() {
  filters.value = readRouteState()
  await loadCategories()
}

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize) || 1))

watch(() => route.query, syncFromRoute)

onMounted(syncFromRoute)
</script>

<template>
  <AdminShell
    title="分类管理"
    description="管理分类名称、排序和说明。分类是点位管理的基础结构，因此删除前会检查是否仍有关联点位。"
  >
    <section class="space-y-5">
      <SectionTitle title="分类列表" subtitle="支持关键词检索、分页浏览以及新建与编辑。">
        <button class="admin-button-secondary w-auto px-5" @click="openCreate">新建分类</button>
      </SectionTitle>

      <div class="rounded-[2rem] border border-slate-200 bg-white p-5 shadow-sm">
        <form class="grid gap-3 lg:grid-cols-[1fr_auto]" @submit.prevent="submitFilters">
          <input v-model="filters.keyword" class="admin-input" placeholder="按分类名称、slug 或说明搜索" />
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

      <EmptyState v-if="pageError" title="分类加载失败" :description="pageError" />
      <template v-else>
        <AdminTable
          :columns="columns"
          :rows="rows"
          :loading="loading"
          empty-title="暂无分类"
          empty-description="可以先新建一个分类，为后续点位录入打好基础。"
        >
          <template #cell-description="{ row }">
            <p class="line-clamp-3 text-sm leading-6 text-slate-600">{{ row.description || '—' }}</p>
          </template>
          <template #cell-actions="{ row }">
            <div class="flex flex-wrap gap-2">
              <button class="admin-button-secondary w-auto px-4 py-2 text-sm" @click="openEdit(row)">编辑</button>
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
      :title="editingId ? '编辑分类' : '新建分类'"
      description="分类会直接影响点位录入时的可选项。建议保持名称明确、slug 稳定。"
      max-width-class="max-w-2xl"
    >
      <form class="space-y-4" @submit.prevent="submitForm">
        <div class="grid gap-4 md:grid-cols-2">
          <input v-model="form.name" required class="admin-input" placeholder="分类名称" />
          <input v-model="form.slug" required class="admin-input" placeholder="slug" />
          <input v-model="form.icon" class="admin-input" placeholder="图标标识" />
          <input v-model="form.cover_image" class="admin-input" placeholder="封面图片链接" />
          <input v-model.number="form.sort_order" type="number" class="admin-input" placeholder="排序值" />
        </div>
        <textarea v-model="form.description" rows="5" class="admin-input" placeholder="分类说明"></textarea>
        <p v-if="formError" class="text-sm text-rose-600">{{ formError }}</p>
        <div class="flex flex-wrap justify-end gap-3">
          <button type="button" class="admin-button-secondary w-auto px-5" @click="dialogOpen = false">取消</button>
          <button class="admin-button w-auto px-5" :disabled="submitting">{{ submitting ? '保存中…' : '保存分类' }}</button>
        </div>
      </form>
    </AdminDialog>

    <AdminConfirmDialog
      v-model="confirmOpen"
      title="确认删除分类"
      :description="deletingRow ? `删除“${deletingRow.name}”后将无法恢复。若该分类下仍有点位，系统会阻止删除。` : ''"
      :loading="deleting"
      confirm-text="确认删除"
      @confirm="confirmDelete"
    />
  </AdminShell>
</template>
