<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const favouriteProfiles = ref([])
const error = ref('')
const success = ref('')
const loading = ref(true)

async function loadFavourites() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/favourites')
    favouriteProfiles.value = response.data
  } catch (err) {
    error.value = err.response?.data?.error || 'Could not load favourites'
  } finally {
    loading.value = false
  }
}

async function removeFavourite(userID) {
  error.value = ''
  success.value = ''

  try {
    const response = await api.delete(`/favourites/${userID}`)
    favouriteProfiles.value = favouriteProfiles.value.filter(user => user.userID !== userID)
    success.value = response.data.message
  } catch (err) {
    error.value = err.response?.data?.error || 'Could not remove favourite'
  }
}

onMounted(loadFavourites)
</script>

<template>
  <main class="favourite-page">
    <section class="favourite-header">
      <h1>Saved Favourite Profiles</h1>
      <p>Profiles you saved from the Browse page.</p>
    </section>

    <p v-if="loading">Loading favourites...</p>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>

    <section v-if="!loading && favouriteProfiles.length === 0" class="empty-state">
      <h3>No favourite profiles found.</h3>
      <p>Go to Browse and click Favourite on a profile to save it here.</p>
    </section>

    <section v-else class="grid">
      <article v-for="user in favouriteProfiles" :key="user.userID" class="card">
        <img
          v-if="user.profile_picture"
          :src="`/static/uploads/${user.profile_picture}`"
          alt="Profile picture"
          class="profile-img"
        />

        <div v-else class="profile-placeholder">
          {{ user.first_name?.charAt(0) || user.username?.charAt(0) || '?' }}
        </div>

        <h3>{{ user.first_name }} {{ user.last_name }}</h3>
        <p class="muted">@{{ user.username }}</p>
        <p v-if="user.bio">{{ user.bio }}</p>

        <button @click="removeFavourite(user.userID)">Remove</button>
      </article>
    </section>
  </main>
</template>

<style scoped>
.favourite-page {
  padding: 40px 24px;
  min-height: calc(100vh - 140px);
}

.favourite-header {
  text-align: center;
  margin-bottom: 32px;
}

.favourite-header h1 {
  color: #9f1239;
  margin-bottom: 8px;
}

.favourite-header p {
  color: #6b213d;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 20px;
}

.card,
.empty-state {
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

.muted {
  color: #7f3148;
  margin-bottom: 10px;
}

button {
  margin-top: 12px;
  border: none;
  border-radius: 999px;
  padding: 8px 14px;
  background: #ffe4e6;
  color: #be123c;
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
  max-width: 480px;
  margin: 0 auto;
  text-align: center;
}
</style>