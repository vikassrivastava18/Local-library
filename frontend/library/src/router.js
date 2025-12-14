
import { createRouter, createWebHistory } from 'vue-router'

// Import your page components
import HomeComponent from './pages/home/HomeComponent.vue'

const routes = [
    // Router for home page
    { path: '/', name: 'Home', component: HomeComponent, meta: { requiresAuth: true } },
    // Router for authntication
    { path: '/auth',
        component: () => import('./pages/auth/AuthCommon.vue'),
        children: [
            {path: '', // default child
             name: 'AuthLogin',
             component: () => import('./pages/auth/LoginComponent.vue')
            }, 
            {path: 'register',
             name: 'AuthRegister',
             component: () => import('./pages/auth/RegisterComponent.vue')
            }
        ]
    },
    // Router for books
    {path: '/books/:id',
     name: 'BookDetail',
     component: () => import('./pages/books/BookDetailComponent.vue'),
     meta: { requiresAuth: true }
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
