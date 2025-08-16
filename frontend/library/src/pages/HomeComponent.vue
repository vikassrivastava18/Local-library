<template>
  <!-- Navbar -->
  <nav-component></nav-component>
  <!-- Main Content -->
  <main class="container my-5">
    <!-- Quote Section -->
    <section class="mb-5 text-center px-3">
      <blockquote class="fs-4 fst-italic text-secondary mx-auto"
        style="max-width: 700px; border-left: 4px solid var(--accent-color); padding-left: 1rem;">
        “The more that you read, the more things you will know. The more that you learn, the more places you’ll go.”
        <footer class="blockquote-footer mt-2">Dr. Seuss</footer>
      </blockquote>
    </section>

    <h2 class="text-center mb-4" style="color: var(--primary-color); font-weight: 700;">
      Featured Books
    </h2>
    <div class="row g-3 justify-content-center">
      
      <!-- Book 1 -->
      <div class="col-sm-6 col-md-4 col-lg-3">
        <div class="book-card h-100">
          <img src="https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=400&q=80"
            alt="The Great Gatsby" />
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">The Great Gatsby</h5>
            <p class="card-text author">by F. Scott Fitzgerald</p>
            <p class="card-text description">
              A classic novel of the Roaring Twenties, filled with love,
              ambition, and tragedy.
            </p>
            <a href="#" class="btn btn-primary mt-auto" style="background-color: var(--accent-color); border: none;">
              View Details
            </a>
          </div>
        </div>
      </div>

      <!-- Book 2 -->
      <div class="col-sm-6 col-md-4 col-lg-3">
        <div class="book-card h-100">
          <img src="https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?auto=format&fit=crop&w=400&q=80"
            alt="To Kill a Mockingbird" />
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">To Kill a Mockingbird</h5>
            <p class="card-text author">by Harper Lee</p>
            <p class="card-text description">
              A timeless story of justice and morality in the Deep South.
            </p>
            <a href="#" class="btn btn-primary mt-auto" style="background-color: var(--accent-color); border: none;">
              View Details
            </a>
          </div>
        </div>
      </div>

      <!-- Book 3 -->
      <div class="col-sm-6 col-md-4 col-lg-3">
        <div class="book-card h-100">
          <img src="https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80"
            alt="1984" />
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">1984</h5>
            <p class="card-text author">by George Orwell</p>
            <p class="card-text description">
              A dystopian novel exploring surveillance, truth, and freedom.
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
  <footer-component></footer-component>
</template>

<script>
import FooterComponent from '../components/common/FooterComponent.vue';
import NavComponent from '../components/common/NavComponent.vue';

export default {
  name: 'HomeComponent',
  props: {
    msg: String
  },
  components: {
    NavComponent,
    FooterComponent
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
  height: 250px;
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

/* Footer */
footer {
  background-color: var(--primary-color);
  color: #bdc3c7;
  padding: 1rem 0;
  text-align: center;
  font-size: 0.9rem;
  margin-top: 4rem;
  user-select: none;
}

footer a {
  color: var(--accent-color);
  text-decoration: none;
  font-weight: 600;
}

footer a:hover {
  text-decoration: underline;
}

/* Responsive adjustments */
@media (max-width: 576px) {
  .book-card img {
    height: 180px;
  }
}
</style>