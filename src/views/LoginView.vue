<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const error = ref('')
const submitting = ref(false)

async function login() {
  error.value = ''
  submitting.value = true

  try {
    await authStore.login({
      email: email.value,
      password: password.value
    })

    const redirectTarget =
      typeof route.query.redirect === 'string' ? route.query.redirect : '/profile'

    router.replace(redirectTarget)
  } catch (err) {
    error.value = err.response?.data?.error || 'Login failed'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <main class="auth-page">
    <div class="hearts" aria-hidden="true">
      <span class="heart">♥</span>
      <span class="heart">♥</span>
      <span class="heart">♥</span>
      <span class="heart">♥</span>
    </div>

    <form class="auth-card" @submit.prevent="login">
      <h1>Login</h1>

      <div class="form-group">
        <label>Email</label>
        <input v-model="email" type="email" required />
      </div>

      <div class="form-group">
        <label>Password</label>
        <input v-model="password" type="password" required />
      </div>

      <p v-if="error" class="error">{{ error }}</p>

      <button type="submit" :disabled="submitting">
        {{ submitting ? 'Signing In...' : 'Login' }}
      </button>

      <p class="switch-link">
        Need an account?
        <RouterLink to="/register">Register</RouterLink>
      </p>
    </form>
  </main>
</template>

<style scoped>
.auth-page {
  min-height: calc(100vh - 140px);
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 16px;
  overflow: hidden;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  background: rgba(255, 255, 255, 0.94);
  padding: 32px;
  border-radius: 14px;
  border: 1px solid rgba(251, 113, 133, 0.18);
  box-shadow: 0 18px 38px rgba(190, 24, 93, 0.18);
  z-index: 1;
}

.auth-card h1 {
  text-align: center;
  margin-bottom: 24px;
  color: #be123c;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 16px;
}

label {
  margin-bottom: 6px;
  font-weight: 600;
}

input {
  padding: 11px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 15px;
}

button {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #fb7185, #e11d48);
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 8px;
}

button:disabled {
  cursor: wait;
  opacity: 0.75;
}

.error {
  color: #c0392b;
  margin-bottom: 12px;
}

.switch-link {
  text-align: center;
  margin-top: 18px;
}

.hearts {
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  position: absolute;
}

.heart {
  position: absolute;
  color: rgba(244, 63, 94, 0.35);
  animation: floatUp 5.5s infinite ease-in-out;
  font-size: 28px;
}

.heart:nth-child(1) {
  top: 30%;
  left: 10%;
}

.heart:nth-child(2) {
  top: 78%;
  left: 85%;
  animation-delay: 0.8s;
}

.heart:nth-child(3) {
  top: 22%;
  left: 82%;
  animation-delay: 1.3s;
}

.heart:nth-child(4) {
  top: 75%;
  left: 12%;
  animation-delay: 2s;
}

@keyframes floatUp {
  0% {
    transform: translateY(0) scale(1);
    opacity: 0.2;
  }

  50% {
    opacity: 0.9;
  }

  100% {
    transform: translateY(-60px) scale(1.18);
    opacity: 0;
  }
}
</style>
