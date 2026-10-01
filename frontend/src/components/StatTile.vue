<script setup lang="ts">
defineProps<{ label: string; value: string }>()
</script>

<template>
  <div class="rounded-lg border border-border bg-graphite px-4 py-3">
    <p class="text-xs uppercase tracking-wide text-zinc-500">{{ label }}</p>
    <p class="text-xl font-bold mt-1">{{ value }}</p>
  </div>
</template>
