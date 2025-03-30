import axios from 'axios'

const state = {
  reportData: null,
  loading: false,
  error: null
}

const getters = {
  reportData: state => state.reportData,
  loading: state => state.loading,
  error: state => state.error
}

const actions = {
  async generateReport({ commit }, params) {
    try {
      commit('SET_LOADING', true)
      const response = await axios.get('/api/admin/reports/generate', { params })
      commit('SET_REPORT_DATA', response.data)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async exportPDF({ commit }, params) {
    try {
      commit('SET_LOADING', true)
      const response = await axios.get('/api/admin/reports/export/pdf', {
        params,
        responseType: 'blob'
      })

      // Create a blob URL and trigger download
      const blob = new Blob([response.data], { type: 'application/pdf' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `fixrify-report-${new Date().toISOString().split('T')[0]}.pdf`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async exportExcel({ commit }, params) {
    try {
      commit('SET_LOADING', true)
      const response = await axios.get('/api/admin/reports/export/excel', {
        params,
        responseType: 'blob'
      })

      // Create a blob URL and trigger download
      const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `fixrify-report-${new Date().toISOString().split('T')[0]}.xlsx`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  }
}

const mutations = {
  SET_REPORT_DATA(state, data) {
    state.reportData = data
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