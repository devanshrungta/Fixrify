<template>
  <div class="admin-dashboard">
    <div class="container">
      <h1 class="mb-4">Admin Dashboard</h1>

      <div class="row">
        <div class="col-md-3 mb-4">
          <div class="card bg-primary text-white">
            <div class="card-body">
              <h5 class="card-title">Total Users</h5>
              <h2 class="card-text">{{ totalUsers }}</h2>
              <h5 class="card-title">Total Customers</h5>
              <h2 class="card-text">{{ totalCustomers }}</h2>
              <h5 class="card-title">Total Professionals</h5>
              <h2 class="card-text">{{ totalProfessionals }}</h2>
            </div>
          </div>
        </div>

        <div class="col-md-3 mb-4">
          <div class="card bg-success text-white">
            <div class="card-body">
              <h5 class="card-title">Total Services</h5>
              <h2 class="card-text">{{ activeServices }}</h2>

            </div>
          </div>
        </div>

        <div class="col-md-3 mb-4">
          <div class="card bg-info text-white">
            <div class="card-body">
              <h5 class="card-title">Total Requests</h5>
              <h2 class="card-text">{{ totalRequests }}</h2>
              <h5 class="card-title">Completed Bookings</h5>
              <h2 class="card-text">{{ completedBookings }}</h2>
              <h5 class="card-title">Pending Bookings</h5>
              <h2 class="card-text">{{ pendingBookings }}</h2>
            </div>
          </div>
        </div>

        <div class="col-md-3 mb-4">
          <div class="card bg-warning text-white">
            <div class="card-body">
              <h5 class="card-title">Placeholder for further data</h5>
              <h2 class="card-text">  </h2>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-md-8">
          <div class="card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0">Recent Bookings</h5>
              <button class="btn btn-sm btn-primary" @click="refreshBookings">
                Refresh
              </button>
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

              <div v-else class="table-responsive">
                <table class="table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Service</th>
                      <th>Customer</th>
                      <th>Professional</th>
                      <th>Date</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="booking in recentBookings.slice(-5)" :key="booking.id">
                      <td>{{ booking.id }}</td>
                      <td>{{ booking.service.name }}</td>
                      <td>{{ booking.customer.name }}</td>
                      <td>{{ booking.professional.name }}</td>
                      <td>{{ (booking.date) }}</td>
                      <td>
                        <span :class="getStatusBadgeClass(booking.status)">
                          {{ booking.status }}
                        </span>
                      </td>
                      <td>
                        <button
                          v-if="booking.status === 'pending'"
                          class="btn btn-sm btn-success me-2"
                          @click="completeBooking(booking.id)"
                        >
                          Complete
                        </button>
                        <button
                          v-if="booking.status === 'pending'"
                          class="btn btn-sm btn-danger"
                          @click="cancelBooking(booking.id)"
                        >
                          Cancel
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="mb-0">Quick Actions</h5>
            </div>
            <div class="card-body">
              <div class="d-grid gap-2">
                <router-link to="/admin/services" class="btn btn-primary">
                  Manage Services
                </router-link>
                <router-link to="/admin/users" class="btn btn-primary">
                  Manage Users
                </router-link>
                <router-link to="/admin/reports" class="btn btn-primary">
                  View Reports
                </router-link>
                <button 
                  class="btn btn-success" 
                  @click="generateExport"
                  :disabled="exporting"
                >
                  {{ exporting ? 'Generating...' : 'Export Service Requests' }}
                </button>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-header">
              <h5 class="mb-0">System Status</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label class="form-label">Server Status</label>
                <p class="text-success">Online</p>
              </div>
              <div class="mb-3">
                <label class="form-label">Database Status</label>
                <p class="text-success">Connected</p>
              </div>
              <div class="mb-3">
                <label class="form-label">Last Backup</label>
                <p>{{ lastBackup }}</p>
              </div>
              <div class="mb-3">
                <label class="form-label">System Version</label>
                <p>v1.0.0</p>
              </div>
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
import { adminAPI } from '@/services/api'
import { useToast } from 'vue-toastification'

