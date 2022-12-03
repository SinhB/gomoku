
import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'

// Vuetify
import vuetify from './plugins/vuetify'
import './assets/css/common.css'

createApp(App).use(createPinia()).use(vuetify).mount('#app')