<template>
  <!-- Navbar -->
  <nav-component />
  <!-- Main Content -->
  <main class="container my-2">
    <!-- Quote Section -->
    <section class="mb-3 text-center px-3">
      <blockquote class="fs-4 fst-italic text-secondary mx-auto">
        “I will learn whatever is great, wherever I find it.”
        <footer class="blockquote-footer mt-0">Swami Vivekananda</footer>
      </blockquote>
    </section>

    <!-- <GenreListComponent /> -->
    <section class="genres text-center">
      <button type="button" class="btn btn-primary px-4 py-2 rounded-pill m-2" @click="fetchBooksByGenre('Science')">
        Science
      </button>

      <button type="button" class="btn btn-success px-4 py-2 rounded-pill m-2" @click="fetchBooksByGenre('History')">
        History
      </button>

      <button type="button" class="btn btn-warning px-4 py-2 rounded-pill m-2" @click="fetchBooksByGenre('Philosophy')">
        Philosophy
      </button>

      <button type="button" class="btn btn-info px-4 py-2 rounded-pill m-2" @click="fetchBooksByGenre('Biography')">
        Biography
      </button>

      <button type="button" class="btn btn-danger px-4 py-2 rounded-pill m-2" @click="fetchBooksByGenre('Fiction')">
        Fiction
      </button>
    </section>


    <h2 class="text-center mb-4" id="homeHeader">
      {{activeGenre}} Books
    </h2>
    <div class="row g-3 justify-content-center">

      <!-- Book 1 -->
      <div v-if="loading">
        <LoaderComponent />
      </div>

      <div v-else v-for="book of books" :key="book.id" class="col-sm-6 col-md-4 col-lg-3">
        <div class="book-card h-100" style="max-height: 400px;">

          <img v-if="book.cover" :src="book.cover" alt="Book cover" class="img-fluid" />
          <img v-else :src="book.cover_url" alt="Book cover" class="img-fluid" />
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">
              <router-link :to="`/books/${book.id}`">{{ book.title }}</router-link>
            </h5>
            <p class="card-text author">{{ book.author_name }}</p>
            <p class="card-text description">
              {{ shortSummary(book.summary) }}
            </p>
            
          </div>

        </div>
      </div>

    </div>

  </main>
  <!-- Footer -->
  <footer-component />
</template>

<script>
import { mapGetters, mapActions } from "vuex";

import FooterComponent from '../../components/common/FooterComponent.vue';
import NavComponent from '../../components/common/NavComponent.vue';
import LoaderComponent from '../../components/common/LoaderComponent.vue';
// import GenreListComponent from './components/GenreListComponent.vue';

export default {
  name: 'HomeComponent',
  computed: {
    ...mapGetters("books", ["books", "isLoading", "activeGenre"]),
    loading() {
      return this.isLoading;
    }
  },
  data() {
    return {
      genres: ["fiction", "history", "science", "biography"],
      error: '',
    }

  },
  components: {
    NavComponent,
    FooterComponent,
    LoaderComponent,
    // GenreListComponent
  },
  methods: {

    ...mapActions("books", ["fetchBooksByGenre"]),
    loadBooks(genre) {
      this.fetchBooksByGenre(genre);
    },
    shortSummary(text, words = 15) {
      if (!text) return "";
      const parts = text.split(" ");
      return parts.length > words
        ? parts.slice(0, words).join(" ") + "..."
        : text;
    }
  },
  created() {
    if (!this.$store.state.books.activeGenre) {
      console.log("Bug")
      this.fetchBooksByGenre("Feature");
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* Color palette */
:root {
  --primary-color: #2c3e50;
  --accent-color: #18bc9c;
  --light-gray: #f7f9fa;
  --text-color: #34495e;
}

body {
  background-color: var(--light-gray);
  color: var(--text-color);
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.homeHeader {
  color: var(--primary-color);
  font-weight: 700;
}

/* Navbar */
.navbar {
  background-color: var(--primary-color);
}

.navbar-brand,
.nav-link,
.form-control,
.btn-outline-light {
  color: #000 !important;
}

.nav-link:hover,
.navbar-brand:hover {
  color: var(--accent-color) !important;
}

.form-control {
  background-color: #34495e;
  border: none;
  color: #ecf0f1;
  transition: background-color 0.3s ease;
}

.form-control::placeholder {
  color: #bdc3c7;
}

.form-control:focus {
  background-color: #2c3e50;
  color: #ecf0f1;
  box-shadow: none;
  border: 1px solid var(--accent-color);
}

.btn-outline-light {
  border-color: #ecf0f1;
  transition: all 0.3s ease;
}

.btn-outline-light:hover {
  background-color: var(--accent-color);
  border-color: var(--accent-color);
  color: #fff !important;
}

/* Book cards */
.book-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgb(0 0 0 / 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.book-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgb(0 0 0 / 0.15);
}

.book-card img {
  height: 200px;
  object-fit: cover;
  border-bottom: 1px solid #eee;
}

.card-body {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1.25rem;
}

.card-title {
  font-weight: 700;
  color: var(--primary-color);
}

.card-text.author {
  font-style: italic;
  color: var(--accent-color);
  margin-bottom: 0.5rem;
}

.card-text.description {
  flex-grow: 1;
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 1rem;
}

blockquote {
  max-width: 700px;
  border-left: 4px solid var(--accent-color);
  padding-left: 1rem;
}


/* Responsive adjustments */
@media (max-width: 576px) {
  .book-card img {
    height: 180px;
  }
}
</style>