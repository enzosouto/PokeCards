<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { api } from '../api/client'
import type { RecentSale } from '../api/types'

const sales = ref<RecentSale[]>([])
const loading = ref(true)

function money(v: number, currency: string) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(v)
}

function date(v: string) {
  return new Intl.DateTimeFormat('pt-BR').format(new Date(v))
}

onMounted(async () => {
  try {
    sales.value = await api.getRecentSales(50)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <main class="max-w-5xl mx-auto px-4 sm:px-6 py-6 sm:py-16 pb-24 md:pb-16">
    <h1 class="text-xl sm:text-2xl font-bold mb-6 sm:mb-8">Últimas vendas</h1>
    <p v-if="loading" class="text-zinc-500">Carregando...</p>
    <p v-else-if="sales.length === 0" class="text-zinc-500">Nenhuma venda registrada ainda.</p>
    <div v-else class="flex flex-col gap-2">
      <RouterLink
        v-for="sale in sales"
        :key="sale.id"
        :to="`/cards/${sale.card_id}`"
        class="flex items-center gap-3 sm:gap-4 rounded-lg border border-border bg-graphite p-3 transition hover:border-accent/60 hover:bg-graphite-light active:bg-graphite-light"
      >
        <div class="h-16 w-12 flex-shrink-0 overflow-hidden rounded bg-black/40">
          <img
            v-if="sale.image_small"
            :src="sale.image_small"
            :alt="sale.card_name"
            class="h-full w-full object-contain"
            loading="lazy"
          />
        </div>
        <div class="flex-1 min-w-0">
          <p class="font-semibold truncate">{{ sale.card_name }} · {{ sale.card_number }}</p>
          <p class="text-sm text-zinc-400 truncate">{{ sale.title }}</p>
        </div>
        <div class="text-right flex-shrink-0">
          <p class="font-bold">{{ money(sale.price, sale.currency) }}</p>
          <p class="text-xs text-zinc-500">{{ date(sale.sold_at) }}</p>
        </div>
      </RouterLink>
    </div>
  </main>
</template>
