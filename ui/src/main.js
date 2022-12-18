
import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'

// Vuetify
import vuetify from './plugins/vuetify'
import './assets/css/common.css'
import router from './plugins/router.ts'

createApp(App).use(createPinia()).use(vuetify).use(router).mount('#app')