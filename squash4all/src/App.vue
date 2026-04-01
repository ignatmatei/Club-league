<template>
  <div class="min-h-screen bg-gray-50 text-gray-800">
    <nav class="bg-blue-900 text-white p-4 shadow-md">
      <div class="max-w-4xl mx-auto flex justify-between items-center">
        <h1 class="text-xl font-bold italic">Squash4All Club</h1>
        
        <div v-if="isAuthenticated" class="space-x-4 flex items-center">
          <router-link to="/" class="hover:text-blue-300">Leaderboard</router-link>
          <router-link to="/rules" class="hover:text-blue-300">Rules</router-link>
          <router-link to="/messages" class="hover:text-blue-300">Messages</router-link>
          <router-link to="/profile" class="hover:text-blue-300">Profile</router-link>
          <button @click="logout" class="ml-4 bg-red-500 hover:bg-red-600 px-3 py-1 rounded text-sm transition-colors">
            Logout
          </button>
        </div>
        <div v-else class="space-x-4">
          <router-link to="/login" class="hover:text-blue-300">Login</router-link>
        </div>

      </div>
    </nav>
    <main class="max-w-4xl mx-auto p-6">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isAuthenticated = ref(false);

const checkAuth = () => {
  isAuthenticated.value = !!localStorage.getItem('user');
};

const logout = () => {
  localStorage.removeItem('user');
  checkAuth();
  router.push('/login');
};

onMounted(() => {
  checkAuth();
  // Listen for login/register events from other components
  window.addEventListener('auth-change', checkAuth);
});

onUnmounted(() => {
  window.removeEventListener('auth-change', checkAuth);
});
</script>
