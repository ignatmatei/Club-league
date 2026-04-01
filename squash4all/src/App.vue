<template>
  <div class="min-h-screen bg-gray-50 text-gray-800">
    <nav class="bg-blue-900 text-white p-4 shadow-md">
      <div class="max-w-4xl mx-auto flex justify-between items-center">
        <h1 class="text-xl font-bold italic">Squash4All Club</h1>
        <div class="space-x-4">
          <router-link to="/" class="hover:text-blue-300">Leaderboard</router-link>
          <router-link to="/rules" class="hover:text-blue-300">Rules</router-link>
          <router-link to="/messages" class="hover:text-blue-300">Messages</router-link>
          <router-link to="/profile" class="hover:text-blue-300">Profile</router-link>
        </div>
      </div>
    </nav>
    <main class="max-w-4xl mx-auto p-6">
      <router-view></router-view>
    </main>
  </div>
</template>
