<script setup lang="ts">
import { currency, setCurrency } from '../composables/useCurrency'
</script>

<template>
  <div class="flex items-center gap-2.5">
    <button
      type="button"
      title="Dólar (USD)"
      aria-label="Mostrar preços em dólar"
      @click="setCurrency('USD')"
      class="flex items-center gap-1.5 text-xs font-semibold transition"
      :class="currency === 'USD' ? 'text-white' : 'text-zinc-500 opacity-60'"
    >
      <span
        class="h-6 w-6 rounded-full overflow-hidden flex-shrink-0 border-2"
        :class="currency === 'USD' ? 'border-accent' : 'border-border'"
      >
        <svg viewBox="0 0 24 24" class="h-full w-full">
          <clipPath id="flag-us"><circle cx="12" cy="12" r="12" /></clipPath>
          <g clip-path="url(#flag-us)">
            <rect width="24" height="24" fill="#B22234" />
            <rect y="1.85" width="24" height="1.85" fill="#fff" />
            <rect y="5.54" width="24" height="1.85" fill="#fff" />
            <rect y="9.23" width="24" height="1.85" fill="#fff" />
            <rect y="12.92" width="24" height="1.85" fill="#fff" />
            <rect y="16.62" width="24" height="1.85" fill="#fff" />
            <rect y="20.31" width="24" height="1.85" fill="#fff" />
            <rect width="10" height="13" fill="#3C3B6E" />
          </g>
        </svg>
      </span>
      USD
    </button>
    <button
      type="button"
      title="Real (BRL)"
      aria-label="Mostrar preços em real"
      @click="setCurrency('BRL')"
      class="flex items-center gap-1.5 text-xs font-semibold transition"
      :class="currency === 'BRL' ? 'text-white' : 'text-zinc-500 opacity-60'"
    >
      <span
        class="h-6 w-6 rounded-full overflow-hidden flex-shrink-0 border-2"
        :class="currency === 'BRL' ? 'border-accent' : 'border-border'"
      >
        <svg viewBox="0 0 24 24" class="h-full w-full">
          <clipPath id="flag-br"><circle cx="12" cy="12" r="12" /></clipPath>
          <g clip-path="url(#flag-br)">
            <rect width="24" height="24" fill="#009739" />
            <polygon points="12,3 21,12 12,21 3,12" fill="#FEDD00" />
            <circle cx="12" cy="12" r="5" fill="#002776" />
          </g>
        </svg>
      </span>
      BRL
    </button>
  </div>
</template>
