<template>
  <section class="grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
    <article class="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
      <p class="text-sm font-medium uppercase tracking-[0.2em] text-cyan-700">项目介绍</p>
      <h1 class="mt-4 text-3xl font-semibold text-slate-900">为什么做城市公共便民点位整合网站</h1>
      <div class="mt-6 space-y-5 text-base leading-8 text-slate-600">
        <p>项目从公共事务管理视角切入，关注居民高频、贴近日常生活的公益性公共服务设施，而不是商业消费和打卡场景。</p>
        <p>首版聚焦城市公园、社区服务中心、政务服务大厅、公共卫生间等常见资源，通过统一入口降低市民查找成本，也为课程作业提供更有现实意义的展示主题。</p>
        <p>技术上使用 FastAPI、Vue 3、Tailwind CSS 和 SQLite，兼顾课程项目的可落地性、演示友好度和后续扩展空间。</p>
      </div>
    </article>

    <aside class="rounded-[2rem] bg-slate-900 p-8 text-slate-100 shadow-xl">
      <h2 class="text-2xl font-semibold">首版功能边界</h2>
      <ul class="mt-5 space-y-4 text-sm leading-7 text-slate-300">
        <li>提供点位分类浏览、关键词搜索和详情展示。</li>
        <li>提供后台登录、分类管理和点位管理。</li>
        <li>不包含地图导航、实时定位、支付、商业推广和普通用户体系。</li>
      </ul>
    </aside>
  </section>
</template>
