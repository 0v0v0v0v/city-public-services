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
const categoryOptions = ref([])
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
  category_id: '',
  status: '',
  page: 1,
})

const form = ref(createPointForm())

const columns = [
  { key: 'name', label: '点位名称' },
  { key: 'category', label: '所属分类', slot: 'cell-category' },
  { key: 'address', label: '地址', className: 'max-w-sm' },
  { key: 'status', label: '状态' },
  { key: 'is_featured', label: '推荐' },
  { key: 'updated_at', label: '更新时间' },
  { key: 'actions', label: '操作', className: 'w-72' },
]

function createPointForm() {
  return {
    name: '',
    category_id: '',
    address: '',
    opening_hours: '',
    description: '',
    service_content: '',
    target_people: '',
    image_url: '',
    is_featured: false,
    status: 'draft',
  }
}

function pointPayload(source, overrides = {}) {
  return {
    name: source.name,
    category_id: Number(source.category_id),
    address: source.address,
    opening_hours: source.opening_hours || '',
    description: source.description,
    service_content: source.service_content || '',
    target_people: source.target_people || '',
    image_url: source.image_url || '',
    is_featured: Boolean(source.is_featured),
    status: overrides.status || source.status,
  }
}

function readRouteState() {
  return {
    keyword: String(route.query.keyword || ''),
    category_id: String(route.query.category_id || ''),
    status: String(route.query.status || ''),
    page: Math.max(Number(route.query.page || 1), 1),
  }
}

