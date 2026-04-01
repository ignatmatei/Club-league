<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-800">Club Ranking</h2>
      <button 
        @click="activateGoldenMatch"
        :disabled="!canUseGoldenMatch"
        class="bg-yellow-400 hover:bg-yellow-500 text-yellow-900 font-bold py-2 px-4 rounded shadow disabled:opacity-50 transition-colors"
      >
        🌟 Golden Match {{ isGoldenActive ? '(ACTIVE)' : '' }}
      </button>
    </div>

    <div class="bg-white shadow rounded-lg overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead class="bg-gray-800 text-white">
          <tr>
            <th class="p-4">Rank</th>
            <th class="p-4">Player</th>
            <th class="p-4">Points</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(player, index) in leaderboard" :key="player.id" 
              @click="handleRowClick(player, index)"
              :class="getRowClass(index)"
              class="border-b transition-colors">
            <td class="p-4 font-bold">{{ index + 1 }}</td>
            <td class="p-4 flex items-center gap-2">
              {{ player.username }} 
              <span v-if="index === currentUserIndex" class="bg-blue-600 text-white text-xs px-2 py-1 rounded shadow-sm">You</span>
            </td>
            <td class="p-4 font-mono">{{ player.points }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="selectedPlayer" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50" @click.self="closeModal">
      <div class="bg-white p-6 rounded-xl w-96 shadow-2xl">
        <h3 class="text-xl font-bold mb-2 text-gray-800">
          Challenge {{ selectedPlayer.username }}
        </h3>
        <p class="mb-6 text-sm text-gray-600">
          Currently ranked #{{ leaderboard.indexOf(selectedPlayer) + 1 }}. Choose your action.
        </p>
        
        <div class="flex flex-col gap-3">
          <button class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded transition-colors">
            💬 Send Message
          </button>
          <button @click="submitResult" class="bg-green-600 hover:bg-green-700 text-white font-semibold py-3 rounded transition-colors">
            🏆 Enter Result (I Won!)
          </button>
          <button @click="closeModal" class="mt-2 text-gray-500 hover:text-gray-800 font-medium py-2 transition-colors">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

// Safely grab the username from LocalStorage, or fallback to empty string if not logged in
const storedUser = JSON.parse(localStorage.getItem('user') || '{}');
const myUsername = storedUser.username || '';const leaderboard = ref([]);

const selectedPlayer = ref(null);
const isGoldenActive = ref(false);

// Dynamically grab your full user object from the downloaded leaderboard
const currentUser = computed(() => {
  return leaderboard.value.find(p => p.username === myUsername) || {};
});

// Dynamically find your exact index
const currentUserIndex = computed(() => {
  return leaderboard.value.findIndex(p => p.username === myUsername);
});

// Check if Golden Match is available
const canUseGoldenMatch = computed(() => {
  if (!currentUser.value.last_golden_match) return true;
  const lastDate = new Date(currentUser.value.last_golden_match);
  const sixMonthsAgo = new Date();
  sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);
  return lastDate < sixMonthsAgo;
});

const activateGoldenMatch = () => {
  if (canUseGoldenMatch.value) {
    isGoldenActive.value = !isGoldenActive.value;
  }
};

const canChallenge = (index) => {
  const myIndex = currentUserIndex.value;
  
  // Failsafe: If myIndex is -1, it means 'Matei Ignat' is missing from the DB entirely!
  if (myIndex === -1 || index >= myIndex) return false; 
  
  const distance = myIndex - index;
  
  if (isGoldenActive.value) return true; 
  return distance > 0 && distance <= 4; 
};

const handleRowClick = (player, index) => {
  if (canChallenge(index)) {
    selectedPlayer.value = player;
  }
};

const closeModal = () => {
  selectedPlayer.value = null;
};

const getRowClass = (index) => {
  const myIndex = currentUserIndex.value;
  
  if (index === myIndex) return 'bg-blue-50 text-blue-900 border-l-4 border-blue-600'; 
  
  if (canChallenge(index)) {
    const distance = myIndex - index;
    if (isGoldenActive.value && distance > 4) return 'bg-yellow-50 hover:bg-yellow-100 cursor-pointer border-l-4 border-yellow-400';
    if (distance === 1) return 'bg-green-200 hover:bg-green-300 cursor-pointer border-l-4 border-green-600';
    if (distance === 2) return 'bg-green-100 hover:bg-green-200 cursor-pointer border-l-4 border-green-500';
    if (distance === 3) return 'bg-green-50 hover:bg-green-100 cursor-pointer border-l-4 border-green-400';
    if (distance === 4) return 'bg-green-50/50 hover:bg-green-50 cursor-pointer border-l-4 border-green-300';
  }
  
  return 'text-gray-500 bg-white cursor-not-allowed opacity-75';
};

const submitResult = async () => {
  try {
    // We now use currentUser.value.id, which is guaranteed to be correct!
    await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/submit_result`, {
      challenger_id: currentUser.value.id, 
      opponent_id: selectedPlayer.value.id,
      is_golden: isGoldenActive.value
    });
    alert(`Result submitted! Waiting for ${selectedPlayer.value.username} to confirm.`);
    closeModal();
    isGoldenActive.value = false;
  } catch (error) {
    console.error("Error submitting result", error);
    alert("Failed to submit result.");
  }
};

onMounted(async () => {
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/leaderboard`);
    leaderboard.value = res.data;
  } catch (err) {
    console.error("Could not load leaderboard.", err);
  }
});
</script>
