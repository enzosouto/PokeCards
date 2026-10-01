<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { Card } from '../api/types'

defineProps<{ card: Card; salesCount?: number }>()
</script>

<template>
  <RouterLink
    :to="`/cards/${card.id}`"
    class="group block rounded-xl border border-border bg-graphite p-3 sm:p-4 transition hover:border-accent/60 hover:bg-graphite-light active:border-accent/60 active:bg-graphite-light"
  >
    <div class="relative aspect-[5/7] w-full overflow-hidden rounded-lg bg-black/40 mb-2 sm:mb-3">
      <img
        v-if="card.image_small"
        :src="card.image_small"
        :alt="card.name"
        class="h-full w-full object-contain transition group-hover:scale-[1.03]"
        loading="lazy"
      />
      <span
        v-if="salesCount"
        class="absolute top-1.5 right-1.5 sm:top-2 sm:right-2 rounded-full bg-accent px-1.5 sm:px-2 py-0.5 text-[10px] sm:text-xs font-semibold"
      >
        {{ salesCount }} {{ salesCount === 1 ? 'venda' : 'vendas' }}
      </span>
    </div>
    <p class="text-sm sm:text-base font-semibold leading-tight truncate">{{ card.name }}</p>
    <p class="text-xs sm:text-sm text-zinc-400 truncate">{{ card.set_name }} · {{ card.card_number }}</p>
    <p v-if="card.rarity" class="hidden sm:block text-xs text-zinc-500 mt-1 truncate">
      {{ card.rarity }}
    </p>
  </RouterLink>
</template>
