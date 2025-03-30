<template>
  <div class="customer-services">
    <div class="container">
      <header class="services-header">
        <h1>Available Services</h1>
        <p>Browse and request services from our professional network</p>
        
        <div class="search-filters">
          <div class="search-bar">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search by service name..." 
              class="form-control"
              @input="handleSearch"/>
            <i class="fas fa-search search-icon"></i>
          </div>

          <!-- <div class="location-filter">
            <input 
              v-model="locationQuery" 
              type="text" 
              placeholder="Enter location or PIN code..." 
              class="form-control"
              @input="handleLocationSearch"/>
            <i class="fas fa-map-marker-alt location-icon"></i>
          </div> -->

          <div class="category-filter">
            <select v-model="selectedCategory" class="form-control">
              <option value="">All Categories</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>
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
          <div class="service-image-container">
            <img :src="service.image_url || 'https://picsum.photos/1300/200'" :alt="service.name" />
            <div class="service-category">{{ service.category?.name }}</div>
          </div>
          <div class="service-content">
            <h3 class="card-title">{{ service.name }}</h3>
            <p class="service-description">{{ service.description }}</p>
            <div class="service-details">
              <div class="service-price">
                <i class="fas fa-dollar-sign"></i>
                Starting from ${{ service.base_price }}
              </div>
              <div class="service-rating">
                <i class="fas fa-star"></i>
                {{ service.average_rating || 'NA' }}
              </div>
            </div>
            <div class="service-footer">
              <button 
                class="btn btn-primary"
                @click="requestService(service)"
              >
                Request Service
              </button>
              <!-- <button 
                class="btn btn-outline-primary"
                @click="viewDetails(service)"
              >
                View Details
              </button> -->
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

            <!-- New Professional Dropdown -->
            <div class="form-group">
              <label class="form-label">Select Professional</label>
              <select v-model="requestForm.professional_id" class="form-control" required>
                <option value="">Select a Professional</option>
                <option v-for="professional in professionals" :key="professional.id" :value="professional.id">
                  {{ professional.name }} - Experience: {{ professional.experience || 'NA' }} years
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="servicePrice" class="form-label">Price ($)</label>
              <input
                id="servicePrice"
                v-model="requestForm.price"
                type="number"
                class="form-control"
                :min= "selectedService?.base_price"
                step="0.01"
                required
              />
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

            <!-- <div class="form-group">
              <label class="form-label">Preferred Time</label>
              <select v-model="requestForm.preferred_time" class="form-control" required>
                <option value="">Select time</option>
                <option value="morning">Morning (8 AM - 12 PM)</option>
                <option value="afternoon">Afternoon (12 PM - 4 PM)</option>
                <option value="evening">Evening (4 PM - 8 PM)</option>
              </select>
            </div> -->

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
import { servicesAPI, customerAPI } from '@/services/api'

export default {
  name: 'CustomerServices',
  
  setup() {
    const router = useRouter()
    const toast = useToast()
    
    // State
    const services = ref([])
    const categories = ref([])
    const loading = ref(true)
    const error = ref(null)
    const searchQuery = ref('')
    const locationQuery = ref('')
    const selectedCategory = ref('')
    const showModal = ref(false)
    const selectedService = ref(null)
    const submitting = ref(false)
    const professionals = ref([]); // Holds the list of professionals

    const requestForm = ref({
      professional_id: '',
      address: '',
      preferred_date: '',
      preferred_time: '',
      description: '',
      price: ''
    })

    // Computed
    const filteredServices = computed(() => {
      let filtered = services.value

      // Filter by search query
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(service => 
          service.name.toLowerCase().includes(query) ||
          service.description.toLowerCase().includes(query)
        )
      }

      // Filter by location
      if (locationQuery.value) {
        const location = locationQuery.value.toLowerCase()
        filtered = filtered.filter(service => 
          service.location?.toLowerCase().includes(location) ||
          service.pin_code?.includes(location)
        )
      }

      // Filter by category
      if (selectedCategory.value) {
        filtered = filtered.filter(service => 
          service.category_id === selectedCategory.value
        )
      }

      return filtered
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

    const loadCategories = async () => {
      try {
        const response = await servicesAPI.getCategories()
        categories.value = response.data
      } catch (err) {
        console.error('Error loading categories:', err)
      }
    }

    const loadProfessionals = async (serviceId) => {
      try {
        const response = await customerAPI.getProfessionals(serviceId)
        console.log('API Response:', response)
        console.log('Response Data:', response.data)
        professionals.value = response.data.professionals
        console.log('Professionals Array:', professionals.value)
      } catch (err) {
        console.error('Error loading professionals:', err)
        toast.error('Failed to load professionals. Please try again.')
      }
    }

    const handleSearch = () => {
      // Debounce implementation could be added here if needed
    }

    const handleLocationSearch = () => {
      // Debounce implementation could be added here if needed
    }

    const requestService = async (service) => {
      selectedService.value = service
      showModal.value = true
      await loadProfessionals(service.id)
    }

    const viewDetails = (service) => {
      router.push(`/services/${service.id}`)
    }

    const closeModal = () => {
      showModal.value = false
      selectedService.value = null
      professionals.value = []
      requestForm.value = {
        professional_id: '',
        address: '',
        preferred_date: '',
        preferred_time: '',
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
        toast.error('Failed to submit request. Please try again.')
        console.error('Error submitting request:', err)
      } finally {
        submitting.value = false
      }
    }

    // Lifecycle
    onMounted(() => {
      loadServices()
      loadCategories()
    })

    return {
      services,
      categories,
      loading,
      error,
      searchQuery,
      locationQuery,
      selectedCategory,
      showModal,
      selectedService,
      requestForm,
      submitting,
      filteredServices,
      minDate,
      professionals,
      handleSearch,
      handleLocationSearch,
      requestService,
      viewDetails,
      closeModal,
      submitRequest
    }
  }
}
</script>

<style scoped>
.customer-services {
  padding: 2rem 0;
}

.services-header {
  text-align: center;
  margin-bottom: 2rem;
}

.search-filters {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  flex-wrap: wrap;
}

.search-bar,
.location-filter,
.category-filter {
  flex: 1;
  min-width: 200px;
  position: relative;
}

.search-icon,
.location-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.service-card {
  transition: transform 0.2s;
  height: 100%;
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.service-image-container {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.service-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.service-category {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0,0,0,0.7);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.service-content {
  padding: 1rem;
}

.service-details {
  display: flex;
  justify-content: space-between;
  margin: 1rem 0;
  color: #666;
}

.service-footer {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 1rem;
}

.modal-footer {
  padding: 1rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

@media (max-width: 768px) {
  .search-filters {
    flex-direction: column;
  }
  
  .search-bar,
  .location-filter,
  .category-filter {
    width: 100%;
  }
}
</style> 