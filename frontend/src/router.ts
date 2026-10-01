import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import CardDetail from './views/CardDetail.vue'
import About from './views/About.vue'
import TopSelling from './views/TopSelling.vue'
import RecentSales from './views/RecentSales.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home },
    { path: '/cards/:id', component: CardDetail, props: true },
    { path: '/sobre', component: About },
    { path: '/mais-vendidas', component: TopSelling },
    { path: '/ultimas-vendas', component: RecentSales },
  ],
})
