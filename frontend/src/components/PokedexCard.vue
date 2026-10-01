<script setup lang="ts">
import type { PokedexEntry } from '../pokedex/types'
import TypeBadge from './TypeBadge.vue'

defineProps<{ pokemon: PokedexEntry }>()
</script>

<template>
  <RouterLink :to="`/pokedex/${pokemon.id}`" class="poke-card">
    <span class="poke-number">#{{ String(pokemon.id).padStart(3, '0') }}</span>
    <img class="poke-sprite" :src="pokemon.spriteUrl" :alt="pokemon.name" loading="lazy" width="72" height="72" />
    <span class="poke-name">{{ pokemon.name.toUpperCase() }}</span>
    <div class="poke-types">
      <TypeBadge v-for="t in pokemon.types" :key="t" :type="t" size="sm" />
    </div>
  </RouterLink>
</template>

<style scoped>
.poke-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  background: var(--color-graphite);
  border: 4px solid var(--color-border);
  padding: 12px 8px;
  text-decoration: none;
  color: #f4f4f5;
  transition: border-color 0.15s;
}

.poke-card:hover {
  border-color: var(--color-accent);
}

.poke-number {
  font-family: var(--font-pixel);
  font-size: 0.55rem;
  color: #9ca3af;
  align-self: flex-start;
}

.poke-sprite {
  width: 72px;
  height: 72px;
  object-fit: contain;
  image-rendering: pixelated;
}

.poke-name {
  font-family: var(--font-pixel);
  font-size: 0.55rem;
  text-align: center;
}

.poke-types {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
  justify-content: center;
}
</style>
