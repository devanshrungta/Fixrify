<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>Professional Dashboard</h1>
      <div class="stats">
        <div class="stat-card">
          <h3>Total Jobs</h3>
          <p>{{ stats.total_jobs }}</p>
        </div>
        <div class="stat-card">
          <h3>Active Requests</h3>
          <p>{{ stats.active_requests }}</p>
        </div>
        <div class="stat-card">
          <h3>Pending Requests</h3>
          <p>{{ stats.pending_requests }}</p>
        </div>
        <div class="stat-card">
          <h3>Rating</h3>
          <p>{{ stats.average_rating || 'N/A' }} ⭐</p>
        </div>
      </div>
    </header>

    <section class="service-requests">
      <div class="section-header">
        <h2>Service Requests</h2>
        <div class="filter-buttons">
          <button 
            v-for="status in ['pending', 'accepted', 'completed']" 
            :key="status"
            :class="['filter-btn', { active: currentFilter === status }]"
            @click="filterRequests(status)"
          >
            {{ status.charAt(0).toUpperCase() + status.slice(1) }}
          </button>
        </div>
      </div>

      <div v-if="filteredRequests.length" class="requests-grid">
        <div v-for="request in filteredRequests" :key="request.id" class="request-card">
          <div class="request-header">
            <h3>{{ request.service.name }}</h3>
            <span :class="['status', request.status]">{{ request.status }}</span>
          </div>
          <div class="request-details">
            <p><strong>Customer:</strong> {{ request.customer.name }}</p>
            <p><strong>Date:</strong> {{ formatDate(request.preferred_date) }}</p>
            <p><strong>Time:</strong> {{ request.preferred_time }}</p>
            <p><strong>Address:</strong> {{ request.address }}</p>
            <p v-if="request.notes"><strong>Notes:</strong> {{ request.notes }}</p>
          </div>
          <div class="request-actions">
            <template v-if="request.status === 'pending'">
              <button class="btn-primary" @click="acceptRequest(request.id)">Accept</button>
              <button class="btn-cancel" @click="rejectRequest(request.id)">Reject</button>
            </template>
            <button 
              v-if="request.status === 'accepted'" 
              class="btn-success" 
              @click="completeRequest(request.id)"
            >
              Mark as Complete
            </button>
          </div>
        </div>
      </div>
      <p v-else>No {{ currentFilter }} requests found</p>
    </section>

    <!-- Rejection Modal -->
    <div v-if="showRejectionModal" class="modal">
      <div class="modal-content">
        <h2>Reject Request</h2>
        <form @submit.prevent="submitRejection">
          <div class="form-group">
            <label>Reason for Rejection</label>
            <textarea v-model="rejectionReason" required></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="showRejectionModal = false">Cancel</button>
            <button type="submit" class="btn-primary">Submit</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { professionalAPI } from '@/services/api';

export default {
  name: 'ProfessionalDashboard',
  data() {
    return {
      stats: {
        total_jobs: 0,
        completed_jobs: 0,
        rating: null
      },
      requests: [],
      currentFilter: 'pending',
      showRejectionModal: false,
      rejectionReason: '',
      pendingRejectionId: null
    };
  },
  computed: {
    filteredRequests() {
      return this.requests.filter(request => request.status === this.currentFilter);
    }
  },
  created() {
    this.loadDashboard();
    console.log('Dashboard created');
  },
  methods: {
    async loadDashboard() {
      try {
        const response = await professionalAPI.getDashboard();
        console.log('Dashboard data:', response.data);
        const data = response.data;
        console.log('Data:', data);
        this.requests = [
          ...data.active_requests.map(request => ({ ...request, status: 'accepted' })),
          ...data.pending_requests.map(request => ({ ...request, status: 'pending' })),
          ...data.completed_services.map(request => ({ ...request, status: 'completed' }))
        ];
        console.log('Requests:', this.requests);

    this.stats = data.stats;
    console.log('Stats:', this.stats);
      } catch (error) {
        console.error('Error loading dashboard:', error);
        this.$toast.error('Failed to load dashboard data');
      }
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString();
    },
    filterRequests(status) {
      this.currentFilter = status;
    },
    async acceptRequest(requestId) {
      try {
        await professionalAPI.acceptRequest(requestId);
        this.$toast.success('Request accepted successfully');
        this.loadDashboard();
      } catch (error) {
        console.error('Error accepting request:', error);
        this.$toast.error('Failed to accept request');
      }
    },
    rejectRequest(requestId) {
      this.pendingRejectionId = requestId;
      this.showRejectionModal = true;
    },
    async submitRejection() {
      try {
        await professionalAPI.rejectRequest(this.pendingRejectionId, this.rejectionReason);
        this.$toast.success('Request rejected successfully');
        this.showRejectionModal = false;
        this.rejectionReason = '';
        this.pendingRejectionId = null;
        this.loadDashboard();
      } catch (error) {
        console.error('Error rejecting request:', error);
        this.$toast.error('Failed to reject request');
      }
    },
    async completeRequest(requestId) {
      if (!confirm('Are you sure you want to mark this request as complete?')) return;
      
      try {
        await professionalAPI.completeRequest(requestId);
        this.$toast.success('Request marked as complete');
        this.loadDashboard();
      } catch (error) {
        console.error('Error completing request:', error);
        this.$toast.error('Failed to complete request');
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

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.filter-buttons {
  display: flex;
  gap: 0.5rem;
}

.filter-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
}

.filter-btn.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.requests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.request-card {
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

.request-details p {
  margin-bottom: 0.5rem;
}

.request-actions {
  padding: 1rem;
  border-top: 1px solid #eee;
  display: flex;
  gap: 0.5rem;
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

.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-height: 100px;
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

.btn-success {
  background: #28a745;
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