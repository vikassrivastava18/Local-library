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
<script>

export default {
  name: 'LoginComponent',
  components: {

  },
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      error: '',
      success: ''
    }
  },
  methods: {
    async login() {
      this.error = ''
      this.success = ''
      try {
        const response = await fetch('http://127.0.0.1:8000/auth/login/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.form)
        })
        if (response.ok) {
          const data =await response.json();
          const token = data.token
          localStorage.setItem('auth_token', token)
          this.$router.push({ name: 'Home' })
        } else {
          const data = await response.json()
          this.error = data['non_field_errors']
        }
      } catch (err) {
        this.error = 'Network error. Please try again.'
      }
    }
  }
}
</script>
