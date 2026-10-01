<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, computed } from 'vue'
import logo from '../assets/logo.png'
import video169 from '../assets/video-169.mp4'
import video916 from '../assets/video-916.mp4'

const emit = defineEmits<{ done: [] }>()

const isMobile = window.matchMedia('(max-width: 767px)').matches
const src = isMobile ? video916 : video169

const containerEl = ref<HTMLDivElement | null>(null)
const videoEl = ref<HTMLVideoElement | null>(null)
const progress = ref(0)
const duration = ref(0)
const showLogo = ref(false)
let rafId = 0
let isSeeking = false
let pendingTime: number | null = null

const texts = [
  { from: 0, to: 0.22, text: 'Preços reais de cartas Pokémon' },
  { from: 0.22, to: 0.44, text: 'Vendas direto do eBay' },
  { from: 0.44, to: 0.66, text: 'Última venda, média, mediana' },
  { from: 0.66, to: 0.88, text: 'Histórico de preços em tempo real' },
  { from: 0.88, to: 1.01, text: isMobile ? 'Bem-vindo' : 'Role para começar' },
]
const activeText = computed(
  () => texts.find((t) => progress.value >= t.from && progress.value < t.to)?.text ?? ''
)

// Never issue a new seek while one is still in flight — queuing them up behind
// each other is what made scrubbing feel like it was "catching up" in jumps.
// Only the latest pending target survives; it fires the instant the current seek settles.
function seekTo(t: number) {
  if (!videoEl.value) return
  if (isSeeking) {
    pendingTime = t
    return
  }
  isSeeking = true
  videoEl.value.currentTime = t
}

function onSeeked() {
  isSeeking = false
  if (pendingTime !== null) {
    const t = pendingTime
    pendingTime = null
    seekTo(t)
  }
}

function onScroll() {
  cancelAnimationFrame(rafId)
  rafId = requestAnimationFrame(() => {
    if (!containerEl.value || !duration.value || showLogo.value) return
    const rect = containerEl.value.getBoundingClientRect()
    const scrollable = containerEl.value.offsetHeight - window.innerHeight
    const p = Math.min(Math.max(-rect.top / scrollable, 0), 1)
    progress.value = p
    seekTo(p * duration.value)
    if (p >= 0.995) reachEnd()
  })
}

function onTimeUpdate() {
  if (!duration.value || !videoEl.value) return
  progress.value = videoEl.value.currentTime / duration.value
}

function reachEnd() {
  if (showLogo.value) return
  showLogo.value = true
  if (!isMobile) window.removeEventListener('scroll', onScroll)
  setTimeout(finish, 1300)
}

function finish() {
  localStorage.setItem('pokemarket_intro_seen', '1')
  window.scrollTo(0, 0)
  emit('done')
}

function onLoadedMetadata() {
  duration.value = videoEl.value?.duration ?? 0
  if (isMobile) {
    videoEl.value?.play().catch(reachEnd)
  }
}

let loadTimeout = 0

onMounted(() => {
  if (!isMobile) window.addEventListener('scroll', onScroll, { passive: true })
  loadTimeout = window.setTimeout(() => {
    if (!duration.value) reachEnd() // video failed/too slow — don't trap the user
  }, 6000)
})
onBeforeUnmount(() => {
  if (!isMobile) window.removeEventListener('scroll', onScroll)
  cancelAnimationFrame(rafId)
  clearTimeout(loadTimeout)
})
</script>

<template>
  <!-- desktop: scroll-driven scrub -->
  <div v-if="!isMobile" ref="containerEl" class="relative" style="height: 400vh">
    <div class="sticky top-0 h-screen w-full overflow-hidden bg-black">
      <video
        ref="videoEl"
        :src="src"
        class="absolute inset-0 h-full w-full object-cover"
        muted
        playsinline
        preload="auto"
        @loadedmetadata="onLoadedMetadata"
        @seeked="onSeeked"
        @error="reachEnd"
      />
      <div class="absolute inset-0 bg-black/35" />

      <Transition name="fade" mode="out-in">
        <p
          :key="activeText"
          class="absolute inset-x-0 top-1/2 -translate-y-1/2 px-6 text-center text-2xl sm:text-4xl font-bold text-white drop-shadow-lg"
        >
          {{ activeText }}
        </p>
      </Transition>

      <div
        v-if="progress < 0.05"
        class="absolute bottom-10 inset-x-0 flex flex-col items-center gap-2 text-white/80 animate-bounce"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-7 w-7">
          <path d="M6 9l6 6 6-6" />
        </svg>
        <span class="text-xs uppercase tracking-widest">Role para explorar</span>
      </div>

      <Transition name="fade">
        <div v-if="showLogo" class="absolute inset-0 flex items-center justify-center bg-black">
          <img :src="logo" alt="PokéMarket" class="w-56 sm:w-72" />
        </div>
      </Transition>
    </div>
  </div>

  <!-- mobile: plays on its own, no scroll required -->
  <div v-else class="fixed inset-0 z-50 h-screen w-full overflow-hidden bg-black">
    <video
      ref="videoEl"
      :src="src"
      class="absolute inset-0 h-full w-full object-cover"
      muted
      playsinline
      preload="auto"
      @loadedmetadata="onLoadedMetadata"
      @timeupdate="onTimeUpdate"
      @ended="reachEnd"
      @error="reachEnd"
    />
    <div class="absolute inset-0 bg-black/35" />

    <Transition name="fade" mode="out-in">
      <p
        :key="activeText"
        class="absolute inset-x-0 top-1/2 -translate-y-1/2 px-6 text-center text-2xl font-bold text-white drop-shadow-lg"
      >
        {{ activeText }}
      </p>
    </Transition>

    <Transition name="fade">
      <div v-if="showLogo" class="absolute inset-0 flex items-center justify-center bg-black">
        <img :src="logo" alt="PokéMarket" class="w-56" />
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.35s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
