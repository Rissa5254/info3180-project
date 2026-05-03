<script setup>
import { RouterView } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
</script>

<template>
  <div class="app-shell">
    <AppHeader />

    <main class="app-main">
      <RouterView />
    </main>

    <AppFooter />
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background:
    radial-gradient(circle at top, rgba(251, 113, 133, 0.22), transparent 30%),
    radial-gradient(circle at bottom right, rgba(244, 114, 182, 0.18), transparent 28%),
    linear-gradient(180deg, #fff4f6 0%, #fff1f2 55%, #ffffff 100%);
}

.app-main {
  flex: 1;
}
</style>
