<template>
  <form @submit.prevent="register">
                <div class="mb-3">
                  <label for="username" class="form-label">Username</label>
                  <input type="text" v-model="form.username" class="form-control" id="username" required>
                  <div v-if="errors.username" class="text-danger mt-1">
                    <div v-for="err in errors.username" :key="err">{{ err }}</div>
                  </div>
                </div>
                <div class="mb-3">
                  <label for="email" class="form-label">Email</label>
                  <input type="email" v-model="form.email" class="form-control" id="email">
                  <div v-if="errors.email" class="text-danger mt-1">
                    <div v-for="err in errors.email" :key="err">{{ err }}</div>
                  </div>
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input type="password" v-model="form.password" class="form-control" id="password" required>
                  <div v-if="errors.password" class="text-danger mt-1">
                    <div v-for="err in errors.password" :key="err">{{ err }}</div>
                  </div>
                </div>
                <button type="submit" class="btn btn-primary w-100">Register</button>
              </form>
</template>
<script>

export default {
  name: 'RegisterComponent',
  components: {

  },
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: ''
      },
      errors: {}, // Change from error: '' to errors: {}
      success: ''
    }
  },
  methods: {
    async register() {
      this.error = ''
      this.success = ''
      try {
        const response = await fetch('http://127.0.0.1:8000/auth/register/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.form)
        })
        if (response.ok) {
          this.success = 'Registration successful!'
          this.errors = {}
        } else {
          const data = await response.json()
          this.errors = data
        }
      } catch (err) {
        this.error = 'Network error. Please try again.'
      } 
    }
  }
}
</script>
