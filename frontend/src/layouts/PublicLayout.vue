<template>
  <div class="public-layout">
    <nav class="navbar">
      <div class="nav-brand">
        <router-link to="/">Fixrify</router-link>
      </div>
      
      <div class="nav-menu">
        <router-link to="/services">Services</router-link>
        <router-link to="/about">About</router-link>
        <router-link to="/contact">Contact</router-link>
        <router-link to="/login" class="btn btn-outline-primary">Login</router-link>
        <router-link to="/register" class="btn btn-outline-primary">Register</router-link>
      </div>
    </nav>

    <main class="public-content">
      <router-view/>
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
export default {
  name: 'PublicLayout'
}
</script>

<style scoped>
.public-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.public-content {
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

.nav-menu .btn {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: 500;
  text-decoration: none;
}

.nav-menu .btn-primary {
  background: #007bff;
  color: white;
  border: 1px solid #007bff;
}

.nav-menu .btn-outline-primary {
  background: transparent;
  color: #007bff;
  border: 1px solid #007bff;
}

.nav-menu .btn-primary:hover {
  background: #0056b3;
  border-color: #0056b3;
}

.nav-menu .btn-outline-primary:hover {
  background: #007bff;
  color: white;
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