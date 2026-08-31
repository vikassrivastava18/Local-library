<template>
  <!-- Navbar -->
  <nav-component />

  <!-- Main Content -->
  <main>
    <div v-if="loading">
      <LoaderComponent />
    </div>

    <div class="container mt-5">
      <h5 class="text-success">{{ success }}</h5>
      <h5 class="text-danger">{{ error }}</h5>

      <div class="card shadow">
        <div v-if="book" class="row g-0">
          <div class="col-md-3 d-flex p-2">
            <img
              v-if="book.cover"
              :src="book.cover"
              class="book-cover"
              alt="Book Cover"
            />
            <img
              v-else-if="book.cover_url"
              :src="book.cover_url"
              class="book-cover"
              alt="Book Cover"
            />
            <img
              v-else
              src="../../assets/book.jpg"
              class="book-cover"
              alt="Book Cover"
            />
          </div>

          <div class="col-md-9">
            <div class="card-header">
              <h4 class="book-title">{{ book.title }}</h4>

              <button
                v-if="booksAvailable > 0"
                type="button"
                class="btn btn-primary borrow-btn"
                data-bs-toggle="modal"
                data-bs-target="#exampleModal"
              >
                Borrow
              </button>

              <span v-else class="text-primary unavailable-text">
                Sorry, the book is not available currently.
              </span>
            </div>

            <div class="card-body">
              <h5 class="card-title">Author: {{ book.author_name }}</h5>
              <p class="card-text"><strong>Summary:</strong> {{ book.summary }}</p>
              <p class="card-text"><strong>ISBN:</strong> {{ book.isbn }}</p>

              <h5 class="mt-4">Book Instances</h5>

              <div v-for="(copy, index) in book.instances" :key="copy.id" class="mb-2 p-2">
                <p
                  :class="{
                    'text-success': copy.status === 'a',
                    'text-danger': copy.status === 'm',
                    'text-warning': copy.status !== 'a' && copy.status !== 'm'
                  }"
                >
                  <b>{{ index + 1 }})</b> &nbsp;{{ copy.status_display }}
                </p>

                <p v-if="copy.status == 'o'">
                  <strong>Due to be returned:</strong> {{ copy.due_back }}
                </p>

                <p v-if="copy.imprint">
                  <strong>Imprint:</strong> {{ copy.imprint }}
                </p>

                <p class="text-muted">
                  <strong>Id:</strong> {{ copy.id }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4 shadow">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Borrow Agreement</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>

          <div class="modal-body">
            You agree to return this book by {{ due_date }} in good shape.
          </div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Close
            </button>
            <button type="button" class="btn btn-primary" @click="borrowBook">
              Agree
            </button>
          </div>
        </div>
      </div>
    </div>
  </main>

  <!-- Footer -->
  <footer-component />
</template>

<style scoped>
.book-cover {
  display: block;
  max-height: 300px;
  margin: 1rem auto 0;
  object-fit: contain;
}

.book-title {
  display: inline;
}

.borrow-btn {
  float: right;
  line-height: initial;
}

.unavailable-text {
  float: right;
  font-weight: 500;
}
</style>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import FooterComponent from '../../components/common/FooterComponent.vue';
import NavComponent from '../../components/common/NavComponent.vue';
import LoaderComponent from '../../components/common/LoaderComponent.vue';
import { backendUrl, apiRequest } from '@/config';


const route = useRoute();
const router = useRouter();

const book = ref(null);
const loading = ref(true);
const booksAvailable = ref(0);
const success = ref('');
const error = ref('');
const due_date = ref(new Date(new Date().setMonth(new Date().getMonth() + 2)).toISOString().split('T')[0]);

watch(
    () => route.params.id,
    () => {
        router.go(0);
    }
);

const getBookDetails = async () => {
    console.log(route.params.id);
    const id = route.params.id;
    const url = `${backendUrl}catalog/books/${id}`;

    try {
        const response = await axios.get(url, {
            headers: {
                'Authorization': 'token ' + localStorage.getItem('auth_token')
            },
        });

        book.value = response.data;
        console.log('book: ', response.data);
        booksAvailable.value = book.value.instances.filter(inst => inst.status === 'a').length;
    } catch (err) {
        error.value = `Error occured: ${err}`;
    } finally {
        loading.value = false;
    }
};

const borrowBook = async () => {
    loading.value = true;
    error.value = '';

    const id = book.value?.instances
        .find(inst => inst.status === 'a')
        ?.id;

    if (!id) {
        error.value = 'No available copy of this book.';
        loading.value = false;
        return;
    }

    try {
        await apiRequest(`catalog/borrow-book/${id}`, {
            method: 'PUT',
        });

        success.value = 'Book has been assigned to you on loan, please collect from library by tomorrow!';
    } catch (err) {
        error.value = err.message || 'Network error. Please try again.';
    } finally {
        loading.value = false;
        document.querySelector('.btn-close')?.click();
    }
};

onMounted(() => {
    getBookDetails();
});
</script>