<template>
  <form @submit.prevent="login">
    <div v-if="error" class="text-danger mt-1">
      <div>{{ error }}</div>
    </div>
    <div class="mb-3">
      <label for="username" class="form-label">Username</label>
      <input type="text" v-model="form.username" class="form-control" id="username" required>
    </div>

    <div class="mb-3">
      <label for="password" class="form-label">Password</label>
      <input type="password" v-model="form.password" class="form-control" id="password" required>
    </div>
    <button type="submit" class="btn btn-primary w-100">Login</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { backendUrl } from '../../config'

const form = ref({
  username:'',
  password: ''
})
const router = useRouter()
const error = ref('')

const login = async ()=> {
      try {
        const url = backendUrl + 'auth/login/'
        const response = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(form.value)
        })
        if (response.ok) {
          const data =await response.json();
          const token = data.token
          localStorage.setItem('auth_token', token)
          router.push({ name: 'Home' })
        } else {
          const data = await response.json()
          error.value = data['non_field_errors']
        }
      } catch (err) {
        error.value = 'Network error. Please try again.'
      }
    }

</script>

<style>

</style>