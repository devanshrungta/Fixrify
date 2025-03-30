<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1>Admin Login</h1>
        <p>Access admin dashboard</p>
      </div>

      <form class="auth-form" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Email</label>
          <input 
            v-model="form.email" 
            type="email" 
            required 
            placeholder="Enter admin email"
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input 
            v-model="form.password" 
            type="password" 
            required 
            placeholder="Enter admin password"
          />
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-primary" :disabled="loading">
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </div>

        <div class="auth-links">
          <router-link to="/login">Back to user login</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { authAPI } from '@/services/api';

export default {
  name: 'AdminLogin',
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      loading: false
    };
  },
  methods: {
    async handleSubmit(event) {
      event.preventDefault(); // Explicitly prevent form submission
      if (this.loading) return; // Return early if already loading

      this.loading = true;
      try {
        const response = await authAPI.adminLogin({email : this.form.email, password : this.form.password});
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('refreshToken', response.data.refresh_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        
        this.$router.push('/admin/dashboard');
      } catch (error) {
        console.error('Admin login error:', error);
        this.$toast.error(error.response?.data?.message || 'Failed to sign in');
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  padding: 1rem;
}

.auth-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  padding: 2rem;
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-header h1 {
  font-size: 1.75rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.auth-header p {
  color: #666;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #333;
}

.form-group input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.form-actions {
  margin-top: 1rem;
}

.btn-primary {
  width: 100%;
  padding: 0.75rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-primary:not(:disabled):hover {
  background: #0056b3;
}

.auth-links {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1.5rem;
  text-align: center;
}

.auth-links a {
  color: #007bff;
  text-decoration: none;
}

.auth-links a:hover {
  text-decoration: underline;
}
</style> 