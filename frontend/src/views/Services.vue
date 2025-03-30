<template>
  <div class="services">
    <div class="container">
      <header class="services-header">
        <h1>Our Services</h1>
        <p>Find the perfect service for your home maintenance needs</p>
        
        <div class="search-bar">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Search services..." 
            class="form-control"
            @input="handleSearch"/>
        </div>
      </header>

      <div v-if="loading" class="text-center mt-4">
        <div class="spinner"></div>
      </div>

      <div v-else-if="error" class="alert alert-danger mt-4">
        {{ error }}
      </div>

      <div v-else class="services-grid grid-3 mt-4">
        <div v-for="service in filteredServices" :key="service.id" class="service-card card">
          <img 
            :src="'https://picsum.photos/694/80?random=' + service.id" 
            :alt="service.name" 
            class="service-image"/>
          <div class="service-content">
            <h3 class="card-title">{{ service.name }}</h3>
            <p class="service-description">{{ service.description }}</p>
            <div class="service-footer">
              <span class="service-price">Starting from ${{ service.base_price }}</span>
              <button 
                v-if="isCustomer" 
                class="btn btn-primary"
                @click="requestService(service)"
              >
                Request Service
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Service Request Modal -->
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content card">
          <div class="modal-header">
            <h2>Request Service</h2>
            <button class="close-button" @click="closeModal">&times;</button>
          </div>
          
          <form class="modal-body" @submit.prevent="submitRequest">
            <div class="form-group">
              <label class="form-label">Service</label>
              <input
                type="text"
                :value="selectedService?.name"
                class="form-control"
                disabled/>
            </div>

            <div class="form-group">
              <label class="form-label">Address</label>
              <textarea 
                v-model="requestForm.address" 
                class="form-control" 
                rows="3" 
                required
              ></textarea>
            </div>

            <div class="form-group">
              <label class="form-label">Preferred Date</label>
              <input 
                v-model="requestForm.preferred_date" 
                type="date" 
                class="form-control"
                :min="minDate"
                required/>
            </div>

            <div class="form-group">
              <label class="form-label">Description</label>
              <textarea 
                v-model="requestForm.description" 
                class="form-control" 
                rows="4" 
                placeholder="Please describe your service needs..."
                required
              ></textarea>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="submitting">
                {{ submitting ? 'Submitting...' : 'Submit Request' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { servicesAPI, customerAPI } from '../services/api'

export default {
  name: 'Services',
  
  setup() {
    const router = useRouter()
    const toast = useToast()
    
    // State
    const services = ref([])
    const loading = ref(true)
    const error = ref(null)
    const searchQuery = ref('')
    const showModal = ref(false)
    const selectedService = ref(null)
    const submitting = ref(false)
    
    const requestForm = ref({
      address: '',
      preferred_date: '',
      description: ''
    })

    // Computed
    const isCustomer = computed(() => {
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      return user.role === 'customer'
    })

    const filteredServices = computed(() => {
      if (!searchQuery.value) return services.value

      const query = searchQuery.value.toLowerCase()
      
      return services.value.filter(service => {
        const name = service.name ? service.name.toLowerCase() : ''
        const description = service.description ? service.description.toLowerCase() : ''

        return name.includes(query) || description.includes(query)
      })
    })


    const minDate = computed(() => {
      const today = new Date()
      return today.toISOString().split('T')[0]
    })

    // Methods
    const loadServices = async () => {
      try {
        loading.value = true
        error.value = null
        const response = await servicesAPI.getAll()
        services.value = response.data
      } catch (err) {
        error.value = 'Failed to load services. Please try again later.'
        console.error('Error loading services:', err)
      } finally {
        loading.value = false
      }
    }

    const handleSearch = () => {
      // Debounce implementation could be added here if needed
    }

    const requestService = (service) => {
      if (!isCustomer.value) {
        router.push('/login')
        return
      }
      
      selectedService.value = service
      showModal.value = true
    }

    const closeModal = () => {
      showModal.value = false
      selectedService.value = null
      requestForm.value = {
        address: '',
        preferred_date: '',
        description: ''
      }
    }

    const submitRequest = async () => {
      if (!selectedService.value) return
      
      try {
        submitting.value = true
        await customerAPI.createRequest({
          service_id: selectedService.value.id,
          ...requestForm.value
        })
        
        toast.success('Service request submitted successfully!')
        closeModal()
        router.push('/customer/requests')
      } catch (err) {
        console.error('Error submitting request:', err)
      } finally {
        submitting.value = false
      }
    }

    // Lifecycle
    onMounted(() => {
      loadServices()
    })

    return {
      services,
      loading,
      error,
      searchQuery,
      showModal,
      selectedService,
      requestForm,
      submitting,
      isCustomer,
      filteredServices,
      minDate,
      handleSearch,
      requestService,
      closeModal,
      submitRequest
    }
  }
}
</script>

<style scoped>
.services {
  padding: 2rem 0;
}

.services-header {
  text-align: center;
  margin-bottom: 2rem;
}

.services-header h1 {
  color: var(--dark-color);
  margin-bottom: 0.5rem;
}

.services-header p {
  color: var(--secondary-color);
  font-size: 1.1rem;
}

.search-bar {
  max-width: 600px;
  margin: 2rem auto 0;
}

.service-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  transition: transform 0.2s ease-in-out;
}

.service-card:hover {
  transform: translateY(-5px);
}

.service-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: var(--border-radius) var(--border-radius) 0 0;
}

.service-content {
  padding: 1.5rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.service-description {
  color: var(--secondary-color);
  margin-bottom: 1.5rem;
  flex-grow: 1;
}

.service-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.service-price {
  font-weight: 600;
  color: var(--dark-color);
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid #dee2e6;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--secondary-color);
}

.close-button:hover {
  color: var(--dark-color);
}

.modal-body {
  margin-bottom: 1rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .services {
    padding: 1rem 0;
  }

  .service-image {
    height: 150px;
  }

  .service-footer {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .service-price {
    text-align: center;
  }
}
</style> 