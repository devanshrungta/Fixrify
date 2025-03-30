<template>
  <div class="privacy">
    <div class="container">
      <div class="content-card card">
        <h1>Privacy Policy</h1>
        <p class="last-updated">Last updated: {{ new Date().toLocaleDateString() }}</p>

        <section>
          <h2>1. Introduction</h2>
          <p>
            Welcome to Fixrify. We respect your privacy and are committed to protecting your personal data. 
            This privacy policy will inform you about how we look after your personal data when you visit 
            our website and tell you about your privacy rights and how the law protects you.
          </p>
        </section>

        <section>
          <h2>2. Information We Collect</h2>
          <p>We collect several different types of information for various purposes:</p>
          <ul>
            <li>Personal identification information (Name, email address, phone number, etc.)</li>
            <li>Address and location data</li>
            <li>Service request details and history</li>
            <li>Payment information</li>
            <li>Communication preferences</li>
          </ul>
        </section>

        <section>
          <h2>3. How We Use Your Information</h2>
          <p>We use the collected information for various purposes:</p>
          <ul>
            <li>To provide and maintain our service</li>
            <li>To notify you about changes to our service</li>
            <li>To provide customer support</li>
            <li>To process payments and prevent fraud</li>
            <li>To send you marketing and promotional communications (with your consent)</li>
          </ul>
        </section>

        <section>
          <h2>4. Data Security</h2>
          <p>
            We implement appropriate security measures to protect your personal information. However, 
            no method of transmission over the internet is 100% secure, and we cannot guarantee absolute security.
          </p>
        </section>

        <section>
          <h2>5. Your Rights</h2>
          <p>Under certain circumstances, you have rights under data protection laws in relation to your personal data:</p>
          <ul>
            <li>The right to access your personal data</li>
            <li>The right to correction of your personal data</li>
            <li>The right to erasure of your personal data</li>
            <li>The right to restrict processing of your personal data</li>
            <li>The right to data portability</li>
            <li>The right to object to processing</li>
          </ul>
        </section>

        <section>
          <h2>6. Contact Us</h2>
          <p>
            If you have any questions about this Privacy Policy, please contact us:
          </p>
          <ul>
            <li>By email: privacy@fixrify.com</li>
            <li>By phone: +1 (555) 123-4567</li>
            <li>By mail: 123 Service Street, Business District, City, State 12345</li>
          </ul>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Privacy'
}
</script>

<style scoped>
.privacy {
  padding: 3rem 0;
}

.content-card {
  max-width: 800px;
  margin: 0 auto;
}

.content-card h1 {
  color: var(--dark-color);
  margin-bottom: 1rem;
}

.last-updated {
  color: var(--secondary-color);
  font-style: italic;
  margin-bottom: 2rem;
}

section {
  margin-bottom: 2rem;
}

section:last-child {
  margin-bottom: 0;
}

h2 {
  color: var(--dark-color);
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

p {
  color: var(--secondary-color);
  line-height: 1.6;
  margin-bottom: 1rem;
}

ul {
  list-style-type: disc;
  margin-left: 1.5rem;
  color: var(--secondary-color);
}

li {
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .privacy {
    padding: 2rem 0;
  }
}
</style> 