<script setup>
import { onMounted, ref } from 'vue'
import api from '@/services/api'

const users = ref([])
const error = ref('')
const success = ref('')
const loading = ref(true)
const reportingUser = ref(null)
const reportReason = ref('')
const blockingUser = ref(null)

function openBlock(user) {
  blockingUser.value = user
  error.value = ''
  success.value = ''
}

function cancelBlock() {
  blockingUser.value = null
}

async function confirmBlock() {
  error.value = ''
  success.value = ''

  try {
    await api.post(`/users/${blockingUser.value.userID}/block`)
    users.value = users.value.filter(user => user.userID !== blockingUser.value.userID)
    success.value = 'User blocked successfully.'
    blockingUser.value = null
  } catch (err) {
    error.value = err.response?.data?.error || 'Could not block user'
  }
}

function openReport(user) {
  reportingUser.value = user
  reportReason.value = ''
  error.value = ''
  success.value = ''
}

function cancelReport() {
  reportingUser.value = null
  reportReason.value = ''
}

async function submitReport() {
  error.value = ''
  success.value = ''

  if (!reportReason.value.trim()) {
    error.value = 'Please enter a reason for the report.'
    return
  }

  try {
    await api.post(`/users/${reportingUser.value.userID}/report`, {
      reason: reportReason.value
    })

    success.value = 'User reported successfully.'
    reportingUser.value = null
    reportReason.value = ''
  } catch (err) {
    error.value = err.response?.data?.error || 'Could not report user'
  }
}

async function loadUsers() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/users/browse')
    users.value = response.data
  } catch (err) {
    error.value = err.response?.data?.error || 'Could not load users'
  } finally {
    loading.value = false
  }
}

onMounted(loadUsers)
</script>

<template>
  <main class="browse-page">
    <section class="browse-header">
      <h1>Browse Matches</h1>
      <p>Discover public profiles on DriftDater.</p>
    </section>

    <p v-if="loading">Loading profiles...</p>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>

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

        <div class="card-actions">
          <button type="button" class="block-btn" @click.stop="openBlock(user)"> Block</button>
          <button type="button" class="report-btn" @click.stop="openReport(user)"> Report </button>
        </div>
      </article>
    </section>

    <div v-if="blockingUser" class="modal-overlay">
      <section class="modal-box">
        <h2>Block @{{ blockingUser.username }}</h2>
        <p>
          Are you sure you want to block this user? They will no longer appear in your browse list.
        </p>

        <div class="report-actions">
          <button class="block-btn" @click="confirmBlock">Yes, Block</button>
          <button class="cancel-btn" @click="cancelBlock">Cancel</button>
        </div>
      </section>
    </div>

    <div v-if="reportingUser" class="modal-overlay">
      <section class="modal-box">
        <h2>Report @{{ reportingUser.username }}</h2>

        <textarea
          v-model="reportReason"
          placeholder="Enter reason for report"
        ></textarea>

        <div class="report-actions">
          <button class="report-btn" @click="submitReport">Submit Report</button>
          <button class="cancel-btn" @click="cancelReport">Cancel</button>
        </div>
      </section>
    </div>

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

.success {
  color: #15803d;
  font-weight: 600;
  text-align: center;
}

.card-actions {
  display: flex;
  gap: 10px;
  margin-top: 14px;
}

.card-actions button,
.report-actions button {
  border: none;
  border-radius: 999px;
  padding: 8px 14px;
  cursor: pointer;
  font-weight: 600;
}

.block-btn {
  background: #fee2e2;
  color: #b91c1c;
}

.report-btn {
  background: #ffe4e6;
  color: #be123c;
}

.cancel-btn {
  background: #e5e7eb;
  color: #374151;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(74, 29, 43, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  z-index: 100;
  backdrop-filter: blur(3px);
}

.modal-box {
  width: min(520px, 100%);
  background: white;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 18px 40px rgba(74, 29, 43, 0.25);

  display: flex;
  flex-direction: column;
  gap: 12px;
}

.modal-box h2 {
  color: #9f1239;
  margin-bottom: 10px;
}

.modal-box p {
  color: #4a1d2b;
  margin-bottom: 16px;
}

.modal-box textarea {
  width: 100%;
  min-height: 110px;
  margin: 12px 0;
  padding: 12px;
  border: 1px solid #fecdd3;
  border-radius: 10px;
  resize: vertical;
}

.report-actions {
  display: flex;
  gap: 10px;
}

</style>