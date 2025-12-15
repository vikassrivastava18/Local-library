<template>
  <div id="registerBackground" class="auth-wrapper">
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100">
        <div class="col-md-6 col-lg-5">
          <div class="card shadow-lg border-0 auth-card">
            
            <!-- Header -->
            <div class="card-header bg-primary text-white text-center">
              <h4 class="mb-1">Welcome 👋</h4>
              <p class="mb-0 small opacity-75">
                <span v-if="$route.path.includes('register')">
                  Create your account to get started
                </span>
                <span v-else>
                  Login to continue to your account
                </span>
              </p>
            </div>

            <!-- Tabs -->
            <div class="auth-tabs d-flex">
              <router-link
                to="/auth"
                class="auth-tab"
                :class="{ active: !$route.path.includes('register') }"
              >
                Login
              </router-link>

              <router-link
                to="/auth/register"
                class="auth-tab"
                :class="{ active: $route.path.includes('register') }"
              >
                Register
              </router-link>
            </div>

            <!-- Body -->
            <div class="card-body p-4">
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
.auth-wrapper {
  background: linear-gradient(135deg, rgb(93, 186, 215), #3b82f6);
}

.auth-card {
  border-radius: 16px;
  overflow: hidden;
  animation: fadeIn 0.5s ease-in-out;
}

.auth-tabs {
  background: #f8f9fa;
}

.auth-tab {
  flex: 1;
  text-align: center;
  padding: 12px;
  font-weight: 500;
  color: #6c757d;
  text-decoration: none;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
}

.auth-tab:hover {
  background: #e9ecef;
}

.auth-tab.active {
  color: #0d6efd;
  background: #ffffff;
  border-bottom: 2px solid #0d6efd;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
