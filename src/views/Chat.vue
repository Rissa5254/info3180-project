<template>
  <div class="chat">
    <h2>Chat</h2>

    <div class="messages">
      <div v-for="msg in messages" :key="msg.timestamp" class="bubble">
        {{ msg.content }}
      </div>
    </div>

    <div class="input-row">
      <input v-model="text" placeholder="Type a message..." @keydown.enter="send" />
      <button @click="send">Send</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const messages = ref([])
const text = ref('')
const receiver = 2 // replace later

async function load() {
  const res = await fetch(`/api/messages/${receiver}`)
  messages.value = await res.json()
}

async function send() {
  await fetch('/api/messages', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      receiver_id: receiver,
      content: text.value
    })
  })
  text.value = ''
  load()
}

onMounted(() => {
  load()
  setInterval(load, 3000)
})
</script>

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
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 8px 14px;
  max-width: 70%;
  font-size: 14px;
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
</style>