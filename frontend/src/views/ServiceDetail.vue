<template>
  <div class="service-detail">
    <div class="container">
      <div v-if="loading" class="text-center">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="error" class="alert alert-danger">
        {{ error }}
      </div>

      <div v-else-if="service" class="row">
        <div class="col-md-8">
          <img
            :src="service.image"
            class="img-fluid rounded mb-4"
            :alt="service.name"
          />
          <h1>{{ service.name }}</h1>
          <p class="lead">{{ service.description }}</p>
          <div class="mb-4">
            <h3>Service Details</h3>
            <ul class="list-unstyled">
              <li><strong>Category:</strong> {{ service.category }}</li>
              <li><strong>Duration:</strong> {{ service.duration }} hours</li>
              <li><strong>Price:</strong> ${{ service.price }}</li>
            </ul>
          </div>
          <div class="mb-4">
            <h3>What's Included</h3>
            <ul>
              <li v-for="(item, index) in service.includes" :key="index">
                {{ item }}
              </li>
            </ul>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card">
            <div class="card-body">
              <h3 class="card-title">Book This Service</h3>
              <form @submit.prevent="handleBooking">
                <div class="mb-3">
                  <label for="date" class="form-label">Preferred Date</label>
                  <input
                    id="date"
                    v-model="bookingForm.date"
                    type="date"
                    class="form-control"
                    required
                    :min="minDate"
                  />
                </div>
                <div class="mb-3">
                  <label for="time" class="form-label">Preferred Time</label>
                  <select
                    id="time"
                    v-model="bookingForm.time"
                    class="form-select"
                    required
                  >
                    <option value="">Select a time</option>
                    <option v-for="time in availableTimes" :key="time" :value="time">
                      {{ time }}
                    </option>
                  </select>
                </div>
                <div class="mb-3">
                  <label for="notes" class="form-label">Additional Notes</label>
                  <textarea
                    id="notes"
                    v-model="bookingForm.notes"
                    class="form-control"
                    rows="3"
                  ></textarea>
                </div>
                <div class="d-grid">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="loading || !isAuthenticated"
                  >
                    {{ loading ? 'Processing...' : 'Book Now' }}
                  </button>
                </div>
                <div v-if="!isAuthenticated" class="text-center mt-3">
                  <p>Please <router-link to="/login">login</router-link> to book this service.</p>
                </div>
                <div v-if="bookingError" class="alert alert-danger mt-3">
                  {{ bookingError }}
                </div>
              </form>
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
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'ServiceDetail',
  setup() {
    const store = useStore()
    const route = useRoute()
    const router = useRouter()
    const loading = ref(false)
    const error = ref(null)
    const bookingError = ref(null)
    const isAuthenticated = computed(() => store.getters['auth/isAuthenticated'])
    const service = computed(() => store.getters['services/currentService'])

    const bookingForm = ref({
      date: '',
      time: '',
      notes: ''
    })

    const minDate = computed(() => {
      const today = new Date()
      return today.toISOString().split('T')[0]
    })

    const availableTimes = [
      '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00'
    ]

    const handleBooking = async () => {
      if (!isAuthenticated.value) {
        router.push('/login')
        return
      }

      loading.value = true
      bookingError.value = null

      try {
        const bookingData = {
          service_id: service.value.id,
          date: bookingForm.value.date,
          time: bookingForm.value.time,
          notes: bookingForm.value.notes
        }
        await store.dispatch('bookings/createBooking', bookingData)
        router.push('/dashboard')
      } catch (err) {
        bookingError.value = err.message || 'Failed to create booking'
      } finally {
        loading.value = false
      }
    }

    onMounted(async () => {
      loading.value = true
      error.value = null
      try {
        await store.dispatch('services/fetchService', route.params.id)
      } catch (err) {
        error.value = err.message || 'Failed to fetch service details'
      } finally {
        loading.value = false
      }
    })

    return {
      service,
      loading,
      error,
      bookingForm,
      minDate,
      availableTimes,
      isAuthenticated,
      bookingError,
      handleBooking
    }
  }
}
</script>

<style scoped>
.spinner-border {
  width: 3rem;
  height: 3rem;
}

.card {
  border: none;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
</style> 