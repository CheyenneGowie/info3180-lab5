<template>
  <div class="container mt-4">
    <h2>Movies</h2>
    <div v-if="movies.length === 0" class="text-muted">
      No movies found. Add some movies!
    </div>
    <div class="row">
      <div v-for="movie in movies" :key="movie.id" class="col-md-6 mb-4">
        <div class="card h-100">
          <div class="row g-0">
            <div class="col-4">
              <img :src="movie.poster" :alt="movie.title" class="img-fluid rounded-start" style="height: 100%; object-fit: cover;" />
            </div>
            <div class="col-8">
              <div class="card-body">
                <h5 class="card-title">{{ movie.title }}</h5>
                <p class="card-text">{{ movie.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let movies = ref([]);

function fetchMovies() {
  fetch('/api/v1/movies')
    .then((response) => response.json())
    .then((data) => {
      movies.value = data.movies;
    })
    .catch((error) => {
      console.log(error);
    });
}

onMounted(() => {
  fetchMovies();
});
</script>

<style scoped>
.card {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>