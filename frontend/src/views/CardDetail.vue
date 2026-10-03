<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { api } from '../api/client'
import type { Card, CardStats, Sale } from '../api/types'
import StatTile from '../components/StatTile.vue'
import PriceChart from '../components/PriceChart.vue'
import HoloCard from '../components/HoloCard.vue'
import { money } from '../composables/useCurrency'

const props = defineProps<{ id: string }>()

const card = ref<Card | null>(null)
const sales = ref<Sale[]>([])
const stats30 = ref<CardStats | null>(null)
const loading = ref(true)
const error = ref('')

function date(v: string | null) {
  if (!v) return '—'
  return new Intl.DateTimeFormat('pt-BR').format(new Date(v))
}

const cardId = computed(() => Number(props.id))

onMounted(async () => {
  try {
    const [c, s, st] = await Promise.all([
      api.getCard(cardId.value),
      api.getSales(cardId.value),
      api.getStats(cardId.value, 30),
    ])
    card.value = c
    sales.value = s
    stats30.value = st
  } catch {
    error.value = 'Falha ao carregar dados da carta.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <main class="max-w-5xl mx-auto px-4 sm:px-6 py-6 sm:py-10 pb-24 md:pb-10">
    <p v-if="loading" class="text-zinc-500">Carregando...</p>
    <p v-else-if="error" class="text-accent">{{ error }}</p>

    <template v-else-if="card">
      <div class="grid md:grid-cols-[minmax(0,320px)_1fr] gap-6 md:gap-10">
        <div class="max-w-[240px] sm:max-w-none mx-auto md:mx-0 w-full">
          <HoloCard
            v-if="card.image_large"
            :image-url="card.image_large"
            :alt="card.name"
            :rarity="card.rarity"
            :supertype="card.supertype"
            :subtypes="card.subtypes"
            :card-number="card.card_number"
          />
        </div>

        <div>
          <h1 class="text-2xl sm:text-3xl font-bold text-center md:text-left">{{ card.name }}</h1>
          <p class="text-zinc-400 mt-1 text-center md:text-left">
            {{ card.set_name }} · {{ card.card_number }}
          </p>
          <p v-if="card.rarity" class="text-sm text-zinc-500 mt-1 text-center md:text-left">
            {{ card.rarity }}
          </p>

          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6">
            <StatTile label="Última venda" :value="money(stats30?.latest_sale ?? null)" />
            <StatTile label="Mediana 30d" :value="money(stats30?.median ?? null)" />
            <StatTile label="Média 30d" :value="money(stats30?.average ?? null)" />
            <StatTile label="Vendas analisadas" :value="String(stats30?.count ?? 0)" />
          </div>
        </div>
      </div>

      <section class="mt-8 sm:mt-10">
        <h2 class="text-sm font-semibold uppercase tracking-wide text-zinc-400 mb-3">
          Price History
        </h2>
        <PriceChart :sales="sales" />
      </section>

      <section class="mt-8 sm:mt-10">
        <h2 class="text-sm font-semibold uppercase tracking-wide text-zinc-400 mb-3">
          Recent Sales
        </h2>
        <p v-if="sales.length === 0" class="text-zinc-500 text-sm">
          Nenhuma venda encontrada ainda.
        </p>

        <!-- mobile: stacked cards -->
        <div v-else class="flex flex-col gap-2 sm:hidden">
          <component
            :is="s.listing_url ? 'a' : 'div'"
            v-for="s in sales"
            :key="s.id"
            :href="s.listing_url ?? undefined"
            target="_blank"
            rel="noopener"
            class="rounded-lg border border-border bg-graphite p-3 active:bg-graphite-light"
          >
            <div class="flex items-center justify-between">
              <span class="font-bold">{{ money(s.price, s.currency) }}</span>
              <span class="text-xs text-zinc-500">{{ date(s.sold_at) }}</span>
            </div>
            <div class="flex flex-wrap gap-x-2 text-xs text-zinc-400 mt-1">
              <span v-if="s.condition">{{ s.condition }}</span>
              <span v-if="s.grading_company && s.grade"
                >{{ s.grading_company }} {{ s.grade }}</span
              >
              <span v-if="s.listing_type">{{ s.listing_type }}</span>
              <span class="text-accent">{{ s.provider }}</span>
            </div>
          </component>
        </div>

        <!-- desktop: table -->
        <div v-if="sales.length" class="hidden sm:block overflow-x-auto rounded-lg border border-border">
          <table class="w-full text-sm">
            <thead class="bg-graphite text-zinc-400 text-left">
              <tr>
                <th class="px-4 py-2 font-medium">Data</th>
                <th class="px-4 py-2 font-medium">Preço</th>
                <th class="px-4 py-2 font-medium">Condição</th>
                <th class="px-4 py-2 font-medium">Grade</th>
                <th class="px-4 py-2 font-medium">Tipo</th>
                <th class="px-4 py-2 font-medium">Fonte</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="s in sales"
                :key="s.id"
                class="border-t border-border hover:bg-graphite-light"
              >
                <td class="px-4 py-2">{{ date(s.sold_at) }}</td>
                <td class="px-4 py-2 font-semibold">{{ money(s.price, s.currency) }}</td>
                <td class="px-4 py-2">{{ s.condition ?? '—' }}</td>
                <td class="px-4 py-2">
                  {{ s.grading_company && s.grade ? `${s.grading_company} ${s.grade}` : '—' }}
                </td>
                <td class="px-4 py-2">{{ s.listing_type ?? '—' }}</td>
                <td class="px-4 py-2">
                  <a
                    v-if="s.listing_url"
                    :href="s.listing_url"
                    target="_blank"
                    rel="noopener"
                    class="text-accent hover:underline"
                    >{{ s.provider }}</a
                  >
                  <span v-else>{{ s.provider }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </template>
  </main>
</template>
