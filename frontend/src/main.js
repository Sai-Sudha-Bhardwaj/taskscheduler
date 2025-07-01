// taskScheduler/frontend/src/main.js

import { createApp } from 'vue';
import App from './App.vue';
import vuetify from './plugins/vuetify'; // Your Vuetify plugin setup

// No need to import styles or mdi font/aliases here if already done in plugins/vuetify.js
// 'vuetify/styles' and '@mdi/font/css/materialdesignicons.css' are already in plugins/vuetify.js
// { aliases, mdi } from 'vuetify/iconsets/mdi' is handled by icons: { defaultSet: 'mdi' } in plugins/vuetify.js

createApp(App).use(vuetify).mount('#app');