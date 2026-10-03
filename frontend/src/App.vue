<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import logo from './assets/logo.png'
import BottomNav from './components/BottomNav.vue'
import IntroScrub from './components/IntroScrub.vue'
import CurrencyToggle from './components/CurrencyToggle.vue'

const showIntro = ref(!localStorage.getItem('pokemarket_intro_seen'))
const route = useRoute()
const isLogin = computed(() => route.path === '/login')
</script>

<template>
  <IntroScrub v-if="showIntro" @done="showIntro = false" />

  <div v-show="isLogin || !showIntro" class="min-h-screen bg-ink">
    <header v-if="!isLogin" class="sticky top-0 z-30 border-b border-border bg-ink/90 backdrop-blur">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 py-3 sm:py-4 flex items-center justify-between gap-6">
        <RouterLink to="/">
          <img :src="logo" alt="PokéMarket" class="h-10 sm:h-14 w-auto" />
        </RouterLink>
        <nav class="hidden md:flex items-center gap-6 text-sm font-medium text-zinc-400">
          <RouterLink to="/mais-vendidas" class="hover:text-white transition"
            >Mais vendidas</RouterLink
          >
          <RouterLink to="/ultimas-vendas" class="hover:text-white transition"
            >Últimas vendas</RouterLink
          >
          <RouterLink to="/pokedex" class="hover:text-white transition">Pokédex</RouterLink>
          <RouterLink to="/sobre" class="hover:text-white transition">Sobre</RouterLink>
        </nav>
        <CurrencyToggle />
      </div>
    </header>
    <RouterView />
    <BottomNav v-if="!isLogin" />
  </div>
</template>

<style scoped>
nav a.router-link-active {
  color: #f4f4f5;
}
</style>
