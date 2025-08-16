<template>
  <div id="registerBackground">
    <div class="container mb-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card shadow">
            <div class="card-header bg-primary text-white">
              <h4 class="mb-0">Login</h4>
            </div>
            <div class="card-body">
              <form @submit.prevent="login">
                <div v-if="error" class="text-danger mt-1">
                    <div >{{ error }}</div>
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

              <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
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
          this.success = 'Login successful!'
          this.$router.push({ name: 'Home' })
        } else {
          const data = await response.json()
          this.error = data
        }
      } catch (err) {
        this.error = 'Network error. Please try again.'
      } 
    }
  }
}
</script>

<style scoped>
  #registerBackground {
    background-image: url("data:image/svg+xml,%3Csvg width='800' height='600' xmlns='http://www.w3.org/2000/svg'%3E%3Cg%3E%3Crect x='60' y='120' width='120' height='260' rx='15' fill='%23f8ecd4' stroke='%235a3d2b' stroke-width='6'/%3E%3Crect x='210' y='140' width='100' height='240' rx='12' fill='%23e3e6e8' stroke='%234d5c6b' stroke-width='6'/%3E%3Crect x='340' y='110' width='140' height='270' rx='14' fill='%23d1e7dd' stroke='%233c6e47' stroke-width='6'/%3E%3Crect x='510' y='130' width='110' height='220' rx='10' fill='%23c9b7a7' stroke='%235a3d2b' stroke-width='6'/%3E%3Crect x='120' y='420' width='500' height='40' rx='10' fill='%23bfae9e' stroke='%235a3d2b' stroke-width='4'/%3E%3Crect x='180' y='180' width='40' height='180' rx='6' fill='%23fff' stroke='%23bfae9e' stroke-width='2'/%3E%3Crect x='370' y='160' width='30' height='150' rx='5' fill='%23fff' stroke='%23bfae9e' stroke-width='2'/%3E%3C/g%3E%3C/svg%3E");
    background-size: cover;
    background-repeat: no-repeat;
    background-color: rgba(221, 54, 54, 0.7);
    background-position: center center;
    min-height: 100vh;
  }

  .card {
    margin-top: 50px;
    opacity: 0.98;

  }
</style>