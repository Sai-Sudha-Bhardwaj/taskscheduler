<template>
  <v-container fill-height fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Login</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="login">
              <v-text-field
                label="Email"
                name="email"
                prepend-icon="mdi-email"
                type="text"
                v-model="email"
                required
              ></v-text-field>

              <v-text-field
                label="Password"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                v-model="password"
                required
              ></v-text-field>

              <v-alert v-if="error" type="error" dense dismissible class="mt-3">
                {{ error }}
              </v-alert>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" type="submit" :loading="loading">Login</v-btn>
              </v-card-actions>
            </v-form>
          </v-card-text>
          <v-card-actions class="d-flex justify-center pb-4">
            <router-link to="/register">Don't have an account? Register</router-link>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      error: null,
      loading: false,
    };
  },
  methods: {
    async login() {
      this.error = null;
      this.loading = true;
      try {
        const response = await axios.post('http://127.0.0.1:8000/token', new URLSearchParams({
          username: this.email,
          password: this.password,
        }), {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        });
        localStorage.setItem('access_token', response.data.access_token);
        // Redirect to tasks page after successful login
        this.$router.push('/tasks');
      } catch (err) {
        if (err.response && err.response.data && err.response.data.detail) {
          this.error = err.response.data.detail;
        } else {
          this.error = 'An unexpected error occurred during login.';
        }
        console.error('Login error:', err);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Add any specific styles for this component here */
</style>