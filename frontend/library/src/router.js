
import { createRouter, createWebHistory } from 'vue-router'

// Import your page components
import HomeComponent from './pages/HomeComponent.vue'
import LoginComponent from './pages/auth/LoginComponent.vue'
import RegisterComponent from './pages/auth/RegisterComponent.vue'

const routes = [
    { path: '/', name: 'Home', component: HomeComponent },
    { path: '/login', name: 'Login', component: LoginComponent },
    { path: '/register', name: 'Register', component: RegisterComponent }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
