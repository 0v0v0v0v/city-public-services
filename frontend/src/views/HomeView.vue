<script setup>
import { onMounted, ref } from 'vue'

import api from '../api/client'
import CategoryCard from '../components/CategoryCard.vue'
import FeaturePanel from '../components/FeaturePanel.vue'
import HeroBanner from '../components/HeroBanner.vue'
import LoadingState from '../components/LoadingState.vue'
import NewsCard from '../components/NewsCard.vue'
import PointCard from '../components/PointCard.vue'
import QuickNavCard from '../components/QuickNavCard.vue'
import SectionTitle from '../components/SectionTitle.vue'
import StatCard from '../components/StatCard.vue'

const home = ref(null)
const loading = ref(true)
const keyword = ref('')

const quickEntries = [
  {
    title: '按分类进入',
    description: '先看公园、社区服务中心、政务大厅等模块，再进入对应点位列表。',
    to: '/categories',
    tag: '常用入口',
  },
  {
    title: '查看便民点位',
    description: '直接浏览点位列表，配合关键词和筛选条件快速缩小范围。',
    to: '/points',
    tag: '核心功能',
  },
  {
    title: '了解资讯公告',
    description: '查看开放提醒、临时公告和面向市民的便民通知。',
    to: '/news',
    tag: '信息更新',
  },
  {
    title: '进入后台录入',
    description: '管理员可维护分类、点位和资讯，形成从录入到展示的完整闭环。',
    to: '/admin',
    tag: '管理台',
  },
]

async function loadHome() {
  loading.value = true
  try {
    const { data } = await api.get('/home')
    home.value = data
  } finally {
    loading.value = false
  }
}

onMounted(loadHome)
</script>

<template>
  <div class="space-y-10">
    <HeroBanner
      title="让居民更快找到身边的公共便民资源"
      subtitle="聚合城市公园、社区服务中心、政务大厅、公共卫生间等公益设施信息，帮助大家通过分类与搜索快速查询日常所需服务。"
    />

    <section class="grid gap-5 lg:grid-cols-[1.35fr_0.65fr]">
      <FeaturePanel
        badge="平台目标"
        title="先把高频民生信息整合清楚，再逐步扩展到更复杂的服务能力。"
        description="首版围绕信息整合、分类浏览、后台录入三个核心动作构建，尽量减少华而不实的功能，让系统先形成稳定可演示的使用闭环。"
      >
        <div class="grid gap-3 sm:grid-cols-3">
          <StatCard eyebrow="收录对象" value="9 类" description="首版覆盖课程演示常用公共设施。" tone="cyan" />
          <StatCard eyebrow="核心路径" value="3 步" description="搜索、浏览、查看详情。" tone="emerald" />
          <StatCard eyebrow="管理方式" value="后台录入" description="由管理员统一维护展示内容。" tone="amber" />
        </div>
      </FeaturePanel>

      <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-1">
        <StatCard eyebrow="建设方向" value="公益型平台" description="不做商业流量，不植入广告，以公共服务可达性为核心。" />
        <StatCard eyebrow="演示重点" value="录入到展示闭环" description="后台新增一条数据，前台可以立即看到并进入详情页。" />
      </div>
    </section>

    <section class="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
      <SectionTitle
        title="快速检索"
        subtitle="输入关键词后，直接跳转到点位列表页进行搜索。"
      />
      <form action="/points" class="grid gap-3 lg:grid-cols-[1fr_auto]">
        <input
          v-model="keyword"
          name="keyword"
          type="text"
          placeholder="例如：公园、政务大厅、卫生间、社区服务"
          class="rounded-2xl border border-slate-300 px-4 py-3 outline-none ring-0 transition focus:border-cyan-500"
        />
        <button class="rounded-2xl bg-cyan-700 px-6 py-3 font-medium text-white transition hover:bg-cyan-800">
          搜索点位
        </button>
      </form>
    </section>

    <section>
      <SectionTitle title="平台框架" subtitle="先搭好网站的主要入口和功能层次，后续再逐步填充真实数据。" />
      <div class="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
        <QuickNavCard
          v-for="entry in quickEntries"
          :key="entry.title"
          :title="entry.title"
          :description="entry.description"
          :to="entry.to"
          :tag="entry.tag"
        />
      </div>
    </section>

    <LoadingState v-if="loading" />

    <template v-else-if="home">
      <section>
        <SectionTitle title="重点推荐点位" subtitle="优先展示实用性强、覆盖面广的便民设施。">
          <RouterLink to="/points" class="text-sm font-medium text-cyan-700">查看全部</RouterLink>
        </SectionTitle>
        <div class="grid gap-6 lg:grid-cols-3">
          <PointCard v-for="point in home.featured_points" :key="point.id" :point="point" />
        </div>
      </section>

      <section>
        <SectionTitle title="分类浏览" subtitle="按公共服务类型快速进入对应场景。">
          <RouterLink to="/categories" class="text-sm font-medium text-cyan-700">全部分类</RouterLink>
        </SectionTitle>
        <div class="grid gap-5 md:grid-cols-2 lg:grid-cols-4">
          <CategoryCard v-for="category in home.categories" :key="category.id" :category="category" />
        </div>
      </section>

      <section>
        <SectionTitle title="最新便民资讯" subtitle="展示与民生服务相关的公告、提醒和开放信息。">
          <RouterLink to="/news" class="text-sm font-medium text-emerald-700">资讯列表</RouterLink>
        </SectionTitle>
        <div class="grid gap-5 lg:grid-cols-3">
          <NewsCard v-for="item in home.latest_news" :key="item.id" :item="item" />
        </div>
      </section>
    </template>
  </div>
</template>
