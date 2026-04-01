import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css' // Your Tailwind v4 import is in here
import App from './App.vue'

// Import your View components
import Leaderboard from './views/Leaderboard.vue'
import Rules from './views/Rules.vue'
import Messages from './views/Messages.vue'
import Profile from './views/Profile.vue'

// Define your routes
const routes = [
  { path: '/', component: Leaderboard },
  { path: '/rules', component: Rules },
  { path: '/messages', component: Messages },
  { path: '/profile', component: Profile }
]

// Create the router instance
const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Create and mount the Vue app
const app = createApp(App)
app.use(router)
app.mount('#app')
