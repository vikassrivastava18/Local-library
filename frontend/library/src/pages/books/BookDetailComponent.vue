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
                        <img v-if="book.cover" :src="book.cover" class="img-fluid rounded-start" alt="Book Cover"
                            style="max-height: 300px; object-fit: contain;">
                        <img v-else :src="book.cover_url" class="img-fluid rounded-start" alt="Book Cover"
                            style="max-height: 300px; object-fit: contain;">

                    </div>
                    <div class="col-md-9">
                        <div class="card-header">
                            <h4 style="display: inline;">{{ book.title }}</h4>

                            <button v-if="booksAvailable > 0" 
                                type="button"
                                class="btn btn-primary" data-bs-toggle="modal" 
                                data-bs-target="#exampleModal"
                                style="float: right;">Borrow
                            </button>

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
                                <p v-if="copy.status == 'o'">
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
                        You agree to return this book by {{due_date}} in good shape.
                    </div>

                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Close
                        </button>
                        <button type="button" 
                            class="btn btn-primary"
                            @click="borrowBook">
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

<script>
import FooterComponent from '../../components/common/FooterComponent.vue';
import NavComponent from '../../components/common/NavComponent.vue';
import LoaderComponent from '../../components/common/LoaderComponent.vue';
import { backendUrl } from '@/config';

export default {
    name: 'BookComponent',
    data() {
        return {
            book: null,
            loading: true,
            booksAvailable: 0,
            success: '',
            error: '',
            due_date: new Date(new Date().setMonth(new Date().getMonth() + 2)).toISOString().split('T')[0],
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
            await new Promise(resolve => setTimeout(resolve, 500));
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
                    console.log("book: ", data);
                    
                    this.booksAvailable = this.book.instances.filter(inst => inst.status === 'a').length

                } else {
                    const data = await response.json()
                    this.error = data['non_field_errors']
                }
            } catch (err) {
                this.error = `Error occured: ${err}`
            } finally {
                this.loading = false
            }
        },

        async borrowBook() {
            // Implement borrow logic here
            const id = this.book.instances.filter(inst => inst.status === 'a').map(inst => inst.id)[0]
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
                    this.success = 'Book has been assigned to you on loan, please collect from library by tomorrow!';

                } else {
                    const data = await response.json()
                    this.error = data['error']
                }
            } catch (err) {
                this.error = 'Network error. Please try again.'
            } finally {
                this.loading = false
                // Close the modal
                document.querySelector(".btn-close").click()
            }
        }
    },
    mounted() {
        this.getBookDetails()

    }
}
</script>