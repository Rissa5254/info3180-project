<script setup>
import { computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.authenticated)
const displayName = computed(() => authStore.user?.first_name || authStore.user?.username || 'Profile')

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>

<template>
  <header class="site-header">
    <nav class="nav-shell">
      <RouterLink class="brand" to="/">DriftDater</RouterLink>

      <div class="nav-links">
        <RouterLink class="nav-link" to="/">Home</RouterLink>
        <RouterLink class="nav-link" to="/about">About</RouterLink>

        <template v-if="isAuthenticated">
          <RouterLink class="nav-link" to="/browse">Browse</RouterLink>
          <RouterLink class="nav-link" to="/chat">Chat</RouterLink>
          <RouterLink class="nav-link" to="/profile">{{ displayName }}</RouterLink>
          <button class="nav-action nav-action-secondary" type="button" @click="handleLogout">
            Logout
          </button>
        </template>

        <template v-else>
          <RouterLink class="nav-link" to="/login">Login</RouterLink>
          <RouterLink class="nav-action" to="/register">Sign Up</RouterLink>
        </template>
      </div>
    </nav>
  </header>
</template>

<style scoped>
.site-header {
  position: sticky;
  top: 0;
  z-index: 20;
  backdrop-filter: blur(14px);
  background: rgba(255, 245, 247, 0.94);
  border-bottom: 1px solid rgba(244, 63, 94, 0.12);
  box-shadow: 0 10px 24px rgba(190, 24, 93, 0.08);
}

.nav-shell {
  width: min(1120px, calc(100% - 32px));
  margin: 0 auto;
  min-height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.brand {
  color: #be123c;
  font-size: 1.2rem;
  font-weight: 800;
  letter-spacing: 0.04em;
  text-decoration: none;
  text-transform: uppercase;
}

.nav-links {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  flex-wrap: wrap;
}

.nav-link,
.nav-action {
  border-radius: 999px;
  color: #881337;
  font-weight: 600;
  padding: 10px 14px;
  text-decoration: none;
  transition: background-color 0.2s ease, color 0.2s ease, transform 0.2s ease;
}

.nav-link:hover,
.nav-action:hover {
  background: rgba(251, 113, 133, 0.12);
  color: #e11d48;
  transform: translateY(-1px);
}

.router-link-active.nav-link {
  color: #e11d48;
}

.nav-action {
  background: linear-gradient(135deg, #fb7185, #e11d48);
  color: #fff;
}

.nav-action-secondary {
  background: #ffe4e6;
  border: 0;
  color: #9f1239;
  cursor: pointer;
  font: inherit;
}

@media (max-width: 720px) {
  .nav-shell {
    padding: 14px 0;
    align-items: flex-start;
    flex-direction: column;
  }

  .nav-links {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>
