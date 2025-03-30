<template>
  <div class="customer-requests">
    <h1>My Service Requests</h1>
    
    <div class="filters mb-4">
      <div class="btn-group">
        <button 
          v-for="status in ['all', 'pending', 'accepted', 'completed', 'cancelled']" 
          :key="status"
          :class="['btn', currentFilter === status ? 'btn-primary' : 'btn-outline-primary']"
          @click="currentFilter = status"
        >
          {{ status.charAt(0).toUpperCase() + status.slice(1) }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="filteredRequests.length === 0" class="text-center">
      <p class="text-muted">No service requests found.</p>
      <router-link to="/services" class="btn btn-primary">Browse Services</router-link>
    </div>

    <div v-else class="requests-list">
      <div v-for="request in filteredRequests" :key="request.id" class="request-card">
        <div class="card">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <h5 class="card-title">{{ request.service.name }}</h5>
                <p class="card-text text-muted">{{ request.service.category }}</p>
              </div>
              <span :class="['badge', statusClass(request.status)]">
                {{ request.status }}
              </span>
            </div>

            <div class="request-details mt-3">
              <p><strong>Address:</strong> {{ request.address }}</p>
              <p><strong>Preferred Date:</strong> {{ formatDate(request.preferred_date) }}</p>
              <p v-if="request.professional">
                <strong>Professional:</strong> {{ request.professional.name }}
              </p>
              <p v-if="request.final_price">
                <strong>Final Price:</strong> ${{ request.final_price.toFixed(2) }}
              </p>
              <p v-if="request.professional.average_rating">
                <strong>Professional's Rating:</strong> {{ request.professional.average_rating.toFixed(2) }}
              </p>
              <div v-for="review in request.reviews" :key="review.id">
                <p><strong>Rating Given:</strong> {{ review.rating }}</p>
                <p><strong>Comment Given:</strong> {{ review.comment.split(' ').slice(0, 5).join(' ') }}...</p> 
                <p><strong>Last Rating updated at:</strong> {{ formatDate(review.updated_at) }}</p> 
              </div>
            </div>

            <div class="request-actions mt-3">
              <button 
                v-if="request.status === 'pending'"
                class="btn btn-primary me-2"
                @click="openEditModal(request)"
              >
                Edit Request
              </button>
              <button 
                v-if="request.status === 'completed'"
                class="btn btn-primary me-2"
                @click="openReviewModal(request)"
              >
                Leave Review
              </button>
              <button 
                v-if="request.status === 'pending'"
                class="btn btn-danger"
                @click="cancelRequest(request.id)"
              >
                Cancel Request
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Request Modal -->
    <div v-if="showEditModal" class="modal-overlay vh-100" @click.self="closeEditModal">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Edit Service Request</h5>
          <button type="button" class="btn-close" @click="closeEditModal"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitEdit">
            <div class="form-group mb-3">
              <label class="form-label">Service</label>
              <input
                type="text"
                :value="selectedRequest?.service?.name"
                class="form-control"
                disabled/>
            </div>

            <div class="form-group mb-3">
              <label class="form-label">Select Professional</label>
              <select v-model="editForm.professional_id" class="form-control" required>
                <option value="">Select a Professional</option>
                <option v-for="professional in professionals" :key="professional.id" :value="professional.id">
                  {{ professional.name }} - Experience: {{ professional.experience || 'NA' }} years
                </option>
              </select>
            </div>

            <div class="form-group mb-3">
              <label class="form-label">Price ($)</label>
              <input
                v-model="editForm.price"
                type="number"
                class="form-control"
                :min="selectedRequest?.service?.base_price"
                step="0.01"
                required
              />
            </div>

            <div class="form-group mb-3">
              <label class="form-label">Address</label>
              <textarea 
                v-model="editForm.address" 
                class="form-control" 
                rows="3" 
                required
              ></textarea>
            </div>

            <div class="form-group mb-3">
              <label class="form-label">Preferred Date</label>
              <input 
                v-model="editForm.preferred_date" 
                type="date" 
                class="form-control"
                :min="minDate"
                required/>
            </div>

            <div class="form-group mb-3">
              <label class="form-label">Description</label>
              <textarea 
                v-model="editForm.description" 
                class="form-control" 
                rows="4" 
                placeholder="Please describe your service needs..."
                required
              ></textarea>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeEditModal">Cancel</button>
              <button 
                type="submit" 
                class="btn btn-primary" 
                :disabled="submitting"
              >
                {{ submitting ? 'Updating...' : 'Update Request' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Review Modal -->
    <div v-if="showReviewModal" class="modal-overlay" @click.self="closeReviewModal">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Leave a Review</h5>
          <button type="button" class="btn-close" @click="closeReviewModal"></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label class="form-label">Rating</label>
            <div class="rating">
              <i 
                v-for="star in 5" 
                :key="star"
                :class="['fas', 'fa-star', { active: star <= review.rating }]"
                @click="review.rating = star"
              ></i>
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">Comment</label>
            <textarea 
              v-model="review.comment"
              class="form-control"
              rows="3"
              placeholder="Share your experience..."
            ></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeReviewModal">Cancel</button>
          <button 
            type="button" 
            class="btn btn-primary" 
            @click="submitReview"
            :disabled="!review.rating || !review.comment"
          >
            Submit Review
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'

export default {
  name: 'CustomerRequests',
  setup() {
    const toast = useToast()
    const requests = ref([])
    const loading = ref(true)
    const currentFilter = ref('all')
    const showReviewModal = ref(false)
    const showEditModal = ref(false)
    const selectedRequest = ref(null)
    const professionals = ref([])
    const submitting = ref(false)
    const review = ref({
      rating: 0,
      comment: ''
    })

    const editForm = ref({
      professional_id: '',
      address: '',
      preferred_date: '',
      description: '',
      price: ''
    })

    const minDate = computed(() => {
      const today = new Date()
      return today.toISOString().split('T')[0]
    })

    const filteredRequests = computed(() => {
      if (currentFilter.value === 'all') {
        return requests.value
      }
      return requests.value.filter(request => request.status === currentFilter.value)
    })

    const fetchRequests = async () => {
      try {
        loading.value = true
        const response = await axios.get('/api/customer/requests')
        requests.value = response.data
      } catch (error) {
        console.error('Error fetching requests:', error)
        toast.error('Failed to fetch requests')
      } finally {
        loading.value = false
      }
    }

    const loadProfessionals = async (serviceId) => {
      try {
        const response = await axios.get(`/api/customer/professionals/${serviceId}`)
        professionals.value = response.data.professionals
      } catch (error) {
        console.error('Error loading professionals:', error)
        toast.error('Failed to load professionals')
      }
    }

    const openEditModal = async (request) => {
      selectedRequest.value = request
      showEditModal.value = true
      editForm.value = {
        professional_id: request.professional_id || '',
        address: request.address,
        preferred_date: new Date(request.preferred_date).toISOString().split('T')[0],
        description: request.notes || '',
        price: request.final_price || ''
      }
      await loadProfessionals(request.service.id)
    }

    const closeEditModal = () => {
      showEditModal.value = false
      selectedRequest.value = null
      editForm.value = {
        professional_id: '',
        address: '',
        preferred_date: '',
        description: '',
        price: ''
      }
    }

    const submitEdit = async () => {
      try {
        submitting.value = true
        await axios.put(`/api/customer/requests/${selectedRequest.value.id}`, editForm.value)
        toast.success('Request updated successfully')
        await fetchRequests()
        closeEditModal()
      } catch (error) {
        console.error('Error updating request:', error)
        toast.error('Failed to update request')
      } finally {
        submitting.value = false
      }
    }

    const cancelRequest = async (requestId) => {
      try {
        await axios.get(`/api/customer/requests/${requestId}/cancel`)
        toast.success('Request cancelled successfully')
        await fetchRequests()
      } catch (error) {
        console.error('Error cancelling request:', error)
        toast.error('Failed to cancel request')
      }
    }

    const openReviewModal = (request) => {
      selectedRequest.value = request
      showReviewModal.value = true
      review.value = { rating: 0, comment: '' }
    }

    const closeReviewModal = () => {
      showReviewModal.value = false
      selectedRequest.value = null
      review.value = { rating: 0, comment: '' }
    }

    const submitReview = async () => {
      try {
        await axios.post(`/api/customer/reviews`, {
          service_request_id: selectedRequest.value.id,
          professional_id: selectedRequest.value.professional.id,
          rating: review.value.rating,
          comment: review.value.comment
        })
        toast.success('Review submitted successfully')
        await fetchRequests()
        closeReviewModal()
      } catch (error) {
        console.error('Error submitting review:', error)
        toast.error('Failed to submit review')
      }
    }

    const statusClass = (status) => {
      const classes = {
        pending: 'bg-warning',
        accepted: 'bg-info',
        completed: 'bg-success',
        cancelled: 'bg-danger'
      }
      return classes[status] || 'bg-secondary'
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    // Fetch requests when component is mounted
    onMounted(() => {
      fetchRequests()
    })

    return {
      requests,
      loading,
      currentFilter,
      filteredRequests,
      showReviewModal,
      showEditModal,
      review,
      editForm,
      professionals,
      submitting,
      minDate,
      cancelRequest,
      openReviewModal,
      closeReviewModal,
      submitReview,
      openEditModal,
      closeEditModal,
      submitEdit,
      statusClass,
      formatDate
    }
  }
}
</script>

<style scoped>
.customer-requests {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.requests-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.request-card {
  height: 100%;
}

.request-card .card {
  height: 100%;
  transition: transform 0.2s;
}

.request-card .card:hover {
  transform: translateY(-2px);
}

.rating {
  display: flex;
  gap: 0.5rem;
  font-size: 1.5rem;
  color: #ddd;
}

.rating i {
  cursor: pointer;
}

.rating i.active {
  color: #ffc107;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  width: 90%;
  max-width: 500px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.modal-header {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-control:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .customer-requests {
    padding: 1rem;
  }

  .requests-list {
    grid-template-columns: 1fr;
  }

  .filters .btn-group {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: 0.5rem;
  }
}
</style> 