<script setup lang="ts">
import { computed } from 'vue'
import type { TypeName } from '../pokedex/types'

const props = withDefaults(defineProps<{ type: TypeName; size?: 'sm' | 'md' }>(), { size: 'md' })

const TYPE_COLOR: Record<TypeName, string> = {
  normal: '#a8a878', fire: '#f08030', water: '#6890f0', electric: '#f8d030',
  grass: '#78c850', ice: '#98d8d8', fighting: '#c03028', poison: '#a040a0',
  ground: '#e0c068', flying: '#a890f0', psychic: '#f85888', bug: '#a8b820',
  rock: '#b8a038', ghost: '#705898', dragon: '#7038f8', dark: '#705848',
  steel: '#b8b8d0', fairy: '#ee99ac',
}

const TYPE_LABEL_PT: Record<TypeName, string> = {
  normal: 'NORMAL', fire: 'FOGO', water: 'ÁGUA', electric: 'ELÉTRICO',
  grass: 'GRAMA', ice: 'GELO', fighting: 'LUTADOR', poison: 'VENENOSO',
  ground: 'TERRESTRE', flying: 'VOADOR', psychic: 'PSÍQUICO', bug: 'INSETO',
  rock: 'PEDRA', ghost: 'FANTASMA', dragon: 'DRAGÃO', dark: 'SOMBRIO',
  steel: 'AÇO', fairy: 'FADA',
}

const bg = computed(() => TYPE_COLOR[props.type])
</script>

<template>
  <span class="type-badge" :class="`type-badge--${size}`" :style="{ background: bg }">
    {{ TYPE_LABEL_PT[type] }}
  </span>
</template>

<style scoped>
.type-badge {
  display: inline-block;
  font-weight: 600;
  color: #15151a;
  border-radius: 4px;
  padding: 3px 8px;
}

.type-badge--sm {
  font-size: 0.6rem;
  padding: 2px 7px;
}

.type-badge--md {
  font-size: 0.7rem;
}
</style>
