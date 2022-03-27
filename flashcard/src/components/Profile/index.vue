<template>
    <div v-if="user" id="profile">

        <div class="container profileDetails">
            <UserDetails />
            <hr>
            <div v-if="user.response && user.response[0]">
                <final-deck :final="user.response[0]" />
                <hr>
            </div>

            <div v-if="user.response && user.response.length > 0">
                <SolvedDecks :decks="user.response" />
            </div>
            
            <UpdateProfile />
            <webhooks />
        </div>
    </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import FinalDeck from './FinalDeck.vue'
import SolvedDecks from './SolvedDecks.vue'
import UpdateProfile from './UpdateProfile.vue'
import UserDetails from './UserDetails.vue'
import Webhooks from './Webhooks.vue'
export default {
    components: { SolvedDecks, FinalDeck, UserDetails, UpdateProfile, Webhooks },
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
        this.set_user({isAll:true, isLogout:false})
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

@media screen and (max-width:992px) {
    #profile .container{
        min-width:95%;
    }
}
</style>