<template>
  <div class="admin-services">
    <div class="container">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Manage Service Categories</h1>
        <button class="btn btn-primary" @click="showAddModal">
          Add New Service
        </button>
      </div>

      <div class="search-bar mb-3">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Search services..." 
            class="form-control"
            @input="handleSearch"/>
      </div>

      <!-- Loading and Error States -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="error" class="alert alert-danger">
        {{ error }}
      </div>

      <!-- Services Table -->
      <div v-else class="card">
        <div class="card-body">
          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Image</th>
                  <th>Name</th>
                  <th>Category</th>
                  <th>Price</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="service in filteredServices" :key="service.id">
                  <td>{{ service.id }}</td>
                  <td>
                    <img
                      :src="'https://picsum.photos/200/200?random=' + service.id"
                      :alt="service.name"
                      class="service-thumbnail"
                    />
                  </td>
                  <td>{{ service.name }}</td>
                  <td>{{ service.category }}</td>
                  <td>${{ service.base_price }}</td>
                  <td>
                    <span
                      :class="[
                        'badge',
                        service.is_active ? 'bg-success' : 'bg-danger'
                      ]"
                    >
                      {{ service.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td>
                    <button
                      class="btn btn-sm btn-info me-2"
                      @click="editService(service)"
                    >
                      Edit
                    </button>
                    <button
                      class="btn btn-sm btn-danger me-2"
                      @click="deleteService(service)"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Add/Edit Service Modal -->
      <div
        id="serviceModal"
        class="modal fade"
        tabindex="-1"
        aria-labelledby="serviceModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 id="serviceModalLabel" class="modal-title">
                {{ isEditing ? 'Edit Service Category' : 'Add New Service Category' }}
              </h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="saveService">
                <div class="mb-3">
                  <label for="serviceName" class="form-label">Name</label>
                  <input
                    id="serviceName"
                    v-model="serviceForm.name"
                    type="text"
                    class="form-control"
                    required
                  />
                </div>

                <div class="mb-3">
                  <label for="serviceCategory" class="form-label">Category</label>
                  <select
                    id="serviceCategory"
                    v-model="serviceForm.category"
                    class="form-select"
                    required
                  >
                    <option value="">Select a category</option>
                    <option
                      v-for="category in categories"
                      :key="category"
                      :value="category"
                    >
                      {{ category }}
                    </option>
                  </select>
                </div>

                <div class="mb-3">
                  <label
                    for="serviceDescription"
                    class="form-label"
                  >Description</label>
                  <textarea
                    id="serviceDescription"
                    v-model="serviceForm.description"
                    class="form-control"
                    rows="3"
                    required
                  ></textarea>
                </div>

                <div class="row">
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label for="servicePrice" class="form-label">Price ($)</label>
                      <input
                        id="servicePrice"
                        v-model="serviceForm.price"
                        type="number"
                        class="form-control"
                        min="0"
                        step="0.01"
                        required
                      />
                    </div>
                    <div class="mb-3">
                      <label for="serviceStatus" class="form-label mx-1">Status</label>
                      <input
                        id="serviceStatus"
                        v-model="serviceForm.is_active"
                        type="checkbox"
                        class="form-check-input mx-3"
                      />
                      <label class="form-check-label" for="serviceStatus">
                        {{ serviceForm.is_active ? 'Active' : 'Inactive' }}
                      </label>
                    </div>
                  </div>
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                Cancel
              </button>
              <button type="button" class="btn btn-primary" @click="saveService">
                {{ isEditing ? 'Update' : 'Create' }}
              </button>
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
import { Modal } from 'bootstrap'
import {adminAPI} from '@/services/api'

export default {
  name: 'AdminServices',
  setup() {
    const searchQuery = ref('')
    const services = ref([])
    const store = useStore()
    const loading = ref(false)
    const error = ref(null)
    const isEditing = ref(false)
    const serviceModal = ref(null)
    const categories = ref([
      'Plumbing',
      'Electrical',
      'Carpentry',
      'Cleaning',
      'Painting',
      'HVAC',
      'Landscaping',
      'General Maintenance'
    ])

    const serviceForm = ref({
      id: null,
      name: '',
      category: '',
      description: '',
      price: 0,
      duration: 0,
      imageUrl: '',
      includes: [''],
      is_active: true
    })

    const fetchAdminServices = async () => {
      try {
        loading.value = true;
        const response = await adminAPI.getServices(); // Call the admin-specific API
        services.value = response.data;  // Store the fetched services in the ref
      } catch (err) {
        error.value = err.message || 'Failed to fetch services';
      } finally {
        loading.value = false;
      }
    };

    const resetForm = () => {
      serviceForm.value = {
        id: null,
        name: '',
        category: '',
        description: '',
        price: 0,
        duration: 0,
        imageUrl: '',
        includes: ['']
      }
      isEditing.value = false
    }

    const showAddModal = () => {
      resetForm()
      serviceModal.value.show()
    }

    const editService = (service) => {
      serviceForm.value = { ...service }
      isEditing.value = true
      serviceModal.value.show()
    }

    const handleImageUpload = (event) => {
      const file = event.target.files[0]
      if (file) {
        // Handle image upload logic here
        // You might want to use FormData to upload the image to your server
        // and get back the URL to store in serviceForm.imageUrl
      }
    }

    const addIncludedItem = () => {
      serviceForm.value.includes.push('')
    }

    const removeIncludedItem = (index) => {
      serviceForm.value.includes.splice(index, 1)
    }

    const saveService = async () => {
      try {
        loading.value = true
        error.value = null

        if (isEditing.value) {
          await store.dispatch('services/updateService', serviceForm.value)
        } else {
          await store.dispatch('services/createService', serviceForm.value)
        }

        serviceModal.value.hide()
        resetForm()
      } catch (err) {
        error.value = err.message || 'Failed to save service'
      } finally {
        loading.value = false
      }
    }

    const toggleServiceStatus = async (service) => {
      try {
        loading.value = true
        error.value = null
        await store.dispatch('services/toggleServiceStatus', service.id)
      } catch (err) {
        error.value = err.message || 'Failed to toggle service status'
      } finally {
        loading.value = false
      }
    }

    const filteredServices = computed(() => {
      if (!searchQuery.value) return services.value

      const query = searchQuery.value.toLowerCase()
      
      return services.value.filter(service => {
        const name = service.name ? service.name.toLowerCase() : ''
        const description = service.description ? service.description.toLowerCase() : ''
        const category = service.category ? service.category.toLowerCase() : ''

        return name.includes(query) || description.includes(query) || category.includes(query)
      })
    })
    const deleteService = async (service) => {
      // Confirm with the user before deleting
      const confirmDelete = confirm(`Are you sure you want to delete the service "${service.name}"? This action cannot be undone.`);
      
      if (!confirmDelete) {
        return; // Do nothing if the user cancels the action
      }

      try {
        loading.value = true;
        error.value = null;

        // Make the API call to delete the service
        await store.dispatch('services/deleteService', service.id);

        // Remove the service from the local list
        services.value = services.value.filter((s) => s.id !== service.id);

        // Optionally, show a success message
        alert('Service deleted successfully');
      } catch (err) {
        error.value = err.message || 'Failed to delete the service';
      } finally {
        loading.value = false;
      }
    };


    onMounted(() => {
      serviceModal.value = new Modal(document.getElementById('serviceModal'))
      fetchAdminServices()
    })

    return {
      searchQuery,
      loading,
      error,
      isEditing,
      categories,
      serviceForm,
      services,
      showAddModal,
      editService,
      handleImageUpload,
      addIncludedItem,
      removeIncludedItem,
      saveService,
      toggleServiceStatus,
      filteredServices,
      deleteService
    }
  }
}
</script>

<style scoped>
.service-thumbnail {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 4px;
}

.modal-dialog {
  max-width: 600px;
}
</style> 