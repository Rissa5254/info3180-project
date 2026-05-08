import { defineStore } from 'pinia'
import api from '@/services/api'

export const useMatchesStore = defineStore('matches', {
  state: () => ({
    discoveredProfiles: [],  // potential matches from /api/matches/discover
    myMatches: [],           // confirmed mutual matches from /api/matches
    matchCount: 0,
    loading: false,
    error: null
  }),

  actions: {
    // Fetch scored potential matches for the browse page
    async fetchDiscoveredProfiles() {
      this.loading = true
      this.error = null
      try {
        const res = await api.get('/matches/discover')
        this.discoveredProfiles = res.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to load profiles'
      } finally {
        this.loading = false
      }
    },

    // Like or pass on a user — removes them from the list after action
    async likeUser(likedUserID, action) {
      try {
        const res = await api.post(`/matches/like/${likedUserID}`, { action })
        // Remove the card from the list immediately
        this.discoveredProfiles = this.discoveredProfiles.filter(
          p => p.userID !== likedUserID
        )
        // If mutual match, update the count
        if (res.data.mutual_match) {
          this.matchCount += 1
        }
        return res.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Action failed'
        return null
      }
    },

    // Fetch all confirmed mutual matches
    async fetchMyMatches() {
      this.loading = true
      this.error = null
      try {
        const res = await api.get('/matches')
        this.myMatches = res.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to load matches'
      } finally {
        this.loading = false
      }
    },

    // Fetch total match count for the navbar
    async fetchMatchCount() {
      try {
        const res = await api.get('/matches/count')
        this.matchCount = res.data.match_count
      } catch (err) {
        console.error('Could not fetch match count')
      }
    }
  }
})