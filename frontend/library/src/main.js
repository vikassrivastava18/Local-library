import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store';
// Import Bootstrap CSS
import "bootstrap/dist/css/bootstrap.min.css";
// Import Bootstrap JS (for modal, dropdown, tooltip, etc.)
import "bootstrap/dist/js/bootstrap.bundle.min.js";

createApp(App)
  .use(router)
  .use(store)
  .mount('#app')
  