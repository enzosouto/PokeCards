<script setup lang="ts">
import { ref, computed, onBeforeUnmount } from 'vue'
import glitter from '../assets/glitter.png'
import illusionMask from '../assets/illusion-mask.png'
import illusion from '../assets/illusion.png'
import geometric from '../assets/geometric.png'
import grain from '../assets/grain.webp'
import trainerbg from '../assets/trainerbg.png'
import cosmosBottom from '../assets/cosmos-bottom.png'
import cosmosMiddle from '../assets/cosmos-middle-trans.png'
import cosmosTop from '../assets/cosmos-top-trans.png'

const props = defineProps<{
  imageUrl: string
  alt: string
  rarity: string | null
  supertype?: string | null
  subtypes?: string | null
  setId?: string | null
  cardNumber?: string | null
}>()

// Ported from github.com/simeydotme/pokemon-cards-css (GPL-3.0) — exact gradients/blend
// modes transcribed from the project's own base.css / regular-holo.css / rainbow-holo.css /
// etc (fetched via raw.githubusercontent.com, not re-derived), rewritten with plain CSS
// custom properties + Vue instead of Svelte spring physics.
const round = (v: number, p = 3) => parseFloat(v.toFixed(p))
const clamp = (v: number, min = 0, max = 100) => Math.min(Math.max(v, min), max)
const adjust = (v: number, fromMin: number, fromMax: number, toMin: number, toMax: number) =>
  round(toMin + ((toMax - toMin) * (v - fromMin)) / (fromMax - fromMin))

type Effect =
  | 'none' | 'holo' | 'cosmos' | 'amazing' | 'radiant' | 'v' | 'ultra' | 'shiny' | 'rainbow' | 'secret'
  | 'tg-holo' | 'trainer-ultra'

// Exact data-rarity strings the source project defines effects for (confirmed by
// grepping every selector in its CSS) — nothing else gets an effect. No substring
// guessing: a rarity the source doesn't cover doesn't get an invented look.
function classifyRarity(
  rarity: string | null,
  supertype?: string | null,
  subtypes?: string | null,
  cardNumber?: string | null
): Effect {
  const r = (rarity ?? '').toLowerCase().trim()
  const isTrainerGallery = /^tg/i.test(cardNumber ?? '')
  const isSupporter = (subtypes ?? '').toLowerCase().includes('supporter')
  const isTrainer = (supertype ?? '').toLowerCase() === 'trainer'

  if (r === 'rare holo' && isTrainerGallery) return 'tg-holo'
  if (r === 'rare ultra' && isTrainer && isSupporter) return 'trainer-ultra'

  switch (r) {
    case 'rare holo':
      return 'holo'
    case 'trainer gallery rare holo':
      return 'tg-holo'
    case 'rare holo cosmos':
      return 'cosmos'
    case 'amazing rare':
      return 'amazing'
    case 'radiant rare':
      return 'radiant'
    case 'rare holo v':
      return 'v'
    case 'rare holo vmax':
    case 'rare holo vstar':
    case 'rare ultra':
      return 'ultra'
    case 'rare shiny':
    case 'rare shiny v':
    case 'rare shiny vmax':
      return 'shiny'
    case 'rare rainbow':
    case 'rare rainbow alt':
      return 'rainbow'
    case 'rare secret':
      return 'secret'
    default:
      return 'none'
  }
}

const effect = computed(() =>
  classifyRarity(props.rarity, props.supertype, props.subtypes, props.cardNumber)
)
const cosmosBg = `${Math.floor(Math.random() * 734)}px ${Math.floor(Math.random() * 1280)}px`

const el = ref<HTMLDivElement | null>(null)
const interacting = ref(false)
const expanded = ref(false)
const spinDeg = ref(0)
const vars = ref<Record<string, string>>({})

