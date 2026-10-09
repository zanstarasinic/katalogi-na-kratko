import type { StoreId } from './types'

export const STORES: { id: StoreId; label: string; card: string; color: string; note?: string }[] = [
  { id: 'lidl', label: 'Lidl', card: 'Lidl Plus', color: '#0050aa' },
  { id: 'spar', label: 'Spar', card: 'SPAR plus', color: '#d8232a', note: 'Podatki iz SPAR Online; nekatere akcije iz letaka v trgovini morda manjkajo.' },
  { id: 'eurospin', label: 'Eurospin', card: 'kartica', color: '#1a3e8c' },
  { id: 'hofer', label: 'Hofer', card: 'kartica', color: '#f39200' },
]

export const storeById = Object.fromEntries(STORES.map(s => [s.id, s])) as Record<StoreId, (typeof STORES)[number]>
