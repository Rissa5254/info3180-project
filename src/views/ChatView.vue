<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import api from '@/services/api'

const conversations = ref([])
const selectedUser = ref(null)
const messages = ref([])
const text = ref('')
const error = ref('')
const currentUserID =
  JSON.parse(localStorage.getItem('authStore') || localStorage.getItem('user') || '{}')?.user?.userID ||
  JSON.parse(localStorage.getItem('user') || '{}')?.userID

let intervalId = null

async function loadConversations() {
  try {
    error.value = ''
    const response = await api.get('/conversations')
    conversations.value = response.data

    if (!selectedUser.value && conversations.value.length > 0) {
      selectedUser.value = conversations.value[0]
      await loadMessages()
    }
  } catch (err) {
    error.value = err.response?.data?.error || err.message
  }
}

async function loadMessages() {
  if (!selectedUser.value) return

  try {
    error.value = ''
    const response = await api.get(`/messages/${selectedUser.value.userID}`)
    messages.value = response.data
  } catch (err) {
    error.value = err.response?.data?.error || err.message
  }
}

async function selectConversation(user) {
  selectedUser.value = user
  messages.value = []
  await loadMessages()
}

async function send() {
  if (!text.value.trim() || !selectedUser.value) return

  try {
    error.value = ''

    await api.post('/messages', {
      receiver_id: selectedUser.value.userID,
      content: text.value
    })

    text.value = ''
    await loadMessages()
  } catch (err) {
    error.value = err.response?.data?.error || err.message
  }
}

function formatTime(timestamp) {
  if (!timestamp) return ''

  return new Date(timestamp).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(async () => {
  await loadConversations()

  intervalId = setInterval(() => {
    loadMessages()
  }, 3000)
})

onUnmounted(() => {
  clearInterval(intervalId)
})
</script>


<template>
  <div class="chat">
    <h2>Chat</h2>

    <div class="conversation-list" v-if="conversations.length > 0">
      <button
        v-for="user in conversations"
        :key="user.userID"
        @click="selectConversation(user)"
        :class="{ active: selectedUser?.userID === user.userID }"
      >
        {{ user.username }}
      </button>
    </div>

    <p v-else class="empty">
      No conversations yet.
    </p>

    <p v-if="error" class="error">
      {{ error }}
    </p>

    <div class="messages">
      <div
        v-for="msg in messages"
        :key="msg.messageID"
        class="bubble"
      >
        <strong class="sender">
          {{ msg.sender_name || msg.sender_username || 'User' }}
        </strong>

        <p>{{ msg.content }}</p>

        <span class="timestamp">
          {{ formatTime(msg.timestamp) }}
        </span>
      </div>

      <p v-if="messages.length === 0" class="empty">
        No messages yet.
      </p>
    </div>

    <div v-if="selectedUser" class="input-row">
      <input
        v-model="text"
        placeholder="Type a message..."
        @keydown.enter="send"
      />

      <button @click="send">
        Send
      </button>
    </div>
  </div>
</template>


<style scoped>
.chat {
  max-width: 600px;
  margin: 2rem auto;
  font-family: sans-serif;
}

.messages {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  height: 400px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: #f9f9f9;
  margin-bottom: 12px;
}

.bubble {
  align-self: flex-start;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 14px;
  padding: 10px 14px;
  max-width: 70%;
  font-size: 14px;
}

.bubble.mine {
  align-self: flex-end;
  background: #ffe4e6;
  border-color: #fecdd3;
}

.bubble p {
  margin: 0;
}

.timestamp {
  display: block;
  margin-top: 4px;
  font-size: 11px;
  color: #7f3148;
  text-align: right;
}

.input-row {
  display: flex;
  gap: 8px;
}

.input-row input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
}

.input-row button {
  padding: 10px 20px;
  background: #1a1a2e;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}

.conversation-list {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.conversation-list button {
  border: none;
  border-radius: 999px;
  padding: 8px 14px;
  background: #ffe4e6;
  color: #be123c;
  cursor: pointer;
  font-weight: 600;
}

.conversation-list button.active {
  background: #e11d48;
  color: white;
}

.sender {
  display: block;
  margin-bottom: 4px;
  color: #be123c;
  font-size: 12px;
}

.error {
  color: red;
  margin-bottom: 10px;
}

.empty {
  text-align: center;
  color: #888;
  margin-top: 20px;
}
</style>