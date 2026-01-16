import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import store from './store';
// Import Bootstrap CSS
import "bootstrap/dist/css/bootstrap.min.css";
// Import Bootstrap JS (for modal, dropdown, tooltip, etc.)
import "bootstrap/dist/js/bootstrap.bundle.min.js";


let app = createApp(App)
  .use(router)
  .use(store)

app.config.globalProperties.$axios = axios
app.mount('#app')
  
// Redirect to login page in case of authentication error
axios.interceptors.response.use(
  response => response,
  error => {
    console.log("Coming..");
    
    // Add more error handling here
    if (error.response && [401, 403].includes(error.response.status)) {
      console.log("Login failed.");
      
      window.location.href = '/auth'; // Redirect to login
    }
    return Promise.reject(error);
  }
);
