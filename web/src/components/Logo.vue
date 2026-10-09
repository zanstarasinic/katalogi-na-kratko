<script setup lang="ts">
withDefaults(defineProps<{ size?: number; board?: string; ink?: string }>(), { size: 36, board: '#ffffff', ink: '#1d2421' })
</script>

<template>
  <!-- A market price stake: notched board on a post, with a % built from geometry. -->
  <svg :width="size" :height="size * 1.2" viewBox="0 0 40 48" aria-hidden="true">
    <path :fill="board" d="M7 2h20l11 11v16a7 7 0 0 1-7 7H7a7 7 0 0 1-7-7V9a7 7 0 0 1 7-7z" />
    <rect :fill="board" x="16.5" y="35" width="7" height="13" rx="1.5" />
    <circle :fill="ink" cx="11.5" cy="12.5" r="4.2" />
    <circle :fill="ink" cx="25.5" cy="26" r="4.2" />
    <rect :fill="ink" x="16.4" y="5.5" width="4.4" height="27" rx="2.2" transform="rotate(32 18.6 19)" />
  </svg>
</template>
