<template>
  <div class="about">
    <div class="container">
      <header class="about-header">
        <h1>About Fixrify</h1>
        <p class="lead">Your trusted platform for home services</p>
      </header>

      <div class="about-content">
        <section class="mission-section">
          <h2>Our Mission</h2>
          <p>
            At Fixrify, we're committed to connecting homeowners with skilled professionals to make home maintenance 
            simple, reliable, and hassle-free. Our platform ensures quality service delivery while providing 
            opportunities for skilled professionals to grow their business.
          </p>
        </section>

        <section class="features-section grid-3">
          <div class="feature-card card">
            <div class="feature-icon">
              <i class="fas fa-shield-alt"></i>
            </div>
            <h3>Verified Professionals</h3>
            <p>
              All our service providers undergo thorough background checks and skill verification to ensure 
              you receive the highest quality service.
            </p>
          </div>

          <div class="feature-card card">
            <div class="feature-icon">
              <i class="fas fa-clock"></i>
            </div>
            <h3>Quick Response</h3>
            <p>
              Get connected with available professionals quickly and schedule services at your convenience.
            </p>
          </div>

          <div class="feature-card card">
            <div class="feature-icon">
              <i class="fas fa-star"></i>
            </div>
            <h3>Quality Guaranteed</h3>
            <p>
              We stand behind our service quality with satisfaction guarantees and responsive customer support.
            </p>
          </div>
        </section>

        <section class="how-it-works">
          <h2>How It Works</h2>
          <div class="steps-container">
            <div class="step">
              <div class="step-number">1</div>
              <h3>Request a Service</h3>
              <p>Browse our services and submit a request with your specific needs.</p>
            </div>

            <div class="step">
              <div class="step-number">2</div>
              <h3>Get Matched</h3>
              <p>We'll match you with qualified professionals in your area.</p>
            </div>

            <div class="step">
              <div class="step-number">3</div>
              <h3>Service Delivery</h3>
              <p>Your assigned professional will arrive at the scheduled time to complete the service.</p>
            </div>

            <div class="step">
              <div class="step-number">4</div>
              <h3>Rate & Review</h3>
              <p>Share your experience to help maintain our high service standards.</p>
            </div>
          </div>
        </section>

        <section class="join-section">
          <div class="join-content">
            <h2>Join Our Network</h2>
            <p>
              Are you a skilled professional looking to expand your business? Join our network of trusted 
              service providers and connect with customers in your area.
            </p>
            <router-link to="/register" class="btn btn-primary">Register as a Professional</router-link>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
.about {
  padding: 3rem 0;
}

.about-header {
  text-align: center;
  margin-bottom: 4rem;
}

.about-header h1 {
  color: var(--dark-color);
  margin-bottom: 1rem;
}

.about-header .lead {
  font-size: 1.25rem;
  color: var(--secondary-color);
}

.mission-section {
  max-width: 800px;
  margin: 0 auto 4rem;
  text-align: center;
}

.mission-section h2 {
  margin-bottom: 1.5rem;
}

.mission-section p {
  font-size: 1.1rem;
  line-height: 1.8;
  color: var(--secondary-color);
}

.features-section {
  margin-bottom: 4rem;
}

.feature-card {
  text-align: center;
  padding: 2rem;
}

.feature-icon {
  font-size: 2.5rem;
  color: var(--primary-color);
  margin-bottom: 1.5rem;
}

.feature-card h3 {
  margin-bottom: 1rem;
}

.feature-card p {
  color: var(--secondary-color);
}

.how-it-works {
  margin-bottom: 4rem;
  text-align: center;
}

.how-it-works h2 {
  margin-bottom: 3rem;
}

.steps-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.step {
  position: relative;
  padding: 2rem;
}

.step-number {
  width: 40px;
  height: 40px;
  background-color: var(--primary-color);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: bold;
  margin: 0 auto 1.5rem;
}

.step h3 {
  margin-bottom: 1rem;
}

.step p {
  color: var(--secondary-color);
}

.join-section {
  background-color: var(--light-color);
  padding: 4rem 0;
  text-align: center;
  border-radius: var(--border-radius);
}

.join-content {
  max-width: 600px;
  margin: 0 auto;
}

.join-content h2 {
  margin-bottom: 1.5rem;
}

.join-content p {
  margin-bottom: 2rem;
  color: var(--secondary-color);
}

.join-content .btn {
  font-size: 1.1rem;
  padding: 0.75rem 2rem;
}

@media (max-width: 768px) {
  .about {
    padding: 2rem 0;
  }

  .about-header {
    margin-bottom: 3rem;
  }

  .mission-section {
    margin-bottom: 3rem;
  }

  .features-section {
    margin-bottom: 3rem;
  }

  .how-it-works {
    margin-bottom: 3rem;
  }

  .steps-container {
    gap: 1.5rem;
  }

  .join-section {
    padding: 3rem 1rem;
  }
}
</style> 