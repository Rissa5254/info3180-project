<script setup>
import { onMounted, ref } from 'vue'
import api from '@/services/api'

const blockedUsers = ref([])
const loading = ref(true)
const error = ref('')
const success = ref('')

async function loadBlockedUsers() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/users/blocked')
    blockedUsers.value = response.data
  } catch (err) {
    error.value = err.response?.data?.error || 'Could not load blocked users'
  } finally {
    loading.value = false
  }
}

async function unblockUser(userID) {
  error.value = ''
  success.value = ''

  try {
    await api.delete(`/users/${userID}/unblock`)
    blockedUsers.value = blockedUsers.value.filter(user => user.userID !== userID)
    success.value = 'User unblocked successfully.'
  } catch (err) {
    error.value = err.response?.data?.error || 'Could not unblock user'
  }
}

onMounted(loadBlockedUsers)
</script>

<template>
  <main class="blocked-page">
    <section class="blocked-header">
      <h1>Blocked Users</h1>
      <p>Manage users you have blocked.</p>
    </section>

    <p v-if="loading">Loading blocked users...</p>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>

    <section v-if="!loading && blockedUsers.length === 0" class="empty-state">
      <h2>No blocked users</h2>
      <p>You have not blocked anyone yet.</p>
    </section>

    <section class="blocked-list">
      <article
        v-for="user in blockedUsers"
        :key="user.userID"
        class="blocked-card"
      >
        <div>
          <h2>@{{ user.username }}</h2>
          <p>{{ user.email }}</p>
        </div>

        <button @click="unblockUser(user.userID)">
          Unblock
        </button>
      </article>
    </section>
  </main>
</template>

<style scoped>
.blocked-page {
  padding: 40px 24px;
  min-height: calc(100vh - 140px);
}

.blocked-header {
  text-align: center;
  margin-bottom: 28px;
}

.blocked-header h1 {
  color: #9f1239;
}

.blocked-header p {
  color: #6b213d;
}

.blocked-list {
  max-width: 760px;
  margin: 0 auto;
  display: grid;
  gap: 14px;
}

.blocked-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 18px;
  border-radius: 14px;
  border: 1px solid rgba(251, 113, 133, 0.16);
  box-shadow: 0 10px 24px rgba(190, 24, 93, 0.08);
}

.blocked-card h2 {
  color: #4a1d2b;
  margin-bottom: 4px;
}

.blocked-card p {
  color: #7f3148;
}

button {
  border: none;
  border-radius: 999px;
  background: #fee2e2;
  color: #b91c1c;
  padding: 8px 14px;
  cursor: pointer;
  font-weight: 600;
}

.error {
  color: #c0392b;
  text-align: center;
}

.success {
  color: #15803d;
  font-weight: 600;
  text-align: center;
}

.empty-state {
  text-align: center;
  background: rgba(255, 255, 255, 0.96);
  max-width: 480px;
  margin: 0 auto;
  padding: 28px;
  border-radius: 14px;
}
</style>