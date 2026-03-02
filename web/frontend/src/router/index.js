import {createRouter, createWebHistory} from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import History from '../views/History.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),  //在公共服务器中你的地基目录
    routes: [
        {path: '/', redirect: '/login'}, //默认跳到登录页
        {path: '/login', component: Login},
        {path: '/register', component: Register},
        {path: '/home', component: Home},
        {path: '/history', component: History},
    ]
})

export default router