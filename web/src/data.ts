// The only module that knows where data comes from. Switching to a backend API
// later means changing this file only.
import type { Meta, Offer } from './types'

const base = import.meta.env.BASE_URL

async function getJson<T>(path: string): Promise<T> {
  const res = await fetch(`${base}${path}`, { cache: 'no-cache' })
  if (!res.ok) throw new Error(`${path}: HTTP ${res.status}`)
  return res.json() as Promise<T>
}

export function loadOffers(): Promise<Offer[]> {
  return getJson<Offer[]>('data/offers.json')
}

export function loadMeta(): Promise<Meta> {
  return getJson<Meta>('data/meta.json')
}
