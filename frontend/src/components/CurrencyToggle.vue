<script setup lang="ts">
import { currency, setCurrency } from '../composables/useCurrency'
</script>

<template>
  <div class="flex items-center gap-1.5">
    <button
      type="button"
      title="Dólar (USD)"
      aria-label="Mostrar preços em dólar"
      @click="setCurrency('USD')"
      class="h-7 w-7 rounded-full overflow-hidden flex items-center justify-center text-base leading-none border-2 transition"
      :class="currency === 'USD' ? 'border-accent' : 'border-border opacity-50'"
    >
      🇺🇸
    </button>
    <button
      type="button"
      title="Real (BRL)"
      aria-label="Mostrar preços em real"
      @click="setCurrency('BRL')"
      class="h-7 w-7 rounded-full overflow-hidden flex items-center justify-center text-base leading-none border-2 transition"
      :class="currency === 'BRL' ? 'border-accent' : 'border-border opacity-50'"
    >
      🇧🇷
    </button>
  </div>
</template>
