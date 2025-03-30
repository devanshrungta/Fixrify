<template>
  <div class="dashboard">
    <div class="container">
      <h1 class="mb-4">Dashboard</h1>

      <div class="row">
        <div class="col-md-4 mb-4">
          <div class="card bg-primary text-white">
            <div class="card-body">
              <h5 class="card-title">Upcoming Bookings</h5>
              <h2 class="card-text">{{ upcomingBookings.length }}</h2>
              <router-link to="/dashboard#bookings" class="text-white">
                View Details <i class="fas fa-arrow-right"></i>
              </router-link>
            </div>
          </div>
        </div>

        <div class="col-md-4 mb-4">
          <div class="card bg-success text-white">
            <div class="card-body">
              <h5 class="card-title">Completed Services</h5>
              <h2 class="card-text">{{ completedBookings.length }}</h2>
              <router-link to="/dashboard#history" class="text-white">
                View History <i class="fas fa-arrow-right"></i>
              </router-link>
            </div>
          </div>
        </div>

        <div class="col-md-4 mb-4">
          <div class="card bg-info text-white">
            <div class="card-body">
              <h5 class="card-title">Total Spent</h5>
              <h2 class="card-text">${{ totalSpent }}</h2>
              <router-link to="/dashboard#transactions" class="text-white">
                View Details <i class="fas fa-arrow-right"></i>
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-md-8">
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="mb-0">Upcoming Bookings</h5>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </div>

              <div v-else-if="error" class="alert alert-danger">
                {{ error }}
              </div>

              <div v-else-if="upcomingBookings.length === 0" class="text-center">
                <p class="lead">No upcoming bookings</p>
                <router-link to="/services" class="btn btn-primary">
                  Book a Service
                </router-link>
              </div>

              <div v-else class="list-group">
                <div
                  v-for="booking in upcomingBookings"
                  :key="booking.id"
                  class="list-group-item"
                >
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <h6 class="mb-1">{{ booking.service.name }}</h6>
                      <small class="text-muted">
                        {{ formatDate(booking.date) }} at {{ booking.time }}
                      </small>
                    </div>
                    <div>
                      <button
                        class="btn btn-sm btn-outline-danger"
                        @click="cancelBooking(booking.id)"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="mb-0">Profile Information</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label class="form-label">Name</label>
                <p>{{ user.name }}</p>
              </div>
              <div class="mb-3">
                <label class="form-label">Email</label>
                <p>{{ user.email }}</p>
              </div>
              <div class="mb-3">
                <label class="form-label">Phone</label>
                <p>{{ user.phone }}</p>
              </div>
              <router-link to="/profile" class="btn btn-primary">
                Edit Profile
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Dashboard',
  setup() {
    const store = useStore()
    const loading = ref(false)
    const error = ref(null)

    const user = computed(() => store.getters['auth/user'])
    const bookings = computed(() => store.getters['bookings/userBookings'])
    const upcomingBookings = computed(() => {
      return bookings.value.filter(booking => {
        const bookingDate = new Date(booking.date)
        return bookingDate >= new Date() && booking.status !== 'completed'
      })
    })
    const completedBookings = computed(() => {
      return bookings.value.filter(booking => booking.status === 'completed')
    })
    const totalSpent = computed(() => {
      return completedBookings.value.reduce((total, booking) => {
        return total + booking.service.price
      }, 0)
    })

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString()
    }

    const cancelBooking = async (bookingId) => {
      if (!confirm('Are you sure you want to cancel this booking?')) {
        return
      }

      try {
        await store.dispatch('bookings/cancelBooking', bookingId)
      } catch (err) {
        error.value = err.message || 'Failed to cancel booking'
      }
    }

    onMounted(async () => {
      loading.value = true
      error.value = null
      try {
        await store.dispatch('bookings/fetchBookings')
      } catch (err) {
        error.value = err.message || 'Failed to fetch bookings'
      } finally {
        loading.value = false
      }
    })

    return {
      user,
      bookings,
      upcomingBookings,
      completedBookings,
      totalSpent,
      loading,
      error,
      formatDate,
      cancelBooking
    }
  }
}
</script>

<style scoped>
.card {
  border: none;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style> 