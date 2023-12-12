import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import CartView from '../views/CartView.vue'
import AdminSummaryView from '../views/AdminSummaryView.vue'
import OrdersView from '../views/OrdersView.vue'
import SearchView from '../views/SearchView.vue'
import AdminApprovalView from '../views/AdminApprovalView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/cart',
      name: 'cart',
      component: CartView
    },
    {
      path: '/summary',
      name: 'summary',
      component: AdminSummaryView
    },
    {
      path: '/orders',
      name: 'orders',
      component: OrdersView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/approve',
      name: 'approve',
      component: AdminApprovalView
    }
  ]
})

export default router
