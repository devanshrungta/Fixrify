<template>
  <div class="profile">
    <div class="container">
      <h1 class="mb-4">Profile Settings</h1>

      <div class="row">
        <div class="col-md-8">
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="mb-0">Personal Information</h5>
            </div>
            <div class="card-body">
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
                  <label for="address" class="form-label">Address</label>
                  <textarea
                    id="address"
                    v-model="form.address"
                    class="form-control"
                    rows="3"
                  ></textarea>
                </div>
                <div class="d-grid">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="loading"
                  >
                    {{ loading ? 'Saving...' : 'Save Changes' }}
                  </button>
                </div>
                <div v-if="error" class="alert alert-danger mt-3">
                  {{ error }}
                </div>
                <div v-if="success" class="alert alert-success mt-3">
                  Profile updated successfully!
                </div>
              </form>
            </div>
          </div>

          <div class="card">
            <div class="card-header">
              <h5 class="mb-0">Change Password</h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="handlePasswordChange">
                <div class="mb-3">
                  <label for="currentPassword" class="form-label">Current Password</label>
                  <input
                    id="currentPassword"
                    v-model="passwordForm.currentPassword"
                    type="password"
                    class="form-control"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label for="newPassword" class="form-label">New Password</label>
                  <input
                    id="newPassword"
                    v-model="passwordForm.newPassword"
                    type="password"
                    class="form-control"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label for="confirmPassword" class="form-label">Confirm New Password</label>
                  <input
                    id="confirmPassword"
                    v-model="passwordForm.confirmPassword"
                    type="password"
                    class="form-control"
                    required
                  />
                </div>
                <div class="d-grid">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="passwordLoading"
                  >
                    {{ passwordLoading ? 'Updating...' : 'Update Password' }}
                  </button>
                </div>
                <div v-if="passwordError" class="alert alert-danger mt-3">
                  {{ passwordError }}
                </div>
                <div v-if="passwordSuccess" class="alert alert-success mt-3">
                  Password updated successfully!
                </div>
              </form>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card">
            <div class="card-header">
              <h5 class="mb-0">Account Information</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label class="form-label">Member Since</label>
                <p>{{ formatDate(user.created_at) }}</p>
              </div>
              <div class="mb-3">
                <label class="form-label">Account Type</label>
                <p>{{ user.role === 'admin' ? 'Administrator' : 'Customer' }}</p>
              </div>
              <div class="mb-3">
                <label class="form-label">Total Bookings</label>
                <p>{{ totalBookings }}</p>
              </div>
              <div class="mb-3">
                <label class="form-label">Completed Services</label>
                <p>{{ completedServices }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Profile',
  setup() {
    const store = useStore()
    const loading = ref(false)
    const error = ref(null)
    const success = ref(false)
    const passwordLoading = ref(false)
    const passwordError = ref(null)
    const passwordSuccess = ref(false)

    const user = computed(() => store.getters['auth/user'])
    const bookings = computed(() => store.getters['bookings/userBookings'])
    const totalBookings = computed(() => bookings.value.length)
    const completedServices = computed(() => {
      return bookings.value.filter(booking => booking.status === 'completed').length
    })

    const form = reactive({
      name: '',
      email: '',
      phone: '',
      address: ''
    })

    const passwordForm = reactive({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    })

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString()
    }

    const handleSubmit = async () => {
      loading.value = true
      error.value = null
      success.value = false

      try {
        await store.dispatch('auth/updateProfile', form)
        success.value = true
      } catch (err) {
        error.value = err.message || 'Failed to update profile'
      } finally {
        loading.value = false
      }
    }

    const handlePasswordChange = async () => {
      if (passwordForm.newPassword !== passwordForm.confirmPassword) {
        passwordError.value = 'New passwords do not match'
        return
      }

      passwordLoading.value = true
      passwordError.value = null
      passwordSuccess.value = false

      try {
        await store.dispatch('auth/updatePassword', {
          currentPassword: passwordForm.currentPassword,
          newPassword: passwordForm.newPassword
        })
        passwordSuccess.value = true
        passwordForm.currentPassword = ''
        passwordForm.newPassword = ''
        passwordForm.confirmPassword = ''
      } catch (err) {
        passwordError.value = err.message || 'Failed to update password'
      } finally {
        passwordLoading.value = false
      }
    }

    onMounted(() => {
      form.name = user.value.name
      form.email = user.value.email
      form.phone = user.value.phone
      form.address = user.value.address
    })

    return {
      user,
      form,
      passwordForm,
      loading,
      error,
      success,
      passwordLoading,
      passwordError,
      passwordSuccess,
      totalBookings,
      completedServices,
      formatDate,
      handleSubmit,
      handlePasswordChange
    }
  }
}
</script>

<style scoped>
.card {
  border: none;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
</style> 