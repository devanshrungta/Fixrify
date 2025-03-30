import { createStore } from 'vuex'
import admin from './modules/admin'
import auth from './modules/auth'
import bookings from './modules/bookings'
import reports from './modules/reports'
import services from './modules/services'
import users from './modules/users'

export default createStore({
  state: {
    loading: false,
    error: null
  },
  mutations: {
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  actions: {
    setLoading({ commit }, loading) {
      commit('SET_LOADING', loading)
    },
    setError({ commit }, error) {
      commit('SET_ERROR', error)
    },
    clearError({ commit }) {
      commit('SET_ERROR', null)
    }
  },
  modules: {
    admin,
    auth,
    bookings,
    reports,
    services,
    users
  }
}) 