<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '../api/client'
import type { CardSearchResult, CardWithSalesCount } from '../api/types'
import CardTile from '../components/CardTile.vue'

const query = ref('')
const results = ref<CardSearchResult[]>([])
const loading = ref(false)
const error = ref('')
const searched = ref(false)

const allCards = ref<CardWithSalesCount[]>([])

async function search() {
  if (query.value.trim().length < 2) return
  loading.value = true
  error.value = ''
  searched.value = true
  try {
    results.value = await api.searchCards(query.value.trim())
  } catch {
    error.value = 'Falha ao buscar cartas. Tente novamente.'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    allCards.value = await api.getAllCards()
  } catch {
    // silent — catalog section is non-essential
  }
})
</script>

<template>
  <main class="max-w-5xl mx-auto px-4 sm:px-6 py-6 sm:py-16 pb-24 md:pb-16">
    <div class="text-center mb-6 sm:mb-10">
      <p class="text-sm sm:text-base text-zinc-400">Pokémon TCG Market Intelligence</p>
    </div>

    <form @submit.prevent="search" class="max-w-xl mx-auto flex gap-2 mb-8 sm:mb-12">
      <input
        v-model="query"
        type="text"
        inputmode="search"
        placeholder="Busque uma carta"
        class="flex-1 min-w-0 rounded-lg border border-border bg-graphite px-4 py-3 text-base outline-none focus:border-accent placeholder:text-zinc-500"
      />
      <button
        type="submit"
        class="rounded-lg bg-accent px-5 py-3 font-semibold hover:bg-red-500 active:bg-red-600 transition disabled:opacity-50"
        :disabled="loading"
      >
        {{ loading ? '...' : 'Buscar' }}
      </button>
    </form>

    <div v-if="loading" class="flex flex-col items-center gap-3 py-12 text-zinc-400">
      <div class="h-8 w-8 rounded-full border-2 border-border border-t-accent animate-spin" />
      <p class="text-sm">Buscando carta...</p>
    </div>

    <div v-else-if="error" class="text-center">
      <p class="text-accent mb-3">{{ error }}</p>
      <button
        @click="search"
        class="rounded-lg border border-border px-4 py-2 text-sm font-medium hover:border-accent transition"
      >
        Tentar novamente
      </button>
    </div>

    <p v-else-if="searched && results.length === 0" class="text-center text-zinc-500">
      Nenhuma carta encontrada.
    </p>

    <div v-if="!loading && results.length" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 sm:gap-4">
      <CardTile v-for="card in results" :key="card.id" :card="card" />
    </div>

    <template v-else-if="!searched && allCards.length">
      <h2 class="text-sm font-semibold uppercase tracking-wide text-zinc-400 mb-4">
        Todas as cartas ({{ allCards.length }})
      </h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 sm:gap-4">
        <CardTile
          v-for="card in allCards"
          :key="card.id"
          :card="card"
          :sales-count="card.sales_count"
        />
      </div>
    </template>
  </main>
</template>
