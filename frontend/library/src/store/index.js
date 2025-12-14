import { createStore } from "vuex";
import books from "./modules/books";


const store = createStore({
  modules: {
    books
  }
});
export default  store
