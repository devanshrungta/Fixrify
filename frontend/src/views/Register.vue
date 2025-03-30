<template>
  <div class="register">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-4">
          <div class="card shadow">
            <div class="card-body p-5">
              <h2 class="text-center mb-4">Register</h2>
              <form @submit.prevent="handleSubmit">
                <div class="mb-3">
                  <label for="name" class="form-label">Full Name</label>
                  <input
                    id="name"
                    v-model="form.name"
                    type="text"
                    class="form-control"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label for="email" class="form-label">Email</label>
                  <input
                    id="email"
                    v-model="form.email"
                    type="email"
                    class="form-control"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label for="phone" class="form-label">Phone Number</label>
                  <input
                    id="phone"
                    v-model="form.phone"
                    type="tel"
                    class="form-control"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input
                    id="password"
                    v-model="form.password"
                    type="password"
                    class="form-control"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label for="confirmPassword" class="form-label">Confirm Password</label>
                  <input
                    id="confirmPassword"
                    v-model="form.confirmPassword"
                    type="password"
                    class="form-control"
                    required
                  />
                </div>
                <div class="d-grid">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="loading"
                  >
                    {{ loading ? 'Registering...' : 'Register' }}
                  </button>
                </div>
                <div v-if="error" class="alert alert-danger mt-3">
                  {{ error }}
                </div>
              </form>
              <div class="text-center mt-3">
                <p>Already have an account? <router-link to="/login">Login</router-link></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'Register',
  setup() {
    const store = useStore()
    const router = useRouter()
    const loading = ref(false)
    const error = ref(null)
    const form = reactive({
      name: '',
      email: '',
      phone: '',
      password: '',
      confirmPassword: ''
    })

    const handleSubmit = async () => {
      if (form.password !== form.confirmPassword) {
        error.value = 'Passwords do not match'
        return
      }

      loading.value = true
      error.value = null

      try {
        const userData = {
          name: form.name,
          email: form.email,
          phone: form.phone,
          password: form.password
        }
        await store.dispatch('auth/register', userData)
        router.push('/dashboard')
      } catch (err) {
        error.value = err.message || 'An error occurred during registration'
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      loading,
      error,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.register {
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
}

.card {
  border: none;
  border-radius: 10px;
}
</style> 