<template>
    <!-- Navbar -->
    <nav-component />
    <!-- Main Content -->
    <main>
        <div v-if="loading">
            <LoaderComponent />
        </div>
        <div class="container mt-5">
            <h4 class="text-success">{{ success }}</h4>
            <div class="card shadow">
                <div v-if="book" class="row g-0">
                    <div class="col-md-4 d-flex align-items-center justify-content-center">
                        <img :src="book.cover" class="img-fluid rounded-start" alt="Book Cover"
                            style="max-height: 300px; object-fit: contain;">
                    </div>
                    <div class="col-md-8">
                        <div class="card-header bg-primary text-white">
                            <h4>{{ book.title }}</h4>
                        </div>
                        <div class="card-body">
                            <h5 class="card-title">Author: {{ book.author_name }}</h5>
                            <p class="card-text"><strong>Summary:</strong> {{ book.summary }}</p>
                            <p class="card-text"><strong>ISBN:</strong> {{ book.isbn }}</p>
                            
                            <div v-for="copy in book.instances" :key="copy.id" class="mb-3 p-4">
                                <p :class="{
                                        'text-success': copy.status === 'a',
                                        'text-danger': copy.status === 'm',
                                        'text-warning': copy.status !== 'a' && copy.status !== 'm'
                                    }">
                                    {{ copy.status_display }}
                                </p>
                                <p v-if="copy.status !== 'a'">
                                    <strong>Due to be returned:</strong> {{ copy.due_back }}
                                </p>
                                <p>
                                    <strong>Imprint:</strong> {{ copy.imprint }}
                                </p>
                                <p class="text-muted">
                                    <strong>Id:</strong> {{ copy.id }}
                                </p>
                            </div>
                        </div>
                        <div v-if="booksAvailable > 0" 
                            class="card-footer text-end">
                            <button class="btn btn-success" 
                                @click="borrowBook"
                            >Borrow</button>
                        </div>
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
import LoaderComponent from '../home/LoaderComponent.vue';
import { backendUrl } from '@/config';

export default {
    name: 'BookComponent',
    data() {
        return {
            book: null,
            loading: true,
            booksAvailable: 0,
            success: ''
        }
    },
    components: {
        NavComponent,
        FooterComponent,
        LoaderComponent
    },
    methods: {
        async getBookDetails() {
            console.log(this.$route.params.id);
            const id = this.$route.params.id
            const url = `${backendUrl}catalog/books/${id}`;
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
                    this.book = data;
                    this.booksAvailable = this.book.instances.filter(inst => inst.status ==='a').length

                } else {
                    const data = await response.json()
                    this.error = data['non_field_errors']
                }
            } catch (err) {
                this.error = 'Network error. Please try again.'
            } finally {
                this.loading = false
            }
        },

        async borrowBook() {
            // Implement borrow logic here
            const id = this.book.instances.filter(inst => inst.status ==='a').map(inst => inst.id)[0]
            const url = `${backendUrl}catalog/borrow-book/${id}`;
            try {
                const response = await fetch(url, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'token ' + localStorage.getItem('auth_token')
                    },
                })
                if (response.ok) {
                    console.log('Sucessfully loaned');
                    this.success = 'Book has been assigned to you on loan!';
                    await new Promise(resolve => setTimeout(resolve, 2000));
                    this.$router.go(0);
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
        this.getBookDetails()
        
    }
}
</script>