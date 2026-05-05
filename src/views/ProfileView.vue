<script setup>
import { onMounted, ref } from 'vue'
import api from '@/services/api'

const form = ref({
  first_name: '',
  last_name: '',
  date_of_birth: '',
  gender: '',
  looking_for: '',
  bio: '',
  preferred_radius: '',
  profile_visibility: true
})

const error = ref('')
const message = ref('')
const interestsText = ref('')
const selectedFile = ref(null)
const profilePicture = ref('')

onMounted(async () => {
  try {
    const response = await api.get('/profile')
    interestsText.value = response.data.interests?.join(', ') || ''
    profilePicture.value = response.data.profile_picture || ''
    form.value.first_name = response.data.first_name || ''
    form.value.last_name = response.data.last_name || ''
    form.value.date_of_birth = response.data.date_of_birth || ''
    form.value.gender = response.data.gender || ''
    form.value.looking_for = response.data.looking_for || ''
    form.value.bio = response.data.bio || ''
    form.value.preferred_radius = response.data.preferred_radius || ''
    form.value.profile_visibility = response.data.profile_visibility ?? true
  } catch (err) {
    error.value = err.response?.data?.error || 'Could not load profile'
  }
})

function handleFileChange(event) {
  selectedFile.value = event.target.files[0]
}

async function uploadProfilePicture() {
  error.value = ''
  message.value = ''

  if (!selectedFile.value) {
    error.value = 'Please select an image first.'
    return
  }

  const formData = new FormData()
  formData.append('profile_picture', selectedFile.value)

  try {
    const response = await api.post('/profile/picture', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    profilePicture.value = response.data.profile_picture
    message.value = response.data.message
  } catch (err) {
    error.value = err.response?.data?.error || 'Could not upload profile picture'
  }
}

async function updateProfile() {
  error.value = ''
  message.value = ''

  try {
    const interests = interestsText.value
  .split(',')
  .map((interest) => interest.trim())
  .filter((interest) => interest.length > 0)

const response = await api.put('/profile', {
  ...form.value,
  interests
})
    message.value = response.data.message
  } catch (err) {
    error.value = err.response?.data?.error || 'Could not update profile'
  }
}
</script>

<template>
  <main class="profile-page">
    <form class="profile-card" @submit.prevent="updateProfile">
      <h1>Edit Profile</h1>

      <div class="form-row">
        <div class="form-group">
          <label>First Name</label>
          <input v-model="form.first_name" />
        </div>

        <div class="form-group">
          <label>Last Name</label>
          <input v-model="form.last_name" />
        </div>
      </div>

      <div class="form-group">
        <label>Date of Birth</label>
        <input v-model="form.date_of_birth" type="date" />
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Gender</label>
          <select v-model="form.gender">
            <option value="">Select gender</option>
            <option>Male</option>
            <option>Female</option>
            <option>Other</option>
          </select>
        </div>

        <div class="form-group">
          <label>Looking For</label>
          <select v-model="form.looking_for">
            <option value="">Any</option>
            <option>Male</option>
            <option>Female</option>
            <option>Other</option>
          </select>
        </div>
      </div>

      <div class="form-group">
        <label>Bio</label>
        <textarea v-model="form.bio" rows="4"></textarea>
      </div>

      <div class="form-group">
  <label>Interests/Hobbies</label>
  <input
    v-model="interestsText"
    placeholder="Example: football, music, cooking"
  />
  <small>Enter at least 3 interests separated by commas.</small>
</div>

      <div class="form-group">
        <label>Preferred Radius</label>
        <input
          v-model="form.preferred_radius"
          type="number"
          placeholder="Example: 10"
        />
      </div>

      <label class="checkbox-row">
        <input v-model="form.profile_visibility" type="checkbox" />
        Public Profile
      </label>

      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="message" class="success">{{ message }}</p>
<div class="form-group">
  <label>Profile Picture</label>

  <div v-if="profilePicture" class="preview-box">
    <img
      :src="`http://localhost:5000/static/uploads/${profilePicture}`"
      alt="Profile picture"
      class="profile-preview"
    />
  </div>

  <input type="file" accept="image/*" @change="handleFileChange" />

  <button type="button" class="secondary-button" @click="uploadProfilePicture">
    Upload Picture
  </button>
</div>
      <button type="submit">Save Changes</button>
    </form>
  </main>
</template>

<style scoped>
.profile-page {
  min-height: calc(100vh - 140px);
  display: flex;
  justify-content: center;
  padding: 40px 16px;
  background: #f5f7fb;
}

.profile-card {
  width: 100%;
  max-width: 620px;
  background: white;
  padding: 32px;
  border-radius: 14px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
}

.profile-card h1 {
  text-align: center;
  margin-bottom: 24px;
  color: #0d6efd;
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
select,
textarea {
  padding: 11px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 15px;
}

.checkbox-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

button {
  width: 100%;
  padding: 12px;
  background: #0d6efd;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}

.error {
  color: #c0392b;
}

.success {
  color: #198754;
}

.preview-box {
  margin-bottom: 12px;
}

.profile-preview {
  width: 120px;
  height: 120px;
  border-radius: 12px;
  object-fit: cover;
  border: 1px solid #ddd;
}

.secondary-button {
  margin-top: 10px;
  background: #6c757d;
}

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>