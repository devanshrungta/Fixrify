import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

// Import Bootstrap CSS and JS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// Import Font Awesome
import '@fortawesome/fontawesome-free/css/all.min.css'

// Configure axios defaults
axios.defaults.baseURL = process.env.VUE_APP_API_URL || 'http://localhost:5000'
axios.defaults.headers.common['Content-Type'] = 'application/json'

// // Add request interceptor for authentication
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// // Add response interceptor for error handling
// axios.interceptors.response.use(
//   response => response,
//   error => {
//     if (error.response?.status === 401) {
//       store.dispatch('auth/logout')
//       router.push('/login')
//     }
//     return Promise.reject(error)
//   }
// )

// Create Vue app instance
const app = createApp(App)

// Use plugins
app.use(router)
app.use(store)

// Global error handler
// app.config.errorHandler = (err, vm, info) => {
//   console.error('Global error:', err)
//   console.error('Error info:', info)
// }

// Check authentication status on app start
store.dispatch('auth/checkAuth').then(() => {
  app.mount('#app')
}).catch(error => {
  console.error('Auth check failed:', error)
  app.mount('#app')
}) 