import { createStore } from 'vuex'
import global from './global'
import profile from './profile'
import decks from './decks'

export default createStore({
	state: {
	},
	mutations: {
	},
	actions: {
	},
	modules: {
		global,
		profile,
		decks,
	}
})
