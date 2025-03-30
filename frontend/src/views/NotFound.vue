<template>
  <div class="not-found">
    <div class="not-found-content">
      <h1>404</h1>
      <h2>Page Not Found</h2>
      <p>The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.</p>
      <router-link to="/" class="btn btn-primary">Go Home</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2rem;
  background-color: var(--light-color);
}

.not-found-content {
  max-width: 600px;
}

.not-found h1 {
  font-size: 6rem;
  font-weight: bold;
  color: var(--primary-color);
  margin-bottom: 1rem;
  line-height: 1;
}

.not-found h2 {
  font-size: 2rem;
  color: var(--dark-color);
  margin-bottom: 1.5rem;
}

.not-found p {
  color: var(--secondary-color);
  margin-bottom: 2rem;
}

.not-found .btn {
  font-size: 1.1rem;
  padding: 0.75rem 2rem;
}
</style> 