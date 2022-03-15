<template>
    <div id="profile">

        <div class="container profileDetails">
            <UserDetails />
            <hr>
            <div v-if="user.response">
                <final-deck :final="user.response[0]" />
                <hr>
            </div>

            <div v-if="user.response && user.response.length > 0">
                <SolvedDecks :decks="user.response.slice(1)" />
            </div>
            
            <UpdateProfile />
        </div>
    </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import FinalDeck from './FinalDeck.vue'
import SolvedDecks from './SolvedDecks.vue'
import UpdateProfile from './UpdateProfile.vue'
import UserDetails from './UserDetails.vue'
export default {
    components: { SolvedDecks, FinalDeck, UserDetails, UpdateProfile },
    name:"Profile",
    data(){
        return{
            
        }
    },
    computed:{
        ...mapGetters([
            "user"
        ])
    },
    methods:{
        ...mapActions([
            "set_user"
        ])
    },
    created(){
        this.set_user(true)
    }
}
</script>

<style scoped>
#profile{
    position: relative;
}
#profile .container{
    border: 1px solid transparent;
    background: var(--backgroundColor);
    padding:10px 15px;
    min-width:85%;
}
</style>