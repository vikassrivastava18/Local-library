<template>
  <div id="registerBackground">
    <div class="container mb-5 mt-4">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card shadow">
            <div class="card-header bg-primary text-white">
            <h4 class="mb-0">
                <div v-if="$route.path.includes('register')">
                    <a href="/auth/register" class="text-white text-decoration-none">Register</a>
                    <a href="/auth" class="text-white text-decoration-none" style="float: inline-end;">Login</a>
                </div>
                <div v-else>
                    <a href="/auth" class="text-white text-decoration-none" >Login</a>
                    <a href="/auth/register" class="text-white text-decoration-none" style="float: inline-end;">Register</a>
                </div>
            </h4>
            </div>
            <div class="card-body">
                <!-- Add Login and registration child components based on URL -->
              <router-view />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

export default {
  name: 'AuthCommmon',

}
</script>

<style scoped>

  .card {
    margin-top: 100px;
    opacity: 0.98;
    padding: 10px
  }

</style>