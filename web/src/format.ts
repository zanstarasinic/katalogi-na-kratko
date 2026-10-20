const eur = new Intl.NumberFormat('sl-SI', { style: 'currency', currency: 'EUR' })

export const price = (n: number) => eur.format(n)

/** '2026-10-14' -> '14. 10.' */
export function shortDate(iso?: string): string {
  if (!iso) return ''
  const [, m, d] = iso.split('-')
  return `${Number(d)}. ${Number(m)}.`
}

const WEEKDAYS = ['ned.', 'pon.', 'tor.', 'sre.', 'čet.', 'pet.', 'sob.']

/** When an offer starts, relative to today: 'jutri', 'pet. 16. 10.' */
export function startDay(iso: string, today: string): string {
  const day = (d: string) => Date.UTC(+d.slice(0, 4), +d.slice(5, 7) - 1, +d.slice(8, 10))
  if (day(iso) - day(today) === 864e5) return 'jutri'
  return `${WEEKDAYS[new Date(day(iso)).getUTCDay()]} ${shortDate(iso)}`
}

export function dateTime(iso?: string): string {
  if (!iso) return ''
  return new Intl.DateTimeFormat('sl-SI', {
    day: 'numeric', month: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit',
    timeZone: 'Europe/Ljubljana',
  }).format(new Date(iso))
}

/**
 * Slovene count of "izdelek". Nominative for labels ("103 izdelki"), accusative after a verb
 * ("Pokaži 103 izdelke"): 1 izdelek, 2 izdelka, 3–4 izdelki / izdelke, 5+ izdelkov.
 */
export function izdelkov(n: number, grammaticalCase: 'nom' | 'acc' = 'nom'): string {
  const m = n % 100
  if (m === 1) return `${n} izdelek`
  if (m === 2) return `${n} izdelka`
  if (m === 3 || m === 4) return `${n} ${grammaticalCase === 'acc' ? 'izdelke' : 'izdelki'}`
  return `${n} izdelkov`
}
