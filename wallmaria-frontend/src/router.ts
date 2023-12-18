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
        path: '/search-results',
        name: 'ImageSearchResults',
        component: () => import('./pages/ImageSearchResults.vue'), // Ensure you have this Vue file created
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
