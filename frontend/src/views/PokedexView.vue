<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { ensureFullPokedex, pokedexList, pokedexLoading } from '../pokedex/pokedexData'
import PokedexCard from '../components/PokedexCard.vue'

const query = ref('')

onMounted(() => {
  ensureFullPokedex()
})

const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return pokedexList.value
  return pokedexList.value.filter((p) => p.name.includes(q) || String(p.id).includes(q))
})
</script>

<template>
  <main class="max-w-5xl mx-auto px-4 sm:px-6 py-6 sm:py-10 pb-24 md:pb-16">
    <div class="text-center mb-6">
      <h1 class="text-2xl sm:text-3xl font-bold text-accent mb-2">Pokédex</h1>
      <p class="text-xs sm:text-sm text-zinc-500">{{ filtered.length }} pokémon</p>
    </div>

    <input
      v-model="query"
      type="text"
      placeholder="Buscar pokémon..."
      class="w-full max-w-xl mx-auto block mb-8 rounded-lg border border-border bg-graphite px-4 py-3 text-sm outline-none focus:border-accent placeholder:text-zinc-500"
    />

    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 sm:gap-4">
      <PokedexCard v-for="p in filtered" :key="p.id" :pokemon="p" />
    </div>

    <div v-if="pokedexLoading" class="flex flex-col items-center gap-3 py-10 text-zinc-400">
      <div class="h-8 w-8 rounded-full border-2 border-border border-t-accent animate-spin" />
      <p class="text-sm">Carregando mais pokémon...</p>
    </div>
  </main>
</template>
