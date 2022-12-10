import { createWebHistory, createRouter } from 'vue-router'
import RoomSelect from '../components/RoomSelect.vue'
import BoardTest from '../components/BoardTest.vue'

const routes = [
    {
        path: '/',
        name: 'RoomSelect',
        component: RoomSelect
    },
    {
        path: '/game/:roomName',
        name: 'BoardTest',
        component: BoardTest,
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router