<template>
  <div class="home">
    <div class="hero-section text-center py-5 bg-light">
      <h1 class="display-4">Welcome to Fixrify</h1>
      <p class="lead">Your one-stop solution for all home repair and maintenance services</p>
      <router-link to="/services" class="btn btn-primary btn-lg">
        Browse Services
      </router-link>
    </div>

    <div class="features-section py-5">
      <div class="container">
        <h2 class="text-center mb-4">Why Choose Fixrify?</h2>
        <div class="row">
          <div class="col-md-4">
            <div class="card h-100">
              <div class="card-body text-center">
                <i class="fas fa-tools fa-3x mb-3 text-primary"></i>
                <h3 class="card-title">Professional Services</h3>
                <p class="card-text">Our experienced technicians provide high-quality repair and maintenance services.</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card h-100">
              <div class="card-body text-center">
                <i class="fas fa-clock fa-3x mb-3 text-primary"></i>
                <h3 class="card-title">Quick Response</h3>
                <p class="card-text">Book your service online and get quick response from our service providers.</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card h-100">
              <div class="card-body text-center">
                <i class="fas fa-shield-alt fa-3x mb-3 text-primary"></i>
                <h3 class="card-title">Guaranteed Work</h3>
                <p class="card-text">All our services come with satisfaction guarantee and warranty.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="popular-services py-5 bg-light">
      <div class="container">
        <h2 class="text-center mb-4">Popular Services</h2>
        <div class="row">
          <div v-for="service in popularServices" :key="service.id" class="col-md-4 mb-4">
            <div class="card h-100">
              <img :src="'https://picsum.photos/400?random=' + service.id" class="card-img-top" :alt="service.name" />
              <div class="card-body">
                <h3 class="card-title">{{ service.name }}</h3>
                <p class="card-text">{{ service.description }}</p>
                <router-link :to="'/service/' + service.id" class="btn btn-outline-primary">
                  Learn More
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="cta-section py-5 text-center">
      <div class="container">
        <h2>Ready to Get Started?</h2>
        <p class="lead">Join thousands of satisfied customers who trust Fixrify for their home repair needs.</p>
        <router-link to="/register" class="btn btn-primary btn-lg">
          Sign Up Now
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Home',
  setup() {
    const store = useStore()
    const popularServices = ref([])

    onMounted(async () => {
      try {
        await store.dispatch('services/fetchServices')
        popularServices.value = store.getters['services/allServices'].slice(0, 3)
      } catch (error) {
        console.error('Error fetching services:', error)
      }
    })

    return {
      popularServices
    }
  }
}
</script>

<style scoped>
.hero-section {
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('@/assets/hero-bg.jpg');
  background-size: cover;
  background-position: center;
  color: white;
  padding: 100px 0;
}

.card {
  transition: transform 0.3s ease;
  border: none;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.card:hover {
  transform: translateY(-5px);
}

.card-img-top {
  height: 200px;
  object-fit: cover;
}

.cta-section {
  background-color: #f8f9fa;
}
</style> 