<template>
  <div class="admin-users">
    <div class="container">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Manage Users</h1>
        <div class="d-flex gap-2">
          <div class="input-group">
            <input
              v-model="searchQuery"
              type="text"
              class="form-control"
              placeholder="Search users..."
              @input="handleSearch"
            />
            <button class="btn btn-outline-secondary" type="button">
              <i class="fas fa-search"></i>
            </button>
          </div>
          <button class="btn btn-primary" @click="showAddModal">
            Add New User
          </button>
        </div>
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

      <!-- Users Table -->
      <div v-else class="card">
        <div class="card-body">
          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Joined</th>
                  <th>Login Count</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in filteredUsers" :key="user.id">
                  <td>{{ user.id }}</td>
                  <td>{{ user.name }}</td>
                  <td>{{ user.email }}</td>
                  <td>{{ user.phone }}</td>
                  <td>
                    <span
                      :class="[
                        'badge',
                        user.role === 'admin' ? 'bg-warning' : user.role === 'customer' ? 'bg-info' : 'bg-primary'
                      ]"
                    >
                      {{ user.role }}
                    </span>
                  </td>
                  <td>
                    <span
                      :class="[
                        'badge',
                        user.is_approved ? 'bg-success' : 'bg-danger'
                      ]"
                    >
                      {{ user.is_approved ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td>{{ formatDate(user.created_at) }}</td>
                  <td>{{ user.login_count }}</td>
                  <td>
                    <div class="btn-group">
                      <button
                        class="btn btn-sm btn-info"
                        @click="editUser(user)"
                      >
                        Edit
                      </button>
                      <button
                        class="btn btn-sm"
                        :class="user.is_approved ? 'btn-warning' : 'btn-success'"
                        @click="toggleUserStatus(user)"
                      >
                        {{ user.is_approved ? 'Deactivate' : 'Activate' }}
                      </button>
                      <button
                        v-if="user.role !== 'admin'"
                        class="btn btn-sm btn-danger"
                        @click="deleteUser(user)"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Add/Edit User Modal -->
      <div
        id="userModal"
        class="modal fade"
        tabindex="-1"
        aria-labelledby="userModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 id="userModalLabel" class="modal-title">
                {{ isEditing ? 'Edit User' : 'Add New User' }}
              </h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="saveUser">
                <div class="mb-3">
                  <label for="userName" class="form-label">Full Name</label>
                  <input
                    id="userName"
                    v-model="userForm.name"
                    type="text"
                    class="form-control"
                    required
                  />
                </div>

                <div class="mb-3">
                  <label for="userEmail" class="form-label">Email</label>
                  <input
                    id="userEmail"
                    v-model="userForm.email"
                    type="email"
                    class="form-control"
                    required
                  />
                </div>

                <div class="mb-3">
                  <label for="userPhone" class="form-label">Phone</label>
                  <input
                    id="userPhone"
                    v-model="userForm.phone"
                    type="tel"
                    class="form-control"
                    required
                  />
                </div>

                <div class="mb-3">
                  <label for="userRole" class="form-label">Role</label>
                  <select
                    id="userRole"
                    v-model="userForm.role"
                    class="form-select"
                    required
                  >
                    <option value="customer">Customer</option>
                    <option value="professional">Professional</option>
                  </select>
                </div>

                <div v-if="!isEditing" class="mb-3">
                  <label for="userPassword" class="form-label">Password</label>
                  <input
                    id="userPassword"
                    v-model="userForm.password"
                    type="password"
                    class="form-control"
                    required
                  />
                </div>

                <div class="form-check mb-3">
                  <input
                    id="userActive"
                    v-model="userForm.active"
                    type="checkbox"
                    class="form-check-input"
                  />
                  <label class="form-check-label" for="userActive">
                    Approve Account
                  </label>
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
              <button type="button" class="btn btn-primary" @click="saveUser">
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
import debounce from 'lodash/debounce'

export default {
  name: 'AdminUsers',
  setup() {
    const store = useStore()
    const loading = ref(false)
    const error = ref(null)
    const isEditing = ref(false)
    const userModal = ref(null)
    const searchQuery = ref('')

    const userForm = ref({
      id: null,
      name: '',
      email: '',
      phone: '',
      role: 'user',
      password: '',
      active: true
    })

    const users = computed(() => store.getters['users/allUsers'])
    const filteredUsers = computed(() => {
      const query = searchQuery.value.toLowerCase()
      if (!query) return users.value

      return users.value.filter(user => 
        user.name.toLowerCase().includes(query) ||
        user.email.toLowerCase().includes(query) ||
        user.phone.includes(query)
      )
    })

    const resetForm = () => {
      userForm.value = {
        id: null,
        name: '',
        email: '',
        phone: '',
        role: 'user',
        password: '',
        active: true
      }
      isEditing.value = false
    }

    const showAddModal = () => {
      resetForm()
      userModal.value.show()
    }

    const editUser = (user) => {
      userForm.value = { ...user }
      delete userForm.value.password // Remove password field when editing
      isEditing.value = true
      userModal.value.show()
    }

    const handleSearch = debounce(() => {
      // Additional search logic if needed
    }, 300)

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString()
    }

    const saveUser = async () => {
      try {
        loading.value = true
        error.value = null

        if (isEditing.value) {
          await store.dispatch('users/updateUser', userForm.value)
        } else {
          await store.dispatch('users/createUser', userForm.value)
        }

        userModal.value.hide()
        resetForm()
      } catch (err) {
        error.value = err.message || 'Failed to save user'
      } finally {
        loading.value = false
      }
    }

    const toggleUserStatus = async (user) => {
      if (!confirm(`Are you sure you want to ${user.is_approved ? 'deactivate' : 'activate'} this user?`)) {
        return
      }

      try {
        loading.value = true
        error.value = null
        await store.dispatch('users/toggleUserStatus', user.id)
      } catch (err) {
        error.value = err.message || 'Failed to toggle user status'
      } finally {
        loading.value = false
      }
    }

    const deleteUser = async (user) => {
      if (!confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
        return
      }

      try {
        loading.value = true
        error.value = null
        await store.dispatch('users/deleteUser', user.id)
      } catch (err) {
        error.value = err.message || 'Failed to delete user'
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      userModal.value = new Modal(document.getElementById('userModal'))
      store.dispatch('users/fetchUsers')
    })

    return {
      loading,
      error,
      isEditing,
      userForm,
      users,
      filteredUsers,
      searchQuery,
      showAddModal,
      editUser,
      handleSearch,
      formatDate,
      saveUser,
      toggleUserStatus,
      deleteUser
    }
  }
}
</script>

<style scoped>
.btn-group {
  gap: 0.25rem;
}

.badge {
  font-size: 0.875rem;
  padding: 0.5em 0.75em;
}

.input-group {
  width: auto;
}
</style> 