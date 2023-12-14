import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import CartView from '../views/CartView.vue'
import AdminSummaryView from '../components/admin/AdminSummaryView.vue'
import OrdersView from '../views/OrdersView.vue'
import SearchView from '../views/SearchView.vue'
import AdminApprovalView from '../components/admin/AdminApprovalView.vue'
import axios from 'axios';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      beforeEnter: (to, from, next) => {
        const userSession = JSON.parse(localStorage.getItem("userSession"));
        console.log("User Session:", userSession);

        if (userSession) {
          axios.defaults.headers.common["Authorization"] = `Bearer ${userSession.token}`;
          try {
            axios
            .get('http://localhost:1430/api/role')
            .then((response)=>response)
            .then((response)=>response.data)
            .then((response)=>{

              const role=response['role'];

              if (role === 'admin') {
                console.log("Loading AdminDashboard.vue");
                import('../components/admin/AdminDashboard.vue').then(module => {
                  to.matched[0].components = { default: module.default };
                  next();
                });
              } else if (role === 'manager') {
                console.log("Loading ManagerDashboard.vue");
                import('../components/manager/ManagerDashboard.vue').then(module => {
                  to.matched[0].components = { default: module.default };
                  next();
                });
              } else {
                console.log("Loading UserDashboard.vue");
                import('../components/user/UserDashboard.vue').then(module => {
                  to.matched[0].components = { default: module.default };
                  next();
                });
              }
            
            })
            
            } catch (error) {
            console.error("Error fetching role:", error);
            }
        }
        else {
          console.log("No session or role, redirecting to login");
          next('/login');
        }

        
      }      
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
    },
    {
      path: '/logout',
      name: 'logout',
      beforeEnter: (to, from, next) => {
        localStorage.removeItem("userSession");
        next('/login');
      }
    }
  ]
})

export default router
