<template>
  <nav class="navbar navbar-expand-lg shadow" style="padding: 4px; background-color: rgb(93 186 215);;">
    <div class="container">
      <a class="navbar-brand fs-4 ms-0" href="/" style="color: black;">Local Library</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent"
        aria-controls="navbarContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarContent">
        <form class="d-flex ms-auto me-4" role="search">
          <input class="form-control me-2" type="search" placeholder="Search books..." aria-label="Search"
            @keyup="search" v-model="searchBook" />
          <button class="btn btn-outline-light" type="submit">Search</button>
          <!-- Suggestions dropdown -->
          <ul v-if="bookList.length && searchBook.length >= 4" class="list-group position-absolute"
            style="z-index: 1000; width: 300px; top: 45px;">
            <li v-for="book in bookList" :key="book.id" class="list-group-item list-group-item-action"
              @click="selectBook(book)" style="cursor: pointer;">
              {{ book.title }}
            </li>
          </ul>
        </form>
        <ul class="navbar-nav mb-2 mb-lg-0">
          <li class="nav-item">
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
      searchBook: '',
      bookList: []
    }
  },
  methods: {
    async handleLogout() {
      this.error = ''
      this.success = ''
      try {
        const response = await fetch('http://127.0.0.1:8000/auth/logout/', {
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
    async search() {
      if (this.searchBook.length >= 4) {
        // Filter the books from backend that match the search
        // search-book/
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
            const data = await response.json(); // <-- fix here
            this.bookList = data.books;
            console.log(this.bookList);

          } else {
            const data = await response.json()
            this.error = data['non_field_errors']
          }
        } catch (err) {
          this.error = 'Network error. Please try again.'
        }

      }
    },
    selectBook(book) {
      this.searchBook = book.title
      this.bookList = []
      // Optionally, navigate to the book detail page:
      this.$router.push({ name: 'BookDetail', params: { id: book.id } })
    }
  }
}
</script>