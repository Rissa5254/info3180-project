<template>
      <footer class="mt-5">
          <div class="container">
              <p>Copyright &copy {{ year }} Group#11.</p>
          </div>
      </footer>
</template>

<script setup>
import { ref } from "vue";

const year = (new Date).getFullYear();
</script>

<style>
/* Add any component specific styles here */
</style>