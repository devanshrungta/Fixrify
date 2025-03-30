<template>
  <div class="dashboard-layout">
    <nav class="navbar">
      <div class="nav-brand">
        <router-link to="/">Fixrify</router-link>
      </div>
      
      <div class="nav-menu">
        <template v-if="userRole === 'customer'">
          <router-link to="/customer/dashboard">Dashboard</router-link>
          <router-link to="/customer/services">Services</router-link>
          <router-link to="/customer/requests">My Requests</router-link>
          <router-link to="/customer/profile">My Profile</router-link>
        </template>

        <template v-if="userRole === 'professional'">
          <router-link to="/professional/dashboard">Dashboard</router-link>
          <router-link to="/professional/requests">Service Requests</router-link>
          <router-link to="/professional/profile">Profile</router-link>
        </template>

        <template v-if="userRole === 'admin'">
          <router-link to="/admin/dashboard">Dashboard</router-link>
          <router-link to="/admin/services">Services</router-link>
          <router-link to="/admin/users">Users</router-link>
          <router-link to="/admin/reports">Reports</router-link>
        </template>

        <template v-if="userRole" >
          <a href="#" @click.prevent="handleLogout" class="btn btn-danger text-light">Logout</a>
        </template>

      </div>
    </nav>

    <main class="dashboard-content">
      <router-view />
    </main>

    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <h3>Fixrify</h3>
          <p>Your one-stop solution for home services</p>
        </div>
        <div class="footer-section">
          <h3>Quick Links</h3>
          <router-link to="/about">About Us</router-link>
          <router-link to="/contact">Contact</router-link>
          <router-link to="/privacy">Privacy Policy</router-link>
          <router-link to="/terms">Terms of Service</router-link>
        </div>
        <div class="footer-section">
          <h3>Contact Us</h3>
          <p>Email: support@fixrify.com</p>
          <p>Phone: (555) 123-4567</p>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; {{ new Date().getFullYear() }} Fixrify. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  name: 'DashboardLayout',
  data() {
    return {
      showDropdown: false
    }
  },
  computed: {
    ...mapState({
      user: state => state.auth.user
    }),
    ...mapGetters('auth', ['isAuthenticated']),
    userRole() {
      return this.user?.role
    },
    userName() {
      return this.user?.name
    },
    profileRoute() {
      switch (this.userRole) {
        case 'customer':
          return '/customer/profile'
        case 'professional':
          return '/professional/profile'
        case 'admin':
          return '/admin/profile'
        default:
          return '/profile'
      }
    }
  },
  created() {
    document.addEventListener('click', this.handleClickOutside)
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside)
  },
  methods: {
    ...mapActions('auth', ['logout']),
    toggleDropdown() {
      this.showDropdown = !this.showDropdown
    },
    async handleLogout() {
      await this.logout()
      this.$router.push('/login')
    },
    handleClickOutside(e) {
      if (!e.target.closest('.user-menu')) {
        this.showDropdown = false
      }
    }
  }
}
</script>

<style scoped>
.dashboard-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.dashboard-content {
  flex: 1;
  padding: 2rem;
  background: #f8f9fa;
}

/* Navbar styles */
.navbar {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand a {
  font-size: 1.5rem;
  font-weight: bold;
  color: #007bff;
  text-decoration: none;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-menu a {
  color: #333;
  text-decoration: none;
  font-weight: 500;
}

.nav-menu a:hover {
  color: #007bff;
}

.nav-menu a.router-link-active {
  color: #007bff;
}

/* User menu styles */
.user-menu {
  position: relative;
  cursor: pointer;
}

.user-name {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0.5rem 0;
  min-width: 150px;
  z-index: 1000;
}

.dropdown-menu a {
  display: block;
  padding: 0.5rem 1rem;
  color: #333;
  text-decoration: none;
}

.dropdown-menu a:hover {
  background: #f8f9fa;
}

/* Footer styles */
.footer {
  background: #333;
  color: white;
  padding: 3rem 2rem 1rem;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.footer-section h3 {
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.footer-section a {
  display: block;
  color: #ddd;
  text-decoration: none;
  margin-bottom: 0.5rem;
}

.footer-section a:hover {
  color: white;
}

.footer-bottom {
  text-align: center;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #444;
}

/* Responsive styles */
@media (max-width: 768px) {
  .navbar {
    padding: 1rem;
  }

  .nav-menu {
    gap: 1rem;
  }

  .nav-menu a {
    font-size: 0.875rem;
  }
}
</style> 