function interact(e: PointerEvent) {
  if (!el.value) return
  interacting.value = true
  const rect = el.value.getBoundingClientRect()
  const percentX = clamp(round((100 / rect.width) * (e.clientX - rect.left)))
  const percentY = clamp(round((100 / rect.height) * (e.clientY - rect.top)))
  const centerX = percentX - 50
  const centerY = percentY - 50

  vars.value = {
    ...vars.value,
    '--pointer-x': `${percentX}%`,
    '--pointer-y': `${percentY}%`,
    '--background-x': `${adjust(percentX, 0, 100, 37, 63)}%`,
    '--background-y': `${adjust(percentY, 0, 100, 33, 67)}%`,
    '--rotate-x': `${round(-(centerX / 3.5))}deg`,
    '--rotate-y': `${round(centerY / 3.5)}deg`,
    '--pointer-from-center': `${clamp(Math.sqrt(centerY * centerY + centerX * centerX) / 50, 0, 1)}`,
    '--pointer-from-top': `${percentY / 100}`,
    '--pointer-from-left': `${percentX / 100}`,
    '--card-opacity': '1',
  }
}

function reset() {
  interacting.value = false
  vars.value = {
    '--pointer-x': '50%', '--pointer-y': '50%',
    '--rotate-x': '0deg', '--rotate-y': '0deg',
    '--background-x': '50%', '--background-y': '50%',
    '--pointer-from-center': '0', '--pointer-from-top': '0', '--pointer-from-left': '0',
    '--card-opacity': '0',
  }
}

// spins the card 360° on the Y axis when opened — the back of the card briefly
// shows mid-spin, same "firstPop" flourish as the source project.
function spinOnce() {
  const start = performance.now()
  const duration = 900
  function step(now: number) {
    const t = Math.min((now - start) / duration, 1)
    const eased = 1 - Math.pow(1 - t, 3)
    spinDeg.value = eased * 360
    if (t < 1) requestAnimationFrame(step)
    else spinDeg.value = 0
  }
  requestAnimationFrame(step)
}

function toggleExpand() {
  expanded.value = !expanded.value
  if (expanded.value) spinOnce()
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') expanded.value = false
}
window.addEventListener('keydown', onKeydown)
onBeforeUnmount(() => window.removeEventListener('keydown', onKeydown))

// was a plain object before — spinDeg.value was read ONCE at setup and frozen,
// so the spin animation never visually updated. Must be computed to stay reactive.
const textureVars = computed(() => ({
  '--glitter': `url(${glitter})`,
  '--foil-illusion-mask': `url(${illusionMask})`,
  '--foil-illusion': `url(${illusion})`,
  '--foil-geometric': `url(${geometric})`,
  '--grain': `url(${grain})`,
  '--foil-trainerbg': `url(${trainerbg})`,
  '--cosmos-bottom': `url(${cosmosBottom})`,
  '--cosmos-middle': `url(${cosmosMiddle})`,
  '--cosmos-top': `url(${cosmosTop})`,
  '--cosmosbg': cosmosBg,
  '--spin-y': `${spinDeg.value}deg`,
}))
</script>

<template>
  <Transition name="backdrop">
    <div
      v-if="expanded"
      class="fixed inset-0 z-40 bg-black/80 backdrop-blur-sm"
      @click="expanded = false"
    />
  </Transition>

  <div
    ref="el"
    class="holo-card"
    :class="{ expanded }"
    :style="{ ...vars, ...textureVars }"
    @pointermove="interact"
    @pointerleave="reset"
    @pointerup="reset"
    @pointercancel="reset"
    @click="toggleExpand"
  >
    <div class="holo-card__rotator">
      <img
        class="holo-card__back"
        src="https://tcg.pokemon.com/assets/img/global/tcg-card-back-2x.jpg"
        alt="Verso da carta Pokémon"
      />
      <div class="holo-card__front" :class="[`fx-${effect}`, { interacting }]">
        <img :src="imageUrl" :alt="alt" class="holo-card__img" />
        <div v-if="effect !== 'none'" class="holo-card__shine" />
        <div class="holo-card__glare" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.holo-card {
  --pointer-x: 50%;
  --pointer-y: 50%;
  --pointer-from-center: 0;
  --pointer-from-top: 0;
  --pointer-from-left: 0;
  --card-opacity: 0;
  --rotate-x: 0deg;
  --rotate-y: 0deg;
  --background-x: 50%;
  --background-y: 50%;
  --clip: inset(9.85% 8% 52.85% 8%);
  --violet: #c929f1; --blue: #0dbde9; --green: #21e985; --yellow: #eedf10; --red: #f80e35;
  --sp-1: hsl(2, 100%, 73%); --sp-2: hsl(53, 100%, 69%); --sp-3: hsl(93, 100%, 69%);
  --sp-4: hsl(176, 100%, 76%); --sp-5: hsl(228, 100%, 74%); --sp-6: hsl(283, 100%, 73%);

  position: relative;
  display: block;
  cursor: pointer;
  perspective: 600px;
  transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
  /* without this, a finger-drag across the card is captured by the browser as a
     page-scroll gesture before pointermove ever reaches us — the tilt/shine never
     gets a chance to follow the touch. */
  touch-action: none;
}

