<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>Admin Dashboard</h1>
      <div class="stats">
        <div class="stat-card">
          <h3>Total Users</h3>
          <p>{{ stats.total_users }}</p>
        </div>
        <div class="stat-card">
          <h3>Active Services</h3>
          <p>{{ stats.active_services }}</p>
        </div>
        <div class="stat-card">
          <h3>Pending Approvals</h3>
          <p>{{ stats.pending_approvals }}</p>
        </div>
      </div>
    </header>

    <section v-if="pendingProfessionals.length" class="pending-approvals">
      <h2>Pending Professional Approvals</h2>
      <div class="approvals-grid">
        <div v-for="professional in pendingProfessionals" :key="professional.id" class="approval-card">
          <div class="approval-header">
            <h3>{{ professional.name }}</h3>
            <span class="status pending">Pending</span>
          </div>
          <div class="approval-details">
            <p><strong>Email:</strong> {{ professional.email }}</p>
            <p><strong>Phone:</strong> {{ professional.phone }}</p>
            <p><strong>Services:</strong> {{ professional.services.join(', ') }}</p>
            <p><strong>Experience:</strong> {{ professional.experience }} years</p>
          </div>
          <div class="approval-actions">
            <button class="btn-success" @click="approveProfessional(professional.id)">Approve</button>
            <button class="btn-cancel" @click="rejectProfessional(professional.id)">Reject</button>
          </div>
        </div>
      </div>
    </section>

    <section class="services-management">
      <div class="section-header">
        <h2>Services Management</h2>
        <button class="btn-primary" @click="showServiceModal = true">Add Service</button>
      </div>
      <div class="services-grid">
        <div v-for="service in services" :key="service.id" class="service-card">
          <img 
            :src="service.image_url || 'https://picsum.photos/200'" 
            :alt="service.name"/>
          <div class="service-content">
            <h3>{{ service.name }}</h3>
            <p>{{ service.description }}</p>
            <p class="price">Starting from ${{ service.base_price }}</p>
            <div class="service-actions">
              <button class="btn-secondary" @click="editService(service)">Edit</button>
              <button class="btn-cancel" @click="deleteService(service.id)">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="user-management">
      <div class="section-header">
        <h2>User Management</h2>
        <div class="filter-buttons">
          <button 
            v-for="role in ['all', 'customer', 'professional']" 
            :key="role"
            :class="['filter-btn', { active: currentUserFilter === role }]"
            @click="filterUsers(role)"
          >
            {{ role.charAt(0).toUpperCase() + role.slice(1) }}
          </button>
        </div>
      </div>
      <div class="users-table">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredUsers" :key="user.id">
              <td>{{ user.name }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.role }}</td>
              <td>
                <span :class="['status', user.is_active ? 'active' : 'blocked']">
                  {{ user.is_active ? 'Active' : 'Blocked' }}
                </span>
              </td>
              <td>
                <button 
                  v-if="user.is_active"
                  class="btn-cancel btn-sm"
                  @click="blockUser(user.id)"
                >
                  Block
                </button>
                <button 
                  v-else
                  class="btn-success btn-sm"
                  @click="unblockUser(user.id)"
                >
                  Unblock
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Add this section after the users management section -->
    <section class="exports-section">
      <h2>Export Data</h2>
      <div class="export-card card">
        <h3>Service Requests Export</h3>
        <form class="export-form" @submit.prevent="generateExport">
          <div class="form-group">
            <label>Professional (Optional)</label>
            <select v-model="exportForm.professional_id" class="form-control">
              <option value="">All Professionals</option>
              <option v-for="prof in professionals" :key="prof.id" :value="prof.id">
                {{ prof.name }}
              </option>
            </select>
          </div>
          
          <div class="form-group">
            <label>Date Range</label>
            <div class="date-range">
              <input 
                v-model="exportForm.start_date" 
                type="date" 
                class="form-control"/>
              <span>to</span>
              <input 
                v-model="exportForm.end_date" 
                type="date" 
                class="form-control"/>
            </div>
          </div>
          
          <div class="export-actions">
            <button 
              type="submit" 
              class="btn btn-primary" 
              :disabled="exporting"
            >
              {{ exporting ? 'Generating...' : 'Generate CSV' }}
            </button>
          </div>
        </form>
      </div>
    </section>

    <!-- Service Modal -->
    <div v-if="showServiceModal" class="modal">
      <div class="modal-content">
        <h2>{{ editingService ? 'Edit Service' : 'Add Service' }}</h2>
        <form @submit.prevent="submitService">
          <div class="form-group">
            <label>Service Name</label>
            <input v-model="serviceForm.name" type="text" required />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="serviceForm.description" required></textarea>
          </div>
          <div class="form-group">
            <label>Base Price ($)</label>
            <input
              v-model="serviceForm.base_price"
              type="number"
              required
              min="0"
            />
          </div>
          <div class="form-group">
            <label>Category</label>
            <input v-model="serviceForm.category" type="text" required />
          </div>
          <div class="form-group">
            <label>Image URL</label>
            <input v-model="serviceForm.image_url" type="url" />
          </div>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="showServiceModal = false">Cancel</button>
            <button type="submit" class="btn-primary">{{ editingService ? 'Update' : 'Create' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { adminAPI } from '@/services/api';
import { ref, onMounted } from 'vue';
import { useToast } from 'vue-toastification';

export default {
  name: 'AdminDashboard',
  setup() {
    const toast = useToast();
    const professionals = ref([]);
    const exporting = ref(false);
    const exportForm = ref({
      professional_id: '',
      start_date: '',
      end_date: ''
    });

    const loadProfessionals = async () => {
      try {
        const response = await adminAPI.getProfessionals();
        professionals.value = response.data;
      } catch (error) {
        console.error('Error loading professionals:', error);
        toast.error('Failed to load professionals');
      }
    };

    const generateExport = async () => {
      try {
        exporting.value = true;
        const response = await adminAPI.generateServiceRequestsCSV(exportForm.value);
        
        // Create a download link
        const link = document.createElement('a');
        link.href = `/api/admin/exports/${response.data.cache_key}`;
        link.download = 'service-requests.csv';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        toast.success('Export generated successfully');
      } catch (error) {
        console.error('Error generating export:', error);
        toast.error('Failed to generate export');
      } finally {
        exporting.value = false;
      }
    };

    onMounted(() => {
      loadProfessionals();
    });

    return {
      professionals,
      exportForm,
      exporting,
      generateExport
    };
  }
};
</script>

<style scoped>
.dashboard {
  padding: 2rem;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.stat-card {
  background: #fff;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-card h3 {
  color: #666;
  margin-bottom: 0.5rem;
}

.stat-card p {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.filter-buttons {
  display: flex;
  gap: 0.5rem;
}

.filter-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
}

.filter-btn.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.approvals-grid,
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.approval-card,
.service-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.approval-header,
.service-header {
  padding: 1rem;
  background: #f8f9fa;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.approval-details,
.service-content {
  padding: 1rem;
}

.approval-actions,
.service-actions {
  padding: 1rem;
  border-top: 1px solid #eee;
  display: flex;
  gap: 0.5rem;
}

.service-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.users-table {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-top: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background: #f8f9fa;
  font-weight: 600;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.875rem;
}

.status.pending { background: #fff3cd; color: #856404; }
.status.active { background: #d4edda; color: #155724; }
.status.blocked { background: #f8d7da; color: #721c24; }

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-group textarea {
  min-height: 100px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-primary {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn-cancel {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn-success {
  background: #28a745;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  opacity: 0.9;
}

.exports-section {
  margin-top: 2rem;
}

.export-card {
  padding: 1.5rem;
}

.export-form {
  max-width: 600px;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.date-range span {
  color: var(--secondary-color);
}

.export-actions {
  margin-top: 1.5rem;
}
</style> 