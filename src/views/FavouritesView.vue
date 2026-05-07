<template>
    <div class="favourite-page">
        <h1> Saved Favourite Profiles</h1>

        <p v-if="loading">Loading profiles...</p>
        <p v-if="error" class="error">{{ error }}</p>
        
        <div v-if="!loading && favouriteProfiles.length === 0" >
            <h2>No favourites profiles found.</h2>
        </div>

        <div class="grid" v-else>
            <div v-for="user in favouriteProfiles" :key="user.userID" class="card">
                <h3>{{ user.name }}</h3>
                <p>{{ user.age }} years old</p>
                <p>{{ user.location }}</p>

                <button @click="removeFavourite(user.userID)">Remove</button>
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
</style>
