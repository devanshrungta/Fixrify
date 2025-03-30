import axios from 'axios'

const state = {
  dashboardStats: {
    totalUsers: 0,
    activeServices: 0,
    pendingBookings: 0,
    totalRevenue: 0
  },
  recentBookings: [],
  lastBackup: null,
  loading: false,
  error: null
}

const getters = {
  totalUsers: state => state.dashboardStats.total_users,
  totalCustomers: state => state.dashboardStats.total_customers,
  totalProfessionals: state => state.dashboardStats.total_professionals,
  activeServices: state => state.dashboardStats.total_services,
  completedBookings: state => state.dashboardStats.completed_requests,
  pendingBookings: state => state.dashboardStats.pending_requests,
  totalRequests: state => state.dashboardStats.total_requests,
  recentBookings: state => state.recentBookings,
  lastBackup: state => state.lastBackup,
  loading: state => state.loading,
  error: state => state.error
}

const actions = {
  async fetchDashboardStats({ commit }) {
    try {
      const response = await axios.get('/api/admin/dashboard')
      commit('SET_DASHBOARD_STATS', response.data)
    } catch (error) {
      console.error('Error fetching dashboard stats:', error)
      throw error
    }
  },

  async fetchBookings({ commit }) {
    try {
      const response = await axios.get('/api/admin/bookings')
      commit('SET_RECENT_BOOKINGS', response.data)
    } catch (error) {
      console.error('Error fetching bookings:', error)
      throw error
    }
  },

  async fetchSystemStatus({ commit }) {
    try {
      const response = await axios.get('/api/admin/system/status')
      commit('SET_LAST_BACKUP', response.data.lastBackup)
    } catch (error) {
      console.error('Error fetching system status:', error)
      throw error
    }
  }
}

const mutations = {
  SET_DASHBOARD_STATS(state, stats) {
    state.dashboardStats = stats
  },

  SET_RECENT_BOOKINGS(state, bookings) {
    state.recentBookings = bookings
  },

  SET_LAST_BACKUP(state, timestamp) {
    state.lastBackup = timestamp
  },

  SET_LOADING(state, loading) {
    state.loading = loading
  },

  SET_ERROR(state, error) {
    state.error = error
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
} 