.holo-card.expanded {
  position: fixed;
  inset: 0;
  margin: auto;
  z-index: 50;
  width: min(80vw, 420px);
  height: fit-content;
}

.holo-card__rotator {
  display: grid;
  /* fixed real Pokémon-card ratio — without this, front/back images (which have
     different natural aspect ratios) size the grid row independently, leaving a
     sliver of whichever is shorter (usually the back) peeking out underneath. */
  aspect-ratio: 0.718;
  transform-style: preserve-3d;
  transform: rotateY(calc(var(--rotate-x) + var(--spin-y))) rotateX(var(--rotate-y));
  transition: box-shadow 0.4s ease;
  box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.6), 0 2px 15px -5px rgba(0, 0, 0, 0.4);
  border-radius: 4.55% / 3.5%;
}

.holo-card__back,
.holo-card__front {
  grid-area: 1/1;
  width: 100%;
  height: 100%;
  border-radius: inherit;
  transform-style: preserve-3d;
}

.holo-card__back {
  transform: rotateY(180deg) translateZ(1px);
  backface-visibility: visible;
  border-radius: inherit;
  object-fit: cover;
}

.holo-card__front {
  position: relative;
  display: grid;
  backface-visibility: hidden;
  transform: translateZ(1px);
  overflow: hidden;
}

.holo-card__img,
.holo-card__shine,
.holo-card__glare {
  grid-area: 1/1;
  width: 100%;
  height: 100%;
  border-radius: inherit;
}

.holo-card__img {
  object-fit: cover;
}

.holo-card__shine {
  position: relative;
  overflow: hidden;
  background: transparent;
  background-size: cover;
  background-position: center;
  opacity: var(--card-opacity);
  transition: opacity 0.33s ease-out;
  /* shared default per base.css — rarities only override this when they need
     a different blend; without it, an opaque gradient just paints over the photo. */
  mix-blend-mode: color-dodge;
  filter: brightness(0.85) contrast(2.75) saturate(0.65);
}
.holo-card__shine::before,
.holo-card__shine::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
}

.holo-card__glare {
  position: relative;
  overflow: hidden;
  background-image: radial-gradient(
    farthest-corner circle at var(--pointer-x) var(--pointer-y),
    hsla(0, 0%, 100%, 0.8) 10%,
    hsla(0, 0%, 100%, 0.65) 20%,
    hsla(0, 0%, 0%, 0.5) 90%
  );
  opacity: var(--card-opacity);
  mix-blend-mode: overlay;
  transition: opacity 0.33s ease-out;
}

