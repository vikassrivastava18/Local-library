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
                <div class="row g-0">                    
                    <div>
                        <div class="card-header">
                            <h4 style="display: inline;">{{ user }}</h4>
                        </div>
                        <div class="card-body">
                            <div v-for="copy in books" :key="copy.id" class="mb-3 p-4">
                                <img v-if="copy.cover" :src="copy.cover" alt="book cover" class="img-fluid">
                                <img v-else src="../../assets/book.jpg" alt="book cover" class="img-fluid">
                                <p>
                                    Book: {{ copy.book_name }}
                                </p>
                                <p>
                                    <strong>Due to be returned:</strong> {{ copy.due_back }}
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

    </main>
    <!-- Footer -->
    <footer-component />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import FooterComponent from '../../components/common/FooterComponent.vue';
import NavComponent from '../../components/common/NavComponent.vue';
import LoaderComponent from '../../components/common/LoaderComponent.vue';
import { backendUrl } from '@/config';


const user = ref('');
const books = ref([]);
const loading = ref(true);
const booksAvailable = ref(0);
const success = ref('');
const error = ref('');

const getProfileDetails = async () => {
    const url = `${backendUrl}catalog/user-book-list`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'token ' + localStorage.getItem('auth_token')
            },
        });

        if (response.ok) {
            const data = await response.json();
            books.value = data.books;
            user.value = data.user;
            booksAvailable.value = data.books?.length || 0;
            console.log('books: ', data);
        } else {
            const data = await response.json();
            error.value = data['non_field_errors'];
        }
    } catch (err) {
        error.value = `Error occured: ${err}`;
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    getProfileDetails();
});
</script>