// frontend/src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'; // New imports for Vue Router 4

import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import TaskView from '../views/TaskView.vue';
import ProfileView from '../views/ProfileView.vue';

const routes = [
  {
    path: '/',
    redirect: '/tasks',
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
  },
  {
    path: '/tasks',
    name: 'Tasks',
    component: TaskView,
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView,
    meta: { requiresAuth: true },
  },
];

// Use createWebHistory for history mode (clean URLs)
const router = createRouter({
  history: createWebHistory(), // New way to define history mode
  routes,
});

// Navigation guard remains similar but no longer uses Vue.router property
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('access_token');

  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    console.log('Access denied: Route requires authentication.');
    next('/login');
  } else {
    next();
  }
});

export default router;