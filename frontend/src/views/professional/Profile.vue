<template>
  <div class="professional-profile">
    <div class="profile-header">
      <h1>Professional Profile</h1>
      <button 
        v-if="!isEditing" 
        class="btn btn-primary"
        @click="startEditing">
        Edit Profile
      </button>
    </div>

    <div class="profile-content">
      <form v-if="isEditing" @submit.prevent="saveProfile" class="edit-form">
        <div class="form-group">
          <label>Name</label>
          <input 
            v-model="form.name"
            type="text"
            class="form-control"
            required/>
        </div>

        <div class="form-group">
          <label>Email</label>
          <input 
            v-model="form.email"
            type="email"
            class="form-control"
            required/>
        </div>

        <div class="form-group">
          <label>Phone</label>
          <input 
            v-model="form.phone"
            type="tel"
            class="form-control"
            required/>
        </div>

        <div class="form-group">
          <label>Experience (years)</label>
          <input 
            v-model="form.experience"
            type="number"
            class="form-control"
            min="0"
            required/>
        </div>

        <div class="form-group">
          <label>New Password (optional)</label>
          <input 
            v-model="form.password"
            type="password"
            class="form-control"/>
        </div>

        <div class="form-actions">
          <button type="button" class="btn btn-secondary" @click="cancelEdit">Cancel</button>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>
      </form>

      <div v-else class="profile-details">
        <div class="detail-group">
          <h3>Personal Information</h3>
          <p><strong>Name:</strong> {{ profile.name }}</p>
          <p><strong>Email:</strong> {{ profile.email }}</p>
          <p><strong>Phone:</strong> {{ profile.phone }}</p>
          <p><strong>Experience:</strong> {{ profile.experience }} years</p>
          <p><strong>Member since:</strong> {{ formatDate(profile.created_at) }}</p>
        </div>

        <div class="detail-group">
          <h3>Statistics</h3>
          <div class="stats-grid">
            <div class="stat-card">
              <h4>Experience</h4>
              <p>{{ profile.experience }}</p>
            </div>
            <div class="stat-card">
              <h4>Completed Services</h4>
              <p>{{ profile.total_jobs }}</p>
            </div>
            <div class="stat-card">
              <h4>Average Rating</h4>
              <p>{{ profile.average_rating || 'N/A' }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { professionalAPI } from '@/services/api'

export default {
  name: 'ProfessionalProfile',
  
  setup() {
    const toast = useToast()
    const profile = ref({})
    const stats = ref({})
    const availableServices = ref([])
    const isEditing = ref(false)
    const saving = ref(false)
    
    const form = ref({
      name: '',
      email: '',
      phone: '',
      experience: 0,
      services: [],
      password: ''
    })

    const loadProfile = async () => {
      try {
        const response = await professionalAPI.getProfile()
        profile.value = response.data

        // Initialize form with current values
        form.value = {
          name: profile.value.name,
          email: profile.value.email,
          phone: profile.value.phone,
          experience: profile.value.experience,
          services: profile.value.services.map(s => s.id),
          password: ''
        }
      } catch (err) {
        toast.error('Failed to load profile data')
        console.error('Error loading profile:', err)
      }
    }

    const startEditing = () => {
      isEditing.value = true
    }

    const cancelEdit = () => {
      isEditing.value = false
      // Reset form to current profile values
      form.value = {
        name: profile.value.name,
        email: profile.value.email,
        phone: profile.value.phone,
        experience: profile.value.experience,
        services: profile.value.services.map(s => s.id),
        password: ''
      }
    }

    const saveProfile = async () => {
      try {
        saving.value = true
        await professionalAPI.updateProfile(form.value)
        await loadProfile()
        isEditing.value = false
        toast.success('Profile updated successfully')
      } catch (err) {
        toast.error('Failed to update profile')
        console.error('Error updating profile:', err)
      } finally {
        saving.value = false
      }
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString()
    }

    onMounted(() => {
      loadProfile()
    })

    return {
      profile,
      stats,
      availableServices,
      isEditing,
      saving,
      form,
      startEditing,
      cancelEdit,
      saveProfile,
      formatDate
    }
  }
}
</script>

<style scoped>
.professional-profile {
  padding: 2rem;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.profile-content {
  max-width: 800px;
  margin: 0 auto;
}

.edit-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.services-checkboxes {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.service-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.profile-details {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.detail-group {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.detail-group h3 {
  margin-bottom: 1rem;
  color: var(--dark-color);
}

.detail-group p {
  margin: 0.5rem 0;
  color: var(--secondary-color);
}

.detail-group strong {
  color: var(--dark-color);
}

.services-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.services-list li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.services-list li:last-child {
  border-bottom: none;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  text-align: center;
}

.stat-card h4 {
  margin: 0 0 0.5rem;
  font-size: 0.875rem;
  color: var(--secondary-color);
}

.stat-card p {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--dark-color);
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .professional-profile {
    padding: 1rem;
  }

  .profile-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style> 