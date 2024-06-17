<template>
  <div class="recommendation-container" v-if="sortedAnime.length > 0">
    <h2>Recommended Anime</h2>
    <div class="anime-list">
      <div
        v-for="anime in sortedAnime"
        :key="anime.engName || anime.jpName"
        class="anime-card"
      >
        <h3 class="anime-title">
          <a :href="anime.url">{{ anime?.name ? anime.name : "Name not available" }}</a>
        </h3>
        <div class="match" :class="{ 'bad-match': anime.similarity_percentage < 60, 'good-match': anime.similarity_percentage >= 60 }">
          {{ anime.similarity_percentage < 60 ? 'Bad match' : 'Good match' }}
        </div>
        <div class="similarity-score-container">
          <progress class="similarity-meter" :value="anime.similarity_percentage" max="100"></progress>
          <div class="percentage-label">{{ anime.similarity_percentage.toFixed(2) }}% similar to your input</div>
        </div>
        <p><strong>Score:</strong> {{ anime.score }}</p>
        <div v-if="anime.genres" class="tags">
          <span class="tag" v-for="genre in anime.genres" :key="genre">{{ genre }}</span>
        </div>
        <p v-if="anime.aired"><strong>Aired:</strong> {{ anime.aired }}</p>
        <p v-if="anime.producer"><strong>Producer:</strong> {{ anime.producer }}</p>
        <p v-if="anime.studios"><strong>Studios:</strong> {{ anime.studios.join(", ") }}</p>
        <div class="tags">
          <p><strong>Rank:</strong> <span v-for="rank in anime.allRank[0]" :key="rank">{{ rank }}</span></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps(["recommendedAnime"]);

const sortedAnime = computed(() => {
  return props.recommendedAnime.sort((a, b) => {
    return b.similarity_percentage - a.similarity_percentage;
  });
});
</script>

<style scoped lang="scss">
.recommendation-container {
  font-family: "Arial", sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;

  h2 {
    text-align: center;
    color: #34495e;
    margin-bottom: 20px;
    font-size: 2rem;
    font-weight: bold;
  }

  .anime-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
  }

  .anime-card {
    background: #ffffff;
    border: 1px solid #6d6d6d;
    border-radius: 5px;
    padding: 20px;
    margin: 10px;
    width: 100%; 
    // box-shadow: 0 3px 7px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-sizing: border-box;

    &:hover {
      transform: translateY(-4px) translateX(4px);
      box-shadow: -8px 8px 0 rgb(16,22,47);
    }

    .anime-title {
      margin-top: 0;
      margin-bottom: 15px;

      a {
        text-decoration: none;
        color: #2980b9;
        font-size: 1.5rem;
        transition: color 0.3s ease;

        &:hover {
          color: #1a5276;
        }
      }
    }

    .match {
      margin-bottom: 15px;
      font-weight: bold;
      font-size: 1.1rem;

      &.bad-match {
        color: #e74c3c;
      }

      &.good-match {
        color: #27ae60;
      }
    }

    p {
      margin-bottom: 10px;
      color: #34495e;
    }

    strong {
      color: #2c3e50;
    }

    .tags {
      display: flex;
      flex-wrap: wrap;
      margin: 8px 0;

      .tag {
        background-color: #e1e1e1;
        color: #333;
        padding: 5px 10px;
        border-radius: 20px;
        margin: 5px;
        font-size: 0.9rem;
        transition: background-color 0.3s ease;

        &:hover {
          background-color: #d1d1d1;
        }
      }
    }
  }

  .similarity-score-container {
    position: relative;
    width: 100%;
    color: #333;
  }

  .similarity-meter {
    width: 100%;
    height: 25px;
    border: none;
    border-radius: 4px;
    background-color: #d1d1d1;
    display: flex;
    justify-content: flex-start;
    align-items: center;

    &::-moz-progress-bar {
      background-color: #3498db;
    }

    &::-webkit-progress-bar {
      background-color: #e1e1e1;
    }

    &::-webkit-progress-value {
      background-color: #3498db;
    }
  }

  .percentage-label {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    left: 10px;
    text-align: left;
    line-height: 25px;
  }

  @media (min-width: 768px) {
    .anime-card {
      margin: 15px;
    }
  }

  @media (min-width: 1024px) {
    .anime-card {
      width: calc(50% - 20px);
      margin: 10px;
    }
  }

  @media (min-width: 1200px) {
    .anime-card {
      width: calc(33.33% - 20px);
      margin: 10px;
    }
  }
}
</style>
