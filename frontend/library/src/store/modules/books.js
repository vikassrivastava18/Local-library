import axios from "axios";
import { backendUrl } from '@/config';

export default {
    namespaced: true,

    state: () => ({
        booksByGenre: {},     // { fiction: [...], history: [...] }
        activeGenre: null,
        loading: false,
        error: null,
    }),

    getters: {
        books(state) {
            return state.booksByGenre[state.activeGenre] || [];
        },
        activeGenre(state) {
            return state.activeGenre;
        },
        isLoading(state) {
            return state.loading;
        }
    },

    mutations: {
        SET_ACTIVE_GENRE(state, genre) {
            state.activeGenre = genre;
        },
        SET_BOOKS(state, { genre, books }) {
            state.booksByGenre[genre] = books;
        },
        SET_LOADING(state, value) {
            state.loading = value;
        },
        SET_ERROR(state, error) {
            state.error = error;
        }
    },

    actions: {
        async fetchBooksByGenre({ state, commit }, genre) {
            // ✅ If already loaded, just switch active genre
            if (state.activeGenre === genre && state.booksByGenre[genre]) {
                return;
            }
            commit("SET_LOADING", true);
            commit("SET_ACTIVE_GENRE", genre);

            try {
                const token = localStorage.getItem('auth_token');
                const headers = token ? { Authorization: `token ${token}` } : {};
                const response = await axios.get(`${backendUrl}catalog/books-list/${genre}/`, { headers });
                commit("SET_BOOKS", { genre, books: response.data });
            } catch (error) {
                commit("SET_ERROR", error);
            } finally {
                commit("SET_LOADING", false);
            }
        }
    }
}
