
import { createRouter, createWebHistory } from 'vue-router'

// Import your page components
import HomeComponent from './pages/HomeComponent.vue'
import LoginComponent from './pages/auth/LoginComponent.vue'
import RegisterComponent from './pages/auth/RegisterComponent.vue'
import AuthCommon from './pages/auth/AuthCommon.vue'

const routes = [
    {   path: '/', name: 'Home', component: HomeComponent, meta: { requiresAuth: true } },
    {
        path: '/auth',
        component: AuthCommon,
        children: [
            { path: '', name: 'AuthLogin', component: LoginComponent }, // default child
            { path: 'register', name: 'AuthRegister', component: RegisterComponent }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Global route guard for all protected routes
router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        const token = localStorage.getItem('auth_token')
        if (!token) {
            next({ name: 'AuthLogin' })
        } else {
            next()
        }
    } else {
        next()
    }
})


export default router
