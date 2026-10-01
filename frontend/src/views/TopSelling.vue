<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '../api/client'
import type { CardWithSalesCount } from '../api/types'
import CardTile from '../components/CardTile.vue'

const cards = ref<CardWithSalesCount[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    cards.value = await api.getTopCards(50)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <main class="max-w-5xl mx-auto px-4 sm:px-6 py-6 sm:py-16 pb-24 md:pb-16">
    <h1 class="text-xl sm:text-2xl font-bold mb-6 sm:mb-8">Mais vendidas</h1>
    <p v-if="loading" class="text-zinc-500">Carregando...</p>
    <p v-else-if="cards.length === 0" class="text-zinc-500">
      Nenhuma carta com vendas registradas ainda.
    </p>
    <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 sm:gap-4">
      <CardTile
        v-for="card in cards"
        :key="card.id"
        :card="card"
        :sales-count="card.sales_count"
      />
    </div>
  </main>
</template>
