<template>
  <div class="login">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-4">
          <div class="card shadow">
            <div class="card-body p-5">
              <h2 class="text-center mb-4">Login</h2>
              <form @submit.prevent="handleSubmit">
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
                  <label for="password" class="form-label">Password</label>
                  <input
                    id="password"
                    v-model="form.password"
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
                    {{ loading ? 'Logging in...' : 'Login' }}
                  </button>
                </div>
                <div v-if="error" class="alert alert-danger mt-3">
                  {{ error }}
                </div>
              </form>
              <div class="text-center mt-3">
                <p>Don't have an account? <router-link to="/register">Register</router-link></p>
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
  name: 'Login',
  setup() {
    const store = useStore()
    const router = useRouter()
    const loading = ref(false)
    const error = ref(null)
    const form = reactive({
      email: '',
      password: ''
    })

    const handleSubmit = async () => {
      loading.value = true
      error.value = null

      try {
        await store.dispatch('auth/login', form)
        router.push('/dashboard')
      } catch (err) {
        error.value = err.message || 'An error occurred during login'
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
.login {
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
}

.card {
  border: none;
  border-radius: 10px;
}
</style> 