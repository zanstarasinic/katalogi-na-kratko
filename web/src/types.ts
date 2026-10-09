export type StoreId = 'lidl' | 'spar' | 'eurospin' | 'hofer'

/** The shared offer record written by the scraper (see scraper/model.py). */
export interface Offer {
  id: string
  store: StoreId
  name: string
  brand?: string
  kind: 'discount' | 'special'
  price: number
  regular_price?: number
  discount_pct?: number
  requires_card: boolean
  min_quantity: number
  package?: string
  unit_price?: string
  valid_from?: string
  valid_to?: string
  category: string
  store_category?: string
  image_url?: string
  product_url?: string
  description?: string
  ean?: string
}

export interface StoreMeta {
  ok: boolean
  count?: number
  count_published?: number
  updated_at?: string
  attempted_at?: string
  error?: string
  source?: string
}

export interface Meta {
  generated_at: string
  count: number
  stores: Partial<Record<StoreId, StoreMeta>>
  categories: { id: string; label: string }[]
}
