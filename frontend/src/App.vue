<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Task Scheduler</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text v-if="isAuthenticated" to="/tasks">Tasks</v-btn>
      <v-btn text v-if="isAuthenticated" to="/profile">Profile</v-btn> <v-btn text v-if="!isAuthenticated" to="/login">Login</v-btn>
      <v-btn text v-if="!isAuthenticated" to="/register">Register</v-btn>
      <v-btn text v-if="isAuthenticated" @click="logout">Logout</v-btn>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app>
      <v-list dense nav>
        <v-list-item v-if="isAuthenticated" to="/tasks" link>
          <v-list-item-icon><v-icon>mdi-format-list-checks</v-icon></v-list-item-icon>
          <v-list-item-content><v-list-item-title>My Tasks</v-list-item-title></v-list-item-content>
        </v-list-item>
        <v-list-item v-if="isAuthenticated" to="/profile" link> <v-list-item-icon><v-icon>mdi-account</v-icon></v-list-item-icon>
          <v-list-item-content><v-list-item-title>Profile</v-list-item-title></v-list-item-content>
        </v-list-item>
        <v-list-item v-if="!isAuthenticated" to="/login" link>
          <v-list-item-icon><v-icon>mdi-login</v-icon></v-list-item-icon>
          <v-list-item-content><v-list-item-title>Login</v-list-item-title></v-list-item-content>
        </v-list-item>
        <v-list-item v-if="!isAuthenticated" to="/register" link>
          <v-list-item-icon><v-icon>mdi-account-plus</v-icon></v-list-item-icon>
          <v-list-item-content><v-list-item-title>Register</v-list-item-title></v-list-item-content>
        </v-list-item>
        <v-list-item v-if="isAuthenticated" @click="logout" link>
          <v-list-item-icon><v-icon>mdi-logout</v-icon></v-list-item-icon>
          <v-list-item-content><v-list-item-title>Logout</v-list-item-title></v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      drawer: false, // For navigation drawer
    };
  },
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('access_token');
    },
  },
  methods: {
    logout() {
      console.log('Logging out...'); // Frontend Log
      localStorage.removeItem('access_token');
      // Optionally remove other user data if stored
      this.$router.push('/login');
      console.log('User logged out, redirected to login.'); // Frontend Log
    },
  },
  watch: {
    // Watch for changes in the route to ensure drawer closes
    '$route'() {
      this.drawer = false;
    }
  }
};
</script>

<style>
/* Add global styles here if any */
</style>