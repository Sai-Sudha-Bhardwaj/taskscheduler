<template>
  <v-container>
    <v-row class="mb-4">
      <v-col cols="12">
        <h1 class="text-h4">User Profile</h1>
      </v-col>
    </v-row>

    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="elevation-6 pa-5">
          <v-card-title class="text-h5">Your Information</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="updateProfile">
              <v-text-field
                v-model="user.email"
                label="Email"
                prepend-icon="mdi-email"
                type="email"
                required
                :rules="[v => !!v || 'Email is required', v => /.+@.+\..+/.test(v) || 'E-mail must be valid']"
              ></v-text-field>

              <v-text-field
                v-model="newPassword"
                label="New Password (leave blank to keep current)"
                prepend-icon="mdi-lock"
                type="password"
              ></v-text-field>

              <v-alert v-if="error" type="error" dense dismissible class="mt-3">
                {{ error }}
              </v-alert>
              <v-alert v-if="success" type="success" dense dismissible class="mt-3">
                {{ success }}
              </v-alert>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" type="submit" :loading="loading">Update Profile</v-btn>
              </v-card-actions>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.message }}
      <template v-slot:action="{ attrs }">
        <v-btn color="white" text v-bind="attrs" @click="snackbar.show = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ProfileView',
  data() {
    return {
      user: {
        email: '',
      },
      newPassword: '',
      error: null,
      success: null,
      loading: false,
      snackbar: {
        show: false,
        message: '',
        color: '',
      },
    };
  },
  async created() {
    await this.fetchProfile();
  },
  methods: {
    getAuthHeaders() {
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.showSnackbar('Authentication token not found. Please log in.', 'error');
        this.$router.push('/login');
        return {};
      }
      return {
        Authorization: `Bearer ${token}`,
      };
    },
    showSnackbar(message, color = 'success') {
      this.snackbar.message = message;
      this.snackbar.color = color;
      this.snackbar.show = true;
    },
    async fetchProfile() {
      this.loading = true;
      this.error = null;
      try {
        const headers = this.getAuthHeaders();
        if (!headers.Authorization) return; // Stop if no token

        const response = await axios.get('http://127.0.0.1:8000/users/me/', { headers });
        this.user = { ...response.data }; // Copy user data
      } catch (err) {
        console.error('Error fetching profile:', err.response?.data || err);
        if (err.response && err.response.status === 401) {
          this.showSnackbar('Session expired or unauthorized. Please log in.', 'error');
          this.$router.push('/login');
        } else {
          this.showSnackbar('Failed to fetch profile.', 'error');
        }
        this.error = `Failed to load profile: ${err.response?.data?.detail || err.message}`;
      } finally {
        this.loading = false;
      }
    },
    async updateProfile() {
      this.loading = true;
      this.error = null;
      this.success = null;
      try {
        const headers = this.getAuthHeaders();
        if (!headers.Authorization) return;

        const updateData = { email: this.user.email };
        if (this.newPassword) {
          updateData.password = this.newPassword;
        }

        const response = await axios.put('http://127.0.0.1:8000/users/me/', updateData, { headers });
        this.user = { ...response.data }; // Update local user data
        this.newPassword = ''; // Clear password field
        this.showSnackbar('Profile updated successfully!');
        this.success = 'Profile updated successfully!';
      } catch (err) {
        console.error('Error updating profile:', err.response?.data || err);
        this.showSnackbar(`Failed to update profile: ${err.response?.data?.detail || err.message}`, 'error');
        this.error = `Failed to update profile: ${err.response?.data?.detail || err.message}`;
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