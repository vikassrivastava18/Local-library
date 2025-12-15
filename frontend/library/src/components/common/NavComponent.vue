<template>
  <!-- Navbar -->
  <nav class="navbar-custom navbar navbar-expand-lg shadow"
    style="background-color: rgb(93, 186, 215);">
    <div class="container">
      <!-- Brand / Home link -->
      <router-link :to="`/`" class="navbar-brand fs-4 ms-0 brand">
        Local Library
      </router-link>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent"
        aria-controls="navbarContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarContent">
        <!-- Search form (positioned relative so suggestions can be absolute) -->
        <form class="d-flex ms-auto me-4 search-form" role="search" @submit.prevent>
          <input
            class="form-control me-2"
            type="search"
            placeholder="Search books..."
            aria-label="Search"
            @keyup="search"
            v-model="searchBook"
          />
          <button class="btn btn-outline-light" type="submit">Search</button>

          <!-- Suggestions dropdown -->
          <ul v-if="bookList.length && searchBook.length >= 4" class="list-group suggestions">
            <li
              v-for="book in bookList"
              :key="book.id"
              class="list-group-item list-group-item-action suggestion-item"
              @click="selectBook(book)"
            >
              {{ book.title }}
            </li>
          </ul>
        </form>

        <!-- Profile and logout -->
        <ul class="navbar-nav mb-2 ms-4 mb-lg-0">
          <li class="nav-item me-2">
            <router-link :to="`/profile`" class="nav-link">
              <img src="@/assets/profile_new.png" alt="Profile" class="profile-img" />
            </router-link>
          </li>
          <li class="nav-item ms-2">
            <a class="nav-link" href="#" @click.prevent="handleLogout">
              <button class="btn btn-danger">Logout</button>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { backendUrl } from '@/config';

export default {
  name: 'NavComponent',
  data() {
    return {
      // Current search text
      searchBook: '',
      // Suggestions returned from backend
      bookList: [],
      // ...existing code...
    }
  },
  methods: {
    // Logs the user out by calling the backend logout endpoint
    async handleLogout() {
      this.error = ''
      this.success = ''
      try {
        const response = await fetch(`${backendUrl}auth/logout/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'token ' + localStorage.getItem('auth_token')
          },
        })
        if (response.ok) {
          localStorage.removeItem('auth_token')
          this.$router.push({ name: 'AuthLogin' })
        } else {
          const data = await response.json()
          this.error = data['non_field_errors']
        }
      } catch (err) {
        this.error = 'Network error. Please try again.'
      }
    },

    // Performs search when user has typed >= 4 characters
    async search() {
      if (this.searchBook.length >= 4) {
        const url = `${backendUrl}catalog/search-book/${this.searchBook}`;
        try {
          const response = await fetch(url, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'token ' + localStorage.getItem('auth_token')
            },
          })
          if (response.ok) {
            const data = await response.json();
            this.bookList = data.books;
          } else {
            const data = await response.json()
            this.error = data['non_field_errors']
          }
        } catch (err) {
          this.error = 'Network error. Please try again.'
        }
      } else {
        // Clear suggestions if input too short
        this.bookList = []
      }
    },
    // Select a suggestion and navigate to the book detail
    selectBook(book) {
      this.searchBook = book.title
      this.bookList = []
      this.$router.push({ name: 'BookDetail', params: { id: book.id } })
    }
  }
}
</script>

<style scoped>
/* Navbar customizations moved from inline styles */
.navbar-custom {
  padding: 4px;
  background-color: rgb(93, 186, 215); /* same color as before */
}

/* Brand styling */
.brand {
  color: black;
}

/* Make the search form container relative so the suggestions dropdown can be positioned */
.search-form {
  position: relative;
}

/* Suggestions dropdown styling (was inline) */
.suggestions {
  position: absolute;
  z-index: 1000;
  width: 300px;
  top: 45px;
  left: 0;
}

/* Suggestion item pointer cursor (was inline) */
.suggestion-item {
  cursor: pointer;
}

/* Profile image sizing (was inline) */
.profile-img {
  width: 42px;
  height: 40px;
  border-radius: 50%;
}

/* Ensure list items appear above other content on small screens */
@media (max-width: 576px) {
  .suggestions {
    width: 90%;
    top: 50px;
  }
}
</style>