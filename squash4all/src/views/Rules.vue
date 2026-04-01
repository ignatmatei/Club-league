<template>
  <div class="bg-white p-8 rounded-lg shadow prose max-w-none">
    <h2 class="text-3xl font-bold mb-6 text-blue-900">Club Rules & Ranking System</h2>
    
    <h3 class="text-xl font-bold mt-4">1. Standard Challenges</h3>
    <p>A player can challenge only the <strong>4 players directly above them</strong> in the ranking. On the leaderboard, you will see a green color gradient highlighting the players you are eligible to challenge.</p>

    <h3 class="text-xl font-bold mt-4">2. Point System</h3>
    <p>If you win a challenge, you receive points based on your opponent's rank. Thus, the ranking is dynamically adjusted:</p>
    <ul>
      <li>Beating <strong>Rank 1</strong>: 100 points</li>
      <li>Beating <strong>Rank 2</strong>: 90 points</li>
      <li>Beating <strong>Rank 3-4</strong>: 85 points</li>
      <li>Beating <strong>Rank 5-8</strong>: 80 points</li>
      <li>Beating <strong>Rank 9-16</strong>: 70 points</li>
      <li><strong>A loss</strong>: 0 points (No penalty, but no gain).</li>
    </ul>

    <h3 class="text-xl font-bold mt-4 text-yellow-600">3. The Golden Match</h3>
    <p>Once every <strong>6 months</strong>, you are granted a Golden Match. Activating the yellow "Golden Match" button allows you to challenge <em>anyone</em> above you on the leaderboard.</p>
    <p>If you win a Golden Match, you over-leap in the leaderboard: <strong>Your points become the number of points your opponent has + 1.</strong></p>

    <h3 class="text-xl font-bold mt-4">4. Match Validation</h3>
    <p>After a match is played, the winner clicks "Enter Result" on the leaderboard. This sends a notification to the opponent's <strong>Profile</strong> section, where they must confirm the loss before points are officially awarded.</p>
  </div>
</template>
