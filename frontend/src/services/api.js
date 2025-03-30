import axios from 'axios';
import { useToast } from 'vue-toastification';

const toast = useToast();

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const message = error.response?.data?.message || 'An error occurred';
    toast.error(message);

    if (error.response?.status === 401) {
      // Try to refresh token
      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_URL}/auth/refresh`, {}, {
            headers: { Authorization: `Bearer ${refreshToken}` }
          });
          localStorage.setItem('token', response.data.access_token);
          error.config.headers.Authorization = `Bearer ${response.data.access_token}`;
          return api.request(error.config);
        } catch {
          // Refresh failed, logout user
          localStorage.clear();
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);
const api2 = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  responseType: 'blob'
});

// Add token to requests
api2.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Handle token expiration
api2.interceptors.response.use(
  (response) => response,
  async (error) => {
    const message = error.response?.data?.message || 'An error occurred';
    toast.error(message);

    if (error.response?.status === 401) {
      // Try to refresh token
      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_URL}/auth/refresh`, {}, {
            headers: { Authorization: `Bearer ${refreshToken}` }
          });
          localStorage.setItem('token', response.data.access_token);
          error.config.headers.Authorization = `Bearer ${response.data.access_token}`;
          return api.request(error.config);
        } catch {
          // Refresh failed, logout user
          localStorage.clear();
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (email, password) => api.post('/auth/login', { email, password }),
  adminLogin: (email, password) => api.post('/auth/admin/login', { email, password }),
  getProfile: () => api.get('/auth/profile'),
  updateProfile: (data) => api.put('/auth/profile', data),
  logout: () => api.get('/auth/logout'),
};

// Customer API
export const customerAPI = {
  getDashboard: () => api.get('/customer/dashboard'),
  getRequests: () => api.get('/customer/requests'),
  createRequest: (data) => api.post('/customer/services/request', data),
  cancelRequest: (id) => api.post(`/customer/requests/${id}/cancel`),
  updateProfile: (data) => api.put('/customer/profile', data),
  getProfile: () => api.get('/customer/profile'),
  getProfessionals: (serviceID) => api.get(`/customer/professionals/${serviceID}`)
};

// Professional API
export const professionalAPI = {
  getDashboard: () => api.get('/professional/dashboard'),
  getRequests: () => api.get('/professional/requests'),
  acceptRequest: (id) => api.post(`/professional/requests/${id}/accept`),
  rejectRequest: (id, reason) => api.post(`/professional/requests/${id}/reject`, { reason }),
  completeRequest: (id) => api.post(`/professional/requests/${id}/complete`),
  updateProfile: (data) => api.put('/professional/profile', data),
  getProfile: () => api.get('/professional/profile'),
};

// Admin API
export const adminAPI = {
  getDashboard: () => api.get('/admin/dashboard'),
  getUsers: () => api.get('/admin/users'),
  blockUser: (id) => api.post(`/admin/users/${id}/block`),
  unblockUser: (id) => api.post(`/admin/users/${id}/unblock`),
  getServices: () => api.get('/admin/services'),
  createService: (data) => api.post('/admin/services', data),
  updateService: (id, data) => api.put(`/admin/services/${id}`, data),
  deleteService: (id) => api.delete(`/admin/services/${id}`),
  toggleServiceStatus: (id, serviceData) => api.put(`/admin/services/${id}`, serviceData),
  getPendingProfessionals: () => api.get('/admin/professionals/pending'),
  approveProfessional: (id) => api.post(`/admin/professionals/${id}/approve`),
  rejectProfessional: (id, reason) => api.post(`/admin/professionals/${id}/reject`, { reason }),
  exportServiceRequests: () => api.post('/admin/exports/service-requests'),
  getExport: (taskId) => api2.get(`/admin/exports/${taskId}`),
};

// Services API
export const servicesAPI = {
  getAll: () => api.get('/services/'),
  getById: (id) => api.get(`/services/${id}`),
  searchServices: (query) => api.get(`/services/search?q=${query}`),
  getCategories: () => api.get('/services/categories'),
  createService: (formData) => api.post('/services', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }),
  updateService: (id, formData) => api.put(`/services/${id}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }),
  deleteService: (id) => api.delete(`/admin/services/${id}`)
};

export default api; 