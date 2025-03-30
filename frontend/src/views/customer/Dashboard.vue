<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>Welcome, {{ profile.name }}</h1>
      <div class="stats">
        <!-- <div class="stat-card">
          <h3>Total Services</h3>
          <p>{{ stats.total_services }}</p>
        </div> -->
        <div class="stat-card">
          <h3>Completed</h3>
          <p>{{ stats.completed_requests }}</p>
        </div>
        <div class="stat-card">
          <h3>Active Requests</h3>
          <p>{{ stats.active_requests }}</p>
        </div>
      </div>
    </header>

    <section class="active-requests">
      <h2>Active Requests</h2>
      <div v-if="activeRequests.length" class="requests-grid">
        <div v-for="request in activeRequests" :key="request.id" class="request-card">
          <div class="request-header">
            <h3>{{ request.service.name }}</h3>
            <span :class="['status', request.status]">{{ request.status }}</span>
          </div>
          <div class="request-details">
            <p><strong>Date:</strong> {{ formatDate(request.preferred_date) }}</p>
            <p><strong>Time: </strong>
              <span v-if="request.completed_at === null">Yet to complete</span>
              <span v-else>{{ formatDate(request.completed_at) }}</span> 
            </p>
            <p><strong>Professional:</strong> {{ request.professional.name }} (+91 {{ request.professional.phone }})</p>
            <p><strong>Address:</strong> {{ request.address }}</p>
          </div>
          <div class="request-actions">
            <button v-if="request.status === 'pending'" class="btn-cancel" @click="cancelRequest(request.id)">
              Cancel Request
            </button>
          </div>
        </div>
      </div>
      <p v-else>No active requests</p>
    </section>

    <section class="recent-services">
      <h2>Available Services</h2>
      <div class="services-grid">
        <div v-for="service in recentServices" :key="service.id" class="service-card">
          <img :src="service.image_url || 'https://picsum.photos/200'" :alt="service.name" />
          <div class="service-content">
            <h3>{{ service.name }}</h3>
            <p>{{ service.description }}</p>
            <p class="price">Starting from ${{ service.base_price }}</p>
            <button class="btn-primary" @click="requestService(service.id)">Book Now</button>
          </div>
        </div>
      </div>
    </section>

    <!-- Service Request Modal -->
    <div v-if="showRequestModal" class="modal">
      <div class="modal-content">
        <h2>Request Service</h2>
        <form @submit.prevent="submitServiceRequest">
          <div class="form-group">
            <label>Preferred Date</label>
            <input v-model="requestForm.preferred_date" type="date" required />
          </div>
          <div class="form-group">
            <label>Preferred Time</label>
            <input v-model="requestForm.preferred_time" type="time" required />
          </div>
          <div class="form-group">
            <label>Address</label>
            <textarea v-model="requestForm.address" required></textarea>
          </div>
          <div class="form-group">
            <label>Notes (Optional)</label>
            <textarea v-model="requestForm.notes"></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="showRequestModal = false">Cancel</button>
            <button type="submit" class="btn-primary">Submit Request</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { customerAPI } from '@/services/api';

export default {
  name: 'CustomerDashboard',
  data() {
    return {
      profile: {},
      stats: {
        total_services: 0,
        completed_services: 0,
        active_requests: 0
      },
      activeRequests: [],
      recentServices: [],
      showRequestModal: false,
      requestForm: {
        service_id: null,
        preferred_date: '',
        preferred_time: '',
        address: '',
        notes: ''
      }
    };
  },
  created() {
    this.loadDashboard();
  },
  methods: {
    async loadDashboard() {
      try {
        const response = await customerAPI.getDashboard();
        const data = response.data;
        this.profile = data.profile;
        this.stats = data.stats;
        this.activeRequests = data.active_requests;
        this.recentServices = data.recent_services;
      } catch (error) {
        console.error('Error loading dashboard:', error);
        this.$toast.error('Failed to load dashboard data');
      }
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString();
    },
    async cancelRequest(requestId) {
      if (!confirm('Are you sure you want to cancel this request?')) return;
      
      try {
        await customerAPI.cancelRequest(requestId, 'Cancelled by customer');
        this.$toast.success('Request cancelled successfully');
        this.loadDashboard();
      } catch (error) {
        console.error('Error cancelling request:', error);
        this.$toast.error('Failed to cancel request');
      }
    },
    requestService(serviceId) {
      this.requestForm.service_id = serviceId;
      this.showRequestModal = true;
    },
    async submitServiceRequest() {
      try {
        await customerAPI.requestService(this.requestForm);
        this.$toast.success('Service requested successfully');
        this.showRequestModal = false;
        this.loadDashboard();
        this.requestForm = {
          service_id: null,
          preferred_date: '',
          preferred_time: '',
          address: '',
          notes: ''
        };
      } catch (error) {
        console.error('Error requesting service:', error);
        this.$toast.error('Failed to submit service request');
      }
    }
  }
};
</script>

<style scoped>
.dashboard {
  padding: 2rem;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.stat-card {
  background: #fff;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-card h3 {
  color: #666;
  margin-bottom: 0.5rem;
}

.stat-card p {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.requests-grid, .services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.request-card, .service-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.request-header {
  padding: 1rem;
  background: #f8f9fa;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.875rem;
}

.status.pending { background: #fff3cd; color: #856404; }
.status.accepted { background: #d4edda; color: #155724; }
.status.completed { background: #cce5ff; color: #004085; }

.request-details {
  padding: 1rem;
}

.request-actions {
  padding: 1rem;
  border-top: 1px solid #eee;
}

.service-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.service-content {
  padding: 1rem;
}

.price {
  color: #28a745;
  font-weight: bold;
  margin: 0.5rem 0;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-primary {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn-cancel {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  opacity: 0.9;
}
</style> 