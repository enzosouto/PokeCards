import type { Card, CardSearchResult, CardStats, CardWithSalesCount, RecentSale, Sale } from './types'

const API_BASE = import.meta.env.VITE_API_BASE ?? '/api'

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`)
  if (!res.ok) throw new Error(`Request failed: ${res.status}`)
  return res.json()
}

export const api = {
  searchCards: (q: string) => get<CardSearchResult[]>(`/cards/search?q=${encodeURIComponent(q)}`),
  getTopCards: (limit = 12) => get<CardWithSalesCount[]>(`/cards/top?limit=${limit}`),
  getAllCards: (limit = 500) => get<CardWithSalesCount[]>(`/cards?limit=${limit}`),
  getRecentSales: (limit = 50) => get<RecentSale[]>(`/sales/recent?limit=${limit}`),
  getCard: (id: number) => get<Card>(`/cards/${id}`),
  getSales: (id: number) => get<Sale[]>(`/cards/${id}/sales`),
  getStats: (id: number, days?: number) =>
    get<CardStats>(`/cards/${id}/stats${days ? `?days=${days}` : ''}`),
}
