<template>
  <div class="container">
    <h2>Enter Anime Names</h2>
    <form @submit.prevent="getRecommendations">
      <div class="input-group">
        <input
          type="text"
          id="animeInput"
          v-model="animeInput"
          @input="fetchSuggestions"
          @keydown.enter.prevent="addAnime"
        />
        <ul v-if="showSuggestions" class="suggestions-list">
          <li
            v-for="suggestion in suggestions"
            :key="suggestion"
            @click="selectSuggestion(suggestion)"
          >
            {{ suggestion }}
          </li>
        </ul>
        <div class="pills">
          <div
            v-for="(anime, index) in animeList"
            :key="index"
            class="pill"
          >
            {{ anime }}
            <button type="button" @click="removeAnime(index)">x</button>
          </div>
        </div>
      </div>
      <button type="submit" @click="closeSuggestions">
        Get Recommendations
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Papa from "papaparse";

let animeDataset = [];
const emit = defineEmits();
const animeInput = ref("");
const animeList = ref([]);
const suggestions = ref([]);
const showSuggestions = ref(false);

onMounted(async () => {
  await loadCSV();
});

const loadCSV = async () => {
  const response = await fetch("/anime_list.csv"); // Adjust the path as needed
  const csvData = await response.text();
  Papa.parse(csvData, {
    header: true,
    dynamicTyping: true,
    skipEmptyLines: true,
    complete: function (results) {
      animeDataset = results.data
        .map((row) => row.engName)
        .filter((name) => typeof name === "string" && name.trim() !== "");
    },
    error: function (error, file) {
      console.error("Parsing error:", error, file);
    },
  });
}

const fetchSuggestions = async () => {
  const input = animeInput.value.toLowerCase();
  suggestions.value = animeDataset
    .filter((anime) => anime.toLowerCase().includes(input))
    .sort((a, b) => {
      // Prioritize exact matches
      if (a.toLowerCase() === input) return -1;
      if (b.toLowerCase() === input) return 1;

      // Prioritize shorter titles
      if (a.length !== b.length) return a.length - b.length;

      // Finally, sort by similarity to the user's input
      return a.toLowerCase().indexOf(input) - b.toLowerCase().indexOf(input);
    })
    .slice(0, 30);

  showSuggestions.value = suggestions.value.length > 0;
}

const addAnime = () => {
  if (animeInput.value && !animeList.value.includes(animeInput.value)) {
    animeList.value.push(animeInput.value);
    animeInput.value = "";
    showSuggestions.value = false;
  }
}

const selectSuggestion = (suggestion) => {
  animeInput.value = suggestion;
  addAnime();
}

const removeAnime = (index) => {
  animeList.value.splice(index, 1);
}

const closeSuggestions = () => {
  setTimeout(() => {
    showSuggestions.value = false;
  }, 200);
}

const getRecommendations = async () => {
  const response = await fetch("https://127.0.0.1:3000/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_history: animeList.value }),
  });

  const data = await response.json();
  // Emitting event to parent component
  emit("recommendations", data);
}
</script>
<style scoped lang="scss">
.container {
  font-family: "Arial", sans-serif;
  max-width: 600px;
  margin: 50px auto;
  padding: 0 20px 20px;
  border: 1px solid rgb(99, 98, 98);
  border-radius: 8px;
  background-color: white;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-sizing: border-box;

  form {
    display: flex;
    flex-direction: column;
  }

  &:hover {
    box-shadow: -4px 4px 0 rgb(16,22,47);
    transform: translateY(-2px) translateX(2px);
  }

  h2 {
    color: #2c3e50;
    margin-bottom: 20px;
    text-align: center;
  }

  .input-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 15px;

    label {
      margin-bottom: 10px;
      font-size: 1.1rem;
      color: #34495e;
    }

    input {
      padding: 10px;
      border: 1px solid #bdc3c7;
      border-radius: 4px;
      font-size: 1rem;
      transition: border-color 0.3s ease;

      &:focus {
        border-color: #2980b9;
        outline: none;
      }
    }
  }

  .pills {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 10px;

    .pill {
      display: flex;
      align-items: center;
      padding: 5px 15px;
      background-color: #3498db;
      color: #fff;
      border-radius: 20px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
      transition: background-color 0.3s ease, box-shadow 0.3s ease;

      &:hover {
        background-color: #2980b9;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
      }

      button {
        margin-left: 10px;
        background: none;
        border: none;
        color: white;
        font-weight: bold;
        cursor: pointer;
        font-size: 1rem;
        padding: 0;
        transition: color 0.3s ease;

        &:hover {
          color: #e74c3c;
        }
      }
    }
  }

  button {
    cursor: pointer;
    background-color: #3498db;
    color: #fff;
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    font-size: 1.1rem;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: #2980b9;
    }

    &:active {
      background-color: #2471a3;
    }

    &:focus {
      outline: none;
    }
  }

  .suggestions-list {
    max-height: 200px;
    overflow-y: auto;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    margin-top: 5px;
    box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.1);
    background: #fff;
    padding: 0;

    li {
      padding: 10px;
      cursor: pointer;
      transition: background-color 0.2s ease;
      list-style-type: none;

      &:hover {
        background-color: #f5f5f5;
      }

      &:active {
        background-color: #e0e0e0;
      }
    }
  }
}
</style>