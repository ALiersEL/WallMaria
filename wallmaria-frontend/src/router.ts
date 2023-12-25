// router.ts
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'HomePage',
        component: () => import('./pages/HomePage.vue'),
    },
    {
        path: '/about',
        component: () => import('./pages/About.vue'),
    },
    {
        path: '/search',
        name: 'SearchResults',
        component: () => import('./pages/SearchResults.vue'), 
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
