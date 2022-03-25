import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'
import Home from '../views/Home.vue'

const routes = [
	{
		path: '/',
		name: 'Home',
		component: Home,
		meta: {
			requiresAuth: true
		},
	},
	{
		path: '/add_card',
		name: 'AddCard',
		// route level code-splitting
		// this generates a separate chunk (about.[hash].js) for this route
		// which is lazy-loaded when the route is visited.
		component: () => import('../views/AddCard.vue'),
		meta: {
			requiresAuth: true
		},
	},
	{
		path: '/edit_card/:card_id',
		name: 'EditCard',
		component: () => import('../views/AddCard.vue'),
		meta: {
			requiresAuth: true
		},
	},
	{
		path: '/profile',
		name: 'Profile',
		component: () => import('../views/Profile.vue'),
		meta: {
			requiresAuth: true
		},
	},
	{
		path: '/view_deck/:deck_id',
		name: 'ViewDeck',
		component: () => import('../views/ViewDeck.vue'),
		meta: {
			requiresAuth: true
		},
	},
	{
		path: '/start_test/:deck_id',
		name: 'DeckTest',
		component: () => import('../views/DeckTest.vue'),
		meta: {
			requiresAuth: true
		},
	},
	{
		path: '/review/:response_id',
		name: 'Result',
		component: () => import('../components/Result/index.vue'),
		meta: {
			requiresAuth: true
		},
	},
	{
		path: '/login',
		name: 'Login',
		component: () => import('../views/Login.vue'),
	},
	{
		path:"/register",
		name: 'Register',
		component: () => import('../views/Login.vue'),
	}
]

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes
})


router.beforeEach((to, from, next) => {
	if (!store.getters.user && to.matched.some(record => record.meta.requiresAuth)) {
		// this route requires auth, check if logged in
		// if not, redirect to login page.
		store.dispatch('set_user', {isAll:false, isLogout:false}).then(() => {
			if (!store.getters.user) {
				next({ name: 'Login', query: { next: to.path } })
			} else {
				next() // go to wherever I'm going
			}
		}).catch(() => {
			//we're getting anything but not 200 status code response here, so user is not authorized
			next({ name: 'Login', query: { next: to.path } })
		})
	} else {
		next() // does not require auth, make sure to always call next()!
	}
})

export default router
