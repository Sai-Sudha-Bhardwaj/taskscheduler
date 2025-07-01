// taskScheduler/frontend/src/plugins/vuetify.js

import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles' // Import Vuetify styles
import '@mdi/font/css/materialdesignicons.css' // Import Material Design Icons CSS

export default createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi', // This tells Vuetify to use MDI as the default icon set
  },
  theme: {
    themes: {
      light: {
        colors: {
          primary: '#3f51b5', // A nice blue for primary actions
          secondary: '#b0bec5', // A soft grey for secondary elements
          accent: '#8c9eff', // A brighter accent color
          error: '#f44336',
          info: '#2196f3',
          success: '#4caf50',
          warning: '#ffc107',
        },
      },
    },
  },
})