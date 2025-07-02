import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vuetify from 'vite-plugin-vuetify'; //  Import the Vuetify Vite plugin

export default defineConfig({
  plugins: [
    vue(),
    vuetify({ // Configure the Vuetify Vite plugin
      autoImport: true, // Auto-import Vuetify components
      styles: {
        configFile: 'src/settings.scss', // Optional: if you have a custom SCSS file
      },
    }),
  ],
  resolve: {
    alias: {
      // Optional: If you need to resolve '@/' to 'src/'
      // '@': '/src',
    },
  },
  // If you need to serve on a specific host or port (default is 5173)
  // server: {
  //   port: 5173,
  //   host: true, // Exposes the server to network for easier access
  // },
});