import { ref, watch } from 'vue'

const STORAGE_KEY = 'pokemarket_currency'
const RATE_KEY = 'pokemarket_usd_brl_rate'
const RATE_TTL_MS = 60 * 60 * 1000
const FALLBACK_RATE = 5.3

export type DisplayCurrency = 'USD' | 'BRL'

const stored = localStorage.getItem(STORAGE_KEY)
export const currency = ref<DisplayCurrency>(stored === 'BRL' ? 'BRL' : 'USD')
watch(currency, (v) => localStorage.setItem(STORAGE_KEY, v))

const rate = ref(Number(localStorage.getItem(RATE_KEY)) || FALLBACK_RATE)

async function refreshRate() {
  const cachedAt = Number(localStorage.getItem(`${RATE_KEY}_at`) || 0)
  if (Date.now() - cachedAt < RATE_TTL_MS) return
  try {
    const res = await fetch('https://economia.awesomeapi.com.br/last/USD-BRL')
    const data = await res.json()
    const bid = Number(data?.USDBRL?.bid)
    if (bid > 0) {
      rate.value = bid
      localStorage.setItem(RATE_KEY, String(bid))
      localStorage.setItem(`${RATE_KEY}_at`, String(Date.now()))
    }
  } catch {
    // keep last known/fallback rate
  }
}
refreshRate()

export function setCurrency(c: DisplayCurrency) {
  currency.value = c
}

export function convert(value: number, sourceCurrency = 'USD') {
  if (sourceCurrency === currency.value) return value
  return sourceCurrency === 'USD' && currency.value === 'BRL'
    ? value * rate.value
    : value / rate.value
}

export function money(value: number | null, sourceCurrency = 'USD') {
  if (value === null) return '—'
  return new Intl.NumberFormat(currency.value === 'BRL' ? 'pt-BR' : 'en-US', {
    style: 'currency',
    currency: currency.value,
  }).format(convert(value, sourceCurrency))
}