/* ============ HOLO (rare holo) ============ */
.fx-holo .holo-card__shine {
  --scanlines-space: 1px;
  mask-image: linear-gradient(to bottom, black 0%, black 38%, transparent 55%);
  -webkit-mask-image: linear-gradient(to bottom, black 0%, black 38%, transparent 55%);
  background-image: repeating-linear-gradient(110deg,
      var(--violet), var(--blue), var(--green), var(--yellow), var(--red),
      var(--violet), var(--blue), var(--green), var(--yellow), var(--red)),
    repeating-linear-gradient(90deg,
      black calc(var(--scanlines-space) * 0), black calc(var(--scanlines-space) * 2),
      #666 calc(var(--scanlines-space) * 2), #666 calc(var(--scanlines-space) * 4));
  background-position: calc(((50% - var(--background-x)) * 2.6) + 50%) calc(((50% - var(--background-y)) * 3.5) + 50%), center center;
  background-size: 400% 400%, cover;
  background-blend-mode: overlay;
  filter: brightness(1.1) contrast(1.1) saturate(1.2);
  mix-blend-mode: color-dodge;
}
.fx-holo .holo-card__shine::after {
  background-image: radial-gradient(farthest-corner circle at var(--pointer-x) var(--pointer-y),
    hsla(0, 0%, 90%, 0.8) 0%, hsla(0, 0%, 78%, 0.1) 25%, hsl(0, 0%, 0%) 90%);
  background-position: center center;
  background-size: cover;
  mix-blend-mode: luminosity;
  filter: brightness(0.6) contrast(4);
}
.fx-holo .holo-card__glare { opacity: calc(var(--card-opacity) * 0.8); filter: brightness(0.8) contrast(1.5); }

/* ============ V (rare holo v) ============ */
.fx-v .holo-card__shine {
  filter: brightness(0.8) contrast(2.95) saturate(0.65);
  background-image: var(--grain),
    repeating-linear-gradient(0deg, var(--sp-1) 5%, var(--sp-2) 10%, var(--sp-3) 15%, var(--sp-4) 20%, var(--sp-5) 25%, var(--sp-6) 30%, var(--sp-1) 35%),
    repeating-linear-gradient(133deg, #0e152e 0%, hsl(180,10%,60%) 3.8%, hsl(180,29%,66%) 4.5%, hsl(180,10%,60%) 5.2%, #0e152e 10%, #0e152e 12%),
    radial-gradient(farthest-corner circle at var(--pointer-x) var(--pointer-y), hsla(0,0%,0%,0.1) 12%, hsla(0,0%,0%,0.15) 20%, hsla(0,0%,0%,0.25) 120%);
  background-blend-mode: screen, hue, hard-light;
  background-size: 500px 100%, 200% 700%, 300% 100%, 200% 100%;
  background-position: center, 0% var(--background-y), var(--background-x) var(--background-y), var(--background-x) var(--background-y);
}
.fx-v .holo-card__glare {
  background-image: radial-gradient(farthest-corner circle at var(--pointer-x) var(--pointer-y),
    hsl(0, 0%, 100%) 0%, hsla(210, 3%, 54%, 0.33) 45%, hsla(0, 0%, 20%, 0.9) 130%);
  opacity: calc(var(--card-opacity) * 0.5);
  mix-blend-mode: hard-light;
  filter: brightness(0.9) contrast(1.75);
}

/* ============ ULTRA / VMAX / VSTAR (full art) + SHINY ============ */
.fx-ultra .holo-card__shine,
.fx-shiny .holo-card__shine {
  background-image: var(--foil-illusion),
    repeating-linear-gradient(0deg, var(--sp-1) 5%, var(--sp-2) 10%, var(--sp-3) 15%, var(--sp-4) 20%, var(--sp-5) 25%, var(--sp-6) 30%, var(--sp-1) 35%),
    repeating-linear-gradient(133deg, #0e152e 0%, hsl(180,10%,60%) 3.8%, hsl(180,29%,66%) 4.5%, hsl(180,10%,60%) 5.2%, #0e152e 10%, #0e152e 12%),
    radial-gradient(farthest-corner circle at var(--pointer-x) var(--pointer-y), hsla(0,0%,0%,0.1) 12%, hsla(0,0%,0%,0.15) 20%, hsla(0,0%,0%,0.25) 120%);
  background-size: 33%, 200% 700%, 300% 100%, 200% 100%;
  background-position: center center, 0% var(--background-y), var(--background-x) var(--background-y), var(--background-x) var(--background-y);
  background-blend-mode: exclusion, hue, hard-light;
  filter: brightness(calc((var(--pointer-from-center) * 0.3) + 0.35)) contrast(2) saturate(1.5);
}
.fx-ultra .holo-card__glare,
.fx-shiny .holo-card__glare {
  background-image: radial-gradient(farthest-corner circle at var(--pointer-x) var(--pointer-y),
    hsl(0, 0%, 75%) 5%, hsl(200, 5%, 35%) 60%, hsl(320, 40%, 10%) 150%);
  mix-blend-mode: hard-light;
  filter: brightness(1) contrast(1.2) saturate(1);
  opacity: calc(var(--card-opacity) * 0.75);
}

/* ============ RAINBOW (rare rainbow) ============ */
.fx-rainbow .holo-card__shine {
  --r1: hsl(0, 57%, 37%); --r2: hsl(40, 53%, 39%); --r3: hsl(90, 60%, 35%);
  --r4: hsl(180, 60%, 35%); --r5: hsl(180, 60%, 35%); --r6: hsl(210, 57%, 39%); --r7: hsl(280, 55%, 31%);
  background-image: linear-gradient(-45deg, var(--r1), var(--r5)), var(--glitter),
    linear-gradient(-30deg, var(--r1), var(--r2), var(--r3), var(--r4), var(--r5), var(--r6), var(--r7),
      var(--r1), var(--r2), var(--r3), var(--r4), var(--r5), var(--r6), var(--r7));
  background-blend-mode: luminosity, soft-light;
  background-size: 200% 200%, 25% 25%, 400% 400%;
  background-position: calc(25% + (50% * var(--pointer-from-left))) calc(25% + (50% * var(--pointer-from-top))),
    center center, calc(25% + (var(--pointer-x) / 2)) calc(25% + (var(--pointer-y) / 2));
  filter: brightness(calc((var(--pointer-from-center) * 0.25) + 0.6)) contrast(2.2) saturate(0.9);
}
.fx-rainbow .holo-card__shine::after {
  background-image: var(--foil-illusion-mask);
  background-size: 33%;
  background-position: center center;
  filter: brightness(2.5);
  opacity: calc((var(--pointer-from-center) + 0.4) * 0.6);
  mix-blend-mode: darken;
}
.fx-rainbow .holo-card__glare {
  background-image: radial-gradient(farthest-corner circle at var(--pointer-x) var(--pointer-y),
    hsl(0, 0%, 80%), hsla(187, 10%, 85%, 0.25) 30%, hsl(197, 6%, 25%) 120%);
  filter: brightness(0.9) contrast(1.75);
  opacity: calc(var(--pointer-from-center) * 0.9);
  mix-blend-mode: hard-light;
}

/* ============ SECRET (rare secret, gold) ============ */
.fx-secret .holo-card__shine {
  background-image: var(--glitter), var(--glitter),
    conic-gradient(var(--sp-4), var(--sp-5), var(--sp-6), var(--sp-1), var(--sp-4)),
    radial-gradient(farthest-corner circle at var(--pointer-x) var(--pointer-y),
      hsla(150, 0%, 0%, 0.98) 10%, hsla(0, 0%, 95%, 0.15) 90%);
  background-size: 25% 25%, 25% 25%, cover, cover;
  background-position: 45% 45%, 55% 55%, center center, center center;
  background-blend-mode: soft-light, hard-light, overlay;
  mix-blend-mode: color-dodge;
  filter: brightness(calc(0.4 + (var(--pointer-from-center) * 0.2))) contrast(1) saturate(2.7);
}
.fx-secret .holo-card__shine::before {
  background-image: var(--foil-geometric), linear-gradient(45deg, hsl(46, 95%, 50%), hsl(52, 100%, 69%)),
    radial-gradient(farthest-corner circle at var(--pointer-x) var(--pointer-y),
      hsla(10, 20%, 90%, 0.95) 10%, hsl(0, 0%, 0%) 70%);
  background-size: 33%, cover, cover;
  background-position: center center, center center, center center;
  background-blend-mode: hard-light, multiply;
  mix-blend-mode: lighten;
  filter: brightness(1.25) contrast(1.25) saturate(0.35);
  opacity: 0.8;
}
.fx-secret .holo-card__glare {
  background-image: radial-gradient(farthest-corner circle at var(--pointer-x) var(--pointer-y),
    hsla(45, 8%, 80%, 0.3) 0%, hsl(22, 15%, 12%) 180%);
  filter: brightness(1.3) contrast(1.5);
  mix-blend-mode: hard-light;
}

/* ============ AMAZING RARE ============ */
.fx-amazing .holo-card__shine {
  mask-image: linear-gradient(to bottom, black 0%, black 38%, transparent 55%);
  -webkit-mask-image: linear-gradient(to bottom, black 0%, black 38%, transparent 55%);
  background-image: var(--glitter), var(--glitter),
    radial-gradient(farthest-corner circle at var(--pointer-x) var(--pointer-y),
      hsla(150, 20%, 10%, 1) 10%, hsla(177, 22%, 80%, 0.1) 50%, hsla(0, 0%, 95%, 0.98) 90%);
  background-size: 25% 25%, 25% 25%, cover;
  background-position: 40% 45%, 55% 55%, center center;
  background-blend-mode: soft-light, color-burn;
  filter: brightness(1) contrast(1) saturate(0.9);
}
.fx-amazing .holo-card__shine::after {
  background-image: repeating-linear-gradient(133deg,
    var(--sp-1) 5%, var(--sp-2) 10%, var(--sp-3) 15%, var(--sp-4) 20%, var(--sp-5) 25%, var(--sp-6) 30%, var(--sp-1) 35%);
  background-size: 400% 800%;
  background-position: calc(50% + (50% - var(--background-x)) * 3) calc(50% + (50% - var(--background-y)) * 3);
  filter: brightness(calc(0.75 - (var(--pointer-from-center) * 0.5))) contrast(1) saturate(1);
  mix-blend-mode: saturation;
}
.fx-amazing .holo-card__glare {
  background-image: radial-gradient(farthest-corner circle at var(--pointer-x) var(--pointer-y),
    hsla(0, 0%, 100%, 1) 10%, hsla(0, 0%, 100%, 0.85) 20%, hsla(0, 0%, 0%, 0.35) 90%);
  mix-blend-mode: multiply;
}

/* ============ RADIANT RARE ============ */
.fx-radiant .holo-card__shine {
  --barwidth: 1.2%;
  background-image: radial-gradient(farthest-corner ellipse at calc((var(--pointer-x) * 0.5) + 25%) calc((var(--pointer-y) * 0.5) + 25%),
      hsl(0, 0%, 95%) 20%, hsl(175, 100%, 90%) 130%),
    repeating-linear-gradient(45deg, hsl(0,0%,10%) 0%, hsl(0,0%,20%) var(--barwidth), hsl(0,0%,35%) calc(var(--barwidth)*2), hsl(0,0%,10%) calc(var(--barwidth)*4)),
    repeating-linear-gradient(-45deg, hsl(0,0%,10%) 0%, hsl(0,0%,20%) var(--barwidth), hsl(0,0%,35%) calc(var(--barwidth)*2), hsl(0,0%,10%) calc(var(--barwidth)*4));
  background-size: cover, 210% 210%, 210% 210%;
  background-position: center,
    calc(((var(--background-x) - 50%) * 1.5) + 50%) calc(((var(--background-y) - 50%) * 1.5) + 50%),
    calc(((var(--background-x) - 50%) * 1.5) + 50%) calc(((var(--background-y) - 50%) * 1.5) + 50%);
  background-blend-mode: exclusion, darken;
  filter: brightness(0.5) contrast(2) saturate(1.75);
  mix-blend-mode: color-dodge;
}
.fx-radiant .holo-card__shine::after {
  background-image: var(--foil-trainerbg), repeating-linear-gradient(55deg,
    hsl(3,95%,85%) 5%, hsl(207,100%,84%) 10%, hsl(29,100%,85%) 15%, hsl(160,100%,86%) 20%, hsl(309,94%,87%) 25%, hsl(188,95%,85%) 30%, hsl(3,95%,85%) 35%);
  background-size: 25%, 400% 100%;
  background-position: center, calc(((var(--background-x) - 50%) * -2.5) + 50%) calc(((var(--background-y) - 50%) * -2.5) + 50%);
  filter: brightness(0.6) contrast(3) saturate(2);
  mix-blend-mode: color-dodge;
}
.fx-radiant .holo-card__glare {
  background-image: radial-gradient(farthest-corner circle at var(--pointer-x) var(--pointer-y),
    hsla(0, 0%, 100%, 0.33) 0%, hsl(0, 0%, 25%) 110%);
  filter: brightness(1) contrast(1.5);
  mix-blend-mode: hard-light;
}

/* ============ COSMOS (rare holo cosmos) ============ */
.fx-cosmos .holo-card__shine {
  mask-image: linear-gradient(to bottom, black 0%, black 38%, transparent 55%);
  -webkit-mask-image: linear-gradient(to bottom, black 0%, black 38%, transparent 55%);
  background-image: var(--cosmos-bottom),
    repeating-linear-gradient(82deg, hsl(53,65%,60%) 4%, hsl(93,56%,50%) 8%, hsl(176,54%,49%) 12%, hsl(228,59%,55%) 16%, hsl(283,60%,55%) 20%, hsl(326,59%,51%) 24%, hsl(326,59%,51%) 28%, hsl(283,60%,55%) 32%, hsl(228,59%,55%) 36%, hsl(176,54%,49%) 40%, hsl(93,56%,50%) 44%, hsl(53,65%,60%) 48%),
    radial-gradient(farthest-corner circle at var(--pointer-x) var(--pointer-y), hsla(180,100%,89%,0.5) 5%, hsla(180,14%,57%,0.3) 40%, hsl(0,0%,0%) 130%);
  background-blend-mode: color-burn, multiply;
  background-position: var(--cosmosbg), calc(10% + (var(--pointer-from-left) * 80%)) calc(10% + (var(--pointer-from-top) * 80%)), center center;
  background-size: cover, 400% 900%, cover;
  filter: brightness(1) contrast(1) saturate(0.8);
  mix-blend-mode: color-dodge;
}
.fx-cosmos .holo-card__shine::before {
  background-image: var(--cosmos-middle),
    repeating-linear-gradient(82deg, hsl(53,65%,60%) 4%, hsl(93,56%,50%) 8%, hsl(176,54%,49%) 12%, hsl(228,59%,55%) 16%, hsl(283,60%,55%) 20%, hsl(326,59%,51%) 24%, hsl(326,59%,51%) 28%, hsl(283,60%,55%) 32%, hsl(228,59%,55%) 36%, hsl(176,54%,49%) 40%, hsl(93,56%,50%) 44%, hsl(53,65%,60%) 48%);
  background-blend-mode: lighten, multiply;
  background-position: var(--cosmosbg), calc(15% + (var(--pointer-from-left) * 70%)) calc(15% + (var(--pointer-from-top) * 70%));
  background-size: cover, 400% 900%;
  filter: brightness(1.25) contrast(1.75) saturate(0.8);
  mix-blend-mode: overlay;
}
.fx-cosmos .holo-card__shine::after {
  background-image: var(--cosmos-top),
    repeating-linear-gradient(82deg, hsl(53,65%,60%) 4%, hsl(93,56%,50%) 8%, hsl(176,54%,49%) 12%, hsl(228,59%,55%) 16%, hsl(283,60%,55%) 20%, hsl(326,59%,51%) 24%, hsl(326,59%,51%) 28%, hsl(283,60%,55%) 32%, hsl(228,59%,55%) 36%, hsl(176,54%,49%) 40%, hsl(93,56%,50%) 44%, hsl(53,65%,60%) 48%);
  background-blend-mode: multiply, multiply;
  background-position: var(--cosmosbg), calc(20% + (var(--pointer-from-left) * 60%)) calc(20% + (var(--pointer-from-top) * 60%));
  background-size: cover, 400% 900%;
  filter: brightness(1.25) contrast(1.75) saturate(0.8);
  mix-blend-mode: multiply;
}
.fx-cosmos .holo-card__glare {
  background-image: radial-gradient(farthest-corner circle at var(--pointer-x) var(--pointer-y), hsla(204,100%,95%,0.8) 5%, hsla(250,15%,20%,1) 150%);
  filter: brightness(0.75) contrast(2) saturate(2);
  mix-blend-mode: overlay;
  opacity: calc(var(--card-opacity) * (0.25 + var(--pointer-from-center)));
}

/* ============ TRAINER GALLERY HOLO ============ */
.fx-tg-holo .holo-card__shine {
  mask-image: linear-gradient(to bottom, black 0%, black 70%, transparent 92%);
  -webkit-mask-image: linear-gradient(to bottom, black 0%, black 70%, transparent 92%);
  background-image: repeating-linear-gradient(-22deg,
    hsla(283, 49%, 60%, 0.75) 5%, hsla(2, 74%, 59%, 0.75) 10%, hsla(53, 67%, 53%, 0.75) 15%,
    hsla(93, 56%, 52%, 0.75) 20%, hsla(176, 38%, 50%, 0.75) 25%, hsla(228, 100%, 77%, 0.75) 30%,
    hsla(283, 49%, 61%, 0.75) 35%);
  background-blend-mode: color-dodge;
  background-size: 300% 400%;
  background-position: 0% var(--background-y), var(--background-x) var(--background-y);
  filter: brightness(calc((var(--pointer-from-center) * 0.3) + 0.5)) contrast(2.3) saturate(1);
}
.fx-tg-holo .holo-card__shine::after {
  background-image: radial-gradient(farthest-corner ellipse at calc((var(--pointer-x) * 0.5) + 25%) calc((var(--pointer-y) * 0.5) + 25%),
    hsl(0, 0%, 100%) 5%, hsla(300, 100%, 11%, 0.6) 40%, hsl(0, 0%, 22%) 120%);
  background-position: center center;
  background-size: 400% 500%;
  filter: brightness(calc((var(--pointer-from-center) * 0.2) + 0.4)) contrast(0.85) saturate(1.1);
  mix-blend-mode: hard-light;
}
.fx-tg-holo .holo-card__glare {
  background-image: radial-gradient(farthest-corner circle at var(--pointer-x) var(--pointer-y),
    hsla(0, 0%, 100%, 1) 10%, hsla(0, 0%, 100%, 0.6) 35%, hsla(180, 11%, 35%, 1) 60%);
  mix-blend-mode: soft-light;
}

/* ============ TRAINER FULL ART (supporter + rare ultra) ============ */
.fx-trainer-ultra .holo-card__shine {
  background-image: var(--foil-trainerbg),
    repeating-linear-gradient(0deg, var(--sp-1) 5%, var(--sp-2) 10%, var(--sp-3) 15%, var(--sp-4) 20%, var(--sp-5) 25%, var(--sp-6) 30%, var(--sp-1) 35%),
    repeating-linear-gradient(133deg, #0e152e 0%, hsl(180,10%,60%) 3.8%, hsl(180,29%,66%) 4.5%, hsl(180,10%,60%) 5.2%, #0e152e 10%, #0e152e 12%),
    radial-gradient(farthest-corner circle at var(--pointer-x) var(--pointer-y), hsla(0,0%,0%,0.1) 12%, hsla(0,0%,0%,0.15) 20%, hsla(0,0%,0%,0.25) 120%);
  background-size: 20%, 200% 700%, 300% 100%, 200% 100%;
  background-position: center center, 0% var(--background-y), var(--background-x) var(--background-y), var(--background-x) var(--background-y);
  background-blend-mode: color-burn, hue, hard-light;
  filter: brightness(calc((var(--pointer-from-center) * 0.05) + 0.6)) contrast(1.5) saturate(1.2);
}
.fx-trainer-ultra .holo-card__shine::after {
  background-image: radial-gradient(farthest-corner circle at var(--pointer-x) var(--pointer-y),
    hsl(0, 0%, 100%) 0%, hsla(0, 0%, 0%, 0) 80%);
  mix-blend-mode: screen;
  opacity: 0.5;
}
.fx-trainer-ultra .holo-card__glare {
  opacity: calc(var(--card-opacity) * 0.75);
  mix-blend-mode: multiply;
  filter: brightness(1.5) contrast(1.4) saturate(1);
  background-size: 170% 170%;
}

.backdrop-enter-active, .backdrop-leave-active { transition: opacity 0.3s ease; }
.backdrop-enter-from, .backdrop-leave-to { opacity: 0; }
</style>
