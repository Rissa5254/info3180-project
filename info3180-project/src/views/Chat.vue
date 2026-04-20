<template>
  <div>
    <h2>Chat</h2>

    <div v-for="msg in messages" :key="msg.timestamp">
      <strong>{{ msg.sender_id }}:</strong> {{ msg.content }}
    </div>

    <input v-model="newMessage" placeholder="Type message..." />
    <button @click="sendMessage">Send</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const messages = ref([])
const newMessage = ref('')
const receiverId = 2 // replace dynamically

async function fetchMessages() {
  const res = await fetch(`/api/messages/${receiverId}`)
  messages.value = await res.json()
}

async function sendMessage() {
  await fetch('/api/messages', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      receiver_id: receiverId,
      content: newMessage.value
    })
  })
  newMessage.value = ''
  fetchMessages()
}

onMounted(() => {
  fetchMessages()
  setInterval(fetchMessages, 3000) // polling
})
</script>