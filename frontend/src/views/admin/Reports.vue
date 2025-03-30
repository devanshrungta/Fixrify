<template>
  <div class="admin-reports">
    <div class="container">
      <h1 class="mb-4">Reports & Analytics</h1>

      <!-- Date Range Filter -->
      <div class="card mb-4">
        <div class="card-body">
          <div class="row align-items-end">
            <div class="col-md-4">
              <label class="form-label">Date Range</label>
              <select v-model="dateRange" class="form-select">
                <option value="today">Today</option>
                <option value="week">Last 7 Days</option>
                <option value="month">Last 30 Days</option>
                <option value="year">Last Year</option>
                <option value="custom">Custom Range</option>
              </select>
            </div>
            <div v-if="dateRange === 'custom'" class="col-md-4">
              <label class="form-label">Start Date</label>
              <input
                v-model="startDate"
                type="date"
                class="form-control"
              />
            </div>
            <div v-if="dateRange === 'custom'" class="col-md-4">
              <label class="form-label">End Date</label>
              <input
                v-model="endDate"
                type="date"
                class="form-control"
              />
            </div>
            <div class="col-md-4">
              <button
                class="btn btn-primary w-100"
                :disabled="loading"
                @click="generateReport"
              >
                Generate Report
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="alert alert-danger">
        {{ error }}
      </div>

      <!-- Report Content -->
      <div v-else-if="reportData" class="report-content">
        <!-- Revenue Overview -->
        <div class="row mb-4">
          <div class="col-md-6">
            <div class="card h-100">
              <div class="card-header">
                <h5 class="card-title mb-0">Revenue Overview</h5>
              </div>
              <div class="card-body">
                <canvas ref="revenueChart"></canvas>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="card h-100">
              <div class="card-header">
                <h5 class="card-title mb-0">Service Bookings</h5>
              </div>
              <div class="card-body">
                <canvas ref="bookingsChart"></canvas>
              </div>
            </div>
          </div>
        </div>

        <!-- Key Metrics -->
        <div class="row mb-4">
          <div class="col-md-3">
            <div class="card">
              <div class="card-body">
                <h6 class="card-subtitle mb-2 text-muted">Total Revenue</h6>
                <h3 class="card-title">${{ reportData.totalRevenue }}</h3>
                <p class="card-text text-success">
                  <i class="fas fa-arrow-up"></i>
                  {{ reportData.revenueGrowth }}% from previous period
                </p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card">
              <div class="card-body">
                <h6 class="card-subtitle mb-2 text-muted">Total Bookings</h6>
                <h3 class="card-title">{{ reportData.totalBookings }}</h3>
                <p class="card-text text-success">
                  <i class="fas fa-arrow-up"></i>
                  {{ reportData.bookingsGrowth }}% from previous period
                </p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card">
              <div class="card-body">
                <h6 class="card-subtitle mb-2 text-muted">New Users</h6>
                <h3 class="card-title">{{ reportData.newUsers }}</h3>
                <p class="card-text text-success">
                  <i class="fas fa-arrow-up"></i>
                  {{ reportData.userGrowth }}% from previous period
                </p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card">
              <div class="card-body">
                <h6 class="card-subtitle mb-2 text-muted">Avg. Service Rating</h6>
                <h3 class="card-title">{{ reportData.avgRating }}/5</h3>
                <p class="card-text text-success">
                  <i class="fas fa-arrow-up"></i>
                  {{ reportData.ratingGrowth }}% from previous period
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Popular Services -->
        <div class="card mb-4">
          <div class="card-header">
            <h5 class="card-title mb-0">Popular Services</h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table">
                <thead>
                  <tr>
                    <th>Service</th>
                    <th>Bookings</th>
                    <th>Revenue</th>
                    <th>Avg. Rating</th>
                    <th>Trend</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="service in reportData.popularServices" :key="service.id">
                    <td>{{ service.name }}</td>
                    <td>{{ service.bookings }}</td>
                    <td>${{ service.revenue }}</td>
                    <td>{{ service.rating }}/5</td>
                    <td>
                      <span :class="getTrendClass(service.trend)">
                        <i :class="getTrendIcon(service.trend)"></i>
                        {{ service.trend }}%
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Export Options -->
        <div class="d-flex justify-content-end gap-2">
          <button class="btn btn-secondary" @click="exportPDF">
            <i class="fas fa-file-pdf me-2"></i>
            Export as PDF
          </button>
          <button class="btn btn-success" @click="exportExcel">
            <i class="fas fa-file-excel me-2"></i>
            Export as Excel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import Chart from 'chart.js/auto'