function buildQuery(nextState = filters.value) {
  return {
    keyword: nextState.keyword || undefined,
    category_id: nextState.category_id || undefined,
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

async function loadCategoryOptions() {
  try {
    const { data } = await api.get('/admin/categories/options')
    categoryOptions.value = data
  } catch (err) {
    showNotice(err.response?.data?.detail || '分类选项加载失败。', 'error')
    if (err.response?.status === 401) {
      store.logout()
      router.push('/admin/login')
    }
  }
}

async function loadPoints() {
  loading.value = true
  pageError.value = ''
  try {
    const { data } = await api.get('/admin/points', {
      params: {
        keyword: filters.value.keyword || undefined,
        category_id: filters.value.category_id || undefined,
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
    handleAuthError(err, '点位列表加载失败，请稍后重试。')
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editingId.value = null
  form.value = createPointForm()
  formError.value = ''
  dialogOpen.value = true
}

async function openEdit(row) {
  formError.value = ''
  try {
    const { data } = await api.get(`/admin/points/${row.id}`)
    editingId.value = data.id
    form.value = {
      name: data.name,
      category_id: String(data.category_id),
      address: data.address,
      opening_hours: data.opening_hours || '',
      description: data.description,
      service_content: data.service_content || '',
      target_people: data.target_people || '',
      image_url: data.image_url || '',
      is_featured: Boolean(data.is_featured),
      status: data.status,
    }
    dialogOpen.value = true
  } catch (err) {
    showNotice(err.response?.data?.detail || '点位详情加载失败。', 'error')
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
    const payload = pointPayload(form.value)
    if (editingId.value) {
      await api.put(`/admin/points/${editingId.value}`, payload)
      showNotice('点位已更新。')
    } else {
      await api.post('/admin/points', payload)
      showNotice('点位已创建。')
    }
    dialogOpen.value = false
    await loadPoints()
  } catch (err) {
    formError.value = err.response?.data?.detail || '点位保存失败，请重试。'
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
    await api.put(`/admin/points/${row.id}`, pointPayload(row, { status: nextStatus }))
    showNotice(`点位已切换为${nextStatus === 'published' ? '已发布' : '草稿'}。`)
    await loadPoints()
  } catch (err) {
    showNotice(err.response?.data?.detail || '点位状态切换失败。', 'error')
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
    await api.delete(`/admin/points/${deletingRow.value.id}`)
    confirmOpen.value = false
    showNotice(`点位“${deletingRow.value.name}”已删除。`)
    const shouldGoPrev = rows.value.length === 1 && filters.value.page > 1
    deletingRow.value = null
    if (shouldGoPrev) {
      changePage(filters.value.page - 1)
    } else {
      await loadPoints()
    }
  } catch (err) {
    showNotice(err.response?.data?.detail || '点位删除失败。', 'error')
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
    path: '/admin/points',
    query: buildQuery({ ...filters.value, page: 1 }),
  })
}

function changePage(page) {
  router.push({
    path: '/admin/points',
    query: buildQuery({ ...filters.value, page }),
  })
}

async function syncFromRoute() {
  filters.value = readRouteState()
  await loadPoints()
}

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize) || 1))

watch(() => route.query, syncFromRoute)

onMounted(async () => {
  await loadCategoryOptions()
  await syncFromRoute()
})
</script>

<template>
  <AdminShell
    title="点位管理"
    description="维护点位详情、分类归属和发布状态。前台只展示已发布内容，因此可以先以草稿保存后再上线。"
  >
    <section class="space-y-5">
      <SectionTitle title="点位列表" subtitle="支持关键词、分类和状态筛选，并可直接切换草稿/发布状态。">
        <button class="admin-button-secondary w-auto px-5" @click="openCreate">新建点位</button>
      </SectionTitle>

      <div class="rounded-[2rem] border border-slate-200 bg-white p-5 shadow-sm">
        <form class="grid gap-3 xl:grid-cols-[1.3fr_0.9fr_0.7fr_auto]" @submit.prevent="submitFilters">
          <input v-model="filters.keyword" class="admin-input" placeholder="按名称、地址、简介或服务内容搜索" />
          <select v-model="filters.category_id" class="admin-input">
            <option value="">全部分类</option>
            <option v-for="category in categoryOptions" :key="category.id" :value="String(category.id)">
              {{ category.name }}
            </option>
          </select>
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

      <EmptyState v-if="pageError" title="点位加载失败" :description="pageError" />
      <template v-else>
        <AdminTable
          :columns="columns"
          :rows="rows"
          :loading="loading"
          empty-title="暂无点位"
          empty-description="可以先新建一个点位，完善基础服务信息后再发布到前台。"
        >
          <template #cell-category="{ row }">
            {{ row.category?.name || '—' }}
          </template>
          <template #cell-address="{ row }">
            <p class="line-clamp-3 text-sm leading-6 text-slate-600">{{ row.address }}</p>
          </template>
          <template #cell-status="{ row }">
            <AdminStatusBadge :value="row.status" />
          </template>
          <template #cell-is_featured="{ row }">
            {{ row.is_featured ? '是' : '否' }}
          </template>
          <template #cell-updated_at="{ row }">
            {{ new Date(row.updated_at).toLocaleString('zh-CN') }}
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
      :title="editingId ? '编辑点位' : '新建点位'"
      description="建议优先保证名称、地址、开放时间和简介完整，再根据演示需要补充服务内容与图片。"
    >
      <form class="space-y-4" @submit.prevent="submitForm">
        <div class="grid gap-4 md:grid-cols-2">
          <input v-model="form.name" required class="admin-input" placeholder="点位名称" />
          <select v-model="form.category_id" required class="admin-input">
            <option value="">选择分类</option>
            <option v-for="category in categoryOptions" :key="category.id" :value="String(category.id)">
              {{ category.name }}
            </option>
          </select>
          <input v-model="form.address" required class="admin-input md:col-span-2" placeholder="详细地址" />
          <input v-model="form.opening_hours" class="admin-input" placeholder="开放时间" />
          <select v-model="form.status" class="admin-input">
            <option value="draft">草稿</option>
            <option value="published">已发布</option>
          </select>
        </div>
        <textarea v-model="form.description" rows="4" required class="admin-input" placeholder="点位简介"></textarea>
        <textarea v-model="form.service_content" rows="4" class="admin-input" placeholder="服务内容"></textarea>
        <div class="grid gap-4 md:grid-cols-2">
          <input v-model="form.target_people" class="admin-input" placeholder="适用人群" />
          <input v-model="form.image_url" class="admin-input" placeholder="图片链接" />
        </div>
        <label class="flex items-center gap-3 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600">
          <input v-model="form.is_featured" type="checkbox" />
          设为推荐点位
        </label>
        <p v-if="formError" class="text-sm text-rose-600">{{ formError }}</p>
        <div class="flex flex-wrap justify-end gap-3">
          <button type="button" class="admin-button-secondary w-auto px-5" @click="dialogOpen = false">取消</button>
          <button class="admin-button w-auto px-5" :disabled="submitting">{{ submitting ? '保存中…' : '保存点位' }}</button>
        </div>
      </form>
    </AdminDialog>

    <AdminConfirmDialog
      v-model="confirmOpen"
      title="确认删除点位"
      :description="deletingRow ? `删除“${deletingRow.name}”后将无法恢复，前台相关展示也会立即移除。` : ''"
      :loading="deleting"
      confirm-text="确认删除"
      @confirm="confirmDelete"
    />
  </AdminShell>
</template>
