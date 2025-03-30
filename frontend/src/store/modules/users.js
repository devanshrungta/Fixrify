import axios from 'axios'

const state = {
  users: [],
  loading: false,
  error: null
}

const getters = {
  allUsers: state => state.users,
  activeUsers: state => state.users.filter(user => user.active),
  adminUsers: state => state.users.filter(user => user.role === 'admin'),
  loading: state => state.loading,
  error: state => state.error
}

const actions = {
  async fetchUsers({ commit }) {
    try {
      commit('SET_LOADING', true)
      const response = await axios.get('/api/admin/users')
      commit('SET_USERS', response.data)
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async createUser({ commit }, userData) {
    try {
      commit('SET_LOADING', true)
      const response = await axios.post('/api/admin/users', userData)
      commit('ADD_USER', response.data)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async updateUser({ commit }, userData) {
    try {
      commit('SET_LOADING', true)
      const response = await axios.put(`/api/admin/users/${userData.id}`, userData)
      commit('UPDATE_USER', response.data)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async toggleUserStatus({ commit }, userId) {
    try {
      commit('SET_LOADING', true)
      const response = await axios.put(`/api/admin/users/${userId}/toggle-status`)
      commit('UPDATE_USER', response.data)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async deleteUser({ commit }, userId) {
    try {
      commit('SET_LOADING', true)
      await axios.delete(`/api/admin/users/${userId}`)
      commit('REMOVE_USER', userId)
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async changeUserPassword({ commit }, { userId, password }) {
    try {
      commit('SET_LOADING', true)
      await axios.post(`/api/admin/users/${userId}/change-password`, { password })
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  }
}

const mutations = {
  SET_USERS(state, users) {
    state.users = users
  },

  ADD_USER(state, user) {
    state.users.push(user)
  },

  UPDATE_USER(state, updatedUser) {
    const index = state.users.findIndex(u => u.id === updatedUser.id)
    if (index !== -1) {
      state.users.splice(index, 1, updatedUser)
    }
  },

  REMOVE_USER(state, userId) {
    state.users = state.users.filter(u => u.id !== userId)
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