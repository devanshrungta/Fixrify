<template>
  <div class="customer-profile">
    <div class="profile-header">
      <h1>My Profile</h1>
      <button class="btn btn-primary" @click="isEditing = true" v-if="!isEditing">
        Edit Profile
      </button>
    </div>

    <div class="profile-content">
      <form @submit.prevent="handleSubmit" v-if="isEditing">
        <div class="mb-3">
          <label class="form-label">Name</label>
          <input
            type="text"
            class="form-control"
            v-model="form.name"
            required/>
        </div>

        <div class="mb-3">
          <label class="form-label">Email</label>
          <input
            type="email"
            class="form-control"
            v-model="form.email"
            required/>
        </div>

        <div class="mb-3">
          <label class="form-label">Phone</label>
          <input
            type="tel"
            class="form-control"
            v-model="form.phone"/>
        </div>

        <div class="mb-3">
          <label class="form-label">New Password (leave blank to keep current)</label>
          <input
            type="password"
            class="form-control"
            v-model="form.password"/>
        </div>

        <div class="mb-3">
          <label class="form-label">Confirm New Password</label>
          <input
            type="password"
            class="form-control"
            v-model="form.confirmPassword"/>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            Save Changes
          </button>
          <button type="button" class="btn btn-secondary ms-2" @click="cancelEdit">
            Cancel
          </button>
        </div>
      </form>

      <div class="profile-details" v-else>
        <div class="detail-group">
          <label>Name</label>
          <p>{{ profile.name }}</p>
        </div>

        <div class="detail-group">
          <label>Email</label>
          <p>{{ profile.email }}</p>
        </div>

        <div class="detail-group">
          <label>Phone</label>
          <p>{{ profile.phone || 'Not provided' }}</p>
        </div>

        <div class="detail-group">
          <label>Member Since</label>
          <p>{{ formatDate(profile.created_at) }}</p>
        </div>
      </div>
    </div>

    <div class="profile-stats mt-4">
      <h2>Activity Summary</h2>
      <div class="stats-grid">
        <div class="stat-card">
          <h3>Total Requests</h3>
          <p class="stat-value">{{ stats.total_requests }}</p>
        </div>
        <div class="stat-card">
          <h3>Completed Services</h3>
          <p class="stat-value">{{ stats.completed_services }}</p>
        </div>
        <div class="stat-card">
          <h3>Reviews Given</h3>
          <p class="stat-value">{{ stats.reviews_given }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'CustomerProfile',
  setup() {
    const profile = ref({})
    const stats = ref({
      totalRequests: 0,
      completedServices: 0,
      reviewsGiven: 0
    })
    const isEditing = ref(false)
    const loading = ref(false)
    const form = ref({
      name: '',
      email: '',
      phone: '',
      password: '',
      confirmPassword: ''
    })

    const fetchProfile = async () => {
      try {
        const response = await axios.get('/api/customer/profile')
        profile.value = response.data
        // Initialize form with current values
        form.value = {
          name: profile.value.name,
          email: profile.value.email,
          phone: profile.value.phone || '',
          password: '',
          confirmPassword: ''
        }
      } catch (error) {
        console.error('Error fetching profile:', error)
      }
    }

    const fetchStats = async () => {
      try {
        const response = await axios.get('/api/customer/stats')
        stats.value = response.data
      } catch (error) {
        console.error('Error fetching stats:', error)
      }
    }

    const handleSubmit = async () => {
      if (form.value.password && form.value.password !== form.value.confirmPassword) {
        alert('Passwords do not match')
        return
      }

      try {
        loading.value = true
        const data = {
          name: form.value.name,
          email: form.value.email,
          phone: form.value.phone
        }
        if (form.value.password) {
          data.password = form.value.password
        }
        await axios.put('/api/customer/profile', data)
        await fetchProfile()
        isEditing.value = false
      } catch (error) {
        console.error('Error updating profile:', error)
        alert('Failed to update profile')
      } finally {
        loading.value = false
      }
    }

    const cancelEdit = () => {
      isEditing.value = false
      // Reset form to current profile values
      form.value = {
        name: profile.value.name,
        email: profile.value.email,
        phone: profile.value.phone || '',
        password: '',
        confirmPassword: ''
      }
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    onMounted(() => {
      fetchProfile()
      fetchStats()
    })

    return {
      profile,
      stats,
      isEditing,
      loading,
      form,
      handleSubmit,
      cancelEdit,
      formatDate
    }
  }
}
</script>

<style scoped>
.customer-profile {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.profile-content {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.detail-group {
  margin-bottom: 1.5rem;
}

.detail-group label {
  display: block;
  font-weight: 500;
  color: #666;
  margin-bottom: 0.5rem;
}

.detail-group p {
  margin: 0;
  font-size: 1.1rem;
}

.form-actions {
  margin-top: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-card h3 {
  color: #666;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #007bff;
  margin: 0;
}

@media (max-width: 768px) {
  .customer-profile {
    padding: 1rem;
  }

  .profile-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style> 