<script setup lang="ts">
// One authored icon set: 24px grid, 2px round strokes.
defineProps<{ name: 'search' | 'filter' | 'heart' | 'external' | 'close' | 'chevron' | 'sort' | 'check'; size?: number }>()
</script>

<template>
  <svg :width="size ?? 18" :height="size ?? 18" viewBox="0 0 24 24" fill="none" stroke="currentColor"
    stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" class="icon">
    <template v-if="name === 'search'"><circle cx="11" cy="11" r="7" /><path d="m20 20-3.6-3.6" /></template>
    <template v-else-if="name === 'filter'"><path d="M4 6h16M7 12h10M10 18h4" /></template>
    <template v-else-if="name === 'heart'"><path d="M12 20s-7.5-4.4-8.9-9C2 7.5 4.3 4.5 7.6 4.5c2 0 3.4 1.1 4.4 2.6 1-1.5 2.4-2.6 4.4-2.6 3.3 0 5.6 3 4.5 6.5-1.4 4.6-8.9 9-8.9 9z" /></template>
    <template v-else-if="name === 'external'"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5" /></template>
    <template v-else-if="name === 'close'"><path d="M6 6l12 12M18 6 6 18" /></template>
    <template v-else-if="name === 'chevron'"><path d="m6 9 6 6 6-6" /></template>
    <template v-else-if="name === 'sort'"><path d="M7 4v16M3 16l4 4 4-4M17 20V4M13 8l4-4 4 4" /></template>
    <template v-else-if="name === 'check'"><path d="m5 12 5 5 9-10" /></template>
  </svg>
</template>
