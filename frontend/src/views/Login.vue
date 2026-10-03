<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import logo from '../assets/logo.png'

const router = useRouter()
const user = ref('')
const pass = ref('')
const error = ref('')

function submit() {
  if (user.value === 'admin' && pass.value === 'teste123') {
    sessionStorage.setItem('pokemarket_auth', '1')
    router.push('/')
  } else {
    error.value = 'Usuário ou senha inválidos.'
  }
}
</script>

<template>
  <div class="min-h-screen bg-ink flex items-center justify-center px-4">
    <form @submit.prevent="submit" class="w-full max-w-sm bg-graphite border border-border rounded-xl p-6 space-y-4">
      <img :src="logo" alt="CardTracker" class="h-12 w-auto mx-auto" />
      <div>
        <label class="block text-sm text-zinc-400 mb-1">Usuário</label>
        <input v-model="user" type="text" autocomplete="username"
          class="w-full bg-graphite-light border border-border rounded-lg px-3 py-2 text-sm outline-none focus:border-accent" />
      </div>
      <div>
        <label class="block text-sm text-zinc-400 mb-1">Senha</label>
        <input v-model="pass" type="password" autocomplete="current-password"
          class="w-full bg-graphite-light border border-border rounded-lg px-3 py-2 text-sm outline-none focus:border-accent" />
      </div>
      <p v-if="error" class="text-sm text-accent">{{ error }}</p>
      <button type="submit"
        class="w-full bg-accent hover:bg-accent-soft transition rounded-lg py-2 text-sm font-medium">
        Entrar
      </button>
    </form>
  </div>
</template>
