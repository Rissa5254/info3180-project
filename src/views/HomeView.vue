<script setup>
import { ref } from "vue";

let message = ref(`DriftDater is a web platform that helps you to connect with people who share the same vibe like you, interests and location. 
It also allows you to create detailed profiles, discover compatible matches and initiate connections with other users.`)

</script>

<template>
    <div class="container">
      <div class="text-center">
        <h1 class="title">Hello User👋 Welcome to DriftDater</h1>
        <img alt="App logo" class="logo" src="/src/assets/logo.svg" width="250" height="200" />
        
        <h2 class="mt-3 subtitle">{{ message }}</h2>

        <!---Floating Hearts--->
        <div class="hearts">
          <span class="heart ">💖</span>
          <span class="heart ">💗</span>
          <span class="heart ">❤️</span>
          <span class="heart ">💘</span>
        </div>

      </div>
    </div>
</template>

<style scoped>
/* Add any component specific styles here */

.title{
  margin-top: 20px;
  font-family: Georgia, 'Times New Roman', Times, serif;
}

.subtitle{
  font-size: 20px;
  font-weight: 300;
  font-style: italic;
}

.hearts {
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 1;
}

.heart{
  position: absolute;
  animation: floatUp 5s infinite ease-in-out;
  opacity: 0.8;
  font-size: 24px;
}

.heart:nth-child(1) { top: 35%; left: 10%; }
.heart:nth-child(2) { top: 90%; left: 85%;  }
.heart:nth-child(3) { top: 35%; left: 85%; }
.heart:nth-child(4) { top: 90%; left: 10%; }

@keyframes floatUp {
  0% {
    transform: translateY(0) scale(1);
    opacity: 0.2;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: translateY(-60px) scale(1.2);
    opacity: 0;
  }
}
</style>