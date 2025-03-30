import axios from 'axios'

const state = {
  bookings: [],
  booking: null,
  loading: false,
  error: null
}

const mutations = {
  SET_BOOKINGS(state, bookings) {
    state.bookings = bookings
  },
  SET_BOOKING(state, booking) {
    state.booking = booking
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  }
}

const actions = {
  async fetchBookings({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.get('/api/bookings')
      commit('SET_BOOKINGS', response.data)
      commit('SET_ERROR', null)
    } catch (error) {
      commit('SET_ERROR', error.response?.data || error)
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async fetchBooking({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.get(`/api/bookings/${id}`)
      commit('SET_BOOKING', response.data)
      commit('SET_ERROR', null)
    } catch (error) {
      commit('SET_ERROR', error.response?.data || error)
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async createBooking({ commit }, bookingData) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.post('/api/bookings', bookingData)
      commit('SET_BOOKING', response.data)
      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.response?.data || error)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async updateBooking({ commit }, { id, bookingData }) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.put(`/api/bookings/${id}`, bookingData)
      commit('SET_BOOKING', response.data)
      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.response?.data || error)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async cancelBooking({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.put(`/api/bookings/${id}/cancel`)
      commit('SET_BOOKING', response.data)
      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.response?.data || error)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async completeBooking({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.put(`/api/bookings/${id}/complete`)
      commit('SET_BOOKING', response.data)
      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.response?.data || error)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  }
}

const getters = {
  allBookings: state => state.bookings,
  currentBooking: state => state.booking,
  isLoading: state => state.loading,
  error: state => state.error,
  userBookings: state => state.bookings.filter(booking => booking.user_id === state.auth.user?.id),
  serviceBookings: state => serviceId => state.bookings.filter(booking => booking.service_id === serviceId)
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 