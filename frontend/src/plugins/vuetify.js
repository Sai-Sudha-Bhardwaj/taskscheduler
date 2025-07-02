// frontend/src/plugins/vuetify.js

import { createVuetify } from 'vuetify'; // This is the only Vuetify import you need
// Remove any lines like:
// import Vue from 'vue';
// import Vuetify from 'vuetify/lib';
// import * as components from 'vuetify/components';
// import * as directives from 'vuetify/directives';

import 'vuetify/styles'; // Correct way to import Vuetify 3 CSS
import '@mdi/font/css/materialdesignicons.css'; // Material Design Icons CSS

export default createVuetify({
  // Components and directives are now auto-imported by the Vite plugin (@vuetify/vite-plugin-vuetify)
  icons: {
    iconfont: 'mdi', // 'mdi' is for Material Design Icons
  },
  // You can define a custom theme here if needed
  // theme: {
  //   defaultTheme: 'light',
  //   themes: {
  //     light: {
  //       colors: {
  //         primary: '#1867C0',
  //         secondary: '#5CBBF6',
  //       },
  //     },
  //   },
  // },
});