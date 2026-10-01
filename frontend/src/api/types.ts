export interface Card {
  id: number
  external_id: string
  name: string
  set_id: string
  set_name: string
  card_number: string
  rarity: string | null
  supertype: string | null
  subtypes: string | null
  image_small: string | null
  image_large: string | null
  language: string
}

export interface CardSearchResult extends Card {
  match_score: number
}

export interface CardWithSalesCount extends Card {
  sales_count: number
}

export interface RecentSale extends Sale {
  card_id: number
  card_name: string
  card_number: string
  set_name: string
  image_small: string | null
}

export interface Sale {
  id: number
  provider: string
  title: string
  price: number
  currency: string
  shipping: number | null
  condition: string | null
  grading_company: string | null
  grade: string | null
  listing_type: string | null
  sold_at: string
  listing_url: string | null
}

export interface CardStats {
  latest_sale: number | null
  latest_sale_date: string | null
  average: number | null
  median: number | null
  minimum: number | null
  maximum: number | null
  count: number
}
