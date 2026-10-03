<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import * as echarts from 'echarts'
import type { Sale } from '../api/types'
import { currency, convert } from '../composables/useCurrency'

const props = defineProps<{ sales: Sale[] }>()
const el = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null

function render() {
  if (!el.value) return
  const symbol = currency.value === 'BRL' ? 'R$' : '$'
  const points = [...props.sales]
    .sort((a, b) => new Date(a.sold_at).getTime() - new Date(b.sold_at).getTime())
    .map((s) => [s.sold_at, convert(s.price, s.currency)])

  const isMobile = window.innerWidth < 640
  if (!chart) chart = echarts.init(el.value, null, { renderer: 'svg' })
  chart.setOption({
    backgroundColor: 'transparent',
    grid: { left: isMobile ? 40 : 48, right: isMobile ? 8 : 16, top: 16, bottom: 32 },
    xAxis: { type: 'time', axisLabel: { color: '#a1a1aa' }, axisLine: { lineStyle: { color: '#2a2a2f' } } },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#a1a1aa', formatter: `${symbol}{value}` },
      splitLine: { lineStyle: { color: '#2a2a2f' } },
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: '#1e1e22',
      borderColor: '#2a2a2f',
      textStyle: { color: '#f4f4f5' },
      valueFormatter: (v: number) => `${symbol}${Number(v).toFixed(2)}`,
    },
    series: [
      {
        type: 'line',
        data: points,
        smooth: true,
        symbolSize: 6,
        lineStyle: { color: '#9333ea', width: 2 },
        itemStyle: { color: '#9333ea' },
        areaStyle: { color: 'rgba(220,38,38,0.1)' },
      },
    ],
  })
}

function handleResize() {
  chart?.resize()
}

onMounted(() => {
  render()
  window.addEventListener('resize', handleResize)
})
watch(() => props.sales, render, { deep: true })
watch(currency, render)
onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})
</script>

<template>
  <div
    v-if="sales.length === 0"
    class="rounded-lg border border-border bg-graphite p-6 text-sm text-zinc-500"
  >
    Sem dados suficientes para o gráfico.
  </div>
  <div v-else ref="el" class="rounded-lg border border-border bg-graphite h-56 sm:h-72 w-full" />
</template>