export default {
  name: 'AdminReports',
  setup() {
    const store = useStore()
    const loading = ref(false)
    const error = ref(null)
    const dateRange = ref('month')
    const startDate = ref('')
    const endDate = ref('')
    const reportData = ref(null)
    const revenueChart = ref(null)
    const bookingsChart = ref(null)

    const generateReport = async () => {
      try {
        loading.value = true
        error.value = null

        const params = {
          dateRange: dateRange.value,
          ...(dateRange.value === 'custom' && {
            startDate: startDate.value,
            endDate: endDate.value
          })
        }

        const data = await store.dispatch('reports/generateReport', params)
        reportData.value = data

        // Initialize charts after data is loaded
        initializeCharts()
      } catch (err) {
        error.value = err.message || 'Failed to generate report'
      } finally {
        loading.value = false
      }
    }

    const initializeCharts = () => {
      if (revenueChart.value) {
        new Chart(revenueChart.value, {
          type: 'line',
          data: {
            labels: reportData.value.revenueData.labels,
            datasets: [{
              label: 'Revenue',
              data: reportData.value.revenueData.values,
              borderColor: '#0d6efd',
              tension: 0.1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        })
      }

      if (bookingsChart.value) {
        new Chart(bookingsChart.value, {
          type: 'bar',
          data: {
            labels: reportData.value.bookingsData.labels,
            datasets: [{
              label: 'Bookings',
              data: reportData.value.bookingsData.values,
              backgroundColor: '#198754'
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        })
      }
    }

    const getTrendClass = (trend) => {
      return trend > 0 ? 'text-success' : trend < 0 ? 'text-danger' : 'text-muted'
    }

    const getTrendIcon = (trend) => {
      return trend > 0 ? 'fas fa-arrow-up' : trend < 0 ? 'fas fa-arrow-down' : 'fas fa-minus'
    }

    const exportPDF = async () => {
      try {
        loading.value = true
        await store.dispatch('reports/exportPDF', {
          dateRange: dateRange.value,
          startDate: startDate.value,
          endDate: endDate.value
        })
      } catch (err) {
        error.value = err.message || 'Failed to export PDF'
      } finally {
        loading.value = false
      }
    }

    const exportExcel = async () => {
      try {
        loading.value = true
        await store.dispatch('reports/exportExcel', {
          dateRange: dateRange.value,
          startDate: startDate.value,
          endDate: endDate.value
        })
      } catch (err) {
        error.value = err.message || 'Failed to export Excel'
      } finally {
        loading.value = false
      }
    }

    // Generate initial report
    onMounted(() => {
      generateReport()
    })

    // Watch for date range changes
    watch(dateRange, (newValue) => {
      if (newValue !== 'custom') {
        generateReport()
      }
    })

    return {
      loading,
      error,
      dateRange,
      startDate,
      endDate,
      reportData,
      revenueChart,
      bookingsChart,
      generateReport,
      getTrendClass,
      getTrendIcon,
      exportPDF,
      exportExcel
    }
  }
}
</script>

<style scoped>
.card {
  border: none;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

canvas {
  min-height: 300px;
}

.trend-icon {
  margin-right: 0.5rem;
}

.table th {
  font-weight: 600;
}
</style> 