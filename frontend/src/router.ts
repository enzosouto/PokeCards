import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import CardDetail from './views/CardDetail.vue'
import About from './views/About.vue'
import TopSelling from './views/TopSelling.vue'
import RecentSales from './views/RecentSales.vue'
import Login from './views/Login.vue'
import PokedexView from './views/PokedexView.vue'
import PokedexDetailView from './views/PokedexDetailView.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: Login },
    { path: '/', component: Home },
    { path: '/cards/:id', component: CardDetail, props: true },
    { path: '/sobre', component: About },
    { path: '/mais-vendidas', component: TopSelling },
    { path: '/ultimas-vendas', component: RecentSales },
    { path: '/pokedex', component: PokedexView },
    { path: '/pokedex/:id', component: PokedexDetailView, props: true },
  ],
})

router.beforeEach((to) => {
  const authed = sessionStorage.getItem('pokemarket_auth') === '1'
  if (to.path !== '/login' && !authed) return '/login'
  if (to.path === '/login' && authed) return '/'
})
