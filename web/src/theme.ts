// Crate colours: one produce-market hue per category. They appear only on the
// card's crate edge and the category swatch, never as large fields.
export const CRATE: Record<string, string> = {
  'sadje-zelenjava': '#2f8a45',
  'meso-ribe': '#a8322d',
  'mlecni-jajca': '#f2c230',
  'kruh-pekovski': '#c98a3d',
  'shramba': '#ef7d1a',
  'zamrznjeno': '#3a8fc9',
  'sladko-slano': '#8a4b2f',
  'pijace': '#1f9a9a',
  'alkohol': '#6a2c5e',
  'nega-zdravje': '#c2417a',
  'cistila-gospodinjstvo': '#4a6fd1',
  'otroci': '#ff8fa3',
  'ljubljencki': '#7b8f2a',
  'dom-vrt-orodje': '#5b6b73',
  'oblacila': '#7a5cc9',
  'drugo': '#9aa39d',
}

export const crate = (id: string) => CRATE[id] ?? CRATE.drugo
