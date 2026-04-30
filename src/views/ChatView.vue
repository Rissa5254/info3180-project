<template>
  <div>
    <h2>Chat</h2>

    <div v-for="msg in messages" :key="msg.timestamp">
      {{ msg.content }}
    </div>

    <input v-model="text" />
    <button @click="send">Send</button>
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
    headers: {'Content-Type': 'application/json'},
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