<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const firstName = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')
const dateOfBirth = ref('')
const gender = ref('')
const lookingFor = ref('')
const error = ref('')
const submitting = ref(false)

async function register() {
  error.value = ''
  submitting.value = true

  try {
    await authStore.register({
      username: username.value,
      first_name: firstName.value,
      last_name: lastName.value,
      email: email.value,
      password: password.value,
      date_of_birth: dateOfBirth.value,
      gender: gender.value,
      looking_for: lookingFor.value
    })

    const redirectTarget =
      typeof route.query.redirect === 'string' ? route.query.redirect : '/profile'

    router.replace(redirectTarget)
  } catch (err) {
    error.value = err.response?.data?.error || 'Registration failed'
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

    <form class="auth-card" @submit.prevent="register">
      <h1>Sign Up</h1>

      <div class="form-group">
        <label>Username</label>
        <input v-model="username" required />
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>First Name</label>
          <input v-model="firstName" required />
        </div>

        <div class="form-group">
          <label>Last Name</label>
          <input v-model="lastName" required />
        </div>
      </div>

      <div class="form-group">
        <label>Email</label>
        <input v-model="email" type="email" required />
      </div>

      <div class="form-group">
        <label>Password</label>
        <input v-model="password" type="password" required />
      </div>

      <div class="form-group">
        <label>Date of Birth</label>
        <input v-model="dateOfBirth" type="date" />
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Gender</label>
          <select v-model="gender">
            <option value="">Select gender</option>
            <option>Male</option>
            <option>Female</option>
            <option>Other</option>
          </select>
        </div>

        <div class="form-group">
          <label>Looking For</label>
          <select v-model="lookingFor">
            <option value="">Select preference</option>
            <option>Male</option>
            <option>Female</option>
          </select>
        </div>
      </div>

      <p v-if="error" class="error">{{ error }}</p>

      <button type="submit" :disabled="submitting">
        {{ submitting ? 'Creating Account...' : 'Register' }}
      </button>

      <p class="switch-link">
        Already have an account?
        <RouterLink to="/login">Login</RouterLink>
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
  max-width: 520px;
  background: rgba(255, 255, 255, 0.95);
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

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

label {
  margin-bottom: 6px;
  font-weight: 600;
}

input,
select {
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

button:hover {
  opacity: 0.95;
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
  top: 26%;
  left: 8%;
}

.heart:nth-child(2) {
  top: 80%;
  left: 88%;
  animation-delay: 0.9s;
}

.heart:nth-child(3) {
  top: 20%;
  left: 84%;
  animation-delay: 1.5s;
}

.heart:nth-child(4) {
  top: 82%;
  left: 10%;
  animation-delay: 2.1s;
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

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
