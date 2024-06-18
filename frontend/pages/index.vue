<template>
  <div class="main">
    <AnimeInput @recommendations="updateRecommendations" />
    <Recommendations :recommendedAnime="recommendations" />
  </div>
</template>

<script setup>
const recommendations = ref([]);

function updateRecommendations(newRecommendations) {
  recommendations.value = newRecommendations;
}
</script>

<style>
body {
  background-color: #fff0e5;
  height: 100vh;
}
</style>
