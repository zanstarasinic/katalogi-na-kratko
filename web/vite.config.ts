import { defineConfig, type Plugin } from 'vite'
import vue from '@vitejs/plugin-vue'
import { cpSync, existsSync, mkdirSync, readFileSync } from 'node:fs'
import { resolve } from 'node:path'

// The site reads ../data (written by the daily scraper). Served as /data in dev,
// copied into dist/data on build. History files are not needed by the site.
const DATA = resolve(__dirname, '../data')
const FILES = ['offers.json', 'meta.json']

function dataFiles(): Plugin {
  let outDir = ''
  return {
    name: 'data-files',
    configResolved(c) {
      if (c.command === 'build' && !process.env.VITEST) outDir = resolve(c.root, c.build.outDir)
    },
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const name = req.url?.split('?')[0].replace(/^.*\/data\//, '')
        if (!req.url?.includes('/data/') || !name || !FILES.includes(name)) return next()
        const file = resolve(DATA, name)
        if (!existsSync(file)) return next()
        res.setHeader('Content-Type', 'application/json')
        res.end(readFileSync(file))
      })
    },
    closeBundle() {
      if (!outDir) return
      mkdirSync(resolve(outDir, 'data'), { recursive: true })
      for (const f of FILES) {
        if (existsSync(resolve(DATA, f))) cpSync(resolve(DATA, f), resolve(outDir, 'data', f))
      }
    },
  }
}

export default defineConfig({
  // GitHub Pages serves the site under /<repo>/; the workflow sets BASE_PATH.
  base: process.env.BASE_PATH || '/',
  plugins: [vue(), dataFiles()],
})
