<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1>Create Account</h1>
        <p>Join our platform today</p>
      </div>

      <form class="auth-form" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Full Name</label>
          <input 
            v-model="form.name" 
            type="text" 
            required 
            placeholder="Enter your full name"
          />
        </div>

        <div class="form-group">
          <label>Email</label>
          <input 
            v-model="form.email" 
            type="email" 
            required 
            placeholder="Enter your email"
          />
        </div>

        <div class="form-group">
          <label>Phone</label>
          <input 
            v-model="form.phone" 
            type="tel" 
            required 
            placeholder="Enter your phone number"
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input 
            v-model="form.password" 
            type="password" 
            required 
            placeholder="Create a password"
          />
        </div>

        <div class="form-group">
          <label>Confirm Password</label>
          <input 
            v-model="form.confirmPassword" 
            type="password" 
            required 
            placeholder="Confirm your password"
          />
        </div>

        <div class="form-group">
          <label>Account Type</label>
          <div class="role-selector">
            <button 
              type="button"
              :class="['role-btn', { active: form.role === 'customer' }]"
              @click="form.role = 'customer'"
            >
              Customer
            </button>
            <button 
              type="button"
              :class="['role-btn', { active: form.role === 'professional' }]"
              @click="form.role = 'professional'"
            >
              Service Professional
            </button>
          </div>
        </div>

        <!-- Professional-specific fields -->
        <template v-if="form.role === 'professional'">
          <div class="form-group">
            <label>Services Offered</label>
            <div class="services-grid">
              <div 
                v-for="service in availableServices" 
                :key="service"
                :class="['service-option', { selected: selectedServices.includes(service) }]"
                @click="toggleService(service)"
              >
                {{ service }}
              </div>
            </div>
          </div>

          <div class="form-group">
            <label>Years of Experience</label>
            <input 
              v-model="form.experience" 
              type="number" 
              min="0" 
              required 
              placeholder="Enter years of experience"
            />
          </div>

          <div class="form-group">
            <label>About</label>
            <textarea 
              v-model="form.about" 
              rows="4" 
              required 
              placeholder="Tell us about your experience and expertise"
            ></textarea>
          </div>
        </template>

        <div class="form-actions">
          <button type="submit" class="btn-primary" :disabled="loading || !isFormValid">
            {{ loading ? 'Creating Account...' : 'Create Account' }}
          </button>
        </div>

        <div class="auth-links">
          <router-link to="/login">Already have an account? Sign in</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { authAPI, servicesAPI } from '@/services/api';

export default {
  name: 'Register',
  data() {
    return {
      form: {
        name: '',
        email: '',
        phone: '',
        password: '',
        confirmPassword: '',
        role: 'customer',
        experience: '',
        about: ''
      },
      selectedServices: [],
      availableServices: [],
      loading: false
    };
  },
  computed: {
    isFormValid() {
      const { password, confirmPassword, role } = this.form;
      if (password !== confirmPassword) return false;
      if (role === 'professional') {
        return this.selectedServices.length > 0 && this.form.experience && this.form.about;
      }
      return true;
    }
  },
  created() {
    this.loadServices();
  },
  methods: {
    async loadServices() {
      try {
        const response = await servicesAPI.getCategories();
        this.availableServices = response.data;
      } catch (error) {
        console.error('Error loading services:', error);
        this.$toast.error('Failed to load available services');
      }
    },
    toggleService(service) {
      const index = this.selectedServices.indexOf(service);
      if (index === -1) {
        this.selectedServices.push(service);
      } else {
        this.selectedServices.splice(index, 1);
      }
    },
    async handleSubmit() {
      if (this.form.password !== this.form.confirmPassword) {
        this.$toast.error('Passwords do not match');
        return;
      }

      this.loading = true;
      try {
        const registrationData = {
          name: this.form.name,
          email: this.form.email,
          phone: this.form.phone,
          password: this.form.password,
          role: this.form.role
        };

        if (this.form.role === 'professional') {
          registrationData.services = this.selectedServices;
          registrationData.experience = parseInt(this.form.experience);
          registrationData.about = this.form.about;
        }

        const response = await authAPI.register(registrationData);
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('refreshToken', response.data.refresh_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));

        this.$toast.success('Account created successfully!');
        
        // Redirect based on role
        if (this.form.role === 'customer') {
          this.$router.push('/customer/dashboard');
        } else {
          this.$router.push('/professional/dashboard');
        }
      } catch (error) {
        console.error('Registration error:', error);
        this.$toast.error(error.response?.data?.message || 'Failed to create account');
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
  padding: 2rem;
}

.auth-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
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

.form-group input,
.form-group textarea {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.role-selector {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.role-btn {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
}

.role-btn.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.5rem;
}

.service-option {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  text-align: center;
  transition: all 0.2s;
}

.service-option.selected {
  background: #007bff;
  color: white;
  border-color: #007bff;
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