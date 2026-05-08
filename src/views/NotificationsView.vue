<script setup>
import { onMounted, ref } from 'vue'
import api from '@/services/api'

const notifications = ref([])
const loading = ref(true)
const error = ref('')

async function loadNotifications() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/notifications')
    notifications.value = response.data
  } catch (err) {
    error.value = err.response?.data?.error || 'Could not load notifications'
  } finally {
    loading.value = false
  }
}

async function markAsRead(notificationID) {
  error.value = ''

  try {
    await api.put(`/notifications/${notificationID}/read`)

    const notification = notifications.value.find(
      item => item.notificationID === notificationID
    )

    if (notification) {
      notification.is_read = true
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Could not update notification'
  }
}

onMounted(loadNotifications)
</script>

<template>
  <main class="notifications-page">
    <section class="notifications-header">
      <h1>Notifications</h1>
      <p>View recent updates and alerts from DriftDater.</p>
    </section>

    <p v-if="loading" class="loading">Loading notifications...</p>
    <p v-if="error" class="error">{{ error }}</p>

    <section v-if="!loading && notifications.length === 0" class="empty-state">
      <h2>No notifications yet</h2>
      <p>You have no new notifications right now.</p>
    </section>

    <section v-if="notifications.length > 0" class="notification-list">
      <article
        v-for="notification in notifications"
        :key="notification.notificationID"
        class="notification-card"
        :class="{ unread: !notification.is_read }"
      >
        <div>
          <p class="type">{{ notification.type }}</p>
          <p class="content">{{ notification.content }}</p>

          <small v-if="notification.created_at">
            {{ new Date(notification.created_at).toLocaleString() }}
          </small>
        </div>

        <button
          v-if="!notification.is_read"
          @click="markAsRead(notification.notificationID)"
        >
          Mark as read
        </button>

        <span v-else class="read-label">Read</span>
      </article>
    </section>
  </main>
</template>

<style scoped>
.notifications-page {
  padding: 40px 24px;
  min-height: calc(100vh - 140px);
}

.notifications-header {
  text-align: center;
  margin-bottom: 28px;
}

.notifications-header h1 {
  color: #9f1239;
  margin-bottom: 8px;
}

.notifications-header p {
  color: #6b213d;
}

.loading,
.error {
  text-align: center;
}

.error {
  color: #c0392b;
}

.notification-list {
  max-width: 760px;
  margin: 0 auto;
  display: grid;
  gap: 14px;
}

.notification-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  background: white;
  padding: 18px;
  border-radius: 14px;
  border: 1px solid rgba(251, 113, 133, 0.16);
  box-shadow: 0 10px 24px rgba(190, 24, 93, 0.08);
}

.notification-card.unread {
  border-color: #fb7185;
  background: #fff1f2;
}

.type {
  font-weight: 700;
  color: #be123c;
  text-transform: capitalize;
  margin-bottom: 6px;
}

.content {
  color: #4a1d2b;
  margin-bottom: 6px;
}

button {
  border: none;
  border-radius: 999px;
  background: #be123c;
  color: white;
  padding: 8px 14px;
  cursor: pointer;
  font-weight: 600;
  white-space: nowrap;
}

.read-label {
  color: #15803d;
  font-weight: 600;
}

.empty-state {
  text-align: center;
  background: rgba(255, 255, 255, 0.96);
  max-width: 480px;
  margin: 0 auto;
  padding: 28px;
  border: 1px solid rgba(251, 113, 133, 0.16);
  border-radius: 14px;
}
</style>