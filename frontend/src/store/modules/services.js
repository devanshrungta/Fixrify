import { servicesAPI } from '@/services/api'
import { adminAPI } from '../../services/api'

const state = {
  services: [],
  loading: false,
  error: null
}

const getters = {
  allServices: state => state.services,
  activeServices: state => state.services.filter(service => service.active),
  loading: state => state.loading,
  error: state => state.error
}

const actions = {
  async fetchServices({ commit }) {
    try {
      commit('SET_LOADING', true)
      const response = await servicesAPI.getAll()
      commit('SET_SERVICES', response.data)
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async createService({ commit }, serviceData) {
    try {
      commit('SET_LOADING', true)
      const formData = new FormData()
      
      // Add all service data to FormData
      Object.keys(serviceData).forEach(key => {
        if (key === 'includes') {
          formData.append(key, JSON.stringify(serviceData[key]))
        } else {
          formData.append(key, serviceData[key])
        }
      })

      const response = await adminAPI.createService(formData)
      commit('ADD_SERVICE', response.data)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async updateService({ commit }, serviceData) {
    try {
      commit('SET_LOADING', true)
      const formData = new FormData()
      
      // Add all service data to FormData
      Object.keys(serviceData).forEach(key => {
        if (key === 'includes') {
          formData.append(key, JSON.stringify(serviceData[key]))
        } else {
          formData.append(key, serviceData[key])
        }
      })

      const response = await adminAPI.updateService(serviceData.id, formData)
      commit('UPDATE_SERVICE', response.data)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async toggleServiceStatus({ commit }, serviceId) {
    try {
      commit('SET_LOADING', true)
      
      // Find the service from the store state
      const service = state.services.find(s => s.id === serviceId);
      console.log(service)
      
      if (service) {
        // Toggle the is_active status
        const updatedServiceData = {
          ...service,
          is_active: !service.is_active
        };
  
        // Call the API to update the service with the new status
        const response = await adminAPI.toggleServiceStatus(serviceId, updatedServiceData);
        commit('UPDATE_SERVICE', response.data);  // Update the service in the store
        return response.data;
      } else {
        throw new Error("Service not found.");
      }
  
    } catch (error) {
      commit('SET_ERROR', error.message);
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  async deleteService({ commit }, serviceId) {
    try {
      commit('SET_LOADING', true)
      await servicesAPI.deleteService(serviceId)
      commit('REMOVE_SERVICE', serviceId)
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  }
}

const mutations = {
  SET_SERVICES(state, services) {
    state.services = services
  },

  ADD_SERVICE(state, service) {
    state.services.push(service)
  },

  UPDATE_SERVICE(state, updatedService) {
    const index = state.services.findIndex(s => s.id === updatedService.id)
    if (index !== -1) {
      state.services.splice(index, 1, updatedService)
    }
  },

  REMOVE_SERVICE(state, serviceId) {
    state.services = state.services.filter(s => s.id !== serviceId)
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