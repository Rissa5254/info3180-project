import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    authenticated: false,
    initialized: false
  }),

  actions: {
    async register(payload) {
      const response = await api.post('/register', payload)
      this.user = response.data.user
      this.authenticated = true
      this.initialized = true
      return response.data
    },

    async login(payload) {
      const response = await api.post('/login', payload)
      this.user = response.data.user
      this.authenticated = true
      this.initialized = true
      return response.data
    },

    async logout() {
      try {
        await api.post('/logout')
      } finally {
        this.user = null
        this.authenticated = false
        this.initialized = true
      }
    },

    async checkAuth() {
      try {
        const response = await api.get('/auth/check')
        this.user = response.data.user
        this.authenticated = response.data.authenticated
      } catch {
        this.user = null
        this.authenticated = false
      } finally {
        this.initialized = true
      }
    }
  }
})
