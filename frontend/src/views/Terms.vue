<template>
  <div class="terms">
    <div class="container">
      <div class="content-card card">
        <h1>Terms of Service</h1>
        <p class="last-updated">Last updated: {{ new Date().toLocaleDateString() }}</p>

        <section>
          <h2>1. Agreement to Terms</h2>
          <p>
            By accessing and using Fixrify, you agree to be bound by these Terms of Service and all 
            applicable laws and regulations. If you do not agree with any of these terms, you are 
            prohibited from using or accessing this site.
          </p>
        </section>

        <section>
          <h2>2. Use License</h2>
          <p>
            Permission is granted to temporarily access Fixrify for personal, non-commercial transitory 
            viewing and service requests only. This is the grant of a license, not a transfer of title, 
            and under this license you may not:
          </p>
          <ul>
            <li>Modify or copy the materials</li>
            <li>Use the materials for any commercial purpose</li>
            <li>Attempt to decompile or reverse engineer any software contained on Fixrify</li>
            <li>Remove any copyright or other proprietary notations from the materials</li>
            <li>Transfer the materials to another person or "mirror" the materials on any other server</li>
          </ul>
        </section>

        <section>
          <h2>3. Service Terms</h2>
          <p>When using our service platform:</p>
          <ul>
            <li>You must provide accurate and complete information</li>
            <li>You are responsible for maintaining the confidentiality of your account</li>
            <li>You agree to accept responsibility for all activities that occur under your account</li>
            <li>You must not use the service for any illegal or unauthorized purpose</li>
            <li>You must not interfere with or disrupt the service or servers</li>
          </ul>
        </section>

        <section>
          <h2>4. Payment Terms</h2>
          <p>
            By using our services, you agree to pay all fees and charges associated with your service requests. 
            Payments are processed securely through our payment providers. All fees are non-refundable unless 
            otherwise specified in our refund policy.
          </p>
        </section>

        <section>
          <h2>5. Service Provider Terms</h2>
          <p>For service providers using our platform:</p>
          <ul>
            <li>Must maintain required licenses and insurance</li>
            <li>Must provide services in a professional and workmanlike manner</li>
            <li>Must comply with all applicable laws and regulations</li>
            <li>Must maintain accurate service availability and pricing information</li>
            <li>Must not engage in discriminatory practices</li>
          </ul>
        </section>

        <section>
          <h2>6. Disclaimer</h2>
          <p>
            The materials on Fixrify are provided on an 'as is' basis. We make no warranties, expressed 
            or implied, and hereby disclaim and negate all other warranties including, without limitation, 
            implied warranties or conditions of merchantability, fitness for a particular purpose, or 
            non-infringement of intellectual property or other violation of rights.
          </p>
        </section>

        <section>
          <h2>7. Limitations</h2>
          <p>
            In no event shall Fixrify or its suppliers be liable for any damages (including, without 
            limitation, damages for loss of data or profit, or due to business interruption) arising 
            out of the use or inability to use Fixrify, even if we or an authorized representative has 
            been notified orally or in writing of the possibility of such damage.
          </p>
        </section>

        <section>
          <h2>8. Contact Information</h2>
          <p>
            If you have any questions about these Terms of Service, please contact us:
          </p>
          <ul>
            <li>By email: legal@fixrify.com</li>
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
  name: 'Terms'
}
</script>

<style scoped>
.terms {
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
  .terms {
    padding: 2rem 0;
  }
}
</style> 