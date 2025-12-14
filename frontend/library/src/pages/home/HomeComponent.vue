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
    
    <GenreListComponent />

    <h2 class="text-center mb-4" id="homeHeader">
      Featured Books
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
            <h5 class="card-title"><a :href="`/books/${book.id}`">{{ book.title }}</a></h5>
            <p class="card-text author">{{ book.author_name }}</p>
            <p class="card-text description">
              {{ book.summary.split(' ').slice(0, 15).join(' ') }}{{ book.summary.split(' ').length > 15 ? '...' : '' }}
            </p>
            <a href="#" class="btn btn-primary mt-auto" style="background-color: var(--accent-color); border: none;">
              View Details
            </a>
          </div>

        </div>
      </div>

    </div>

  </main>
  <!-- Footer -->
  <footer-component />
</template>

<script>
import FooterComponent from '../../components/common/FooterComponent.vue';
import NavComponent from '../../components/common/NavComponent.vue';
import LoaderComponent from '../../components/common/LoaderComponent.vue';
import { backendUrl } from '@/config';
import GenreListComponent from './components/GenreListComponent.vue';

export default {
  name: 'HomeComponent',
  props: {
    msg: String
  },
  data() {
    return {
      books: [],
      error: '',
      success: '',
      loading: true
    }

  },
  components: {
    NavComponent,
    FooterComponent,
    LoaderComponent,
    GenreListComponent
  },
  methods: {
    async getBooks() {
      const url = backendUrl + 'catalog/books/';
      await new Promise(resolve => setTimeout(resolve, 1000));
      try {
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'token ' + localStorage.getItem('auth_token')
          },
        })
        if (response.ok) {
          const data = await response.json(); // <-- fix here
          this.books = data;

        } else {
          const data = await response.json()
          this.error = data['non_field_errors']
        }
      } catch (err) {
        this.error = 'Network error. Please try again.'
      } finally {
        this.loading = false
      }

    }
  },
  mounted() {
    // Lifecycle hook: runs when component is mounted
    // Get the books from backend to display
    this.getBooks()
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