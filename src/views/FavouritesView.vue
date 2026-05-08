<template>
    <div class="favourite-page">
        <section class="favourite-header">
            <h1>Saved Favourite Profiles</h1>
        </section>

        <p v-if="loading">Loading profiles...</p>
        <p v-if="error" class="error">{{ error }}</p>
        
        <div v-if="favouriteProfiles.length === 0" class="empty-state">
            <h3>No favourites profiles found.</h3>
        </div>

        <div v-else class="grid">
            <div v-for="user in favouriteProfiles" :key="user.userID" class="card">
                 <button @click="removeFavourite(user.userID)">Remove</button>
            </div>
            <div class="info">
                <h3>{{ user.name }}</h3>
                <p>{{ user.age }} years old</p>
                <p>{{ user.location }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const favouriteProfiles = ref([])
const error = ref('')
const loading = ref(true)

const userID = JSON.parse(localStorage.getItem('user'))?.userID

const loadFavourites = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get(`/favourites/${userID}`)
    const ids = response.data.map(f => f.saved_user_id)
    const profileRequests = ids.map(id => api.get(`/users/${id}`))
    
    const profiles = await Promise.all(profileRequests)

    favouriteProfiles.value = profiles.map(p => p.data)

  } catch (err) {
    error.value = err.response?.data?.error || 'Could not load users'
  } finally {
    loading.value = false
  }
}

// Remove favourite
const removeFavourite = async (savedUserId) => {
  try {
    await api.delete(`/favourites/${userID}/${savedUserId}`)
    loadFavourites()
  } catch (err) {
    error.value = 'Failed to remove favourite'
  }
}

onMounted(() => {
    if (userID) loadFavourites()
})

</script>

<style scoped>
.favourite-page {
  padding: 20px;
}

.favourite-header {
  text-align: center;
  margin-bottom: 32px;
}

.favourite-header h1 {
  color: #9f1239;
  margin-bottom: 8px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 15px;
}

.card {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
}

.error {
  color: red;
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
