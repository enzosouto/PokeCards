<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { api } from '../api/client'
import type { CardSearchResult } from '../api/types'
import { ensureFullPokedex, findPokemon } from '../pokedex/pokedexData'
import CardTile from '../components/CardTile.vue'
import TypeBadge from '../components/TypeBadge.vue'

const props = defineProps<{ id: string }>()
const pokemonId = computed(() => Number(props.id))
const pokemon = computed(() => findPokemon(pokemonId.value))

const cards = ref<CardSearchResult[]>([])
const loading = ref(true)
const error = ref('')

async function loadCards(name: string) {
  loading.value = true
  error.value = ''
  try {
    cards.value = await api.searchCards(name)
  } catch {
    error.value = 'Falha ao buscar cartas.'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await ensureFullPokedex()
  const p = pokemon.value
  if (p) await loadCards(p.name)
  else loading.value = false
})
</script>

<template>
  <main class="max-w-5xl mx-auto px-4 sm:px-6 py-6 sm:py-10 pb-24 md:pb-16">
    <RouterLink to="/pokedex" class="back-btn">&lt; VOLTAR</RouterLink>

    <div v-if="pokemon" class="poke-header">
      <span class="poke-header-number">#{{ String(pokemon.id).padStart(3, '0') }}</span>
      <img :src="pokemon.spriteUrl" :alt="pokemon.name" class="poke-header-sprite" width="120" height="120" />
      <h1 class="poke-header-name">{{ pokemon.name.toUpperCase() }}</h1>
      <div class="poke-header-types">
        <TypeBadge v-for="t in pokemon.types" :key="t" :type="t" />
      </div>
    </div>
    <p v-else class="text-center text-zinc-500 py-10">Pokémon não encontrado.</p>

    <template v-if="pokemon">
      <h2 class="text-sm font-semibold uppercase tracking-wide text-zinc-400 mt-10 mb-4">
        Cartas de {{ pokemon.name }}
      </h2>

      <div v-if="loading" class="flex flex-col items-center gap-3 py-12 text-zinc-400">
        <div class="h-8 w-8 rounded-full border-2 border-border border-t-accent animate-spin" />
        <p class="text-sm">Buscando cartas...</p>
      </div>
      <p v-else-if="error" class="text-center text-accent">{{ error }}</p>
      <p v-else-if="!cards.length" class="text-center text-zinc-500">Nenhuma carta encontrada.</p>
      <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 sm:gap-4">
        <CardTile v-for="card in cards" :key="card.id" :card="card" />
      </div>
    </template>
  </main>
</template>

<style scoped>
.back-btn {
  display: inline-block;
  font-family: var(--font-pixel);
  font-size: 0.6rem;
  color: #f4f4f5;
  border: 3px solid var(--color-accent);
  padding: 8px 12px;
  margin-bottom: 20px;
  text-decoration: none;
  box-shadow: 3px 3px 0 0 #000;
}

.back-btn:hover {
  background: var(--color-accent);
}

.poke-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  background: var(--color-graphite);
  border: 4px solid var(--color-accent);
  padding: 24px;
  box-shadow: 6px 6px 0 0 #000;
}

.poke-header-number {
  font-family: var(--font-pixel);
  font-size: 0.6rem;
  color: #9ca3af;
}

.poke-header-sprite {
  image-rendering: pixelated;
  width: 120px;
  height: 120px;
}

.poke-header-name {
  font-family: var(--font-pixel);
  font-size: 1rem;
}

.poke-header-types {
  display: flex;
  gap: 6px;
}
</style>
