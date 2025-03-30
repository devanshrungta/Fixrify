<template>
  <div class="professional-requests">
    <h1>Service Requests</h1>
    <div class="requests-list">
      <div v-if="loading" class="loading">
        Loading...
      </div>
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      <div v-else class="requests-grid">
        <div v-for="request in requests" :key="request.id" class="request-card">
          <div class="request-header">
            <h3>{{ request.service_name }}</h3>
            <span :class="['status', request.status]">{{ request.status }}</span>
          </div>
          <div class="request-details">
            <p><strong>Customer:</strong> {{ request.customer_name }}</p>
            <p><strong>Address:</strong> {{ request.address }}</p>
            <p><strong>Date:</strong> {{ formatDate(request.preferred_date) }}</p>
            <p><strong>Description:</strong> {{ request.description }}</p>
          </div>
          <div class="request-actions">
            <button 
              v-if="request.status === 'pending'"
              class="btn btn-success"
              @click="acceptRequest(request.id)">
              Accept
            </button>
            <button 
              v-if="request.status === 'pending'"
              class="btn btn-danger"
              @click="rejectRequest(request.id)">
              Reject
            </button>
            <button 
              v-if="request.status === 'accepted'"
              class="btn btn-primary"
              @click="completeRequest(request.id)">
              Mark Complete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { professionalAPI } from '@/services/api'

export default {
  name: 'ProfessionalRequests',
  
  setup() {
    const toast = useToast()
    const requests = ref([])
    const loading = ref(true)
    const error = ref(null)

    const loadRequests = async () => {
      try {
        loading.value = true
        error.value = null
        const response = await professionalAPI.getRequests()
        requests.value = response.data
      } catch (err) {
        error.value = 'Failed to load requests'
        console.error('Error loading requests:', err)
      } finally {
        loading.value = false
      }
    }

    const acceptRequest = async (requestId) => {
      try {
        await professionalAPI.acceptRequest(requestId)
        toast.success('Request accepted successfully')
        await loadRequests()
      } catch (err) {
        toast.error('Failed to accept request')
        console.error('Error accepting request:', err)
      }
    }

    const rejectRequest = async (requestId) => {
      try {
        await professionalAPI.rejectRequest(requestId)
        toast.success('Request rejected')
        await loadRequests()
      } catch (err) {
        toast.error('Failed to reject request')
        console.error('Error rejecting request:', err)
      }
    }

    const completeRequest = async (requestId) => {
      try {
        await professionalAPI.completeRequest(requestId)
        toast.success('Request marked as complete')
        await loadRequests()
      } catch (err) {
        toast.error('Failed to complete request')
        console.error('Error completing request:', err)
      }
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString()
    }

    onMounted(() => {
      loadRequests()
    })

    return {
      requests,
      loading,
      error,
      acceptRequest,
      rejectRequest,
      completeRequest,
      formatDate
    }
  }
}
</script>

<style scoped>
.professional-requests {
  padding: 2rem;
}

.requests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.request-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.request-header h3 {
  margin: 0;
  color: var(--dark-color);
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status.pending {
  background: #fff3cd;
  color: #856404;
}

.status.accepted {
  background: #d4edda;
  color: #155724;
}

.status.completed {
  background: #cce5ff;
  color: #004085;
}

.status.rejected {
  background: #f8d7da;
  color: #721c24;
}

.request-details {
  margin-bottom: 1.5rem;
}

.request-details p {
  margin: 0.5rem 0;
  color: var(--secondary-color);
}

.request-details strong {
  color: var(--dark-color);
}

.request-actions {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn:hover {
  opacity: 0.9;
}

.loading,
.error {
  text-align: center;
  padding: 2rem;
  color: var(--secondary-color);
}

.error {
  color: #dc3545;
}

@media (max-width: 768px) {
  .professional-requests {
    padding: 1rem;
  }

  .requests-grid {
    grid-template-columns: 1fr;
  }
}
</style> 