<script setup>
import { onMounted, ref, reactive, computed } from 'vue'
import { useMatchesStore } from '@/stores/matches'
import MatchCard from '@/components/MatchCard.vue'
import api from '@/services/api'

const matchesStore = useMatchesStore()

const error = ref('')
const success = ref('')

const reportingUser = ref(null)
const reportReason = ref('')
const blockingUser = ref(null)

// Mutual match notification
const showMatchNotification = ref(false)
const matchedName = ref('')

const filters = reactive({
  q: '',
  ageRange: '',
  location: ''
})

const filteredProfiles = computed(() => {
  return matchesStore.discoveredProfiles.filter(user => {
    
    // Search by name or bio
    const searchMatch =
      !filters.q ||
      user.first_name?.toLowerCase().includes(filters.q.toLowerCase()) ||
      user.last_name?.toLowerCase().includes(filters.q.toLowerCase()) ||
      user.bio?.toLowerCase().includes(filters.q.toLowerCase())

    // Location filter
    const userLocation = `${user.location?.city || ''} ${user.location?.country || ''}`.toLowerCase()

    const locationMatch =
      !filters.location ||
      userLocation.includes(filters.location.toLowerCase())

    // Age filter
    let ageMatch = true
    if (filters.ageRange === '18-25') ageMatch = user.age >= 18 && user.age <= 25
    else if (filters.ageRange === '26-35') ageMatch = user.age >= 26 && user.age <= 35
    else if (filters.ageRange === '36-50') ageMatch = user.age >= 36 && user.age <= 50
    else if (filters.ageRange === '51+') ageMatch = user.age >= 51

    return searchMatch && locationMatch && ageMatch
  })
})

function resetFilters() {
  filters.q = ''
  filters.ageRange = ''
  filters.location = ''
}

// Like or Pass handler
async function handleAction({ userID, action }) {
  const profile = matchesStore.discoveredProfiles.find(p => p.userID === userID)
  const result = await matchesStore.likeUser(userID, action)

  if (result?.mutual_match) {
    matchedName.value = profile?.first_name || 'Someone'
    showMatchNotification.value = true
  }
}

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
    // Remove blocked user from the list
    matchesStore.discoveredProfiles = matchesStore.discoveredProfiles.filter(
      u => u.userID !== blockingUser.value.userID
    )
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

async function saveFavourite(userID) {
  error.value = ''
  success.value = ''

  try {
    const response = await api.post('/favourites', {
      saved_user_id: userID
    })

    success.value = response.data.message
  } catch (err) {
    error.value = err.response?.data?.error || 'Could not save favourite'
  }
}

onMounted(() => {
  matchesStore.fetchDiscoveredProfiles()
})
</script>

<template>
  <main class="browse-page">
    <section class="browse-header">
      <h1>Browse Matches</h1>
      <p>Discover compatible profiles on DriftDater.</p>
    </section>

    <!-- Filters -->
    <div class="filters">
      <input v-model="filters.q" placeholder="Search by name or bio..." />
      <select v-model="filters.ageRange">
        <option value="">All Ages</option>
        <option value="18-25">18-25</option>
        <option value="26-35">26-35</option>
        <option value="36-50">36-50</option>
        <option value="51+">51+</option>
      </select>
      <input v-model="filters.location" placeholder="Filter by location..." />
    </div>

    <button class="reset-btn" @click="resetFilters">Reset Filters</button>

    <p v-if="matchesStore.loading">Loading profiles...</p>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>

    <section v-if="!matchesStore.loading && filteredProfiles.length === 0" class="empty-state">
      <h2>No profiles found</h2>
      <p>Try adjusting your filters or check back later.</p>
    </section>

    <!-- Profile Cards using MatchCard component -->
    <section class="profile-grid">
      <MatchCard
        v-for="profile in filteredProfiles"
        :key="profile.userID"
        :profile="profile"
        :showActions="true"
        @action="handleAction"
        @block="openBlock"
        @report="openReport"
        @favourite="saveFavourite"
      />
    </section>

    <!-- Mutual Match Popup -->
    <div v-if="showMatchNotification" class="modal-overlay">
      <section class="modal-box">
        <h2>🎉 It's a Match!</h2>
        <p>You and {{ matchedName }} liked each other!</p>
        <div class="report-actions">
          <button class="like-btn" @click="$router.push('/matches')">View Matches</button>
          <button class="cancel-btn" @click="showMatchNotification = false">Keep Browsing</button>
        </div>
      </section>
    </div>

    <!-- Block Modal -->
    <div v-if="blockingUser" class="modal-overlay">
      <section class="modal-box">
        <h2>Block @{{ blockingUser.username }}</h2>
        <p>Are you sure you want to block this user?</p>
        <div class="report-actions">
          <button class="block-btn" @click="confirmBlock">Yes, Block</button>
          <button class="cancel-btn" @click="cancelBlock">Cancel</button>
        </div>
      </section>
    </div>

    <!-- Report Modal -->
    <div v-if="reportingUser" class="modal-overlay">
      <section class="modal-box">
        <h2>Report @{{ reportingUser.username }}</h2>
        <textarea v-model="reportReason" placeholder="Enter reason for report"></textarea>
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
.browse-header h1 { color: #9f1239; margin-bottom: 8px; }
.browse-header p { color: #6b213d; }
.filters {
  display: flex;
  gap: 12px;
  margin-bottom: 10px;
  margin-top: 15px;
}
.filters input, select, .reset-btn {
  width: 100%;
  border: none;
  border-radius: 5px;
  padding: 5px;
}
.reset-btn {
  margin-bottom: 10px;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
  background: linear-gradient(135deg, #fb7185, #e11d48);
  border-radius: 8px;
}
.reset-btn:hover { background-color: rgb(163, 159, 159); }
.profile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 20px;
}
.error { color: #c0392b; }
.success { color: #15803d; font-weight: 600; text-align: center; }
.empty-state {
  text-align: center;
  background: rgba(255, 255, 255, 0.96);
  max-width: 480px;
  margin: 0 auto 28px;
  padding: 28px;
  border: 1px solid rgba(251, 113, 133, 0.16);
  border-radius: 14px;
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
.modal-box h2 { color: #9f1239; }
.modal-box p { color: #4a1d2b; }
.modal-box textarea {
  width: 100%;
  min-height: 110px;
  padding: 12px;
  border: 1px solid #fecdd3;
  border-radius: 10px;
  resize: vertical;
}
.report-actions { display: flex; gap: 10px; }
.report-actions button {
  border: none;
  border-radius: 999px;
  padding: 8px 14px;
  cursor: pointer;
  font-weight: 600;
}
.block-btn { background: #fee2e2; color: #b91c1c; }
.report-btn { background: #ffe4e6; color: #be123c; }
.cancel-btn { background: #e5e7eb; color: #374151; }
.like-btn { background: #dcfce7; color: #15803d; }
</style>