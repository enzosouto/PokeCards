<script setup lang="ts">
const tabs = [
  {
    to: '/',
    label: 'Buscar',
    icon: 'M21 21l-5.2-5.2m0 0a7.5 7.5 0 10-10.6-10.6 7.5 7.5 0 0010.6 10.6z',
  },
  {
    to: '/mais-vendidas',
    label: 'Mais vendidas',
    icon: 'M3 17l6-6 4 4 8-8M21 7v5h-5',
  },
  {
    to: '/ultimas-vendas',
    label: 'Últimas',
    icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
  },
  {
    to: '/sobre',
    label: 'Sobre',
    icon: 'M12 16v-4m0-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
  },
]
</script>

<template>
  <nav
    class="fixed bottom-0 inset-x-0 z-40 flex items-stretch border-t border-border bg-graphite md:hidden pb-[env(safe-area-inset-bottom)]"
  >
    <RouterLink
      v-for="tab in tabs"
      :key="tab.to"
      :to="tab.to"
      class="flex-1 flex flex-col items-center justify-center gap-1 py-2.5 text-[11px] font-medium text-zinc-500 transition"
      active-class="text-accent"
      exact-active-class="text-accent"
    >
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="h-5 w-5"
      >
        <path :d="tab.icon" />
      </svg>
      {{ tab.label }}
    </RouterLink>
  </nav>
</template>
