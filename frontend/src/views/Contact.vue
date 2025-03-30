<template>
  <div class="contact">
    <div class="container">
      <header class="contact-header">
        <h1>Contact Us</h1>
        <p class="lead">Get in touch with our support team</p>
      </header>

      <div class="contact-content grid-2">
        <section class="contact-info">
          <div class="info-card card">
            <h2>Contact Information</h2>
            
            <div class="info-item">
              <div class="info-icon">
                <i class="fas fa-map-marker-alt"></i>
              </div>
              <div class="info-text">
                <h3>Address</h3>
                <p>123 Service Street<br/>Business District<br/>City, State 12345</p>
              </div>
            </div>

            <div class="info-item">
              <div class="info-icon">
                <i class="fas fa-phone"></i>
              </div>
              <div class="info-text">
                <h3>Phone</h3>
                <p>
                  <a href="tel:+15551234567">+1 (555) 123-4567</a>
                </p>
              </div>
            </div>

            <div class="info-item">
              <div class="info-icon">
                <i class="fas fa-envelope"></i>
              </div>
              <div class="info-text">
                <h3>Email</h3>
                <p>
                  <a href="mailto:support@fixrify.com">support@fixrify.com</a>
                </p>
              </div>
            </div>

            <div class="info-item">
              <div class="info-icon">
                <i class="fas fa-clock"></i>
              </div>
              <div class="info-text">
                <h3>Business Hours</h3>
                <p>
                  Monday - Friday: 9:00 AM - 6:00 PM<br/>
                  Saturday: 10:00 AM - 4:00 PM<br/>
                  Sunday: Closed
                </p>
              </div>
            </div>
          </div>
        </section>

        <section class="contact-form">
          <div class="form-card card">
            <h2>Send us a Message</h2>
            
            <form @submit.prevent="handleSubmit">
              <div class="form-group">
                <label class="form-label">Name</label>
                <input 
                  v-model="form.name" 
                  type="text" 
                  class="form-control" 
                  required/>
              </div>

              <div class="form-group">
                <label class="form-label">Email</label>
                <input 
                  v-model="form.email" 
                  type="email" 
                  class="form-control" 
                  required
                />
              </div>

              <div class="form-group">
                <label class="form-label">Subject</label>
                <input 
                  v-model="form.subject" 
                  type="text" 
                  class="form-control" 
                  required
                />
              </div>

              <div class="form-group">
                <label class="form-label">Message</label>
                <textarea 
                  v-model="form.message" 
                  class="form-control" 
                  rows="6" 
                  required
                ></textarea>
              </div>

              <button 
                type="submit" 
                class="btn btn-primary w-100" 
                :disabled="submitting"
              >
                {{ submitting ? 'Sending...' : 'Send Message' }}
              </button>
            </form>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useToast } from 'vue-toastification'

export default {
  name: 'Contact',
  
  setup() {
    const toast = useToast()
    const submitting = ref(false)
    const form = ref({
      name: '',
      email: '',
      subject: '',
      message: ''
    })

    const handleSubmit = async () => {
      try {
        submitting.value = true
        // Here you would typically make an API call to send the message
        // For now, we'll just simulate a delay
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        toast.success('Message sent successfully! We will get back to you soon.')
        form.value = {
          name: '',
          email: '',
          subject: '',
          message: ''
        }
      } catch (err) {
        toast.error('Failed to send message. Please try again later.')
        console.error('Error sending message:', err)
      } finally {
        submitting.value = false
      }
    }

    return {
      form,
      submitting,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.contact {
  padding: 3rem 0;
}

.contact-header {
  text-align: center;
  margin-bottom: 3rem;
}

.contact-header h1 {
  color: var(--dark-color);
  margin-bottom: 1rem;
}

.contact-header .lead {
  font-size: 1.25rem;
  color: var(--secondary-color);
}

.contact-content {
  gap: 2rem;
}

.info-card,
.form-card {
  height: 100%;
}

.info-card h2,
.form-card h2 {
  margin-bottom: 2rem;
  color: var(--dark-color);
}

.info-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-icon {
  font-size: 1.5rem;
  color: var(--primary-color);
  margin-right: 1rem;
  padding-top: 0.25rem;
}

.info-text h3 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: var(--dark-color);
}

.info-text p {
  color: var(--secondary-color);
  line-height: 1.6;
}

.info-text a {
  color: var(--primary-color);
  text-decoration: none;
}

.info-text a:hover {
  text-decoration: underline;
}

.form-card form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .contact {
    padding: 2rem 0;
  }

  .contact-header {
    margin-bottom: 2rem;
  }

  .info-card {
    margin-bottom: 2rem;
  }
}
</style> 