<template>
  <div>
    <!-- Success message -->
    <div v-if="successMessage" class="alert alert-success" role="alert">
      {{ successMessage }}
    </div>

    <!-- Error messages -->
    <div v-if="errors.length > 0" class="alert alert-danger" role="alert">
      <ul class="mb-0">
        <li v-for="error in errors" :key="error">{{ error }}</li>
      </ul>
    </div>

    <form id="movieForm" @submit.prevent="saveMovie" enctype="multipart/form-data">
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input type="text" name="title" id="title" class="form-control" placeholder="Enter movie title" />
      </div>

      <div class="form-group mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea name="description" id="description" class="form-control" rows="4" placeholder="Enter movie description"></textarea>
      </div>

      <div class="form-group mb-3">
        <label for="poster" class="form-label">Photo Upload</label>
        <input type="file" name="poster" id="poster" class="form-control" accept="image/*" />
      </div>

      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let csrf_token = ref("");
let successMessage = ref("");
let errors = ref([]);

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
    })
    .catch((error) => {
      console.log(error);
    });
}

onMounted(() => {
  getCsrfToken();
});

function saveMovie() {
  successMessage.value = "";
  errors.value = [];

  console.log("CSRF token is:", csrf_token.value); // <-- add this

  let movieForm = document.getElementById('movieForm');
  let form_data = new FormData(movieForm);

  fetch("/api/v1/movies", {
    method: 'POST',
    body: form_data,
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (data.errors) {
        errors.value = data.errors;
      } else {
        successMessage.value = data.message || "Movie Successfully added!";
        // Reset the form
        movieForm.reset();
        // Refresh CSRF token for next submission
        getCsrfToken();
      }
    })
    .catch(function (error) {
      console.log(error);
      errors.value = ["An unexpected error occurred. Please try again."];
    });
}
</script>

<style scoped>
/* Component specific styles */
</style>