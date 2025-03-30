import { createRouter, createWebHistory } from 'vue-router'

// Layout components
import PublicLayout from '../layouts/PublicLayout.vue'
import DashboardLayout from '../layouts/DashboardLayout.vue'

// Auth components
import Login from '../views/auth/Login.vue'
import Register from '../views/auth/Register.vue'
import AdminLogin from '../views/auth/AdminLogin.vue'

// Customer components
import CustomerDashboard from '../views/customer/Dashboard.vue'
import CustomerRequests from '../views/customer/Requests.vue'
import CustomerProfile from '../views/customer/Profile.vue'
import CustomerServices from '../views/customer/Services.vue'

// Professional components
import ProfessionalDashboard from '../views/professional/Dashboard.vue'
import ProfessionalRequests from '../views/professional/Requests.vue'
import ProfessionalProfile from '../views/professional/Profile.vue'

// Admin components
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import AdminServices from '../views/admin/Services.vue'
import AdminUsers from '../views/admin/Users.vue'
import AdminReports from '../views/admin/Reports.vue'

// Shared components
import Services from '../views/Services.vue'
import About from '../views/About.vue'
import Contact from '../views/Contact.vue'
import Privacy from '../views/Privacy.vue'
import Terms from '../views/Terms.vue'
import NotFound from '../views/NotFound.vue'
import Home from '../views/Home.vue'

const routes = [
  // Public routes
  {
    path: '/',
    component: PublicLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: Home,
        meta: { requiresGuest: true }
      },
      {
        path: 'login',
        name: 'Login',
        component: Login,
        meta: { requiresGuest: true }
      },
      {
        path: 'register',
        name: 'Register',
        component: Register,
        meta: { requiresGuest: true }
      },
      {
        path: 'admin/login',
        name: 'AdminLogin',
        component: AdminLogin,
        meta: { requiresGuest: true }
      },
      {
        path: 'services',
        name: 'Services',
        component: Services
      },
      {
        path: 'about',
        name: 'About',
        component: About
      },
      {
        path: 'contact',
        name: 'Contact',
        component: Contact
      },
      {
        path: 'privacy',
        name: 'Privacy',
        component: Privacy
      },
      {
        path: 'terms',
        name: 'Terms',
        component: Terms
      }
    ]
  },

  // Customer routes
  {
    path: '/customer',
    component: DashboardLayout,
    meta: { requiresAuth: true, role: 'customer' },
    children: [
      {
        path: 'dashboard',
        name: 'CustomerDashboard',
        component: CustomerDashboard
      },
      {
        path: 'services',
        name: 'CustomerServices',
        component: CustomerServices
      },
      {
        path: 'requests',
        name: 'CustomerRequests',
        component: CustomerRequests
      },
      {
        path: 'profile',
        name: 'CustomerProfile',
        component: CustomerProfile
      }
    ]
  },

  // Professional routes
  {
    path: '/professional',
    component: DashboardLayout,
    meta: { requiresAuth: true, role: 'professional' },
    children: [
      {
        path: 'dashboard',
        name: 'ProfessionalDashboard',
        component: ProfessionalDashboard
      },
      {
        path: 'requests',
        name: 'ProfessionalRequests',
        component: ProfessionalRequests
      },
      {
        path: 'profile',
        name: 'ProfessionalProfile',
        component: ProfessionalProfile
      }
    ]
  },

  // Admin routes
  {
    path: '/admin',
    component: DashboardLayout,
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: AdminDashboard
      },
      {
        path: 'services',
        name: 'AdminServices',
        component: AdminServices
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: AdminUsers
      },
      {
        path: 'reports',
        name: 'AdminReports',
        component: AdminReports
      }
    ]
  },

  // 404 route
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  const userRole = user.role

  // Routes that require guest access
  if (to.matched.some(record => record.meta.requiresGuest)) {
    if (token) {
      // Redirect to appropriate dashboard based on role
      switch (userRole) {
        case 'admin':
          return next('/admin/dashboard')
        case 'professional':
          return next('/professional/dashboard')
        case 'customer':
          return next('/customer/dashboard')
        default:
          return next('/services')
      }
    }
    return next()
  }

  // Routes that require authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      return next('/login')
    }

    // Check role requirements
    if (to.matched.some(record => record.meta.role)) {
      const requiredRole = to.matched.find(record => record.meta.role).meta.role
      if (userRole !== requiredRole) {
        // Redirect to appropriate dashboard based on actual role
        switch (userRole) {
          case 'admin':
            return next('/admin/dashboard')
          case 'professional':
            return next('/professional/dashboard')
          case 'customer':
            return next('/customer/dashboard')
          default:
            return next('/services')
        }
      }
    }
  }

  next()
})

export default router 