export default {
  name: 'AdminDashboard',
  setup() {
    const store = useStore()
    const toast = useToast()
    const loading = ref(false)
    const error = ref(null)
    const exporting = ref(false)

    const totalUsers = computed(() => store.getters['admin/totalUsers'])
    const totalCustomers = computed(() => store.getters['admin/totalCustomers'])
    const totalProfessionals = computed(() => store.getters['admin/totalProfessionals'])
    const activeServices = computed(() => store.getters['admin/activeServices'])
    const completedBookings = computed(() => store.getters['admin/completedBookings'])
    const pendingBookings = computed(() => store.getters['admin/pendingBookings'])
    const totalRequests = computed(() => store.getters['admin/totalRequests'])
    const recentBookings = computed(() => store.getters['admin/recentBookings'])
    const lastBackup = computed(() => store.getters['admin/lastBackup'])

    const getStatusBadgeClass = (status) => {
      const classes = {
        pending: 'badge bg-warning',
        completed: 'badge bg-success',
        cancelled: 'badge bg-danger'
      }
      return classes[status] || 'badge bg-secondary'
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString()
    }

    const refreshBookings = async () => {
      loading.value = true
      error.value = null
      try {
        await store.dispatch('admin/fetchBookings')
      } catch (err) {
        error.value = err.message || 'Failed to refresh bookings'
      } finally {
        loading.value = false
      }
    }

    const completeBooking = async (bookingId) => {
      if (!confirm('Are you sure you want to mark this booking as completed?')) {
        return
      }

      try {
        await store.dispatch('bookings/completeBooking', bookingId)
      } catch (err) {
        error.value = err.message || 'Failed to complete booking'
      }
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

    const generateExport = async () => {
      try {
        exporting.value = true;
        // Start the export task
        const response = await adminAPI.exportServiceRequests();
        const taskId = response.data.task_id;
        
        // Function to stop polling once the task is completed or failed
        let isPolling = true;

        // Poll for the export to be ready
        const checkExport = async () => {
          if (!isPolling) return;  // Stop polling if the task is completed or failed

          try {
            const exportResponse = await adminAPI.getExport(taskId);
            // If the export file exists (i.e., the data is returned), then the task is complete
            if (exportResponse.status === 200) {
              // Create a download link
              const link = document.createElement('a');
              link.href = `/api/admin/exports/${taskId}`;
              link.download = 'service-requests.csv';
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
              toast.success('Export downloaded successfully');
              exporting.value = false;
              isPolling = false;  // Stop polling once the task is completed
            }
          } catch (error) {
            // If error status is 404, it means the export is not ready yet, continue polling
            if (error.response && error.response.status === 404) {
              // Continue polling if the export is not ready yet
              setTimeout(checkExport, 2000);
            } else {
              // Handle other errors (e.g., server issues)
              console.error('Error checking export status:', error);
              toast.error('Failed to check export status');
              exporting.value = false;
              isPolling = false;  // Stop polling in case of other errors
            }
          }
        };

        // Start polling
        checkExport();
      } catch (error) {
        console.error('Error generating export:', error);
        toast.error('Failed to generate export');
        exporting.value = false;
      }
    };


    onMounted(async () => {
      loading.value = true
      error.value = null
      try {
        await Promise.all([
          store.dispatch('admin/fetchDashboardStats'),
          store.dispatch('admin/fetchBookings')
        ])
      } catch (err) {
        error.value = err.message || 'Failed to fetch dashboard data'
      } finally {
        loading.value = false
      }
    })

    return {
      totalUsers,
      totalCustomers,
      totalProfessionals,
      activeServices,
      completedBookings,
      pendingBookings,
      totalRequests,
      recentBookings,
      lastBackup,
      loading,
      error,
      getStatusBadgeClass,
      formatDate,
      refreshBookings,
      completeBooking,
      cancelBooking,
      exporting,
      generateExport
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

.badge {
  font-size: 0.875rem;
  padding: 0.5em 0.75em;
}
</style> 