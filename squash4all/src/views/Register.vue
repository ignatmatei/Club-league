<template>
  <div class="max-w-md mx-auto bg-white p-8 rounded-xl shadow-lg mt-10">
    <h2 class="text-3xl font-bold text-gray-800 mb-6 text-center">Join the Ladder</h2>
    <form @submit.prevent="handleRegister" class="space-y-4">
      <div>
        <label class="block text-gray-700 font-medium mb-1">Username</label>
        <input v-model="username" type="text" required class="w-full border border-gray-300 rounded p-2 focus:outline-none focus:border-blue-500" />
      </div>
      <div>
        <label class="block text-gray-700 font-medium mb-1">Password</label>
        <input v-model="password" type="password" required class="w-full border border-gray-300 rounded p-2 focus:outline-none focus:border-blue-500" />
      </div>
      <p v-if="errorMessage" class="text-red-500 text-sm">{{ errorMessage }}</p>
      <button type="submit" class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 rounded transition-colors">
        Create Account
      </button>
    </form>
    <p class="mt-4 text-center text-gray-600 text-sm">
      Already a member? <router-link to="/login" class="text-blue-600 hover:underline">Sign in</router-link>.
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { API_URL } from '../config.js';

const router = useRouter();
const username = ref('');
const password = ref('');
const errorMessage = ref('');

const handleRegister = async () => {
  try {
    const res = await axios.post(`${API_URL}/register`, {
      username: username.value,
      password: password.value
    });
    // Automatically log them in after registering
    localStorage.setItem('user', JSON.stringify(res.data));
    window.dispatchEvent(new Event('auth-change'));
    router.push('/');
  } catch (err) {
    errorMessage.value = err.response?.data?.error || 'Registration failed.';
  }
};
</script>
