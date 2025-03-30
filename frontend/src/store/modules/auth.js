import { authAPI } from '@/services/api'

const state = {
  token: localStorage.getItem('token') || null,
  user: JSON.parse(localStorage.getItem('user')) || null,
  isAuthenticated: false
}

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  },
  SET_USER(state, user) {
    state.user = user
    if (user) {
      localStorage.setItem('user', JSON.stringify(user))
    } else {
      localStorage.removeItem('user')
    }
  },
  SET_AUTH_STATUS(state, status) {
    state.isAuthenticated = status
  }
}

const actions = {
  async login({ commit }, credentials) {
    try {
      const response = await authAPI.login(credentials.email, credentials.password)
      const { token, user } = response.data
      commit('SET_TOKEN', token)
      commit('SET_USER', user)
      commit('SET_AUTH_STATUS', true)
      return user
    } catch (error) {
      throw error.response?.data || error
    }
  },

  async register({ commit }, userData) {
    try {
      const response = await authAPI.register(userData)
      const { token, user } = response.data
      commit('SET_TOKEN', token)
      commit('SET_USER', user)
      commit('SET_AUTH_STATUS', true)
      return user
    } catch (error) {
      throw error.response?.data || error
    }
  },

  async logout({ commit }) {
    await authAPI.logout()
    commit('SET_TOKEN', null)
    commit('SET_USER', null)
    commit('SET_AUTH_STATUS', false)
  },

  async checkAuth({ commit, state }) {
    if (!state.token) {
      commit('SET_AUTH_STATUS', false)
      return false
    }

    try {
      const response = await authAPI.getProfile()
      commit('SET_USER', response.data)
      commit('SET_AUTH_STATUS', true)
      return true
    } catch (error) {
      commit('SET_TOKEN', null)
      commit('SET_USER', null)
      commit('SET_AUTH_STATUS', false)
      return false
    }
  }
}

const getters = {
  isAuthenticated: state => state.isAuthenticated,
  user: state => state.user,
  isAdmin: state => state.user?.role === 'admin'
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 