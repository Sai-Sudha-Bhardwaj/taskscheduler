<template>
  <v-container fill-height fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Register</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="register">
              <v-text-field
                label="Email"
                name="email"
                prepend-icon="mdi-email"
                type="email"
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

              <v-alert v-if="success" type="success" dense dismissible class="mt-3">
                {{ success }}
              </v-alert>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" type="submit" :loading="loading">Register</v-btn>
              </v-card-actions>
            </v-form>
          </v-card-text>
          <v-card-actions class="d-flex justify-center pb-4">
            <router-link to="/login">Already have an account? Login</router-link>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterView',
  data() {
    return {
      email: '',
      password: '',
      error: null,
      success: null,
      loading: false,
    };
  },
  methods: {
    async register() {
      this.error = null;
      this.success = null;
      this.loading = true;
      try {
        const response = await axios.post('http://127.0.0.1:8000/users/', {
          email: this.email,
          password: this.password,
        });
        this.success = 'Registration successful! Please log in.';
        this.email = '';
        this.password = '';
        console.log('Registration successful:', response.data);
      } catch (err) {
        if (err.response && err.response.data && err.response.data.detail) {
          this.error = err.response.data.detail;
        } else {
          this.error = 'An unexpected error occurred during registration.';
        }
        console.error('Registration error:', err);
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