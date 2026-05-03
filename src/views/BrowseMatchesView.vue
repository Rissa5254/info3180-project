<script setup>
import { onMounted, ref } from 'vue'
import api from '@/services/api'

const users = ref([])
const error = ref('')
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await api.get('/users/browse')
    users.value = response.data
  } catch (err) {
    error.value = err.response?.data?.error || 'Could not load users'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <main class="browse-page">
    <section class="browse-header">
      <h1>Browse Matches</h1>
      <p>Discover public profiles on DriftDater.</p>
    </section>

    <p v-if="loading">Loading profiles...</p>
    <p v-if="error" class="error">{{ error }}</p>

    <section v-if="!loading && users.length === 0" class="empty-state">
      <h2>No profiles found</h2>
      <p>Try again after more users create public profiles.</p>
    </section>

    <section class="profile-grid">
      <article v-for="user in users" :key="user.userID" class="profile-card">
        <img
          v-if="user.profile_picture"
          :src="`http://localhost:5000/static/uploads/${user.profile_picture}`"
          alt="Profile picture"
          class="profile-img"
        />

        <div v-else class="profile-placeholder">
          {{ user.first_name?.charAt(0) || user.username?.charAt(0) }}
        </div>

        <h2>{{ user.first_name }} {{ user.last_name }}</h2>
        <p class="muted">@{{ user.username }}</p>

        <p v-if="user.age"><strong>Age:</strong> {{ user.age }}</p>
        <p v-if="user.gender"><strong>Gender:</strong> {{ user.gender }}</p>
        <p v-if="user.bio">{{ user.bio }}</p>

        <div class="interests">
          <span v-for="interest in user.interests" :key="interest">
            {{ interest }}
          </span>
        </div>
      </article>
    </section>
  </main>
</template>

<style scoped>
.browse-page {
  padding: 40px 24px;
  min-height: calc(100vh - 140px);
}

.browse-header {
  text-align: center;
  margin-bottom: 32px;
}

.browse-header h1 {
  color: #9f1239;
  margin-bottom: 8px;
}

.browse-header p {
  color: #6b213d;
}

.profile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 20px;
}

.profile-card {
  background: rgba(255, 255, 255, 0.96);
  border: 1px solid rgba(251, 113, 133, 0.16);
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 10px 24px rgba(190, 24, 93, 0.1);
}

.profile-img,
.profile-placeholder {
  width: 100%;
  height: 180px;
  border-radius: 12px;
  object-fit: cover;
  margin-bottom: 14px;
}

.profile-placeholder {
  background: linear-gradient(135deg, #ffe4e6, #fecdd3);
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 48px;
  font-weight: bold;
  color: #9f1239;
}

.profile-card h2 {
  margin-bottom: 4px;
  color: #4a1d2b;
}

.muted {
  color: #7f3148;
  margin-bottom: 12px;
}

.interests {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 12px;
}

.interests span {
  background: #ffe4e6;
  color: #be123c;
  padding: 5px 8px;
  border-radius: 999px;
  font-size: 13px;
}

.error {
  color: #c0392b;
}

.empty-state {
  text-align: center;
  background: rgba(255, 255, 255, 0.96);
  max-width: 480px;
  margin: 0 auto 28px;
  padding: 28px;
  border: 1px solid rgba(251, 113, 133, 0.16);
  border-radius: 14px;
}
</style>
