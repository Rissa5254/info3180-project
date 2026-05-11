<template>
  <article class="profile-card">
    <!-- Profile Picture -->
    <img
      v-if="profile.profile_picture"
      :src="getProfilePictureUrl(profile.profile_picture)"
      alt="Profile picture"
      class="profile-img"
    />
    <div v-else class="profile-placeholder">
      {{ profile.first_name?.charAt(0) || '?' }}
    </div>

    <!-- Profile Info -->
    <h2>{{ profile.first_name }} {{ profile.last_name }}, {{ profile.age }}</h2>
    <p class="muted">@{{ profile.username }}</p>
    <p v-if="profile.gender"><strong>Gender:</strong> {{ profile.gender }}</p>
    <p v-if="profile.bio">{{ profile.bio }}</p>

    <!-- Interests -->
    <div class="interests">
      <span v-for="interest in profile.interests" :key="interest">
        {{ interest }}
      </span>
    </div>

    <!-- Match Score — only shown on browse page -->
    <p v-if="profile.match_percentage !== undefined" class="match-score">
      💚 Match Score: {{ profile.match_percentage }}%
    </p>

    <!-- Like/Pass and Favourite buttons — shown on browse page -->
    <div v-if="showActions" class="card-actions">
      <button class="pass-btn" @click="$emit('action', { userID: profile.userID, action: 'pass' })">
        ✕ Pass
      </button>
      <button class="like-btn" @click="$emit('action', { userID: profile.userID, action: 'like' })">
        💚 Like
      </button>
      <button class="favourite-btn" @click="$emit('favourite', profile.userID)">
        Favourite
      </button>
      <button class="block-btn" @click="$emit('block', profile)">
        Block
      </button>
      <button class="report-btn" @click="$emit('report', profile)">
        Report
      </button>
    </div>

    <!-- Message button — shown on matches page -->
    <div v-if="showMessage" class="card-actions">
      <button class="message-btn" @click="$emit('message', profile.userID)">
        💬 Message
      </button>
    </div>
  </article>
</template>

<script setup>
import { getProfilePictureUrl } from '@/utils/profilePictures'

defineProps({
  profile: { type: Object, required: true },
  showActions: { type: Boolean, default: false },
  showMessage: { type: Boolean, default: false }
})

defineEmits(['action', 'message', 'favourite', 'block', 'report'])
</script>

<style scoped>
.profile-card {
  background: rgba(255, 255, 255, 0.96);
  border: 1px solid rgba(251, 113, 133, 0.16);
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 10px 24px rgba(190, 24, 93, 0.1);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.profile-img,
.profile-placeholder {
  width: 100%;
  height: 180px;
  border-radius: 12px;
  object-fit: cover;
}

.profile-placeholder {
  background: linear-gradient(135deg, #ffe4e6, #fecdd3);
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 48px;
  font-weight: bold;
  color: #9f1239;
}

.muted { color: #7f3148; }

.interests {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 8px;
}

.interests span {
  background: #ffe4e6;
  color: #be123c;
  padding: 5px 8px;
  border-radius: 999px;
  font-size: 13px;
}

.match-score {
  color: #15803d;
  font-weight: 600;
  font-size: 14px;
}

.card-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.like-btn, .pass-btn, .message-btn, .favourite-btn, .block-btn, .report-btn {
  flex: 1;
  border: none;
  border-radius: 999px;
  padding: 10px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
}

.like-btn { background: #dcfce7; color: #15803d; }
.pass-btn { background: #fee2e2; color: #b91c1c; }
.message-btn { background: #ffe4e6; color: #be123c; }
.favourite-btn {background: #fef3c7; color: #92400e;}
.block-btn {background: #fee2e2; color: #991b1b;}
.report-btn {background: #ffe4e6; color: #be123c;}
</style>
